---
id: foot_swelling-diagram
title: Hướng dẫn sưng bàn chân (foot swelling)
description: Đánh giá sưng bàn chân: nguyên nhân tim, thận, tắc mạch, chấn thương, nhiễm trùng và hướng xử trí ban đầu.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/foot_swelling-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho bệnh nhân sưng chân; mục tiêu phân biệt phù toàn thân vs phù khu trú, xác định dấu hiệu huyết khối tĩnh mạch sâu (DVT) và xử trí ban đầu.

## Flow

1. stepId: limbThreat
   question: "Có đau dữ dội, tím, bầm tím nặng hoặc mất mạch không?"
   type: boolean
   next:
     true: action=urgentVascularReferral
     false: stepId=bilateralOrUnilateral

2. stepId: bilateralOrUnilateral
   question: "Sưng hai bên hay một bên?"
   type: choice
   answers:
     - code: bilateral
       display: "Hai bên"
       next: stepId=considerSystemicCauses
     - code: unilateral
       display: "Một bên"
       next: stepId=considerDVTOrLocalInjury

3. stepId: considerSystemicCauses
   question: "Có suy tim, thận, gan hoặc dùng thuốc gây phù không?"
   type: boolean
   next:
     true: action=optimizeSystemicTreatment
     false: action=investigateOtherCauses

4. stepId: considerDVTOrLocalInjury
   question: "Có đau khi gấp cổ chân, đỏ nóng khu trú hoặc yếu tố nguy cơ DVT không?"
   type: boolean
   next:
     true: action=orderDopplerUltrasoundAndAnticoagulateIfIndicated
     false: action=imagingOrConservativeCare

5. stepId: infectionCheck
   question: "Dấu hiệu nhiễm trùng (sốt, đỏ lan tỏa) không?"
   type: boolean
   next:
     true: action=startAntibioticsAndRefer
     false: action=conservativeManagement

6. stepId: medicationReview
   question: "Thuốc như NSAID, CCB có góp phần không?"
   type: boolean
   next:
     true: action=adjustMedications
     false: action=monitor

7. stepId: imaging
   question: "Cần X-quang, siêu âm hoặc CT để đánh giá không?"
   type: boolean
   next:
     true: action=orderImaging
     false: action=followUp

8. stepId: compression
   question: "Có chỉ định nén hoặc băng ép không?"
   type: boolean
   next:
     true: action=prescribeCompressionAndPhysio
     false: action=end

9. stepId: disposition
   question: "Cần nhập viện hay ngoại trú?"
   type: choice
   answers:
     - code: admit
       display: "Nhập viện"
       next: action=admitForTreatment
     - code: outpatient
       display: "Ngoại trú"
       next: action=dischargeWithPlan

10. stepId: followUp
    question: "Sắp xếp theo dõi, siêu âm lại hoặc đánh giá chuyên khoa?"
    type: boolean
    next:
      true: action=arrangeFollowup
      false: action=end

## Hành động

- id: urgentVascularReferral
  description: "Tham vấn mạch máu khẩn nếu có dấu hiệu đe dọa chi."
  type: referral
  cpg-activity-type: emergency
  useContext: khẩn

- id: optimizeSystemicTreatment
  description: "Tối ưu điều trị suy tim, thận, gan và điều chỉnh thuốc."
  type: action
  cpg-activity-type: management
  useContext: hệ thống

- id: orderDopplerUltrasoundAndAnticoagulateIfIndicated
  description: "Siêu âm doppler để chẩn đoán DVT và bắt đầu chống đông nếu xác định."
  type: investigation
  cpg-activity-type: imaging
  useContext: DVT

- id: startAntibioticsAndRefer
  description: "Kê kháng sinh và chuyển chuyên khoa nếu nghi nhiễm trùng lan tỏa."
  type: intervention
  cpg-activity-type: medication
  useContext: nhiễm trùng

- id: prescribeCompressionAndPhysio
  description: "Hướng dẫn bó ép, nén và vật lý trị liệu khi phù mạn."
  type: action
  cpg-activity-type: rehabilitation
  useContext: phục hồi

- id: admitForTreatment
  description: "Nhập viện để can thiệp khi phù nặng hoặc nhiễm trùng."
  type: intervention
  cpg-activity-type: inpatient-care
  useContext: nhập viện

- id: arrangeFollowup
  description: "Sắp xếp siêu âm lại hoặc khám chuyên khoa để theo dõi."
  type: action
  cpg-activity-type: administrative
  useContext: follow-up

- id: adjustMedications
  description: "Điều chỉnh thuốc có thể gây phù sau thảo luận."
  type: action
  cpg-activity-type: medication-review
  useContext: dược

- id: orderImaging
  description: "Yêu cầu các xét nghiệm hình ảnh phù hợp để xác định nguyên nhân."
  type: investigation
  cpg-activity-type: diagnostic
  useContext: imaging

- id: dischargeWithPlan
  description: "Xuất viện với hướng dẫn điều trị, nén và hẹn tái khám."
  type: action
  cpg-activity-type: outpatient-care
  useContext: ngoại trú

## Bảng phân loại nguyên nhân sưng chân

| Loại | Ví dụ |
|------|------|
| Hệ thống | Suy tim, thận |
| DVT | Thrombus tĩnh mạch sâu |
| Cục bộ | Nhiễm trùng, chấn thương |

## Ghi chú

- Generated from diagrams/foot_swelling-diagram.png
