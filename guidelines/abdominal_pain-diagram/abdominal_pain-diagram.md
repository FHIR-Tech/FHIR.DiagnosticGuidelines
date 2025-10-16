---
id: abdominal_pain-diagram
title: Hướng dẫn đau bụng (abdominal pain)
description: Quy trình đánh giá đau bụng cấp và mạn, phân loại theo vị trí, mức độ, dấu báo động và hướng xử trí ban đầu.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/abdominal_pain-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho bệnh nhân đau bụng; mục tiêu phân biệt nguyên nhân cấp cứu (viêm ruột thừa, tắc ruột, xuất huyết) và nguyên nhân mạn tính, đưa ra hướng xử trí ban đầu và chỉ định khám thêm.

## Flow

1. stepId: immediateLifeThreat
   question: "Có sốc, dấu bụng cứng, khó thở, hoặc mất ý thức không?"
   type: boolean
   next:
     true: action=resuscitateAndUrgentSurgery
     false: stepId=onsetDuration

2. stepId: onsetDuration
   question: "Khởi phát đột ngột hay từ từ; kèm sốt/nôn/tiêu chảy không?"
   type: choice
   answers:
     - code: acute
       display: "Cấp"
       next: stepId=localizePain
     - code: chronic
       display: "Mạn"
       next: stepId=considerChronicCauses

3. stepId: localizePain
   question: "Đau ở vị trí nào (trên, dưới, phải, trái, quanh rốn)?"
   type: choice
   answers:
     - code: RUQ
       display: "Vùng trên phải"
       next: action=considerBiliaryOrHepatic
     - code: RLQ
       display: "Vùng dưới phải"
       next: action=considerAppendicitis
     - code: LUQ
       display: "Trên trái"
       next: action=considerPancreatitisOrSplenic
     - code: LLQ
       display: "Dưới trái"
       next: action=considerDiverticulitis
     - code: peri
       display: "Quanh rốn"
       next: action=considerObstructionOrGastroenteritis

4. stepId: evaluatePeritonitis
   question: "Có dấu viêm phúc mạc (bụng cứng, phản ứng thành bụng) không?"
   type: boolean
   next:
     true: action=urgentImagingAndSurgicalReview
     false: stepId=labsAndImaging

5. stepId: labsAndImaging
   question: "Cần xét nghiệm máu, nước tiểu, siêu âm hoặc CT không?"
   type: boolean
   next:
     true: action=orderLabsAndImaging
     false: action=conservativeManagement

6. stepId: GIbleed
   question: "Có nôn ra máu, phân đen, tụt huyết áp không?"
   type: boolean
   next:
     true: action=resuscitateAndGIurgent
     false: stepId=medReview

7. stepId: medReview
   question: "Thuốc gần đây (NSAID, aspirin) có thể góp phần không?"
   type: boolean
   next:
     true: action=adjustMedications
     false: action=planFollowup

8. stepId: considerOBGYN
   question: "Phụ nữ: có dấu hiệu thai nghén, đau vùng khung chậu, chảy máu âm đạo không?"
   type: boolean
   next:
     true: action=orderPregnancyTestAndGynReferral
     false: action=continueAssessment

9. stepId: disposition
   question: "Cần nhập viện, can thiệp cấp cứu hay ngoại trú?"
   type: choice
   answers:
     - code: admit
       display: "Nhập viện"
       next: action=admitForObservationOrSurgery
     - code: outpatient
       display: "Ngoại trú"
       next: action=dischargeWithPlan

10. stepId: followUp
    question: "Sắp xếp tái khám hoặc nội soi/ khám chuyên khoa không?"
    type: boolean
    next:
      true: action=arrangeFollowupAndSpecialty
      false: action=end

## Hành động

- id: resuscitateAndUrgentSurgery
  description: "Ổn định ABC, truyền dịch, chuẩn bị mổ cấp nếu cần."
  type: intervention
  cpg-activity-type: emergency
  useContext: cấp cứu

- id: considerAppendicitis
  description: "Đánh giá lâm sàng và hình ảnh nếu nghi viêm ruột thừa; sắp xếp phẫu thuật khi chỉ định."
  type: investigation
  cpg-activity-type: diagnostic
  useContext: phẫu thuật

- id: considerBiliaryOrHepatic
  description: "Xem xét sỏi mật, viêm túi mật, xét nghiệm men gan, siêu âm."
  type: investigation
  cpg-activity-type: imaging
  useContext: gan-mật

- id: considerPancreatitisOrSplenic
  description: "Xem xét viêm tụy, chấn thương lách; kiểm tra amylase/lipase, CT khi cần."
  type: investigation
  cpg-activity-type: laboratory
  useContext: tụy

- id: considerDiverticulitis
  description: "Xem xét diverticulitis với CT bụng và kháng sinh khi cần."
  type: investigation
  cpg-activity-type: treatment
  useContext: diverticulitis

- id: urgentImagingAndSurgicalReview
  description: "Siêu âm/CT khẩn và thăm khám phẫu thuật khi nghi viêm phúc mạc."
  type: intervention
  cpg-activity-type: imaging
  useContext: phúc mạc

- id: orderLabsAndImaging
  description: "Yêu cầu xét nghiệm công thức máu, CRP, điện giải và hình ảnh theo hướng dẫn."
  type: investigation
  cpg-activity-type: laboratory
  useContext: xét nghiệm

- id: resuscitateAndGIurgent
  description: "Ổn định, truyền máu nếu cần, gọi chuyên khoa tiêu hóa khẩn."
  type: intervention
  cpg-activity-type: emergency
  useContext: xuất huyết

- id: adjustMedications
  description: "Dừng hoặc điều chỉnh thuốc có thể gây viêm/ chảy máu (NSAID, anticoagulant)."
  type: action
  cpg-activity-type: medication-review
  useContext: dược

- id: orderPregnancyTestAndGynReferral
  description: "Xét nghiệm thai và chuyển khám phụ khoa nếu nghi ngờ nguyên nhân sản phụ khoa."
  type: investigation
  cpg-activity-type: diagnostic
  useContext: sản-phụ-khoa

- id: admitForObservationOrSurgery
  description: "Nhập viện để quan sát, điều trị hoặc phẫu thuật tùy kết quả chẩn đoán."
  type: intervention
  cpg-activity-type: inpatient-care
  useContext: nhập viện

- id: dischargeWithPlan
  description: "Xuất viện với hướng dẫn điều trị triệu chứng, dinh dưỡng và dấu hiệu cảnh báo."
  type: action
  cpg-activity-type: outpatient-care
  useContext: ngoại trú

- id: arrangeFollowupAndSpecialty
  description: "Sắp xếp khám chuyên khoa tiêu hóa hoặc phẫu thuật theo kết quả."
  type: action
  cpg-activity-type: administrative
  useContext: follow-up

## Bảng phân loại nguyên nhân đau bụng

| Loại | Ví dụ |
|------|------|
| Cấp tính | Viêm ruột thừa, tắc ruột |
| Viêm/ nhiễm | Viêm tụy, viêm túi mật |
| Mạn tính | IBS, IBD |

## Ghi chú

- Generated from `diagrams/abdominal_pain-diagram.png`
