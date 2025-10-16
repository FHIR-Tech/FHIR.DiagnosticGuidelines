---
id: diplopia-diagram
title: Hướng dẫn song thị (diplopia)
description: Quy trình đánh giá song thị, phân biệt song thị một mắt và hai mắt, xác định dị tật vận nhãn, nguyên nhân thần kinh và cần imaging.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/diplopia-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho bệnh nhân song thị; mục tiêu xác định nguyên nhân cấp tính (đột quy, chấn thương, VIêm) hoặc mạn tính và hướng quản lý.

## Flow

1. stepId: monocularOrBinocular
   question: "Song thị chỉ xảy ra khi mở một mắt hay hai mắt?"
   type: choice
   answers:
     - code: monocular
       display: "Một mắt"
       next: action=referOphthalmologyForCornealLens
     - code: binocular
       display: "Hai mắt"
       next: stepId=assessNeurologicalSigns

2. stepId: assessNeurologicalSigns
   question: "Có yếu liệt cơ, liệt mặt, đau đầu nặng, thay đổi ý thức không?"
   type: boolean
   next:
     true: action=urgentNeuroImaging
     false: stepId=ocularMotorExam

3. stepId: ocularMotorExam
   question: "Kiểm tra các cơ vận nhãn, nystagmus, pápilledema có tồn tại không?"
   type: boolean
   next:
     true: action=orderCTorMRI
     false: action=conservativeManagement

4. stepId: considerMyasthenia
   question: "Các triệu chứng gợi ý myasthenia gravis (điểm yếu tăng theo hoạt động) không?"
   type: boolean
   next:
     true: action=orderAChRandReferral
     false: action=assessVascularCauses

5. stepId: assessVascularCauses
   question: "Cần loại trừ đột quỵ, đụng dập, hoặc phình mạch không?"
   type: boolean
   next:
     true: action=orderVascularImaging
     false: action=opticalCorrectionConsideration

6. stepId: medicationReview
   question: "Thuốc hoặc chất có thể gây song thị không (aminoglycoside, phenytoin)?"
   type: boolean
   next:
     true: action=adjustMedications
     false: action=referOphthalmology

7. stepId: prismsOrPatch
   question: "Cần kính lưỡng hoặc che mắt tạm để giảm triệu chứng không?"
   type: boolean
   next:
     true: action=trialPrismOrPatch
     false: action=monitor

8. stepId: disposition
   question: "Cần nhập viện hoặc ngoại trú/ điều trị tại nhà?"
   type: choice
   answers:
     - code: admit
       display: "Nhập viện"
       next: action=admitAndInvestigate
     - code: outpatient
       display: "Ngoại trú"
       next: action=outpatientCare

9. stepId: followUp
   question: "Sắp xếp theo dõi chuyên khoa nhãn/ thần kinh không?"
   type: boolean
   next:
     true: action=arrangeSpecialtyFollowup
     false: action=end

10. stepId: education
    question: "Cần tư vấn về an toàn, lái xe và nguy cơ khi có song thị không?"
    type: boolean
    next:
      true: action=provideSafetyAdvice
      false: action=end

## Hành động

- id: referOphthalmologyForCornealLens
  description: "Tham vấn nhãn khoa khi song thị monocular do bệnh giác mạc hoặc thấu kính."
  type: referral
  cpg-activity-type: referral
  useContext: nhãn khoa

- id: urgentNeuroImaging
  description: "Chụp CT/MRI não khẩn khi có dấu thần kinh khu trú hoặc nghi ngờ đột quỵ."
  type: investigation
  cpg-activity-type: imaging
  useContext: thần kinh

- id: orderCTorMRI
  description: "Chụp CT/MRI để đánh giá tổn thương cấu trúc và tổn thương vận nhãn."
  type: investigation
  cpg-activity-type: imaging
  useContext: diagnostic

- id: orderAChRandReferral
  description: "Yêu cầu xét nghiệm kháng thể AChR và tham vấn thần kinh khi nghi myasthenia."
  type: investigation
  cpg-activity-type: laboratory
  useContext: thần kinh

- id: orderVascularImaging
  description: "Yêu cầu CTA/MRA nếu nghi ngờ nguyên nhân mạch máu."
  type: investigation
  cpg-activity-type: imaging
  useContext: vascular

- id: adjustMedications
  description: "Điều chỉnh các thuốc có thể gây song thị sau thảo luận với đơn vị kê thuốc."
  type: action
  cpg-activity-type: medication-review
  useContext: dược

- id: trialPrismOrPatch
  description: "Thử kính prism hoặc che mắt tạm để giảm triệu chứng trong khi chờ đánh giá."
  type: intervention
  cpg-activity-type: symptomatic-care
  useContext: hỗ trợ

- id: admitAndInvestigate
  description: "Nhập viện để điều tra nguyên nhân nghiêm trọng và theo dõi."
  type: intervention
  cpg-activity-type: inpatient-care
  useContext: nhập viện

- id: outpatientCare
  description: "Quản lý ngoại trú, đánh giá thêm và hẹn tái khám."
  type: action
  cpg-activity-type: outpatient-care
  useContext: ngoại trú

- id: arrangeSpecialtyFollowup
  description: "Sắp xếp theo dõi với nhãn khoa hoặc thần kinh tùy chẩn đoán."
  type: action
  cpg-activity-type: administrative
  useContext: follow-up

- id: provideSafetyAdvice
  description: "Tư vấn về an toàn, cấm lái xe tạm thời nếu cần và các biện pháp phòng ngừa."
  type: action
  cpg-activity-type: patient-education
  useContext: an toàn

## Bảng phân loại nguyên nhân song thị

| Loại | Ví dụ |
|------|------|
| Monocular | Bệnh giác mạc, thấu kính |
| Binocular (neuromuscular) | Myasthenia, palsy cơ, đột quỵ |
| Vascular | Phình mạch, đứt mạch |

## Ghi chú

- Generated from diagrams/diplopia-diagram.png
