---
id: urine_dipstick-diagram
title: Hướng dẫn đọc que thử nước tiểu
description: Hướng dẫn giải thích kết quả que thử nước tiểu (protein, nitrite, leukocyte esterase, glucose, blood) và đề xuất bước tiếp theo.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
  - name: Reviewer Needed
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/urine_dipstick-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho người làm xét nghiệm nhanh nước tiểu tại điểm chăm sóc. Mục tiêu là xác định ý nghĩa các chỉ số và bước tiếp theo.

## Flow

1. stepId: dipStart
   question: "Que thử nước tiểu: có protein, nitrite, leukocyte esterase, hồng cầu hoặc glucose?"
   type: multi
   next:
     protein: stepId=proteinPathway
     nitriteOrLeu: stepId=utiPathway
     blood: stepId=hematuriaPathway

2. stepId: proteinPathway
   question: "Protein dương tính: nghi ngờ bệnh thận hay nhiễm trùng?"
   type: boolean
   next:
     true: action=orderUrineProteinConfirm
     false: action=monitor

3. stepId: utiPathway
   question: "Nitrite hoặc leukocyte esterase dương tính: triệu chứng tiết niệu?"
   type: boolean
   next:
     true: action=manageUTI
     false: action=considerContamination

4. stepId: hematuriaPathway
   question: "Hồng cầu dương tính: có đau quặn hay triệu chứng khác?"
   type: choice
   answers:
     - code: colic
       display: "Đau quặn (nghi sỏi)"
       next: action=orderImaging
     - code: asymptomatic
       display: "Không triệu chứng"
       next: action=referUrology

5. stepId: glycosuria
   question: "Đường niệu dương tính: có tiền sử đái tháo đường hoặc triệu chứng kèm theo không?"
   type: boolean
   next:
     true: action=orderBloodGlucose
     false: action=considerContamination

6. stepId: proteinFollow
   question: "Protein dương tính mức cao hay dai dẳng không?"
   type: boolean
   next:
     true: action=referNephrology
     false: action=monitorAndRepeat

7. stepId: repeatTesting
   question: "Kết quả cần được lặp lại (ghi chú kỹ thuật, lấy mẫu giữa)?"
   type: boolean
   next:
     true: action=considerContamination
     false: action=interpretResults

8. stepId: diabeticCheck
   question: "Bệnh nhân đái tháo đường: có vết thương hoặc loét chân kèm nhiễm trùng không?"
   type: boolean
   next:
     true: action=manageUTI
     false: action=continueManagement

9. stepId: pregnancyConsider
   question: "Có thai hoặc nghi ngờ thai không?"
   type: boolean
   next:
     true: action=orderPregnancyTest
     false: action=monitorAndPlan

10. stepId: disposition
    question: "Cần can thiệp, điều trị tại chỗ hay theo dõi?"
    type: choice
    answers:
      - code: treat
        display: "Điều trị"
        next: action=manageUTI
      - code: observe
        display: "Quan sát"
        next: action=monitorAndPlan

## Hành động

- id: orderUrineProteinConfirm
  description: "Xác nhận protein niệu bằng xét nghiệm định lượng và đánh giá chức năng thận."
  type: investigation
  cpg-activity-type: laboratory
  useContext: proteinuria

- id: manageUTI
  description: "Quản lý nhiễm trùng đường tiết niệu dựa trên triệu chứng và mức độ nghi ngờ; cân nhắc kháng sinh theo hướng dẫn địa phương."
  type: intervention
  cpg-activity-type: management
  useContext: nhiễm trùng tiết niệu

- id: considerContamination
  description: "Xem xét lấy mẫu lại nếu khả năng nhiễm bẩn cao."
  type: action
  cpg-activity-type: sample-collection
  useContext: contamination

- id: orderImaging
  description: "Yêu cầu siêu âm hoặc CT không chuẩn bị nếu nghi sỏi tiết niệu."
  type: investigation
  cpg-activity-type: imaging
  useContext: sỏi tiết niệu

- id: referUrology
  description: "Tham vấn niệu khoa khi có hematuria vô căn hoặc nghi ngờ bệnh lý niệu quản/ bàng quang."
  type: referral
  cpg-activity-type: referral
  useContext: niệu khoa

- id: orderBloodGlucose
  description: "Kiểm tra glucose huyết để xác định đái tháo đường nếu đường niệu dương tính."
  type: investigation
  cpg-activity-type: laboratory
  useContext: đái tháo đường

- id: referNephrology
  description: "Tham vấn thận nếu protein niệu dai dẳng hoặc nghi bệnh lý thận."
  type: referral
  cpg-activity-type: referral
  useContext: thận

- id: interpretResults
  description: "Kết hợp lâm sàng và kết quả que thử để đưa ra quyết định chẩn đoán/điều trị."
  type: action
  cpg-activity-type: interpretation
  useContext: kết quả

- id: orderPregnancyTest
  description: "Làm test thai khi cần để hướng xử trí phù hợp."
  type: investigation
  cpg-activity-type: laboratory
  useContext: thai nghén

- id: monitorAndPlan
  description: "Theo dõi kết quả và lên kế hoạch tái khám hoặc xét nghiệm bổ sung."
  type: follow-up
  cpg-activity-type: follow-up
  useContext: theo dõi

## Ghi chú / TODO

- Generated from diagrams/urine_dipstick-diagram.png

- Bảng phân loại kết quả que thử nước tiểu (theo ý nghĩa):

| Kết quả/Chỉ số     | Ý nghĩa / Gợi ý                                   |
|---------------------|---------------------------------------------------|
| Nitrite / LE        | Gợi ý nhiễm trùng tiết niệu (UTI)                 |
| Blood (hồng cầu)    | Hematuria: sỏi, chấn thương, tổn thương niệu đạo    |
| Protein             | Protein niệu: bệnh thận, cần đánh giá thêm        |
| Glucose             | Gợi ý đái tháo đường nếu kết hợp với lâm sàng     |
| Leukocyte esterase  | Viêm nhiễm hoặc nhiễm trùng                        |
