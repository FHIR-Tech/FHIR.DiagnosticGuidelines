---
id: generalized_pruritus-diagram
title: Hướng dẫn đánh giá ngứa toàn thân
description: Quy trình đánh giá ngứa toàn thân, phân loại nguyên nhân da liễu và hệ thống (gan, thận, nội tiết, thuốc) và đề xuất xét nghiệm sàng lọc.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
  - name: Reviewer Needed
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/generalized_pruritus-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng khi bệnh nhân trình bày ngứa lan tỏa không có tổn thương da rõ rệt hoặc kèm tổn thương da. Mục tiêu là phân loại nguyên nhân và đề xuất xét nghiệm sàng lọc.

## Flow

1. stepId: pruritusStart
   question: "Bệnh nhân có ngứa không?"
   type: boolean
   next:
     true: stepId=skinLesions
     false: action=exit-no-pruritus

2. stepId: skinLesions
   question: "Có tổn thương da kèm theo (phát ban, mụn nước, tổn thương gãi)?"
   type: boolean
   next:
     true: action=referDermatology
     false: stepId=systemicAssessment

3. stepId: systemicAssessment
   question: "Đánh giá các nguyên nhân hệ thống: bệnh gan, thận, tuyến giáp, huyết học, ung thư, thuốc?"
   type: choice
   answers:
     - code: liver
       display: "Bệnh gan"
       next: action=orderLiverTests
     - code: renal
       display: "Bệnh thận"
       next: action=orderRenalTests
     - code: endocrine
       display: "Rối loạn nội tiết (tuyến giáp)"
       next: action=orderThyroidTests
     - code: hematologic
       display: "Rối loạn huyết học / ác tính"
       next: action=orderCBC
     - code: drug
       display: "Do thuốc"
       next: action=reviewMedications

4. stepId: followUp
   question: "Triệu chứng cải thiện sau can thiệp?"
   type: boolean
   next:
     true: action=continueManagement
     false: action=referSpecialist

5. stepId: medicationHistory
   question: "Bệnh nhân có bắt đầu thuốc mới trong vài tuần gần đây không?"
   type: boolean
   next:
     true: action=reviewMedications
     false: stepId=systemicRedFlags

6. stepId: systemicRedFlags
   question: "Có dấu hiệu gợi ý bệnh hệ thống: sút cân, mệt mỏi, vàng da, thay đổi nước tiểu, sốt không?"
   type: boolean
   next:
     true: action=orderSystemicTests
     false: stepId=skinBiopsyConsider

7. stepId: skinBiopsyConsider
   question: "Có tổn thương da bất thường cần sinh thiết không?"
   type: boolean
   next:
     true: action=referDermatology
     false: action=trialAntipruritic

8. stepId: trialAntipruritic
   question: "Thử thuốc chống ngứa (antihistamine/topical) có đáp ứng không?"
   type: boolean
   next:
     true: action=continueManagement
     false: action=referSpecialist

9. stepId: chronicAssessment
   question: "Ngứa kéo dài >6 tuần không?"
   type: boolean
   next:
     true: action=chronicWorkup
     false: action=monitorAndEducate

10. stepId: disposition
    question: "Cần nhập viện hay theo dõi ngoại trú?"
    type: choice
    answers:
      - code: admit
        display: "Nhập viện"
        next: action=urgentAssessment
      - code: outpatient
        display: "Ngoại trú"
        next: action=continueManagement

## Hành động

- id: referDermatology
  description: "Tham vấn chuyên khoa da liễu khi có tổn thương da hoặc nghi ngờ bệnh da chuyên khoa."
  type: referral
  cpg-activity-type: referral
  useContext: da liễu

- id: orderLiverTests
  description: "Yêu cầu xét nghiệm chức năng gan (AST/ALT/ALP/bilirubin) khi nghi ngờ bệnh gan."
  type: investigation
  cpg-activity-type: laboratory
  useContext: gan

- id: orderRenalTests
  description: "Yêu cầu xét nghiệm chức năng thận (creatinine, BUN, điện giải) khi nghi ngờ bệnh thận."
  type: investigation
  cpg-activity-type: laboratory
  useContext: thận

- id: orderThyroidTests
  description: "Yêu cầu xét nghiệm tuyến giáp (TSH, FT4) khi nghi ngờ rối loạn nội tiết."
  type: investigation
  cpg-activity-type: laboratory
  useContext: nội tiết

- id: orderCBC
  description: "Yêu cầu công thức máu để loại trừ rối loạn huyết học hoặc dấu hiệu ác tính."
  type: investigation
  cpg-activity-type: laboratory
  useContext: huyết học

- id: reviewMedications
  description: "Rà soát thuốc đang dùng có thể gây ngứa; xem xét ngưng hoặc thay thế nếu có."
  type: action
  cpg-activity-type: medication-review
  useContext: thuốc

- id: continueManagement
  description: "Tiếp tục quản lý triệu chứng và theo dõi."
  type: follow-up
  cpg-activity-type: follow-up
  useContext: tiếp tục

- id: orderSystemicTests
  description: "Yêu cầu xét nghiệm gan, thận, TSH, và marker huyết học khi nghi ngờ nguyên nhân hệ thống."
  type: investigation
  cpg-activity-type: laboratory
  useContext: xét nghiệm hệ thống

- id: trialAntipruritic
  description: "Thử liệu pháp chống ngứa: antihistamine, kem bôi lên vùng da, liệu pháp giữ ẩm."
  type: intervention
  cpg-activity-type: management
  useContext: điều trị triệu chứng

- id: monitorAndEducate
  description: "Tư vấn về chăm sóc da, tránh chất kích ứng và theo dõi."
  type: action
  cpg-activity-type: patient-education
  useContext: phòng ngừa

- id: chronicWorkup
  description: "Khảo sát sâu cho ngứa mạn: xét nghiệm đặc hiệu, chuyển tuyến chuyên khoa khi cần."
  type: investigation
  cpg-activity-type: specialized-investigation
  useContext: mạn tính

- id: referSpecialist
  description: "Tham vấn chuyên khoa khi không cải thiện hoặc nghi ngờ nguyên nhân nghiêm trọng."
  type: referral
  cpg-activity-type: referral
  useContext: tham vấn

## Ghi chú / TODO

- Thêm mã ICD/SNOMED cho chẩn đoán và xét nghiệm.
- Generated from diagrams/generalized_pruritus-diagram.png

- Bảng phân loại nguyên nhân ngứa toàn thân:

| Loại nguyên nhân    | Đặc điểm / Ví dụ                                  |
|---------------------|---------------------------------------------------|
| Da tại chỗ          | Viêm da tiếp xúc, dị ứng, vảy nến                  |
| Nội tiết / chuyển hóa| Bệnh gan, suy thận, cường giáp                     |
| Thuốc               | Kháng sinh, opioid, statin                         |
| Huyết học / ác tính  | Lymphoma, leukemia                                 |
| Tâm lý              | Lo âu, rối loạn stress                              |
