package com.cardiotriage.service;

import com.cardiotriage.dto.RecordingResponse;
import com.cardiotriage.dto.TriageResultResponse;
import com.cardiotriage.model.Patient;
import com.cardiotriage.model.Recording;
import com.cardiotriage.model.TriageResult;
import com.cardiotriage.repository.PatientRepository;
import com.cardiotriage.repository.RecordingRepository;
import com.cardiotriage.repository.TriageResultRepository;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.server.ResponseStatusException;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class RecordingService {

    @Value("${ML_SERVICE_URL:http://localhost:8000}")
    private String mlServiceUrl;

    @Value("${UPLOAD_DIR:./uploads}")
    private String uploadDir;

    private final RestTemplate restTemplate;
    private final RecordingRepository recordingRepository;
    private final TriageResultRepository triageResultRepository;
    private final PatientRepository patientRepository;
    private final ObjectMapper objectMapper;

    public TriageResultResponse uploadAndTriage(Long patientId, String deviceType, MultipartFile file) {
        Patient patient = patientRepository.findById(patientId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Patient not found with id: " + patientId));

        Path storedFilePath = storeFile(file);

        Recording recording = Recording.builder()
                .patient(patient)
                .deviceType(deviceType)
                .ecgFilePath(storedFilePath.toString())
                .build();
        recording = recordingRepository.save(recording);

        JsonNode signalJson = readSignalJson(storedFilePath);

        List<Double> ecgSignal = objectMapper.convertValue(signalJson.get("ecg_signal"), new TypeReference<List<Double>>() {});
        List<Double> ppgSignal = objectMapper.convertValue(signalJson.get("ppg_signal"), new TypeReference<List<Double>>() {});

        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("ecg_signal", ecgSignal);
        requestBody.put("ppg_signal", ppgSignal);
        requestBody.put("device_type", deviceType);

        Map<String, Object> triageResponse = callTriageService(requestBody);

        TriageResult triageResult = buildTriageResult(recording, triageResponse);
        triageResult = triageResultRepository.save(triageResult);

        return toTriageResultResponse(triageResult);
    }

    public List<RecordingResponse> getRecordingsByPatient(Long patientId) {
        return recordingRepository.findByPatientIdOrderByUploadedAtDesc(patientId).stream()
                .map(this::toRecordingResponse)
                .toList();
    }

    public TriageResultResponse getTriageResult(Long recordingId) {
        TriageResult triageResult = triageResultRepository.findByRecordingId(recordingId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Triage result not found for recording id: " + recordingId));

        return toTriageResultResponse(triageResult);
    }

    private Path storeFile(MultipartFile file) {
        try {
            Path uploadPath = Paths.get(uploadDir);
            Files.createDirectories(uploadPath);

            String originalFilename = file.getOriginalFilename() != null ? file.getOriginalFilename() : "upload";
            String filename = UUID.randomUUID() + "_" + originalFilename;
            Path targetPath = uploadPath.resolve(filename);

            Files.copy(file.getInputStream(), targetPath, StandardCopyOption.REPLACE_EXISTING);
            return targetPath;
        } catch (IOException e) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "Failed to store uploaded file", e);
        }
    }

    private JsonNode readSignalJson(Path filePath) {
        try {
            String content = Files.readString(filePath);
            return objectMapper.readTree(content);
        } catch (IOException e) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Failed to parse uploaded recording file", e);
        }
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> callTriageService(Map<String, Object> requestBody) {
        try {
            Map<String, Object> response = restTemplate.postForObject(mlServiceUrl + "/triage", requestBody, Map.class);
            if (response == null) {
                throw new ResponseStatusException(HttpStatus.BAD_GATEWAY, "Triage service unavailable");
            }
            return response;
        } catch (RestClientException e) {
            throw new ResponseStatusException(HttpStatus.BAD_GATEWAY, "Triage service unavailable", e);
        }
    }

    private TriageResult buildTriageResult(Recording recording, Map<String, Object> response) {
        try {
            return TriageResult.builder()
                    .recording(recording)
                    .severity((String) response.get("severity"))
                    .severityScore(toDouble(response.get("severity_score")))
                    .rhythmLabel((String) response.get("rhythm_label"))
                    .rhythmProbs(objectMapper.writeValueAsString(response.get("rhythm_probs")))
                    .heartRate(toDouble(response.get("heart_rate")))
                    .hrvRmssd(toDouble(response.get("hrv_rmssd")))
                    .spo2(toDouble(response.get("spo2")))
                    .stressLevel((String) response.get("stress_level"))
                    .stressProbs(objectMapper.writeValueAsString(response.get("stress_probs")))
                    .build();
        } catch (JsonProcessingException e) {
            throw new ResponseStatusException(HttpStatus.INTERNAL_SERVER_ERROR, "Failed to process triage response", e);
        }
    }

    private Double toDouble(Object value) {
        if (value == null) {
            return null;
        }
        if (value instanceof Number number) {
            return number.doubleValue();
        }
        return Double.valueOf(value.toString());
    }

    private RecordingResponse toRecordingResponse(Recording recording) {
        TriageResultResponse triageResultResponse = triageResultRepository.findByRecordingId(recording.getId())
                .map(this::toTriageResultResponse)
                .orElse(null);

        return RecordingResponse.builder()
                .id(recording.getId())
                .patientId(recording.getPatient().getId())
                .deviceType(recording.getDeviceType())
                .uploadedAt(recording.getUploadedAt())
                .triageResult(triageResultResponse)
                .build();
    }

    private TriageResultResponse toTriageResultResponse(TriageResult triageResult) {
        return TriageResultResponse.builder()
                .id(triageResult.getId())
                .recordingId(triageResult.getRecording().getId())
                .severity(triageResult.getSeverity())
                .severityScore(triageResult.getSeverityScore())
                .rhythmLabel(triageResult.getRhythmLabel())
                .rhythmProbs(triageResult.getRhythmProbs())
                .heartRate(triageResult.getHeartRate())
                .hrvRmssd(triageResult.getHrvRmssd())
                .spo2(triageResult.getSpo2())
                .stressLevel(triageResult.getStressLevel())
                .stressProbs(triageResult.getStressProbs())
                .createdAt(triageResult.getCreatedAt())
                .build();
    }
}
