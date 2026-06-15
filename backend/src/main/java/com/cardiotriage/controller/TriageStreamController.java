package com.cardiotriage.controller;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.task.TaskExecutor;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;
import org.springframework.web.util.UriComponentsBuilder;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.concurrent.TimeUnit;

@RestController
@RequestMapping("/api")
@RequiredArgsConstructor
@Slf4j
public class TriageStreamController {

    private static final long EMITTER_TIMEOUT_MS = TimeUnit.MINUTES.toMillis(3);

    private final RestTemplate restTemplate;
    private final TaskExecutor taskExecutor;

    @Value("${ML_SERVICE_URL:http://localhost:8000}")
    private String mlServiceUrl;

    @GetMapping(value = "/triage/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public SseEmitter streamTriage(@RequestParam(defaultValue = "Normal") String rhythm) {
        SseEmitter emitter = new SseEmitter(EMITTER_TIMEOUT_MS);
        taskExecutor.execute(() -> relayStream(emitter, rhythm));
        return emitter;
    }

    private void relayStream(SseEmitter emitter, String rhythm) {
        String url = UriComponentsBuilder.fromUriString(mlServiceUrl + "/triage/stream")
                .queryParam("rhythm", rhythm)
                .toUriString();

        try {
            restTemplate.execute(
                    url,
                    HttpMethod.GET,
                    request -> request.getHeaders().setAccept(List.of(MediaType.TEXT_EVENT_STREAM, MediaType.ALL)),
                    response -> {
                        try (BufferedReader reader = new BufferedReader(
                                new InputStreamReader(response.getBody(), StandardCharsets.UTF_8))) {

                            String currentEvent = null;
                            StringBuilder dataBuilder = new StringBuilder();
                            String line;

                            while ((line = reader.readLine()) != null) {
                                if (line.isEmpty()) {
                                    if (dataBuilder.length() > 0) {
                                        SseEmitter.SseEventBuilder event = SseEmitter.event().data(dataBuilder.toString());
                                        if (currentEvent != null) {
                                            event.name(currentEvent);
                                        }
                                        emitter.send(event);
                                        dataBuilder.setLength(0);
                                        currentEvent = null;
                                    }
                                } else if (line.startsWith("event:")) {
                                    currentEvent = line.substring("event:".length()).trim();
                                } else if (line.startsWith("data:")) {
                                    if (dataBuilder.length() > 0) {
                                        dataBuilder.append("\n");
                                    }
                                    dataBuilder.append(line.substring("data:".length()).trim());
                                }
                            }
                        }
                        return null;
                    }
            );
            emitter.complete();
        } catch (Exception e) {
            log.warn("Triage stream relay failed", e);
            emitter.completeWithError(e);
        }
    }
}
