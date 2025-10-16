---
id: vaginal_irritation-diagram
title: Hướng dẫn đánh giá kích ứng âm đạo
description: Quy trình đánh giá kích ứng âm đạo, phân biệt giữa nhiễm trùng, dị ứng và nguyên nhân cơ học, và đề xuất xử trí ban đầu.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
  - name: Reviewer Needed
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/vaginal_irritation-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho bệnh nhân nữ than kích ứng, ngứa hoặc bỏng rát vùng âm đạo; mục tiêu phân loại nguyên nhân và đề xuất xét nghiệm/điều trị ban đầu.

## Flow

1. stepId: vagIrrStart
   question: "Bệnh nhân có triệu chứng kích ứng âm đạo (ngứa, rát, tiết dịch) không?"
   type: boolean
   next:
     true: stepId=assocSymptoms
     false: action=exit-no-complaint

2. stepId: assocSymptoms
   question: "Có tiết dịch mùi, máu, đau khi giao hợp hay rối loạn tiểu tiện không?"
   type: choice
   answers:
     - code: discharge
       display: "Tiết dịch mùi"
       next: action=considerVaginalInfection
     - code: painfulIntercourse
       display: "Đau khi giao hợp"
       next: action=referGynae
     - code: localizedIrritation
       display: "Kích ứng khu trú / dị ứng"
       next: action=manageIrritation

3. stepId: allergyAssessment
   question: "Có tiếp xúc với sản phẩm mới (xà phòng, dung dịch, thuốc) gần đây không?"
   type: boolean
   next:
     true: action=adviseRemoveIrritant
     false: action=considerVaginalInfection

4. stepId: followUp
   question: "Triệu chứng cải thiện sau xử trí ban đầu không?"
   type: boolean
   next:
     true: action=continueManagement
     false: action=referGynae

5. stepId: recurrentEpisodes
   question: "Triệu chứng tái phát nhiều lần trong 12 tháng không?"
   type: boolean
   next:
     true: action=referGynae
     false: action=adviseRemoveIrritant

6. stepId: systemicSymptoms
   question: "Có sốt hoặc dấu hiệu toàn thân không?"
   type: boolean
   next:
     true: action=investigateSystemic
     false: stepId=localExam

7. stepId: localExam
   question: "Khám vùng sinh dục có tổn thương, loét hay phát ban không?"
   type: boolean
   next:
     true: action=referDermatology
     false: action=manageIrritation

8. stepId: pregnancyCheck
   question: "Có khả năng mang thai không?"
   type: boolean
   next:
     true: action=orderPregnancyTest
     false: stepId=allergyAssessment

9. stepId: contraceptionReview
   question: "Sử dụng dụng cụ tránh thai hoặc chất tẩy rửa có liên quan không?"
   type: boolean
   next:
     true: action=adviseRemoveIrritant
     false: action=continueManagement

10. stepId: safetyNet
    question: "Triệu chứng nặng lên (sưng, khó thở, sốt cao) không?"
    type: boolean
    next:
      true: action=referGynae
      false: action=continueManagement

## Hành động

- id: considerVaginalInfection
  description: "Xem xét nhiễm nấm, nhiễm khuẩn, và vi khuẩn âm đạo; lấy mẫu dịch để làm xét nghiệm và điều trị phù hợp."
  type: investigation
  cpg-activity-type: laboratory
  useContext: nhiễm âm đạo

- id: referGynae
  description: "Tham vấn sản phụ khoa khi có đau khi giao hợp, chảy máu bất thường hoặc triệu chứng không cải thiện."
  type: referral
  cpg-activity-type: referral
  useContext: sản phụ khoa

- id: manageIrritation
  description: "Ngưng các chất khả nghi gây kích ứng, hướng dẫn vệ sinh và dùng corticosteroid bôi nhẹ hoặc thuốc kháng nấm/khang khuẩn theo kết quả xét nghiệm."
  type: intervention
  cpg-activity-type: management
  useContext: kích ứng

- id: adviseRemoveIrritant
  description: "Khuyến nghị ngưng dùng sản phẩm nghi ngờ (xà phòng, dung dịch tẩy rửa, gel) và theo dõi."
  type: action
  cpg-activity-type: patient-education
  useContext: vệ sinh

- id: continueManagement
  description: "Tiếp tục điều trị triệu chứng và hẹn tái khám nếu cần."
  type: follow-up
  cpg-activity-type: follow-up
  useContext: theo dõi

- id: investigateSystemic
  description: "Thực hiện công thức máu, CRP và xét nghiệm cần thiết khi nghi ngờ nhiễm trùng hệ thống."
  type: investigation
  cpg-activity-type: laboratory
  useContext: hệ thống

- id: referDermatology
  description: "Tham vấn da liễu nếu có tổn thương da nghiêm trọng hoặc không rõ nguyên nhân."
  type: referral
  cpg-activity-type: referral
  useContext: da liễu

- id: orderPregnancyTest
  description: "Yêu cầu test thai để loại trừ nguyên nhân liên quan thai nghén."
  type: investigation
  cpg-activity-type: laboratory
  useContext: thai nghén

## Ghi chú / TODO

- Generated from diagrams/vaginal_irritation-diagram.png

- Bảng phân loại nguyên nhân kích ứng âm đạo:

| Loại nguyên nhân    | Đặc điểm / Ví dụ                                  |
|---------------------|---------------------------------------------------|
| Nhiễm trùng         | Nhiễm nấm, BV, STI                                  |
| Dị ứng / Kích ứng    | Xà phòng, dung dịch tẩy, thuốc bôi                  |
| Cơ học               | Thoa quá mạnh, tampon, tổn thương cơ học            |
| Nội tiết             | Thay đổi estrogen (hậu mãn kinh)                    |
| Thuốc               | Thuốc gây kích ứng, điều trị tại chỗ                 |

