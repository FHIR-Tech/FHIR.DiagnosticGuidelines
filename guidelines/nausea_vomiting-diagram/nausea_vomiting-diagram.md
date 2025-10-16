---
id: nausea_vomiting-diagram
title: Hướng dẫn buồn nôn và nôn (nausea & vomiting)
description: Quy trình đánh giá buồn nôn/nôn: phân biệt nguyên nhân tiêu hóa, miễn dịch, thần kinh, nội tiết và xử trí hỗ trợ. 
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/nausea_vomiting-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho bệnh nhân buồn nôn/nôn; mục tiêu xác định nguyên nhân cấp tính (ngộ độc, tắc ruột, viêm) và chỉ định bù dịch, chống nôn, và điều tra thêm.

## Flow

1. stepId: airwayRisk
   question: "Có nguy cơ hít sặc, mất khả năng bảo vệ đường thở, hoặc mất ý thức không?"
   type: boolean
   next:
     true: action=secureAirwayAndAdmit
     false: stepId=assessOnset

2. stepId: assessOnset
   question: "Khởi phát đột ngột hay mạn; có sốt, đau bụng, tiêu chảy không?"
   type: choice
   answers:
     - code: acute
       display: "Đột ngột"
       next: stepId=lookForObstructionOrToxin
     - code: chronic
       display: "Mạn"
       next: stepId=considerGIorMetabolic

3. stepId: lookForObstructionOrToxin
   question: "Có đau bụng dữ dội, nôn kéo dài, tiền sử du lịch/ ăn uống nghi ngờ không?"
   type: boolean
   next:
     true: action=orderImagingAndStoolTests
     false: action=symptomaticCare

4. stepId: fluidAssessment
   question: "Có mất nước hoặc rối loạn điện giải cần bù dịch IV không?"
   type: boolean
   next:
     true: action=administerIVFluids
     false: action=oralRehydrationAndAntiemetic

5. stepId: pregnancyCheck
   question: "Phụ nữ có khả năng mang thai không?"
   type: boolean
   next:
     true: action=orderPregnancyTestAndPrenatalCareIfPositive
     false: action=continueInvestigation

6. stepId: medicationReview
   question: "Thuốc (chemo, opioids, antibiotics) có thể gây nôn không?"
   type: boolean
   next:
     true: action=adjustMedications
     false: action=prescribeAntiemetic

7. stepId: neuroSigns
   question: "Có đau đầu dữ dội, thay đổi thị lực, liệt khu trú gợi ý nguyên nhân thần kinh không?"
   type: boolean
   next:
     true: action=urgentNeuroImaging
     false: action=monitor

8. stepId: severeComplication
   question: "Có máu trong nôn, rối loạn điện giải nặng, hay nghi thủng không?"
   type: boolean
   next:
     true: action=admitAndInvestigate
     false: action=outpatientCare

9. stepId: disposition
   question: "Cần nhập viện hay có thể quản lý ngoại trú?"
   type: choice
   answers:
     - code: admit
       display: "Nhập viện"
       next: action=admitForIVSupport
     - code: outpatient
       display: "Ngoại trú"
       next: action=dischargeWithPlan

10. stepId: followUp
    question: "Sắp xếp tái khám hoặc xét nghiệm thêm không?"
    type: boolean
    next:
      true: action=arrangeFollowup
      false: action=end

## Hành động

- id: secureAirwayAndAdmit
  description: "Bảo đảm đường thở, oxy, xét nghiệm khẩn và nhập viện nếu không an toàn."
  type: intervention
  cpg-activity-type: emergency
  useContext: đường-thở

- id: orderImagingAndStoolTests
  description: "Chụp X-quang/CT, cấy phân khi nghi tắc hoặc nhiễm trùng tiêu hóa."
  type: investigation
  cpg-activity-type: diagnostic
  useContext: tiêu-hóa

- id: administerIVFluids
  description: "Bù dịch tĩnh mạch và điều chỉnh điện giải khi cần."
  type: intervention
  cpg-activity-type: supportive-care
  useContext: bù-dịch

- id: oralRehydrationAndAntiemetic
  description: "Bù nước đường miệng và chống nôn (ondansetron/metoclopramide) nếu phù hợp."
  type: action
  cpg-activity-type: medication
  useContext: điều-trị

- id: orderPregnancyTestAndPrenatalCareIfPositive
  description: "Thực hiện test thai và hướng dẫn chăm sóc phù hợp nếu dương."
  type: investigation
  cpg-activity-type: diagnostic
  useContext: sản-phụ-khoa

- id: adjustMedications
  description: "Ngưng hoặc thay thế thuốc gây nôn nếu có thể."
  type: action
  cpg-activity-type: medication-review
  useContext: dược

- id: prescribeAntiemetic
  description: "Kê chống nôn theo nguyên nhân và mức độ nôn."
  type: action
  cpg-activity-type: medication
  useContext: điều-trị

- id: urgentNeuroImaging
  description: "Chụp hình thần kinh nếu nghi ngờ nguyên nhân trung ương."
  type: investigation
  cpg-activity-type: imaging
  useContext: thần-kinh

- id: admitAndInvestigate
  description: "Nhập viện để điều tra nguyên nhân nghiêm trọng và hỗ trợ tích cực."
  type: intervention
  cpg-activity-type: inpatient-care
  useContext: nhập-viện

- id: admitForIVSupport
  description: "Nhập viện để bù dịch IV, theo dõi và điều trị hỗ trợ."
  type: intervention
  cpg-activity-type: inpatient-care
  useContext: hỗ-trợ

- id: dischargeWithPlan
  description: "Xuất viện với hướng dẫn ăn uống, thuốc chống nôn và dấu hiệu cảnh báo."
  type: action
  cpg-activity-type: outpatient-care
  useContext: ngoại-trú

- id: arrangeFollowup
  description: "Sắp xếp tái khám nếu triệu chứng kéo dài hoặc có dấu báo động."
  type: action
  cpg-activity-type: administrative
  useContext: follow-up

## Bảng phân loại nguyên nhân buồn nôn/nôn

| Loại | Ví dụ |
|------|------|
| Tiêu hóa | Gastroenteritis, obstruction |
| Nội tiết/ chuyển hóa | Pregnancy, DKA |
| Thần kinh/ độc | Migraine, toxicity |

## Ghi chú

- Generated from `diagrams/nausea_vomiting-diagram.png`
