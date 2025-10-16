---
id: weakness-diagram
title: Hướng dẫn đánh giá yếu cơ
description: Quy trình đánh giá yếu cơ cấp và mạn, phân loại nguyên nhân (thần kinh trung ương, thần kinh ngoại vi, cơ, chuyển hóa, thuốc) và đề xuất xét nghiệm, can thiệp ban đầu.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
  - name: Reviewer Needed
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/weakness-diagram.png
source-checksum: TODO
---
   question: "Bệnh nhân có yếu cơ không?"
   type: boolean
   next:
     true: stepId=onsetAndPattern
     false: action=exit-no-weakness

2. stepId: onsetAndPattern
   question: "Khởi phát cấp tính hay mạn? Một bên hay hai bên? Kèm mất cảm giác, rối loạn thị lực hay nuốt?"
   type: choice
   answers:
     - code: acute
       display: "Cấp tính"
       next: stepId=strokeScreening
     - code: progressive
       display: "Từ từ/tiến triển"
       next: stepId=electrodiagnostic

3. stepId: strokeScreening
   question: "Có dấu hiệu thần kinh khu trú gợi ý đột quỵ (mất vận động nửa người, rối loạn ngôn ngữ) không?"
   type: boolean
   next:
     true: action=diagnoseStroke
     false: stepId=otherAcuteCauses

4. stepId: otherAcuteCauses
   question: "Có tiền sử chấn thương, nhiễm trùng hay tiếp xúc với thuốc độc không?"
   type: boolean
   next:
     true: action=diagnoseAcuteOther
     false: action=monitorAndPlan

5. stepId: electrodiagnostic
   question: "Cần làm điện cơ/EMG, CK, xét nghiệm miễn dịch hoặc chức năng tuyến giáp không?"
   type: boolean
   next:
     true: action=orderTests
     false: action=adviseMonitor

6. stepId: neuromuscularScreening
   question: "Có biểu hiện bệnh lý thần kinh cơ (teo cơ, rung giật, yếu đối xứng) không?"
   type: boolean
   next:
     true: action=diagnoseNeuromuscular
     false: action=adviseMonitor

7. stepId: medicationReview
   question: "Bệnh nhân có dùng thuốc có thể gây yếu cơ (statin, steroid, thuốc ức chế thần kinh cơ) không?"
   type: boolean
   next:
     true: action=reviewMedications
     false: action=continueAssessment

8. stepId: followUp
   question: "Triệu chứng cải thiện sau can thiệp ban đầu?"
   type: boolean
   next:
     true: action=continueManagement
     false: action=referSpecialist

9. stepId: chronicAssessment
   question: "Yếu cơ kéo dài trên 3 tháng?"
   type: boolean
   next:
     true: action=chronicWorkup
     false: action=monitorAndPlan

10. stepId: disposition
    question: "Cần nhập viện/nhập khoa hay quản lý ngoại trú?"
    type: choice
    answers:
      - code: admit
        display: "Nhập viện"
        next: action=admitPatient
      - code: outpatient
        display: "Quản lý ngoại trú"
        next: action=outpatientFollowUp

11. stepId: respiratoryCheck
    question: "Có dấu hiệu suy hô hấp hoặc rối loạn nuốt không?"
    type: boolean
    next:
      true: action=admitPatient
      false: action=continueManagement

12. stepId: medicationCause
    question: "Có dùng thuốc có thể gây yếu cơ (statin, steroid, linezolid, fluroquinolone) không?"
    type: boolean
    next:
      true: action=reviewMedications
      false: action=considerReferral

## Hành động

- id: diagnoseStroke
  description: "Xử trí và đánh giá khả năng đột quỵ: chụp CT/MRI, nhập viện và tham vấn thần kinh."
  type: action
  cpg-activity-type: acute-management
  useContext: đột quỵ

- id: diagnoseAcuteOther
  description: "Đánh giá nguyên nhân cấp khác: chấn thương, nhiễm trùng, rối loạn chuyển hóa; điều trị theo nguyên nhân."
  type: intervention
  cpg-activity-type: management
  useContext: nguyên nhân cấp

- id: orderTests
  description: "Yêu cầu điện cơ/EMG, CK, TSH, xét nghiệm miễn dịch hoặc hình ảnh thần kinh khi cần."
  type: investigation
  cpg-activity-type: laboratory
  useContext: xét nghiệm

- id: diagnoseNeuromuscular
  description: "Chẩn đoán bệnh lý thần kinh cơ (myasthenia, myopathy) và lên kế hoạch điều trị/tham vấn chuyên khoa."
  type: propose-diagnosis
  cpg-activity-type: diagnosis
  useContext: thần kinh cơ

- id: reviewMedications
  description: "Xem xét thuốc có thể gây yếu cơ; điều chỉnh thuốc nếu cần."
  type: action
  cpg-activity-type: medication-review
  useContext: thuốc

- id: monitorAndPlan
  description: "Theo dõi, lên kế hoạch khám chuyên khoa và tái khám."
  type: follow-up
  cpg-activity-type: follow-up
  useContext: theo dõi

- id: continueManagement
  description: "Tiếp tục quản lý nội khoa hoặc phục hồi chức năng tùy trường hợp."
  type: intervention
  cpg-activity-type: management
  useContext: quản lý

- id: chronicWorkup
  description: "Đánh giá sâu cho yếu cơ mạn: xét nghiệm di truyền, điện cơ, MRI cơ nếu cần."
  type: investigation
  cpg-activity-type: specialized-investigation
  useContext: mạn tính

- id: admitPatient
  description: "Nhập viện khi bệnh nặng, có suy hô hấp, rối loạn nuốt hoặc dấu hiệu tiến triển nhanh."
  type: action
  cpg-activity-type: disposition
  useContext: nhập viện

- id: outpatientFollowUp
  description: "Hẹn khám ngoại trú và chương trình phục hồi chức năng."
  type: follow-up
  cpg-activity-type: follow-up
  useContext: ngoại trú

- id: adviseMonitor
  description: "Tư vấn theo dõi tại nhà, ghi nhật ký triệu chứng và tái khám khi có thay đổi."
  type: action
  cpg-activity-type: patient-education
  useContext: theo dõi

- id: considerReferral
  description: "Xem xét chuyển tuyến chuyên gia thần kinh cơ nếu không xác định nguyên nhân sau sàng lọc."
  type: referral
  cpg-activity-type: referral
  useContext: chuyên khoa

## Ghi chú / TODO

- Thêm mã chuẩn (ICD-10/SNOMED) cho các chẩn đoán và hành động.
- Generated from diagrams/weakness-diagram.png

- Bảng phân loại nguyên nhân yếu cơ:

| Loại nguyên nhân    | Đặc điểm / Ví dụ                                  |
|---------------------|---------------------------------------------------|
| Thần kinh trung ương| Đột quỵ, u tủy, đa xơ cứng                         |
| Thần kinh ngoại vi   | Bệnh lý rễ, plexus, neuropathy                     |
| Cơ (myopathy)       | Myositis, dystrophy, thuốc (steroid)               |
| Chuyển hóa / nội tiết| Rối loạn điện giải, suy giáp                        |
| Thuốc / độc tố      | Statin, steroid, thuốc ức chế thần kinh cơ          |
