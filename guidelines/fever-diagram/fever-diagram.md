---
id: fever-diagram
title: Hướng dẫn chẩn đoán sốt
description: Quy trình có cấu trúc để đánh giá bệnh nhân có sốt ở người lớn, bao gồm tiền sử du lịch, nhập viện, thuốc, và phân loại nguyên nhân chính.
version: 1.0.0
date: 2025-10-09
authors:
  - name: AI Draft
  - name: Reviewer Needed
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/fever-diagram.png
source-checksum: TODO
---

## Context / Scope

This guideline provides a structured approach to evaluating fever in adults, focusing on recent travel, hospitalization, medication, and major etiological categories (infectious, inflammatory, malignancy, other). It is intended for use in clinical decision support systems.

## Flow

1. stepId: feverStart
   question: "Fever in the patient?"
   type: boolean
   next:
     true: stepId=recentTravel
     false: action=exit-no-fever

2. stepId: recentTravel
   question: "Recent travel abroad?"
   type: boolean
   next:
     true: stepId=travelerIncubation
     false: stepId=recentHospitalization

3. stepId: travelerIncubation
   question: "Incubation period since return?"
   type: choice
   answers:
     - code: lt21
       display: "< 21 days"
       next: action=propose-infectious-traveler-short
     - code: gt21
       display: "> 21 days"
       next: action=propose-infectious-traveler-long

4. stepId: recentHospitalization
   question: "Recent or current hospitalization?"
   type: boolean
   next:
     true: action=consider-nosocomial-infection
     false: stepId=newMedication

5. stepId: newMedication
   question: "New medication (that suggests drug fever)?"
   type: boolean
   next:
     true: action=consider-drug-fever
     false: stepId=recentUrinaryCatheter

6. stepId: recentUrinaryCatheter
   question: "Recent urinary catheter?"
   type: boolean
   next:
     true: action=consider-uti
     false: stepId=recentProcedure

7. stepId: recentProcedure
   question: "Recent procedure?"
   type: boolean
   next:
     true: action=consider-abscess-wound-bacteremia-pneumonia
     false: stepId=recentAntibiotics

8. stepId: recentAntibiotics
   question: "Recent antibiotics?"
   type: boolean
   next:
     true: action=consider-cdiff-drug-fever
     false: stepId=majorCategory

9. stepId: majorCategory
   question: "Attempt to identify major category"
   type: choice
   answers:
     - code: infectious
       display: "Infectious etiology"
       next: action=propose-infectious
     - code: inflammatory
       display: "Inflammatory etiology"
       next: action=propose-inflammatory
     - code: malignancy
       display: "Malignancy"
       next: action=propose-malignancy
     - code: other
       display: "Other"
       next: action=propose-other

## Actions

- id: propose-infectious-traveler-short
  description: "Consider infectious etiologies in returning traveler with incubation < 21 days (e.g., traveler's diarrhea, dengue, yellow fever, leptospirosis, malaria, typhus, trypanosomiasis, enteric fevers)"
  type: propose-diagnosis
  cpg-activity-type: propose-diagnosis
  useContext: travel, short-incubation

- id: propose-infectious-traveler-long
  description: "Consider infectious etiologies in returning traveler with incubation > 21 days (e.g., acute HIV, malaria, tuberculosis, viral hepatitis, amebic liver disease)"
  type: propose-diagnosis
  cpg-activity-type: propose-diagnosis
  useContext: travel, long-incubation

- id: consider-nosocomial-infection
  description: "Consider nosocomial infection"
  type: propose-diagnosis
  cpg-activity-type: propose-diagnosis
  useContext: hospitalization

- id: consider-drug-fever
  description: "Consider drug fever due to new medication"
  type: propose-diagnosis
  cpg-activity-type: propose-diagnosis
  useContext: medication

- id: consider-uti
  description: "Consider urinary tract infection (UTI)"
  type: propose-diagnosis
  cpg-activity-type: propose-diagnosis
  useContext: urinary-catheter

- id: consider-abscess-wound-bacteremia-pneumonia
  description: "Consider abscess, wound infection, bacteremia, pneumonia"
  type: propose-diagnosis
  cpg-activity-type: propose-diagnosis
  useContext: procedure

- id: consider-cdiff-drug-fever
  description: "Consider C. difficile diarrhea, drug fever"
  type: propose-diagnosis
  cpg-activity-type: propose-diagnosis
  useContext: antibiotics

- id: propose-infectious
  description: "Infectious etiology: recent sick contact, chemotherapy, travel/hospitalization; subtypes: bacterial, viral, parasitic, fungal, rickettsial"
  type: propose-diagnosis
  cpg-activity-type: propose-diagnosis
  useContext: infectious

- id: propose-inflammatory
  description: "Inflammatory etiology: rash/arthritis, family history; subtypes: SLE, rheumatic fever, vasculitis, IBD, etc."
  type: propose-diagnosis
  cpg-activity-type: propose-diagnosis
  useContext: inflammatory

- id: propose-malignancy
  description: "Malignancy: weight loss, bony pain; subtypes: lymphoma, leukemia, metastases, hepatocellular, renal, pancreas cancer"
  type: propose-diagnosis
  cpg-activity-type: propose-diagnosis
  useContext: malignancy

- id: propose-other
  description: "Other: pulmonary emboli, drug fever, factitious fever, sarcoidosis, adrenal insufficiency, hyperthyroidism, pancreatitis"
  type: propose-diagnosis
  cpg-activity-type: propose-diagnosis
  useContext: other

- id: exit-no-fever
  description: "No fever detected; exit guideline."
  type: exit
  cpg-activity-type: exit

## Major classification table

| Category      | Features/Examples                                                                 |
|--------------|-----------------------------------------------------------------------------------|
| Infectious   | Recent sick contact, chemotherapy, travel/hospitalization; bacterial, viral, etc. |
| Inflammatory | Rash/arthritis, family history; SLE, vasculitis, IBD, etc.                        |
| Malignancy   | Weight loss, bony pain; lymphoma, leukemia, metastases, etc.                      |
| Other        | Pulmonary emboli, drug fever, sarcoidosis, etc.                                   |

## Notes / TODO

- Add standard codes (ICD-10, SNOMED, LOINC) for diagnoses and actions where available.
- Map CQL expressions for PlanDefinition conditions (e.g., RecentTravelAbroad, TravelerIncubationLessThan21Days).
- Review and validate canonical URLs and resource references in generated Bundle.
- Add reviewer and clinical validation.
