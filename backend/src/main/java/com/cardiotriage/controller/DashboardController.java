package com.cardiotriage.controller;

import com.cardiotriage.repository.PatientRepository;
import com.cardiotriage.repository.RecordingRepository;
import com.cardiotriage.repository.TriageResultRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@RequestMapping("/api/dashboard")
@RequiredArgsConstructor
public class DashboardController {
    private final PatientRepository patientRepository;
    private final RecordingRepository recordingRepository;
    private final TriageResultRepository triageResultRepository;

    @GetMapping("/stats")
    public ResponseEntity<Map<String, Object>> getStats() {
        long totalPatients = patientRepository.count();
        long totalRecordings = recordingRepository.count();
        long criticalAlerts = triageResultRepository
            .countBySeverity("RED");
        return ResponseEntity.ok(Map.of(
            "totalPatients", totalPatients,
            "totalRecordings", totalRecordings,
            "criticalAlerts", criticalAlerts
        ));
    }
}
