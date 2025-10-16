---
id: constipation-diagram
title: Hướng dẫn táo bón (constipation)
description: Quy trình đánh giá táo bón cấp/mạn, phân biệt nguyên nhân chức năng, cơ học, thuốc và hướng điều trị.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/constipation-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho bệnh nhân táo bón; mục tiêu xác định nguyên nhân, tối ưu hóa liệu pháp không dùng thuốc và quyết định xét nghiệm khi có dấu báo động.

## Flow

1. stepId: redFlags
   question: "Có sụt cân, máu trong phân, thay đổi thói quen đại tiện hay tuổi >50 không?"
   type: boolean
   next:
     true: action=referForColonoscopy
     false: stepId=durationAndSeverity

2. stepId: durationAndSeverity
   question: "Triệu chứng cấp hay mạn; tần suất và độ cứng phân?"
   type: choice
   answers:
     - code: acute
       display: "Cấp"
       next: action=conservativeMeasures
     - code: chronic
       display: "Mạn"
       next: stepId=medReviewandLifestyle

3. stepId: medReviewandLifestyle
   question: "Thuốc (opioid, anticholinergic), chế độ ăn, fluid, vận động có thể là nguyên nhân?"
   type: boolean
   next:
     true: action=adjustMedicationsAndLifestyle
     false: action=considerLaxatives

4. stepId: considerLaxatives
   question: "Thử laxative osmotic hay stimulant có cải thiện không?"
   type: boolean
   next:
     true: action=continueRegimen
     false: action=referGastroenterology

5. stepId: functionalVsMechanical
   question: "Nghi tắc cơ học (chướng, nôn) hay rối loạn chức năng vận động?"
   type: boolean
   next:
     true: action=orderImagingAndSurgicalReview
     false: action=considerBiofeedback

6. stepId: examForRectal
   question: "Khám trực tràng có máu, u hay giảm reflex không?"
   type: boolean
   next:
     true: action=referForColonoscopy
     false: action=planManagement

7. stepId: severeComplication
   question: "Có tắc ruột, nhiễm trùng hay nghi perforation không?"
   type: boolean
   next:
     true: action=urgentAdmission
     false: action=outpatientCare

8. stepId: disposition
   question: "Cần nhập viện hay ngoại trú?"
   type: choice
   answers:
     - code: admit
       display: "Nhập viện"
       next: action=admitForManagement
     - code: outpatient
       display: "Ngoại trú"
       next: action=dischargeWithPlan

9. stepId: followUp
   question: "Sắp xếp tái khám hoặc xét nghiệm chức năng ruột không?"
   type: boolean
   next:
     true: action=arrangeFollowup
     false: action=end

10. stepId: education
    question: "Cần giáo dục về chế độ ăn, nước và tập luyện không?"
    type: boolean
    next:
      true: action=provideEducation
      false: action=end

## Hành động

- id: referForColonoscopy
  description: "Giới thiệu nội soi khi có dấu báo động hoặc tuổi nguy cơ."
  type: referral
  cpg-activity-type: diagnostic
  useContext: nội-soi

- id: conservativeMeasures
  description: "Tăng chất xơ, fluid, hoạt động thể lực, và thói quen đại tiện."
  type: action
  cpg-activity-type: lifestyle
  useContext: phòng-ngừa

- id: adjustMedicationsAndLifestyle
  description: "Điều chỉnh thuốc góp phần và tư vấn thay đổi lối sống."
  type: action
  cpg-activity-type: medication-review
  useContext: dược

- id: considerLaxatives
  description: "Thử laxatives osmotic hoặc stimulant theo mức độ."
  type: action
  cpg-activity-type: medication
  useContext: điều-trị

- id: orderImagingAndSurgicalReview
  description: "Chụp X-quang/CT khi nghi tắc ruột và tham vấn phẫu thuật."
  type: investigation
  cpg-activity-type: imaging
  useContext: chẩn-đoán

- id: considerBiofeedback
  description: "Cân nhắc điều trị biofeedback cho rối loạn chức năng cơ sàn chậu."
  type: intervention
  cpg-activity-type: therapy
  useContext: phục-hồi

- id: urgentAdmission
  description: "Nhập viện khi có biến chứng: tắc, nhiễm trùng, thủng."
  type: intervention
  cpg-activity-type: inpatient-care
  useContext: nhập-viện

- id: admitForManagement
  description: "Nhập viện để điều trị tắc ruột hoặc biến chứng nặng."
  type: intervention
  cpg-activity-type: inpatient-care
  useContext: can-thiep

- id: dischargeWithPlan
  description: "Xuất viện với hướng dẫn điều trị và hẹn tái khám."
  type: action
  cpg-activity-type: outpatient-care
  useContext: ngoại-trú

- id: arrangeFollowup
  description: "Sắp xếp xét nghiệm thêm và tái khám theo kế hoạch."
  type: action
  cpg-activity-type: administrative
  useContext: follow-up

- id: provideEducation
  description: "Giáo dục về dinh dưỡng, lối sống và sử dụng thuốc nhuận tràng đúng cách."
  type: action
  cpg-activity-type: patient-education
  useContext: giáo-dục

## Bảng phân loại nguyên nhân táo bón

| Loại | Ví dụ |
|------|------|
| Chức năng | IBS, rối loạn vận động |
| Cơ học | U, tắc ruột |
| Thuốc | Opioid, anticholinergic |

## Ghi chú

- Generated from `diagrams/constipation-diagram.png`
