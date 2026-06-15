package com.cardiotriage.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class TriageResultResponse {

    private Long id;
    private Long recordingId;
    private String severity;
    private Double severityScore;
    private String rhythmLabel;
    private String rhythmProbs;
    private Double heartRate;
    private Double hrvRmssd;
    private Double spo2;
    private String stressLevel;
    private String stressProbs;
    private LocalDateTime createdAt;
}
