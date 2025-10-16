---
id: vertigo-diagram
title: Sơ đồ chẩn đoán chóng mặt
description: Quy trình ra quyết định chẩn đoán nguyên nhân chóng mặt.
version: 1.0.0
date: 2025-10-15
authors:
  - name: TODO
fhirVersion: "4.0.1"
source-type: image
source-file: vertigo-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi
Sơ đồ này hướng dẫn quy trình chẩn đoán và xử trí chóng mặt, giúp phát hiện các dấu hiệu báo động, phân loại nguyên nhân, xử trí phù hợp và theo dõi. Áp dụng cho bệnh nhân đến khám vì chóng mặt; không thay thế phán đoán lâm sàng của chuyên gia. Một số mã chuẩn (ICD-10, SNOMED, LOINC) cần được điền — đánh dấu TODO bên dưới.

## Quy trình
1. stepId: onsetAssessment
   question: "Chóng mặt khởi phát cấp tính hay mạn tính?"
   type: string
   next:
     cấp tính: stepId=cnsSymptoms
     mạn tính: stepId=chronicVertigoAssessment

2. stepId: cnsSymptoms
   question: "Có triệu chứng thần kinh trung ương (liệt, nói khó, mất ý thức) hoặc yếu tố nguy cơ đột quỵ không?"
   type: boolean
   next:
     true: stepId=strokeAssessment
     false: stepId=durationAssessment

3. stepId: strokeAssessment
   question: "Đánh giá nguy cơ đột quỵ hoặc các rối loạn thần kinh trung ương khác. Đã thực hiện hình ảnh học (CT/MRI)?"
   type: boolean
   next:
     true: action=diagnoseVBI
     false: stepId=referNeurology

4. stepId: referNeurology
   question: "Có cần tham vấn chuyên khoa thần kinh không?"
   type: boolean
   next:
     true: action=referNeurology
     false: stepId=durationAssessment

5. stepId: durationAssessment
   question: "Đánh giá thời gian xuất hiện triệu chứng"
   type: choice
   answers:
     - code: seconds
       display: "Kéo dài vài giây"
       next: stepId=bppvAssessment
     - code: minutesToHours
       display: "Kéo dài từ vài phút đến vài giờ"
       next: stepId=longDurationAssessment
     - code: variable
       display: "Thời gian thay đổi"
       next: action=diagnoseInnerEarDisease
     - code: moreThanOneDay
       display: "Kéo dài > 1 ngày"
       next: stepId=prolongedVertigoAssessment

6. stepId: bppvAssessment
   question: "Có chóng mặt khi thay đổi tư thế đầu, không kèm triệu chứng thần kinh khác?"
   type: boolean
   next:
     true: action=diagnoseBPPV
     false: stepId=longDurationAssessment

7. stepId: longDurationAssessment
   question: "Triệu chứng kéo dài từ vài phút đến vài giờ có kèm theo ù tai, mất thính lực, hoặc đau đầu không?"
   type: boolean
   next:
     true: action=diagnoseTIAorMenieres
     false: action=diagnoseLabyrinthitis

8. stepId: prolongedVertigoAssessment
   question: "Chóng mặt kéo dài > 1 ngày, có kèm sốt, nhiễm trùng, hoặc triệu chứng tai mũi họng không?"
   type: boolean
   next:
     true: action=diagnoseLabyrinthitis
     false: stepId=chronicVertigoAssessment

9. stepId: chronicVertigoAssessment
   question: "Chóng mặt kéo dài >3 tuần, có kèm mất thính lực, ù tai, hoặc triệu chứng mạn tính khác?"
   type: boolean
   next:
     true: action=referENT
     false: action=adviseMonitor

10. stepId: causeClassification
    question: "Phân loại nguyên nhân chóng mặt: ngoại biên, trung ương, chuyển hóa, tâm lý, thuốc?"
    type: choice
    answers:
      - code: ngoaiBien
        display: "Nguyên nhân ngoại biên (BPPV, viêm dây thần kinh tiền đình, Ménière)"
        next: action=diagnosePeripheralVertigo
      - code: trungUong
        display: "Nguyên nhân trung ương (đột quỵ, u não, đa xơ cứng)"
        next: action=diagnoseCentralVertigo
      - code: chuyenHoa
        display: "Rối loạn chuyển hóa (hạ đường huyết, rối loạn điện giải)"
        next: action=diagnoseMetabolicVertigo
      - code: tamLy
        display: "Nguyên nhân tâm lý (lo âu, hoảng loạn)"
        next: action=diagnosePsychogenicVertigo
      - code: thuoc
        display: "Tác dụng phụ thuốc (kháng sinh, chống trầm cảm, v.v.)"
        next: action=diagnoseDrugVertigo

11. stepId: realCaseExample
    question: "Ví dụ thực tế: Bệnh nhân nữ 65 tuổi, chóng mặt cấp, liệt mặt, nói khó, CT não cho thấy nhồi máu tiểu não. Hướng xử trí?"
    type: info
    next:
      info: "Chẩn đoán đột quỵ tiểu não, xử trí cấp cứu, tham vấn thần kinh, nhập viện, theo dõi sát."

## Hành động

- id: diagnosePeripheralVertigo
  description: "Chẩn đoán nguyên nhân ngoại biên: BPPV, viêm dây thần kinh tiền đình, Ménière. Xử trí theo guideline chuyên khoa."
  type: propose-diagnosis
  cpg-activity-type: propose-diagnosis
  useContext: ngoại biên

