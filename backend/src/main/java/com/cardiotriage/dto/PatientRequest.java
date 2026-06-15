package com.cardiotriage.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PatientRequest {

    @NotBlank
    private String name;

    @NotNull
    private Integer age;

    private String gender;
    private String bloodType;
    private String conditions;
    private String medications;
    private String emergencyContact;
}
