package com.cardiotriage.service;

import com.cardiotriage.dto.PatientRequest;
import com.cardiotriage.dto.PatientResponse;
import com.cardiotriage.dto.PatientSummary;
import com.cardiotriage.model.Patient;
import com.cardiotriage.repository.PatientRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;

@Service
@RequiredArgsConstructor
public class PatientService {

    private final PatientRepository patientRepository;

    public List<PatientSummary> getAllPatients() {
        return patientRepository.findAllByOrderByCreatedAtDesc().stream()
                .map(this::toSummary)
                .toList();
    }

    public PatientResponse getPatientById(Long id) {
        return toResponse(findPatientOrThrow(id));
    }

    public PatientResponse createPatient(PatientRequest request) {
        Patient patient = Patient.builder()
                .name(request.getName())
                .age(request.getAge())
                .gender(request.getGender())
                .bloodType(request.getBloodType())
                .conditions(request.getConditions())
                .medications(request.getMedications())
                .emergencyContact(request.getEmergencyContact())
                .build();

        return toResponse(patientRepository.save(patient));
    }

    public PatientResponse updatePatient(Long id, PatientRequest request) {
        Patient patient = findPatientOrThrow(id);

        patient.setName(request.getName());
        patient.setAge(request.getAge());
        patient.setGender(request.getGender());
        patient.setBloodType(request.getBloodType());
        patient.setConditions(request.getConditions());
        patient.setMedications(request.getMedications());
        patient.setEmergencyContact(request.getEmergencyContact());

        return toResponse(patientRepository.save(patient));
    }

    public void deletePatient(Long id) {
        patientRepository.delete(findPatientOrThrow(id));
    }

    private Patient findPatientOrThrow(Long id) {
        return patientRepository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Patient not found with id: " + id));
    }

    private PatientResponse toResponse(Patient patient) {
        return PatientResponse.builder()
                .id(patient.getId())
                .name(patient.getName())
                .age(patient.getAge())
                .gender(patient.getGender())
                .bloodType(patient.getBloodType())
                .conditions(patient.getConditions())
                .medications(patient.getMedications())
                .emergencyContact(patient.getEmergencyContact())
                .createdAt(patient.getCreatedAt())
                .updatedAt(patient.getUpdatedAt())
                .build();
    }

    private PatientSummary toSummary(Patient patient) {
        return PatientSummary.builder()
                .id(patient.getId())
                .name(patient.getName())
                .age(patient.getAge())
                .gender(patient.getGender())
                .createdAt(patient.getCreatedAt())
                .build();
    }
}
