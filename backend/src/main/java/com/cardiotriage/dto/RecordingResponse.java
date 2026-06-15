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
public class RecordingResponse {

    private Long id;
    private Long patientId;
    private String deviceType;
    private LocalDateTime uploadedAt;
    private TriageResultResponse triageResult;
}
