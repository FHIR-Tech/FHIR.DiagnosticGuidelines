---
id: eye_pain-diagram
title: Hướng dẫn đau mắt (eye pain)
description: Đánh giá đau mắt: phân biệt nguyên nhân bề mặt (keratitis), đau nội nhãn (uveitis, glaucoma), thần kinh (trigeminal) và nhiễm trùng.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/eye_pain-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho bệnh nhân đau mắt; mục tiêu xác định bệnh cấp cứu (glaucoma góc đóng) và chỉ định khám chuyên khoa mắt.

## Flow

1. stepId: visionThreatening
   question: "Mất thị lực đột ngột, đau dữ dội, đỏ mắt nặng kèm nôn không?"
   type: boolean
   next:
     true: action=urgentOphthalmology
     false: stepId=foreignBodyOrSurface

2. stepId: foreignBodyOrSurface
   question: "Có cảm giác dị vật, chấn thương hoặc tiếp xúc hóa chất?"
   type: boolean
   next:
     true: action=removeForeignBodyAndIrrigate
     false: stepId=cornealSigns

3. stepId: cornealSigns
   question: "Mờ giác mạc, ulcus, cơ đau khi mở mắt không?"
   type: boolean
   next:
     true: action=topicalAntibioticsAndRefer
     false: action=assessForUveitisOrGlaucoma

4. stepId: assessForUveitisOrGlaucoma
   question: "Có đau nhãn cầu, photophobia, mid-dilated pupil, tăng áp lực nhãn cầu không?"
   type: boolean
   next:
     true: action=urgentIOPManagementAndRefer
     false: action=conservativeCare

5. stepId: infectionSigns
   question: "Có chảy mủ, tiết dịch, sốt hoặc dấu hiệu toàn thân?"
   type: boolean
   next:
     true: action=systemicAntibioticsIfIndicated
     false: action=symptomaticCare

6. stepId: contactLensUsers
   question: "Người dùng kính áp tròng có nguy cơ keratitis nặng không?"
   type: boolean
   next:
     true: action=coverAndReferUrgent
     false: action=continueEvaluation

7. stepId: redFlags
   question: "Dấu hiệu thần kinh kèm theo (photophobia, nôn, giảm ý thức) không?"
   type: boolean
   next:
     true: action=neuroImagingAndRefer
     false: action=outpatientPlan

8. stepId: painManagement
   question: "Cần kiểm soát đau ngay (analgesia, topical) không?"
   type: boolean
   next:
     true: action=providePainRelief
     false: action=monitor

9. stepId: disposition
   question: "Cần nhập viện hay ngoại trú?"
   type: choice
   answers:
     - code: admit
       display: "Nhập viện"
       next: action=admitForOcularCare
     - code: outpatient
       display: "Ngoại trú"
       next: action=dischargeWithAdvice

10. stepId: followUp
    question: "Cần hẹn tái khám mắt trong 24–48 giờ không?"
    type: boolean
    next:
      true: action=arrangeOphthalmologyFollowup
      false: action=end

## Hành động

- id: urgentOphthalmology
  description: "Gọi chuyên khoa mắt khẩn khi nghi tổn thương đe dọa thị lực."
  type: referral
  cpg-activity-type: emergency
  useContext: khẩn

- id: removeForeignBodyAndIrrigate
  description: "Loại bỏ dị vật bề mặt và rửa mắt kỹ lưỡng nếu là hoá chất."
  type: intervention
  cpg-activity-type: procedure
  useContext: cấp cứu

- id: topicalAntibioticsAndRefer
  description: "Kê kháng sinh tại chỗ và tham vấn nếu nghi keratitis."
  type: intervention
  cpg-activity-type: medication
  useContext: keratitis

- id: urgentIOPManagementAndRefer
  description: "Quản lý tăng nhãn áp cấp và chuyển chuyên khoa mắt ngay."
  type: intervention
  cpg-activity-type: emergency
  useContext: glaucoma

- id: systemicAntibioticsIfIndicated
  description: "Kê kháng sinh toàn thân nếu có nhiễm trùng lan tỏa."
  type: action
  cpg-activity-type: medication
  useContext: nhiễm trùng

- id: coverAndReferUrgent
  description: "Che mắt, ngưng đeo kính áp tròng và chuyển khám khẩn."
  type: action
  cpg-activity-type: safety
  useContext: contact-lens

- id: neuroImagingAndRefer
  description: "Chụp não nếu có dấu thần kinh và tham vấn đa chuyên khoa."
  type: investigation
  cpg-activity-type: imaging
  useContext: thần kinh

- id: providePainRelief
  description: "Cung cấp thuốc giảm đau và hướng dẫn an toàn sử dụng."
  type: action
  cpg-activity-type: symptomatic-care
  useContext: giảm đau

- id: admitForOcularCare
  description: "Nhập viện để điều trị mắt và theo dõi nếu cần."
  type: intervention
  cpg-activity-type: inpatient-care
  useContext: nhập viện

- id: arrangeOphthalmologyFollowup
  description: "Sắp xếp tái khám chuyên khoa mắt trong 24–48 giờ."
  type: action
  cpg-activity-type: administrative
  useContext: follow-up

## Bảng phân loại nguyên nhân đau mắt

| Loại | Ví dụ |
|------|------|
| Bề mặt | Keratitis, foreign body |
| Nội nhãn | Uveitis, glaucoma |
| Thần kinh | Trigeminal neuralgia |

## Ghi chú

- Generated from diagrams/eye_pain-diagram.png
