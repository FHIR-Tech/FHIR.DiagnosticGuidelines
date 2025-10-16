---
id: dyspnea-diagram
title: Hướng dẫn đánh giá khó thở (dyspnea)
description: Quy trình sàng lọc và phân loại nguyên nhân khó thở, ưu tiên phát hiện tình trạng nguy kịch như suy hô hấp, thuyên tắc phổi, suy tim.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/dyspnea-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho bệnh nhân than khó thở; mục tiêu loại trừ nguyên nhân đe doạ tính mạng và phân loại hướng điều trị (tim, phổi, chuyển hóa, nhiễm trùng).

## Flow

1. stepId: airwayBreathingCirculation
   question: "Bệnh nhân có khó thở nặng, không thể nói, tím, hoặc SpO2 < 90% không?"
   type: boolean
   next:
     true: action=secureAirwayAndOxygen
     false: stepId=onsetAndProgression

2. stepId: onsetAndProgression
   question: "Bắt đầu đột ngột hay từ từ? Có yếu tố nguy cơ NMCT, PE, COPD?"
   type: choice
   answers:
     - code: sudden
       display: "Đột ngột"
       next: stepId=considerPEorACS
     - code: gradual
       display: "Từ từ"
       next: stepId=chronicAssessment

3. stepId: vitalSigns
   question: "Huyết áp, nhịp tim, SpO2, nhiệt độ có bất thường không?"
   type: boolean
   next:
     true: action=urgentAssessment
     false: stepId=auscultation

4. stepId: auscultation
   question: "Nghe phổi có ran, wheeze hay giảm âm phổi không?"
   type: choice
   answers:
     - code: wheeze
       display: "Wheeze -> hướng suyễn/COPD"
       next: action=administerBronchodilator
     - code: crackles
       display: "Ran ẩm -> hướng suy tim/phổi" 
       next: action=orderCXRandBNP
     - code: absent
       display: "Giảm âm -> tràn khí/pleural effusion"
       next: action=orderCXR

5. stepId: considerPEorACS
   question: "Có đau ngực, dấu hiệu huyết động, yếu tố nguy cơ thuyên tắc phổi không?"
   type: boolean
   next:
     true: action=orderD-dimerAndCTPA
     false: stepId=infectiousWorkup

6. stepId: infectiousWorkup
   question: "Có sốt, ho, đờm, hoặc x-quang gợi ý viêm phổi không?"
   type: boolean
   next:
     true: action=managePneumonia
     false: action=considerCardiacOrMetabolic

7. stepId: chronicAssessment
   question: "Tiền sử COPD, suy tim mãn tính hay rối loạn thần kinh hô hấp?"
   type: boolean
   next:
     true: action=optimizeChronicTherapy
     false: action=referSpecialist

8. stepId: responseToTreatment
   question: "Phản ứng với oxy, thuốc giãn phế quản, lợi tiểu có cải thiện không?"
   type: boolean
   next:
     true: action=continueManagement
     false: action=escalateCare

9. stepId: disposition
   question: "Cần nhập viện hay quản lý ngoại trú?"
   type: choice
   answers:
     - code: admit
       display: "Nhập viện"
       next: action=admitAndTreat
     - code: outpatient
       display: "Ngoại trú"
       next: action=dischargeWithPlan

10. stepId: followUpAndPrevention
    question: "Cần sắp xếp tái khám, xét nghiệm theo dõi hoặc điều chỉnh thuốc lâu dài không?"
    type: boolean
    next:
      true: action=scheduleFollowup
      false: action=end

## Hành động

- id: secureAirwayAndOxygen
  description: "Bảo đảm đường thở, thở oxy, đặt đường truyền, hỗ trợ hô hấp theo chỉ định (CPAP, intubation)."
  type: intervention
  cpg-activity-type: acute-management
  useContext: hô hấp

- id: urgentAssessment
  description: "Ổn định bệnh nhân, đánh giá huyết động, ECG, xét nghiệm và gọi chuyên khoa sớm."
  type: action
  cpg-activity-type: acute-management
  useContext: cấp cứu

- id: administerBronchodilator
  description: "Cho thuốc giãn phế quản (salbutamol) và đánh giá đáp ứng lâm sàng ngay."
  type: intervention
  cpg-activity-type: medication
  useContext: phổi

- id: orderCXRandBNP
  description: "Chụp X-quang ngực và BNP/NT-proBNP để đánh giá suy tim hoặc bệnh phổi."
  type: investigation
  cpg-activity-type: imaging
  useContext: diagnostic

- id: orderD-dimerAndCTPA
  description: "Yêu cầu D-dimer và CT pulmonary angiography khi nghi ngờ thuyên tắc phổi."
  type: investigation
  cpg-activity-type: laboratory
  useContext: PE

- id: managePneumonia
  description: "Khởi kháng sinh theo hướng dẫn địa phương, bù dịch và oxy nếu cần."
  type: intervention
  cpg-activity-type: management
  useContext: nhiễm trùng

- id: considerCardiacOrMetabolic
  description: "Đánh giá suy tim, thiếu oxy mô, rối loạn chuyển hóa; xét nghiệm tim mạch bổ sung."
  type: investigation
  cpg-activity-type: diagnostic
  useContext: cardiac

- id: optimizeChronicTherapy
  description: "Tối ưu hóa điều trị COPD, suy tim mạn: inhaler, liệu pháp oxy dài hạn, lợi tiểu khi phù."
  type: management
  cpg-activity-type: chronic-care
  useContext: mãn tính

- id: escalateCare
  description: "Chuyển khoa hồi sức/CCU nếu bệnh nhân không đáp ứng với điều trị ban đầu."
  type: referral
  cpg-activity-type: acute-management
  useContext: hồi sức

- id: admitAndTreat
  description: "Nhập viện và điều trị theo nguyên nhân (PE, ARDS, suy tim)."
  type: intervention
  cpg-activity-type: inpatient-care
  useContext: nhập viện

- id: dischargeWithPlan
  description: "Xuất viện với kế hoạch điều trị ngoại trú và hướng dẫn an toàn."
  type: action
  cpg-activity-type: outpatient-care
  useContext: ngoại trú

- id: scheduleFollowup
  description: "Sắp xếp tái khám chuyên khoa hô hấp hoặc tim mạch và điều chỉnh thuốc lâu dài."
  type: action
  cpg-activity-type: administrative
  useContext: follow-up

## Bảng phân loại nguyên nhân khó thở

| Loại nguyên nhân    | Đặc điểm / Ví dụ                                  |
|---------------------|---------------------------------------------------|
| Tim mạch            | Suy tim, NMCT, phù phổi                         |
| Phổi                | COPD, hen, viêm phổi, ARDS                          |
| Vascular            | Thuyên tắc phổi                                    |
| Chuyển hóa          | Mất cân bằng acid-base, thiếu máu                   |
| Tâm lý              | Hoảng loạn, rối loạn lo âu                          |

## Ghi chú / TODO

- Generated from diagrams/dyspnea-diagram.png
