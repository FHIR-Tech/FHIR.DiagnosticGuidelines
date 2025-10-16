---
id: ear_pressure-diagram
title: Hướng dẫn cảm giác đầy tai (ear pressure)
description: Đánh giá cảm giác đầy tai, nguyên nhân do dịch, barotrauma, Eustachian dysfunction, và hướng điều trị. 
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/ear_pressure-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho bệnh nhân than phiền đầy tai, giảm thính lực tạm thời, ù tai liên quan đến áp lực. 

## Flow

1. stepId: acuteSevere
   question: "Có đau tai dữ dội, sốt hoặc chảy mủ không?"
   type: boolean
   next:
     true: action=urgentENTReferral
     false: stepId=recentFlightOrDive

2. stepId: recentFlightOrDive
   question: "Gần đây đi máy bay, lặn biển hoặc thay đổi áp lực không?"
   type: boolean
   next:
     true: action=adviseAutoinflationAndDecongestants
     false: stepId=historyOfOtitis

3. stepId: historyOfOtitis
   question: "Tiền sử viêm tai giữa tái phát hoặc đặt ống thông tai không?"
   type: boolean
   next:
     true: action=examineForEffusionAndRefer
     false: action=trialNasalDecongestant

4. stepId: hearingTest
   question: "Có giảm thính lực đáng kể khi kiểm tra đơn giản không?"
   type: boolean
   next:
     true: action=orderAudiology
     false: action=reassureAndObserve

5. stepId: perforationCheck
   question: "Nghi ngờ thủng màng nhĩ không?"
   type: boolean
   next:
     true: action=avoidWaterAndReferENT
     false: action=continueConservative

6. stepId: chronicSymptoms
   question: "Triệu chứng kéo dài >3 tháng, có effusion mãn tính?"
   type: boolean
   next:
     true: action=referENTForSurgicalConsideration
     false: action=shortCourseTherapy

7. stepId: maneuvers
   question: "Thử Valsalva hoặc sử dụng nhét tai giảm áp có hiệu quả không?"
   type: boolean
   next:
     true: action=adviseSelfCareMeasures
     false: action=referENT

8. stepId: medicationReview
   question: "Thuốc như NSAID hoặc aminoglycoside có liên quan không?"
   type: boolean
   next:
     true: action=reviewMedications
     false: action=continuePlan

9. stepId: disposition
   question: "Cần nhập viện hay ngoại trú?"
   type: choice
   answers:
     - code: admit
       display: "Nhập viện nếu nặng"
       next: action=admitForIVTherapy
     - code: outpatient
       display: "Ngoại trú"
       next: action=dischargeWithPlan

10. stepId: followUp
    question: "Sắp xếp tái khám nếu không cải thiện?"
    type: boolean
    next:
      true: action=scheduleENTFollowup
      false: action=end

## Hành động

- id: urgentENTReferral
  description: "Tham vấn ENT khẩn khi có đau, sốt, chảy mủ hoặc mất thính lực đột ngột."
  type: referral
  cpg-activity-type: emergency
  useContext: khẩn

- id: adviseAutoinflationAndDecongestants
  description: "Khuyên Valsalva, xịt mũi và decongestant ngắn ngày."
  type: action
  cpg-activity-type: self-care
  useContext: pressure

- id: examineForEffusionAndRefer
  description: "Khám ống tai và màng nhĩ để tìm effusion; tham vấn ENT nếu cần."
  type: investigation
  cpg-activity-type: clinical-exam
  useContext: khám

- id: orderAudiology
  description: "Yêu cầu kiểm tra thính lực cơ bản và audiometry khi giảm nghe đáng kể."
  type: investigation
  cpg-activity-type: diagnostic
  useContext: thính lực

- id: avoidWaterAndReferENT
  description: "Hướng dẫn tránh nước vào tai nếu thủng và chuyển ENT."
  type: action
  cpg-activity-type: safety
  useContext: bảo vệ

- id: referENTForSurgicalConsideration
  description: "Giới thiệu ENT cho cân nhắc đặt ống thông tai hoặc phẫu thuật."
  type: referral
  cpg-activity-type: surgical
  useContext: phẫu thuật

- id: adviseSelfCareMeasures
  description: "Hướng dẫn tự chăm sóc, tránh bay/lặn đến khi cải thiện."
  type: action
  cpg-activity-type: patient-education
  useContext: tự chăm sóc

- id: reviewMedications
  description: "Xem xét thuốc có thể góp phần và điều chỉnh nếu cần."
  type: action
  cpg-activity-type: medication-review
  useContext: thuốc

- id: admitForIVTherapy
  description: "Nhập viện để điều trị IV nếu có nhiễm trùng nặng."
  type: intervention
  cpg-activity-type: inpatient-care
  useContext: nhập viện

- id: dischargeWithPlan
  description: "Xuất viện với hướng dẫn theo dõi và chăm sóc tai."
  type: action
  cpg-activity-type: outpatient-care
  useContext: ngoại trú

- id: scheduleENTFollowup
  description: "Sắp xếp tái khám với ENT khi không cải thiện."
  type: action
  cpg-activity-type: administrative
  useContext: follow-up

## Bảng phân loại nguyên nhân đầy tai

| Loại | Ví dụ |
|------|------|
| Barotrauma | Bay, lặn |
| Effusion | Otitis media with effusion |
| Infection | Otitis externa/ media |

## Ghi chú

- Generated from diagrams/ear_pressure-diagram.png
