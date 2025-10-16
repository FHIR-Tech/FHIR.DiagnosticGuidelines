---
id: hearing_loss-diagram
title: Hướng dẫn chẩn đoán mất thính lực
description: Quy trình đánh giá mất thính lực và ù tai, phân loại nguyên nhân (dẫn truyền, cảm giác thần kinh, trung ương) và đề xuất xét nghiệm/điều trị ban đầu.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
  - name: Reviewer Needed
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/hearing_loss-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho bệnh nhân than mất thính lực hoặc ù tai. Mục tiêu là phân loại nguyên nhân, xác định dấu hiệu báo động và đề xuất xét nghiệm (audiometry, hình ảnh) và quản lý ban đầu.

## Quy trình

1. stepId: hearingStart
   question: "Bệnh nhân có mất thính lực hoặc ù tai không?"
   type: boolean
   next:
     true: stepId=onsetAndAssoc
     false: action=exit-no-hearing-complaint

2. stepId: onsetAndAssoc
   question: "Khởi phát đột ngột hay từ từ? Có tiền sử chấn thương, phơi nhiễm tiếng ồn, dùng thuốc độc thính giác?"
   type: choice
   answers:
     - code: sudden
       display: "Đột ngột"
       next: action=urgentAudiology
     - code: gradual
       display: "Từ từ"
       next: stepId=assessType

3. stepId: assessType
   question: "Phân loại: dẫn truyền, cảm giác thần kinh, hỗn hợp hay trung ương?"
   type: choice
   answers:
     - code: conductive
       display: "Dẫn truyền"
       next: action=manageConductive
     - code: sensorineural
       display: "Cảm giác thần kinh"
       next: action=manageSensorineural
     - code: central
       display: "Trung ương"
       next: action=referNeurology

4. stepId: infectionOrTrauma
   question: "Có kèm đau tai, chảy mủ, sốt hoặc tiền sử chấn thương không?"
   type: boolean
   next:
     true: action=investigateInfectionOrTrauma
     false: action=orderAudiometry

5. stepId: followUp
   question: "Đã thực hiện audiometry và cải thiện theo kế hoạch không?"
   type: boolean
   next:
     true: action=interpretAudiometry
     false: action=referSpecialist
  
6. stepId: occupationalNoise
   question: "Bệnh nhân có tiếp xúc tiếng ồn nghề nghiệp hay tai nạn âm thanh gần đây không?"
   type: boolean
   next:
     true: action=adviseHearingProtection
     false: stepId=vestibularSymptoms

7. stepId: vestibularSymptoms
   question: "Có kèm chóng mặt, mất thăng bằng, ù tai nặng không?"
   type: boolean
   next:
     true: action=vestibularAssessment
     false: stepId=medicationReview

8. stepId: chronicProgressive
   question: "Triệu chứng tiến triển nhiều tháng/năm không?"
   type: boolean
   next:
     true: action=considerImaging
     false: action=conservativeManagement

9. stepId: suspectTumour
   question: "Có triệu chứng một bên kèm mất phản xạ corneal/tiếng kêu không rõ nguyên nhân?"
   type: boolean
   next:
     true: action=orderMRI
     false: action=monitorAndReassess

10. stepId: discharge
    question: "Sau can thiệp, bệnh nhân có biểu hiện ổn định và không cần theo dõi chuyên khoa ngay không?"
    type: boolean
    next:
      true: action=provideHearingAidsInfo
      false: action=referSpecialist

## Hành động

- id: urgentAudiology
  description: "Đánh giá và xử trí cấp khi mất thính lực đột ngột: cân nhắc steroid, tham vấn ENT, chụp MRI khi cần."
  type: action
  cpg-activity-type: acute-management
  useContext: mất thính lực đột ngột

- id: manageConductive
  description: "Xác định và điều trị nguyên nhân dẫn truyền: lấy ráy, điều trị dịch tai giữa, cân nhắc phẫu thuật nếu cần."
  type: intervention
  cpg-activity-type: management
  useContext: dẫn truyền

- id: manageSensorineural
  description: "Quản lý mất thính lực cảm giác thần kinh: đo thính lực, xem xét máy trợ thính, điều trị nguyên nhân nếu có."
  type: intervention
  cpg-activity-type: management
  useContext: cảm giác thần kinh

- id: referNeurology
  description: "Tham vấn chuyên khoa thần kinh nếu nghi ngờ nguyên nhân trung ương."
  type: referral
  cpg-activity-type: referral
  useContext: trung ương

- id: investigateInfectionOrTrauma
  description: "Thực hiện xét nghiệm, siêu âm/CT/MRI nếu nghi nhiễm trùng hoặc chấn thương."
  type: investigation
  cpg-activity-type: imaging
  useContext: nhiễm trùng, chấn thương

- id: orderAudiometry
  description: "Yêu cầu đo thính lực (audiometry) để đánh giá mức độ và loại mất thính lực."
  type: investigation
  cpg-activity-type: laboratory
  useContext: audiometry

- id: interpretAudiometry
  description: "Giải thích kết quả đo thính lực và đưa ra kế hoạch theo loại mất thính lực."
  type: action
  cpg-activity-type: interpretation
  useContext: audiometry

- id: referSpecialist
  description: "Tham vấn chuyên khoa (ENT, thần kinh) khi cần can thiệp chuyên sâu."
  type: referral
  cpg-activity-type: referral
  useContext: tham vấn

- id: provideHearingAidsInfo
  description: "Tư vấn về máy trợ thính, đánh giá phù hợp và giới thiệu các nguồn hỗ trợ nếu cần."
  type: action
  cpg-activity-type: patient-education
  useContext: trợ thính

- id: checkOtotoxicMedications
  description: "Rà soát thuốc có độc tính thính giác (aminoglycoside, cisplatin) và điều chỉnh nếu có thể."
  type: action
  cpg-activity-type: medication-review
  useContext: dược

- id: vestibularAssessment
  description: "Thực hiện đánh giá tiền đình nếu có chóng mặt kèm theo; phối hợp với xử trí ù tai."
  type: investigation
  cpg-activity-type: clinical-assessment
  useContext: tiền đình

## Ghi chú / TODO

- Thêm mã chuẩn (ICD-10/SNOMED) cho các chẩn đoán và hành động.
- Generated from diagrams/hearing_loss-diagram.png

- Bảng phân loại nguyên nhân mất thính lực:

| Loại nguyên nhân    | Đặc điểm / Ví dụ                                  |
|---------------------|---------------------------------------------------|
| Dẫn truyền          | Ráy, dịch tai giữa, thủng màng nhĩ, chấn thương   |
| Cảm giác-thần kinh   | Lão hóa, phơi nhiễm tiếng ồn, thuốc độc tai (ototoxic) |
| Trung ương           | U thần kinh, đột quỵ, tổn thương não bộ            |
| Thần kinh cơ/miễn dịch| Bệnh thần kinh cơ, viêm, bệnh tự miễn              |
| Thuốc / độc tố      | Aminoglycoside, cisplatin, thuốc chống lao         |
