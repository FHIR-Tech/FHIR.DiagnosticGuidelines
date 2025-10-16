---
id: epistaxis-diagram
title: Hướng dẫn chảy máu mũi (epistaxis)
description: Quy trình quản lý chảy máu mũi: phân loại trước, giữa, sau mũi, cầm máu sơ cấp, ổn định và chuyển can thiệp.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/epistaxis-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho mọi độ tuổi có chảy máu mũi; mục tiêu cầm máu hiệu quả, xác định nguyên nhân và chuyển chuyên khoa khi cần.

## Flow

1. stepId: severeBleed
   question: "Chảy máu nhiều, khó cầm, mất ý thức hoặc dấu hiệu sốc không?"
   type: boolean
   next:
     true: action=resuscitateAndENTUrgent
     false: stepId=anteriorOrPosterior

2. stepId: anteriorOrPosterior
   question: "Nguồn chảy mũi có vẻ từ trước (nares) hay sau?"
   type: choice
   answers:
     - code: anterior
       display: "Trước"
       next: action=directPressureAndCautery
     - code: posterior
       display: "Sau"
       next: action=posteriorPackingAndENT

3. stepId: directPressure
   question: "Áp lực trực tiếp 10–15 phút có hiệu quả không?"
   type: boolean
   next:
     true: action=observeAndDischargeWithAdvice
     false: action=considerCautery

4. stepId: medicationReview
   question: "Bệnh nhân dùng thuốc chống đông, NSAID hoặc có rối loạn đông máu không?"
   type: boolean
   next:
     true: action=reverseAnticoagulationOrCorrectCoagulopathy
     false: action=continueLocalMeasures

5. stepId: packingOrSurgery
   question: "Cần nhét mũi sau hoặc can thiệp phẫu thuật không?"
   type: boolean
   next:
     true: action=ENTIntervention
     false: action=monitor

6. stepId: vitalSigns
   question: "Dấu hiệu sống bất thường (tachycardia, hypotension) không?"
   type: boolean
   next:
     true: action=resuscitateAndAdmit
     false: action=outpatientManagement

7. stepId: localInfection
   question: "Nhiễm trùng hoặc chấn thương cục bộ góp phần không?"
   type: boolean
   next:
     true: action=antibioticsAndENTFollowup
     false: action=patientEducation

8. stepId: disposition
   question: "Cần nhập viện hay có thể xuất viện?"
   type: choice
   answers:
     - code: admit
       display: "Nhập viện"
       next: action=admitForMonitoring
     - code: discharge
       display: "Xuất viện"
       next: action=dischargeWithFollowup

9. stepId: followUp
   question: "Hẹn tái khám ENT trong 48–72 giờ không?"
   type: boolean
   next:
     true: action=arrangeENTFollowup
     false: action=end

10. stepId: prevention
    question: "Cần tư vấn tránh xì mũi mạnh, giữ ẩm và tạm dừng thuốc gây chảy máu không?"
    type: boolean
    next:
      true: action=providePreventionAdvice
      false: action=end

## Hành động

- id: resuscitateAndENTUrgent
  description: "Ổn định ABC, truyền dịch, kiểm soát mất máu và gọi ENT khẩn."
  type: emergency
  cpg-activity-type: emergency
  useContext: khẩn

- id: directPressureAndCautery
  description: "Áp lực trực tiếp; nếu thất bại, tiến hành cautery dưới gây tê."
  type: intervention
  cpg-activity-type: procedure
  useContext: cầm máu

- id: posteriorPackingAndENT
  description: "Nhét mũi sau và tham vấn ENT để can thiệp thêm."
  type: intervention
  cpg-activity-type: procedure
  useContext: nhét mũi

- id: reverseAnticoagulationOrCorrectCoagulopathy
  description: "Xem xét đảo ngược thuốc chống đông hoặc truyền yếu tố nếu cần."
  type: action
  cpg-activity-type: medication
  useContext: đông máu

- id: ENTIntervention
  description: "Can thiệp bởi ENT: ligation, arterial embolization hoặc phẫu thuật."
  type: intervention
  cpg-activity-type: surgical
  useContext: phẫu thuật

- id: admitForMonitoring
  description: "Nhập viện để theo dõi và ổn định khi mất máu lớn hoặc yếu tố nguy cơ."
  type: intervention
  cpg-activity-type: inpatient-care
  useContext: nhập viện

- id: dischargeWithFollowup
  description: "Xuất viện với hướng dẫn tại nhà và hẹn ENT."
  type: action
  cpg-activity-type: outpatient-care
  useContext: ngoại trú

- id: arrangeENTFollowup
  description: "Sắp xếp tái khám với ENT trong vòng 48–72 giờ."
  type: action
  cpg-activity-type: administrative
  useContext: follow-up

- id: antibioticsAndENTFollowup
  description: "Kê kháng sinh nếu có nhiễm trùng và chuyển ENT theo dõi."
  type: action
  cpg-activity-type: medication
  useContext: nhiễm trùng

- id: providePreventionAdvice
  description: "Tư vấn tránh xì mũi mạnh, giữ ẩm và dừng thuốc gây chảy máu nếu chỉ định."
  type: action
  cpg-activity-type: patient-education
  useContext: phòng ngừa

## Bảng phân loại chảy máu mũi

| Loại | Ví dụ |
|------|------|
| Trước | Kiểm soát bằng áp lực, cautery |
| Sau | Thường nặng hơn, cần packing/ ENT |

## Ghi chú

- Generated from diagrams/epistaxis-diagram.png
