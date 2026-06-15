package com.cardiotriage.repository;

import com.cardiotriage.model.TriageResult;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface TriageResultRepository extends JpaRepository<TriageResult, Long> {

    Optional<TriageResult> findByRecordingId(Long recordingId);
}