- id: diagnoseCentralVertigo
  description: "Chẩn đoán nguyên nhân trung ương: đột quỵ, u não, đa xơ cứng. Xử trí cấp cứu, tham vấn thần kinh."
  type: propose-diagnosis
  cpg-activity-type: propose-diagnosis
  useContext: trung ương

- id: diagnoseMetabolicVertigo
  description: "Chẩn đoán chóng mặt do rối loạn chuyển hóa: hạ đường huyết, rối loạn điện giải. Điều chỉnh chuyển hóa, theo dõi sát."
  type: propose-diagnosis
  cpg-activity-type: propose-diagnosis
  useContext: chuyển hóa

- id: diagnosePsychogenicVertigo
  description: "Chẩn đoán chóng mặt do nguyên nhân tâm lý: lo âu, hoảng loạn. Tham vấn tâm lý, hỗ trợ tinh thần."
  type: propose-diagnosis
  cpg-activity-type: propose-diagnosis
  useContext: tâm lý

- id: diagnoseDrugVertigo
  description: "Chẩn đoán chóng mặt do tác dụng phụ thuốc: kháng sinh, chống trầm cảm, v.v. Xem xét đổi thuốc, giảm liều."
  type: propose-diagnosis
  cpg-activity-type: propose-diagnosis
  useContext: thuốc

- id: diagnoseVBI
  description: "Chẩn đoán đột quỵ tiểu não (VBI) hoặc các rối loạn thần kinh trung ương khác dựa trên triệu chứng thần kinh, hình ảnh học."
  type: propose-diagnosis
  cpg-activity-type: propose-diagnosis
  useContext: thần kinh trung ương, nguy cơ đột quỵ

- id: referNeurology
  description: "Tham vấn chuyên khoa thần kinh khi có dấu hiệu thần kinh hoặc nghi ngờ đột quỵ."
  type: referral
  cpg-activity-type: referral
  useContext: thần kinh trung ương

- id: diagnoseBPPV
  description: "Chẩn đoán chóng mặt tư thế kịch phát lành tính (BPPV) khi chóng mặt xuất hiện khi thay đổi tư thế đầu, không kèm triệu chứng thần kinh."
  type: propose-diagnosis
  cpg-activity-type: propose-diagnosis
  useContext: chóng mặt tư thế

- id: diagnoseInnerEarDisease
  description: "Chẩn đoán bệnh lý tai trong/tai giữa, u góc cầu tiểu não, đa xơ cứng, tác dụng phụ thuốc, v.v. khi triệu chứng phù hợp."
  type: propose-diagnosis
  cpg-activity-type: propose-diagnosis
  useContext: tai trong, tai giữa, bệnh lý phối hợp

- id: diagnoseLabyrinthitis
  description: "Chẩn đoán viêm dây thần kinh tiền đình/labyrinthitis khi chóng mặt kéo dài, không kèm triệu chứng thần kinh trung ương."
  type: propose-diagnosis
  cpg-activity-type: propose-diagnosis
  useContext: viêm dây thần kinh tiền đình

- id: diagnoseTIAorMenieres
  description: "Chẩn đoán TIA, bệnh Ménière, migraine, động kinh cục bộ khi có triệu chứng phù hợp (ù tai, mất thính lực, đau đầu, rối loạn ý thức)."
  type: propose-diagnosis
  cpg-activity-type: propose-diagnosis
  useContext: TIA, Ménière, migraine

- id: referENT
  description: "Tham vấn chuyên khoa Tai Mũi Họng nếu chóng mặt kéo dài, có triệu chứng mạn tính hoặc mất thính lực."
  type: referral
  cpg-activity-type: referral
  useContext: Tai Mũi Họng

- id: adviseMonitor
  description: "Theo dõi, hẹn tái khám nếu không có dấu hiệu báo động hoặc triệu chứng nặng."
  type: follow-up
  cpg-activity-type: follow-up
  useContext: theo dõi, không dấu hiệu báo động

## Ghi chú / TODO
- Bảng phân loại nguyên nhân chóng mặt:

| Loại nguyên nhân   | Đặc điểm / Ví dụ                                 |
|-------------------|--------------------------------------------------|
| Ngoại biên        | BPPV, Ménière, viêm dây thần kinh tiền đình      |
| Trung ương        | Đột quỵ, u não, đa xơ cứng                       |
| Chuyển hóa        | Hạ đường huyết, rối loạn điện giải               |
| Tâm lý            | Lo âu, hoảng loạn                                |
| Thuốc             | Kháng sinh, chống trầm cảm, thuốc chống động kinh|

- Phụ lục: Hướng dẫn thực hành khám chóng mặt: kiểm tra nghiệm pháp Dix-Hallpike, nghiệm pháp Head Impulse, đánh giá dấu hiệu báo động.
- Ví dụ thực tế: Bệnh nhân trẻ chóng mặt khi thay đổi tư thế đầu, không kèm triệu chứng thần kinh, chẩn đoán BPPV, xử trí bằng nghiệm pháp Epley.
- Trẻ em, người già, người suy giảm miễn dịch cần theo dõi sát hơn, cân nhắc nhập viện nếu có dấu hiệu nặng
- Nếu chóng mặt kèm liệt, nói khó, mất ý thức: xử trí cấp cứu, loại trừ đột quỵ
- Cần bổ sung mã hóa tiêu chuẩn (ICD-10, SNOMED, LOINC) cho các chẩn đoán
- Tác giả, ngày, checksum cần cập nhật
- Phụ lục: Các nguyên nhân chóng mặt mạn tính (rối loạn chuyển hóa, thuốc, bệnh lý nội tiết)
- Phụ lục: Hướng dẫn xử trí chóng mặt tư thế, chóng mặt do migraine

Generated from guidelines/vertigo-diagram.png

