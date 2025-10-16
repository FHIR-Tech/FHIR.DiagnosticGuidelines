---
id: ankie_pain-diagram
title: Hướng dẫn đau mắt cá chân (ankle pain)
description: Đánh giá đau mắt cá chân: phân loại chấn thương, bong gân, gãy xương, viêm khớp và xử trí ban đầu.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/ankie_pain-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho bệnh nhân đau mắt cá; mục tiêu phân biệt chấn thương cấp tính cần cố định hay gãy xương, vs nguyên nhân mạn tính như viêm khớp, tendonopathy.

## Flow

1. stepId: limbThreat
   question: "Mất mạch, biến dạng rõ, đau quá mức so với kiểm tra hay dấu tổn thương mạch không?"
   type: boolean
   next:
     true: action=urgentOrthoReferral
     false: stepId=mechanismOfInjury

2. stepId: mechanismOfInjury
   question: "Có chấn thương vấp, xoay cổ chân, té ngã hoặc hoạt động thể thao gần đây không?"
   type: boolean
   next:
     true: action=applyRICEAndAssessForFracture
     false: stepId=chronicCauses

3. stepId: assessForFracture
   question: "Sờ đau khu trú, sưng lớn, không chịu lực được không?"
   type: boolean
   next:
     true: action=orderXrayAndImmobilize
     false: action=trialConservativeCare

4. stepId: neurovascular
   question: "Kiểm tra thần kinh và mạch máu chi khi có chấn thương?"
   type: boolean
   next:
     true: action=documentAndReferIfAbnormal
     false: action=continuePlan

5. stepId: tendonOrLigament
   question: "Nghi bong gân nặng, tendon rupture hay instability không?"
   type: boolean
   next:
     true: action=referOrthopedicsOrPlaster
     false: action=physioAndAnalgesia

6. stepId: infectionConsider
   question: "Có đỏ, nóng, sốt gợi ý nhiễm trùng không?"
   type: boolean
   next:
     true: action=startAntibioticsAndRefer
     false: action=continueSupportiveCare

7. stepId: chronicEvaluation
   question: "Đau kéo dài, yếu tố arthritic hoặc gout không?"
   type: boolean
   next:
     true: action=orderLabsAndReferRheumatology
     false: action=conservativeManagement

8. stepId: imaging
   question: "Cần MRI/US nếu nghi tendon rupture hoặc tổn thương mô mềm?"
   type: boolean
   next:
     true: action=orderAdvancedImaging
     false: action=planRehab

9. stepId: disposition
   question: "Cần nhập viện hay ngoại trú?"
   type: choice
   answers:
     - code: admit
       display: "Nhập viện"
       next: action=admitForSurgeryIfRequired
     - code: outpatient
       display: "Ngoại trú"
       next: action=dischargeWithOrthoFollowup

10. stepId: followUp
    question: "Sắp xếp vật lý trị liệu hoặc tầm soát lại không?"
    type: boolean
    next:
      true: action=arrangeRehabAndFollowup
      false: action=end

## Hành động

- id: urgentOrthoReferral
  description: "Gọi/ chuyển chuyên khoa chấn thương chỉnh hình khẩn nếu có tổn thương nặng."
  type: referral
  cpg-activity-type: emergency
  useContext: khẩn

- id: applyRICEAndAssessForFracture
  description: "Nghỉ, băng, chườm đá, kê cao, và đánh giá gãy xương theo Ottawa rules."
  type: action
  cpg-activity-type: first-aid
  useContext: ban-dau

- id: orderXrayAndImmobilize
  description: "Chụp X-quang; cố định bằng nẹp hoặc băng, chuyển chuyên khoa nếu gãy."
  type: investigation
  cpg-activity-type: imaging
  useContext: chẩn đoán

- id: trialConservativeCare
  description: "Giảm đau, nghỉ, nẹp mềm và theo dõi đáp ứng."
  type: action
  cpg-activity-type: symptomatic-care
  useContext: điều-trị

- id: documentAndReferIfAbnormal
  description: "Ghi nhận kết quả kiểm tra thần kinh/mạch và tham vấn nếu bất thường."
  type: action
  cpg-activity-type: administrative
  useContext: hồ-sơ

- id: referOrthopedicsOrPlaster
  description: "Tham vấn chỉnh hình để cân nhắc phẫu thuật hoặc bó bột."
  type: referral
  cpg-activity-type: procedural
  useContext: chỉnh-hình

- id: startAntibioticsAndRefer
  description: "Bắt đầu kháng sinh nếu nghi nhiễm trùng sâu và chuyển chuyên khoa."
  type: intervention
  cpg-activity-type: medication
  useContext: nhiễm-trùng

- id: orderLabsAndReferRheumatology
  description: "Xét nghiệm sàng lọc gout/viêm khớp và giới thiệu khớp/ thấp khớp nếu cần."
  type: investigation
  cpg-activity-type: laboratory
  useContext: thấp-khớp

- id: orderAdvancedImaging
  description: "Yêu cầu MRI/US để đánh giá tổn thương mô mềm khi chỉ định."
  type: investigation
  cpg-activity-type: imaging
  useContext: mô-mềm

- id: admitForSurgeryIfRequired
  description: "Nhập viện chuẩn bị can thiệp nếu tổn thương yêu cầu phẫu thuật."
  type: intervention
  cpg-activity-type: inpatient-care
  useContext: phẫu-thuật

- id: dischargeWithOrthoFollowup
  description: "Xuất viện với hướng dẫn, nẹp, và hẹn chỉnh hình."
  type: action
  cpg-activity-type: outpatient-care
  useContext: ngoại-trú

- id: arrangeRehabAndFollowup
  description: "Sắp xếp vật lý trị liệu và tái khám theo kế hoạch."
  type: action
  cpg-activity-type: rehabilitation
  useContext: phục-hồi

## Bảng phân loại nguyên nhân đau mắt cá

| Loại | Ví dụ |
|------|------|
| Chấn thương | Bong gân, gãy xương |
| Viêm | Tendonopathy, gout |
| Nhiễm trùng | Cellulitis |

## Ghi chú

- Generated from `diagrams/ankie_pain-diagram.png`
