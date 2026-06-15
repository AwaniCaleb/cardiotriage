package com.cardiotriage.repository;

import com.cardiotriage.model.Recording;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface RecordingRepository extends JpaRepository<Recording, Long> {

    List<Recording> findByPatientIdOrderByUploadedAtDesc(Long patientId);
}
