---
id: foot_pain-diagram
title: Hướng dẫn đánh giá đau bàn chân
description: Quy trình đánh giá đau bàn chân, phân biệt nguyên nhân cơ học, nhiễm trùng, mạch máu và đề xuất xử trí ban đầu.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
  - name: Reviewer Needed
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/foot_pain-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho bệnh nhân than đau bàn chân với hoặc không có chấn thương.

## Flow

1. stepId: footStart
   question: "Có đau ở bàn chân không?"
   type: boolean
   next:
     true: stepId=mechanicalVsInfectious
     false: action=exit-no-foot-pain

2. stepId: mechanicalVsInfectious
   question: "Triệu chứng gợi ý cơ học (đau tăng khi vận động, liên quan giày dép) hay nhiễm trùng (đỏ, sưng, sốt)?"
   type: choice
   answers:
     - code: mechanical
       display: "Cơ học"
       next: action=manageMechanical
     - code: infectious
       display: "Nhiễm trùng"
       next: action=manageInfectious
     - code: vascular
       display: "Mạch máu"
       next: action=considerVascular

3. stepId: followUp
   question: "Cải thiện sau điều trị ban đầu?"
   type: boolean
   next:
     true: action=continueManagement
     false: action=referSpecialist

4. stepId: traumaHistory
   question: "Có tiền sử chấn thương hoặc vết thương ở bàn chân không?"
   type: boolean
   next:
     true: action=orderXray
     false: stepId=diabeticFootCheck

5. stepId: diabeticFootCheck
   question: "Bệnh nhân có đái tháo đường với loét hoặc giảm cảm giác không?"
   type: boolean
   next:
     true: action=urgentWoundCare
     false: stepId=vascularAssessment

6. stepId: vascularAssessment
   question: "Có dấu hiệu thiếu máu chi hoặc mạch kém không?"
   type: boolean
   next:
     true: action=orderDoppler
     false: stepId=considerInflammatory

7. stepId: considerInflammatory
   question: "Có dấu hiệu viêm toàn thân hoặc dấu hiệu khớp viêm không?"
   type: boolean
   next:
     true: action=orderInflammatoryMarkers
     false: action=conservativeManagement

8. stepId: biomechanics
   question: "Đánh giá bất thường cơ chế: phẫu thuật trước, phẳng/chân vòm cao, bàn chân bất đối xứng?"
   type: boolean
   next:
     true: action=referOrtho
     false: action=continueManagement

9. stepId: infectionSigns
   question: "Có sưng đỏ ấm, mủ hay sốt?"
   type: boolean
   next:
     true: action=manageInfectious
     false: action=monitorAndPhysio

10. stepId: disposition
    question: "Cần can thiệp phẫu thuật hay ngoại trú?"
    type: choice
    answers:
      - code: surgical
        display: "Cần phẫu thuật"
        next: action=referredOrtho
      - code: conservative
        display: "Quản lý bảo tồn"
        next: action=continueManagement

## Hành động

- id: manageMechanical
  description: "Điều trị nguyên nhân cơ học: chỉnh giày, vật lý trị liệu, orthotics, nghỉ ngơi."
  type: intervention
  cpg-activity-type: management
  useContext: cơ học

- id: manageInfectious
  description: "Xử trí nhiễm trùng: kháng sinh, thoát mủ nếu cần, theo dõi."
  type: intervention
  cpg-activity-type: management
  useContext: nhiễm trùng

- id: considerVascular
  description: "Xem xét nguyên nhân mạch máu: thuyên tắc, thiếu máu chi; đo mạch, Doppler nếu cần."
  type: investigation
  cpg-activity-type: vascular-assessment
  useContext: mạch máu

- id: continueManagement
  description: "Tiếp tục quản lý triệu chứng và theo dõi."
  type: follow-up
  cpg-activity-type: follow-up
  useContext: tiếp tục

- id: referSpecialist
  description: "Tham vấn chuyên khoa chỉnh hình hoặc nhiễm trùng nếu không cải thiện."
  type: referral
  cpg-activity-type: referral
  useContext: tham vấn

- id: orderXray
  description: "Chụp X-quang bàn chân khi nghi ngờ gãy, trật hoặc tổn thương xương."
  type: investigation
  cpg-activity-type: imaging
  useContext: chấn thương

- id: urgentWoundCare
  description: "Cung cấp chăm sóc vết thương cấp, kháng sinh phổ rộng, và tham vấn lâm sàng nếu cần cho bệnh nhân đái tháo đường."
  type: intervention
  cpg-activity-type: wound-care
  useContext: đái tháo đường

- id: orderDoppler
  description: "Yêu cầu siêu âm Doppler mạch chi nếu nghi ngờ thiếu máu cục bộ."
  type: investigation
  cpg-activity-type: vascular-assessment
  useContext: mạch máu

- id: orderInflammatoryMarkers
  description: "Yêu cầu CRP, ESR, xét nghiệm kháng thể nếu nghi viêm/viêm khớp."
  type: investigation
  cpg-activity-type: laboratory
  useContext: viêm

- id: monitorAndPhysio
  description: "Theo dõi và giới thiệu vật lý trị liệu/orthotics khi phù hợp."
  type: follow-up
  cpg-activity-type: rehabilitation
  useContext: phục hồi

## Ghi chú / TODO

- Generated from diagrams/foot_pain-diagram.png

- Bảng phân loại nguyên nhân đau bàn chân:

| Loại nguyên nhân    | Đặc điểm / Ví dụ                                  |
|---------------------|---------------------------------------------------|
| Cơ học              | Plantar fasciitis, Morton neuroma, thoái hóa       |
| Nhiễm trùng         | Cellulitis, áp xe, viêm xương tủy                  |
| Mạch máu            | Thiếu máu chi, tắc mạch                            |
| Thần kinh            | Neuropathy (đái tháo đường)                        |
| Viêm/Viêm khớp      | Gout, viêm khớp dạng thấp                           |
