---
id: gait_abnormalities-diagram
title: Hướng dẫn đánh giá rối loạn dáng đi
description: Quy trình đánh giá rối loạn dáng đi, phân loại nguyên nhân (thần kinh, cơ xương, tiền đình), và đề xuất xét nghiệm/đánh giá chức năng.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
  - name: Reviewer Needed
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/gait_abnormalities-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho bệnh nhân có rối loạn dáng đi, té ngã lặp, hoặc thay đổi chức năng vận động. Mục tiêu phân loại nguyên nhân và hướng điều trị.

## Flow

1. stepId: gaitStart
   question: "Bệnh nhân có rối loạn dáng đi hoặc té ngã không?"
   type: boolean
   next:
     true: stepId=onsetAndAssoc
     false: action=exit-no-gait-issue

2. stepId: onsetAndAssoc
   question: "Khởi phát cấp hay mạn? Có yếu một bên, run, thay đổi cảm giác, chóng mặt?"
   type: choice
   answers:
     - code: acute
       display: "Cấp tính"
       next: action=urgentNeurology
     - code: chronic
       display: "Mạn tính"
       next: stepId=assessContributors

3. stepId: assessContributors
   question: "Đánh giá các yếu tố: thần kinh, cơ xương, tiền đình, thuốc, mô tả: mất cảm giác, yếu, spasticity?"
   type: choice
   answers:
     - code: neuro
       display: "Thần kinh"
       next: action=referredNeurology
     - code: ortho
       display: "Cơ xương"
       next: action=referredOrtho
     - code: vestibular
       display: "Tiền đình"
       next: action=vestibularAssessment
     - code: drug
       display: "Do thuốc"
       next: action=reviewMedications

4. stepId: fallRisk
   question: "Bệnh nhân có nguy cơ té ngã cao (tiền sử té ngã, dùng thuốc an thần, mất thị lực) không?"
   type: boolean
   next:
     true: action=fallPrevention
     false: stepId=mobilityAssessment

5. stepId: mobilityAssessment
   question: "Đánh giá chức năng đi: thời gian đứng, bước, kiểm tra cân bằng. Có trợ giúp cần thiết không?"
   type: boolean
   next:
     true: action=referredPhysio
     false: stepId=investigateNeurological

6. stepId: investigateNeurological
   question: "Có triệu chứng thần kinh tiến triển hay triệu chứng khu trú không?"
   type: boolean
   next:
     true: action=urgentNeurology
     false: stepId=assessMedications

7. stepId: assessMedications
   question: "Rà soát thuốc: benzodiazepine, antipsychotic, antihypertensive?"
   type: boolean
   next:
     true: action=reviewMedications
     false: stepId=vestibularTesting

8. stepId: vestibularTesting
   question: "Tiền đình nghi ngờ: có nghiệm pháp Dix-Hallpike hay triệu chứng chóng mặt kịch phát?"
   type: boolean
   next:
     true: action=vestibularAssessment
     false: stepId=orthopedicAssessment

9. stepId: orthopedicAssessment
   question: "Có biểu hiện đau, giới hạn khớp hoặc biến dạng ảnh hưởng dáng đi không?"
   type: boolean
   next:
     true: action=referredOrtho
     false: action=monitorAndPlan

10. stepId: disposition
    question: "Cần can thiệp cấp cứu, nhập viện hay quản lý ngoại trú?"
    type: choice
    answers:
      - code: admit
        display: "Nhập viện"
        next: action=urgentNeurology
      - code: outpatient
        display: "Ngoại trú"
        next: action=continueRehab

## Hành động

- id: urgentNeurology
  description: "Đánh giá thần kinh cấp cứu nếu có yếu liệt cấp, nghi ngờ đột quỵ; chụp hình ảnh và nhập viện."
  type: action
  cpg-activity-type: acute-management
  useContext: thần kinh cấp

- id: referredNeurology
  description: "Tham vấn thần kinh cho các rối loạn dáng đi do bệnh thần kinh mạn tính."
  type: referral
  cpg-activity-type: referral
  useContext: thần kinh

- id: referredOrtho
  description: "Tham vấn chuyên khoa chấn thương chỉnh hình khi có nguyên nhân cơ xương."
  type: referral
  cpg-activity-type: referral
  useContext: cơ xương

- id: vestibularAssessment
  description: "Đánh giá tiền đình: nghiệm pháp Dix-Hallpike, thử nghiệm Head Impulse, cân nhắc phục hồi chức năng tiền đình."
  type: investigation
  cpg-activity-type: vestibular-assessment
  useContext: tiền đình

- id: reviewMedications
  description: "Rà soát thuốc có thể gây rối loạn dáng đi (thuốc an thần, thuốc hạ huyết áp)."
  type: action
  cpg-activity-type: medication-review
  useContext: thuốc

- id: fallPrevention
  description: "Đánh giá và can thiệp phòng ngừa té ngã: điều chỉnh thuốc, môi trường sống, dụng cụ hỗ trợ."
  type: intervention
  cpg-activity-type: prevention
  useContext: phòng ngừa té ngã

- id: referredPhysio
  description: "Giới thiệu phục hồi chức năng để cải thiện dáng đi và cân bằng."
  type: referral
  cpg-activity-type: rehabilitation
  useContext: phục hồi

- id: monitorAndPlan
  description: "Theo dõi chức năng và lập kế hoạch điều trị dài hạn."
  type: follow-up
  cpg-activity-type: follow-up
  useContext: theo dõi

- id: continueRehab
  description: "Tiếp tục chương trình phục hồi chức năng, đánh giá định kỳ."
  type: follow-up
  cpg-activity-type: rehabilitation
  useContext: phục hồi

## Ghi chú / TODO

- Thêm mã hóa chuẩn.
- Generated from diagrams/gait_abnormalities-diagram.png

- Bảng phân loại nguyên nhân rối loạn dáng đi:

| Loại nguyên nhân    | Đặc điểm / Ví dụ                                  |
|---------------------|---------------------------------------------------|
| Thần kinh           | Đột quỵ, Parkinson, đa xơ cứng                     |
| Cơ xương            | Viêm khớp, gãy xương, đau cơ                       |
| Tiền đình           | Chóng mặt tiền đình, BPPV                           |
| Thuốc               | Thuốc an thần, thuốc huyết áp                       |
| Chuyển hóa / nội tiết| Thiếu B12, rối loạn điện giải                       |
