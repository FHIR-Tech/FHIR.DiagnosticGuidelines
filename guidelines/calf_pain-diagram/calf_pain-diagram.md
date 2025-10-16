---
id: calf_pain-diagram
title: Hướng dẫn đau bắp chuối (calf pain)
description: Đánh giá đau bắp chân: phân biệt DVT, cơ- gân, giãn cơ, viêm, huyết khối và hướng xử trí ban đầu.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/calf_pain-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho bệnh nhân đau bắp chân; mục tiêu loại trừ DVT, xác định chấn thương mô mềm và điều trị thích hợp.

## Flow

1. stepId: limbThreat
   question: "Tăng đau đột ngột, tím, mất mạch hay dấu sinh tồn bất thường không?"
   type: boolean
   next:
     true: action=urgentVascularReview
     false: stepId=recentInjuryOrActivity

2. stepId: recentInjuryOrActivity
   question: "Hoạt động thể thao, chấn thương hoặc thay đổi vận động gần đây không?"
   type: boolean
   next:
     true: action=considerMuscleStrainOrRupture
     false: stepId=assessDvtRisk

3. stepId: assessDvtRisk
   question: "Yếu tố nguy cơ DVT: bất động, thuốc tránh thai, tiền sử DVT không?"
   type: boolean
   next:
     true: action=orderDopplerUltrasound
     false: action=conservativeCare

4. stepId: localSigns
   question: "Sưng, đỏ, nóng khu trú hoặc nốt đau cơ bản không?"
   type: boolean
   next:
     true: action=considerInfectionOrDVT
     false: action=monitorAndAnalgesia

5. stepId: imaging
   question: "Cần siêu âm, X-quang hay MRI để đánh giá mô mềm?"
   type: boolean
   next:
     true: action=orderAppropriateImaging
     false: action=planRehab

6. stepId: medicationReview
   question: "Thuốc làm tăng DVT hoặc tương tác không?"
   type: boolean
   next:
     true: action=adjustMedications
     false: action=continuePlan

7. stepId: treatmentTrial
   question: "Nên thử nghỉ, chườm, nén, và NSAID không?"
   type: boolean
   next:
     true: action=prescribeConservativeTherapy
     false: action=referSpecialist

8. stepId: disposition
   question: "Cần nhập viện hay ngoại trú?"
   type: choice
   answers:
     - code: admit
       display: "Nhập viện"
       next: action=admitForAnticoagulationIfDVT
     - code: outpatient
       display: "Ngoại trú"
       next: action=dischargeWithPlan

9. stepId: followUp
   question: "Sắp xếp siêu âm lại hoặc tái khám?"
   type: boolean
   next:
     true: action=arrangeFollowup
     false: action=end

10. stepId: education
    question: "Cần tư vấn về phòng ngừa DVT, tái hoạt động an toàn không?"
    type: boolean
    next:
      true: action=providePreventionAdvice
      false: action=end

## Hành động

- id: urgentVascularReview
  description: "Tham vấn mạch/ cấp cứu nếu có dấu đe dọa chi hoặc biến chứng nặng."
  type: referral
  cpg-activity-type: emergency
  useContext: khẩn

- id: considerMuscleStrainOrRupture
  description: "Đánh giá tổn thương cơ, cân nhắc siêu âm hoặc MRI và điều trị."
  type: investigation
  cpg-activity-type: diagnostic
  useContext: chấn-thương

- id: orderDopplerUltrasound
  description: "Siêu âm Doppler để loại trừ DVT khi có chỉ định."
  type: investigation
  cpg-activity-type: imaging
  useContext: DVT

- id: considerInfectionOrDVT
  description: "Phân biệt giữa nhiễm trùng mô mềm và DVT; làm xét nghiệm và điều trị phù hợp."
  type: action
  cpg-activity-type: differential-diagnosis
  useContext: chẩn-đoán

- id: prescribeConservativeTherapy
  description: "Nghỉ, chườm lạnh/ nóng, nén, NSAID và vật lý trị liệu."
  type: action
  cpg-activity-type: symptomatic-care
  useContext: điều-trị

- id: orderAppropriateImaging
  description: "Yêu cầu MRI/US/X-ray để đánh giá chi tiết khi cần."
  type: investigation
  cpg-activity-type: imaging
  useContext: hình-ảnh

- id: adjustMedications
  description: "Điều chỉnh thuốc có thể tăng nguy cơ DVT sau hội chẩn."
  type: action
  cpg-activity-type: medication-review
  useContext: dược

- id: admitForAnticoagulationIfDVT
  description: "Nhập viện và bắt đầu chống đông nếu xác nhận DVT và có chỉ định."
  type: intervention
  cpg-activity-type: inpatient-care
  useContext: chống-đông

- id: dischargeWithPlan
  description: "Xuất viện với kế hoạch điều trị, nén và hẹn theo dõi."
  type: action
  cpg-activity-type: outpatient-care
  useContext: ngoại-trú

- id: arrangeFollowup
  description: "Sắp xếp siêu âm lại hoặc khám chuyên khoa khi cần."
  type: action
  cpg-activity-type: administrative
  useContext: follow-up

- id: providePreventionAdvice
  description: "Hướng dẫn phòng ngừa DVT: vận động, bôi nén, dùng thuốc theo chỉ dẫn."
  type: action
  cpg-activity-type: patient-education
  useContext: phòng-ngừa

## Bảng phân loại nguyên nhân đau bắp chân

| Loại | Ví dụ |
|------|------|
| DVT | Thrombus tĩnh mạch sâu |
| Mô mềm | Chuột rút, strain, rupture |
| Nhiễm trùng | Cellulitis |

## Ghi chú

- Generated from `diagrams/calf_pain-diagram.png`
