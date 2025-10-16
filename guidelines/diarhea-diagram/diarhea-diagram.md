---
id: diarhea-diagram
title: Hướng dẫn tiêu chảy (diarrhea)
description: Quy trình đánh giá tiêu chảy cấp và mạn, phân loại nguyên nhân nhiễm trùng, sinh thái, thuốc và xử trí ban đầu.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/diarhea-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho bệnh nhân tiêu chảy; mục tiêu chẩn đoán nguyên nhân nhiễm trùng, độc tố, viêm ruột, và lập kế hoạch bù dịch, kháng sinh theo chỉ định.

## Flow

1. stepId: assessSeverity
   question: "Có dấu mất nước nặng, sốc, máu trong phân hoặc suy đa cơ quan không?"
   type: boolean
   next:
     true: action=resuscitateAndAdmit
     false: stepId=onsetAndDuration

2. stepId: onsetAndDuration
   question: "Tiêu chảy cấp (<14 ngày) hay mạn (>14 ngày)?"
   type: choice
   answers:
     - code: acute
       display: "Cấp"
       next: stepId=infectiousWorkup
     - code: chronic
       display: "Mạn"
       next: stepId=investigateChronicCauses

3. stepId: infectiousWorkup
   question: "Triệu chứng nhiễm trùng: sốt, đau bụng, nôn, du lịch, thức ăn nghi ngờ?"
   type: boolean
   next:
     true: action=orderStoolTestsAndStartABIfIndicated
     false: action=considerOtherCauses

4. stepId: bùDịch
   question: "Bệnh nhân cần bù dịch đường tĩnh mạch hay bù nước qua miệng?"
   type: choice
   answers:
     - code: iv
       display: "IV fluids"
       next: action=administerIVFluids
     - code: oral
       display: "Oral rehydration"
       next: action=oralRehydration

5. stepId: inflammatoryConsider
   question: "Nghi viêm ruột (IBD) với máu phân, sút cân không?"
   type: boolean
   next:
     true: action=referGastroenterologyAndColonoscopy
     false: action=symptomaticCare

6. stepId: medicationReview
   question: "Thuốc gần đây (antibiotics, metformin, laxatives) có thể gây tiêu chảy không?"
   type: boolean
   next:
     true: action=adjustMedications
     false: action=probioticsOrAdjunct

7. stepId: stoolTesting
   question: "Yêu cầu cấy phân, antigen, PCR tùy nghi ngờ tác nhân?"
   type: boolean
   next:
     true: action=orderStoolTests
     false: action=empiricManagement

8. stepId: disposition
   question: "Cần nhập viện hay ngoại trú?"
   type: choice
   answers:
     - code: admit
       display: "Nhập viện"
       next: action=admitForCare
     - code: outpatient
       display: "Ngoại trú"
       next: action=dischargeWithAdvice

9. stepId: prevention
   question: "Hướng dẫn vệ sinh, thực phẩm và phòng ngừa sau xuất viện?"
   type: boolean
   next:
     true: action=providePreventionAdvice
     false: action=end

10. stepId: followUp
    question: "Sắp xếp tái khám nếu không cải thiện hoặc có dấu đỏ không?"
    type: boolean
    next:
      true: action=scheduleFollowup
      false: action=end

## Hành động

- id: resuscitateAndAdmit
  description: "Ổn định, bù dịch, điều trị nhiễm trùng nghi ngờ và nhập viện."
  type: intervention
  cpg-activity-type: acute-management
  useContext: cấp cứu

- id: orderStoolTestsAndStartABIfIndicated
  description: "Lấy mẫu phân, xét nghiệm và bắt đầu kháng sinh theo hướng dẫn nếu chỉ định."
  type: investigation
  cpg-activity-type: diagnostic
  useContext: xét nghiệm

- id: administerIVFluids
  description: "Bù dịch tĩnh mạch khi mất nước vừa đến nặng."
  type: intervention
  cpg-activity-type: supportive-care
  useContext: bù dịch

- id: oralRehydration
  description: "Bù nước đường miệng cho mất nước nhẹ vừa."
  type: action
  cpg-activity-type: patient-education
  useContext: ngoại trú

- id: referGastroenterologyAndColonoscopy
  description: "Giới thiệu tiêu hóa và nội soi khi nghi viêm ruột mạn hoặc nguyên nhân nghiêm trọng."
  type: referral
  cpg-activity-type: diagnostic
  useContext: tiêu hóa

- id: adjustMedications
  description: "Xem xét và điều chỉnh thuốc có thể gây tiêu chảy."
  type: action
  cpg-activity-type: medication-review
  useContext: dược

- id: orderStoolTests
  description: "Yêu cầu cấy phân, PCR, Clostridioides difficile test khi cần."
  type: investigation
  cpg-activity-type: laboratory
  useContext: xét nghiệm

- id: admitForCare
  description: "Nhập viện để theo dõi, bù dịch và điều trị khi cần."
  type: intervention
  cpg-activity-type: inpatient-care
  useContext: nhập viện

- id: dischargeWithAdvice
  description: "Xuất viện với hướng dẫn bù dịch, ăn uống và dấu hiệu cảnh báo."
  type: action
  cpg-activity-type: outpatient-care
  useContext: ngoại trú

- id: providePreventionAdvice
  description: "Hướng dẫn vệ sinh, an toàn thực phẩm và phòng ngừa lây truyền."
  type: action
  cpg-activity-type: patient-education
  useContext: giáo dục

- id: scheduleFollowup
  description: "Sắp xếp tái khám nếu triệu chứng kéo dài hoặc có dấu đỏ."
  type: action
  cpg-activity-type: administrative
  useContext: follow-up

- id: empiricManagement
  description: "Quản lý triệu chứng khi không có bằng chứng nhiễm trùng rõ ràng."
  type: action
  cpg-activity-type: symptomatic-care
  useContext: điều trị

## Bảng phân loại nguyên nhân tiêu chảy

| Loại | Ví dụ |
|------|------|
| Nhiễm trùng | Vi khuẩn, virus, ký sinh trùng |
| Thuốc | Kháng sinh, laxatives |
| Viêm mạn | IBD |

## Ghi chú

- Generated from diagrams/diarhea-diagram.png
