package com.cardiotriage.controller;

import com.cardiotriage.dto.RecordingResponse;
import com.cardiotriage.dto.TriageResultResponse;
import com.cardiotriage.service.RecordingService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

@RestController
@RequestMapping("/api")
@RequiredArgsConstructor
public class RecordingController {

    private final RecordingService recordingService;

    @PostMapping("/recordings/upload")
    public ResponseEntity<TriageResultResponse> uploadRecording(
            @RequestParam Long patientId,
            @RequestParam(defaultValue = "generic_wearable") String deviceType,
            @RequestParam MultipartFile file) {

        TriageResultResponse response = recordingService.uploadAndTriage(patientId, deviceType, file);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping("/patients/{patientId}/recordings")
    public ResponseEntity<List<RecordingResponse>> getRecordingsByPatient(@PathVariable Long patientId) {
        return ResponseEntity.ok(recordingService.getRecordingsByPatient(patientId));
    }

    @GetMapping("/triage/{recordingId}")
    public ResponseEntity<TriageResultResponse> getTriageResult(@PathVariable Long recordingId) {
        return ResponseEntity.ok(recordingService.getTriageResult(recordingId));
    }
}
