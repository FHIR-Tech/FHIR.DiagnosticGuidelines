---
id: flank_pain-diagram
title: Hướng dẫn đánh giá đau hông sườn
description: Quy trình đánh giá đau hông sườn, phân biệt nguyên nhân thận, cơ xương và sản phụ khoa, và đề xuất xử trí cấp hoặc theo dõi.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
  - name: Reviewer Needed
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/flank_pain-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho bệnh nhân đến khám vì đau vùng hông sườn. Mục tiêu: phân loại nguyên nhân cấp tính và mạn.

## Flow

1. stepId: flankStart
   question: "Bệnh nhân có đau hông sườn không?"
   type: boolean
   next:
     true: stepId=assessSevere
     false: action=exit-no-flank-pain

2. stepId: assessSevere
   question: "Có triệu chứng báo động: sốt cao, dấu nhiễm trùng huyết, tiểu ra máu, khó thở?"
   type: boolean
   next:
     true: action=urgentAssessment
     false: stepId=considerRenalStones

3. stepId: considerRenalStones
   question: "Triệu chứng gợi ý sỏi thận (đau quặn, tiểu ra máu)?"
   type: boolean
   next:
     true: action=manageRenalColic
     false: action=considerMusculoskeletalOrGyne

4. stepId: urinarySymptoms
   question: "Có kèm tiểu buốt, tiểu rắt, sốt hay nước tiểu đục không?"
   type: boolean
   next:
     true: action=investigateUTI
     false: stepId=musculoskeletalExam

5. stepId: musculoskeletalExam
   question: "Đau xuất hiện sau chấn thương hay vận động quá mức không?"
   type: boolean
   next:
     true: action=manageMusculoskeletal
     false: stepId=considerGyne

6. stepId: considerGyne
   question: "Nữ: có triệu chứng sản phụ khoa (rong kinh, đau bụng, xuất tiết) không?"
   type: boolean
   next:
     true: action=referGynae
     false: action=orderImaging

7. stepId: sepsisScreen
   question: "Có dấu hiệu nghi ngờ nhiễm trùng nặng (sốt cao, tụt huyết áp) không?"
   type: boolean
   next:
     true: action=urgentAssessment
     false: action=monitorAndPlan

8. stepId: followUp
   question: "Triệu chứng cải thiện sau điều trị không?"
   type: boolean
   next:
     true: action=continueManagement
     false: action=referSpecialist

9. stepId: disposition
   question: "Cần nhập viện hay khám ngoại trú?"
   type: choice
   answers:
     - code: admit
       display: "Nhập viện"
       next: action=urgentAssessment
     - code: outpatient
       display: "Ngoại trú"
       next: action=outpatient-eval

10. stepId: safetyNet
    question: "Cần hẹn tái khám hoặc cảnh báo nếu triệu chứng tăng nặng không?"
    type: boolean
    next:
      true: action=provideSafetyNet
      false: action=continueManagement

## Hành động

- id: urgentAssessment
  description: "Đánh giá cấp cứu nếu có dấu hiệu nhiễm trùng nặng hoặc mất ổn định huyết động."
  type: action
  cpg-activity-type: acute-management
  useContext: nhiễm trùng, cấp cứu

- id: manageRenalColic
  description: "Quản lý sỏi thận: giảm đau mạnh, chống nôn, xét nghiệm nước tiểu, siêu âm hoặc CT không chuẩn bị."
  type: intervention
  cpg-activity-type: management
  useContext: sỏi thận

- id: considerMusculoskeletalOrGyne
  description: "Xem xét nguyên nhân cơ xương hoặc sản phụ khoa (u nang buồng trứng, xoắn buồng trứng) nếu không phù hợp sỏi thận."
  type: investigation
  cpg-activity-type: differential-diagnosis
  useContext: cơ xương, sản phụ khoa

- id: investigateUTI
  description: "Lấy nước tiểu, xét nghiệm nhanh và cấy nước tiểu khi nghi nhiễm trùng tiết niệu."
  type: investigation
  cpg-activity-type: laboratory
  useContext: nhiễm trùng tiết niệu

- id: manageMusculoskeletal
  description: "Điều trị chấn thương/cơ xương: nghỉ ngơi, thuốc giảm đau, vật lý trị liệu hoặc chụp hình ảnh nếu cần."
  type: intervention
  cpg-activity-type: management
  useContext: cơ xương

- id: provideSafetyNet
  description: "Hướng dẫn bệnh nhân khi nào cần quay lại hoặc đi cấp cứu (tăng đau, sốt, nôn, không đi tiểu)."
  type: action
  cpg-activity-type: patient-education
  useContext: an toàn

- id: outpatient-eval
  description: "Đánh giá ngoại trú theo lịch nếu không cần nhập viện."
  type: follow-up
  cpg-activity-type: outpatient-care
  useContext: ngoại trú

## Ghi chú / TODO

- Generated from diagrams/flank_pain-diagram.png

- Bảng phân loại nguyên nhân đau hông sườn:

| Loại nguyên nhân    | Đặc điểm / Ví dụ                                  |
|---------------------|---------------------------------------------------|
| Thận / Niệu         | Sỏi thận, viêm thận bể thận, hematuria              |
| Cơ xương            | Căng cơ, gãy xương sườn, tổn thương mô mềm         |
| Sản phụ khoa        | U nang buồng trứng, xoắn buồng trứng               |
| Tiền đình / thần kinh| Đau lan tỏa từ cột sống, bệnh thần kinh             |
| Nhiễm trùng         | Abcess, viêm vùng chậu                              |
