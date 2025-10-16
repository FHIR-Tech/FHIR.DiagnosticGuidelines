---
id: confusion-diagram
title: Hướng dẫn lẫn lộn/ lú lẫn (confusion)
description: Quy trình đánh giá bệnh nhân lú lẫn: nguyên nhân cấp (độc chất, nhiễm trùng, rối loạn điện giải, thiếu oxy) và hướng xử trí.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/confusion-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho bệnh nhân có thay đổi trạng thái tinh thần; mục tiêu xác định nguyên nhân kịch phát/ mạn tính và ổn định người bệnh.

## Flow

1. stepId: airwayBreathingCirculation
   question: "Có cần đảm bảo đường thở/ thông khí/ tuần hoàn ngay không?"
   type: boolean
   next:
     true: action=resuscitateAndStabilize
     false: stepId=onset

2. stepId: onset
   question: "Bắt đầu đột ngột hay từ từ; có tiền sử nghi ngờ ngộ độc hay thuốc mới không?"
   type: choice
   answers:
     - code: acute
       display: "Đột ngột"
       next: stepId=lookForInfectionOrStroke
     - code: chronic
       display: "Mạn"
       next: stepId=considerDementiaOrMetabolic

3. stepId: lookForInfectionOrStroke
   question: "Sốt, liệt cục bộ, thay đổi lời nói hay yếu không?"
   type: boolean
   next:
     true: action=urgentNeuroImagingAndSepsisWorkup
     false: stepId=checkMetabolic

4. stepId: checkMetabolic
   question: "Đo đường huyết, điện giải, ABG, thảo dược/ thuốc có gây lú lẫn?"
   type: boolean
   next:
     true: action=correctMetabolicCauses
     false: action=considerPsychiatricOrSubstance

5. stepId: toxicity
   question: "Nghi ngộ độc thuốc/ rượu/ benzodiazepine/opioid không?"
   type: boolean
   next:
     true: action=administerAntidoteIfAvailable
     false: action=continueInvestigation

6. stepId: infectionWorkup
   question: "Nghi nhiễm trùng (UTI, pneumonia) không?"
   type: boolean
   next:
     true: action=startAntibioticsIfSepsisSuspected
     false: action=monitorAndReassess

7. stepId: deliriumManagement
   question: "Người bệnh có dấu deliruim: rối loạn chu kỳ ngủ, thay đổi tâm thần?"
   type: boolean
   next:
     true: action=manageDeliriumNonPharmAndPharmIfSevere
     false: action=planFollowup

8. stepId: disposition
   question: "Cần nhập viện để đánh giá/ điều trị hay có thể quản lý ngoại trú?"
   type: choice
   answers:
     - code: admit
       display: "Nhập viện"
       next: action=admitForObservationAndWorkup
     - code: outpatient
       display: "Ngoại trú"
       next: action=dischargeWithSafetyPlan

9. stepId: safety
   question: "Người bệnh có nguy cơ gây hại cho bản thân/ người khác, an toàn môi trường không?"
   type: boolean
   next:
     true: action=implementSafetyPrecautions
     false: action=continuePlan

10. stepId: followUp
    question: "Sắp xếp tái khám/ phục hồi nhận thức hay can thiệp sớm?"
    type: boolean
    next:
      true: action=arrangeCognitiveFollowup
      false: action=end

## Hành động

- id: resuscitateAndStabilize
  description: "Ổn định ABC, bảo đảm oxy, huyết áp, đường huyết."
  type: intervention
  cpg-activity-type: emergency
  useContext: cấp-cứu

- id: urgentNeuroImagingAndSepsisWorkup
  description: "Chụp CT/MRI nếu nghi đột quỵ; làm cấy máu, X-quang ngực, xét nghiệm huyết học khi nghi nhiễm."
  type: investigation
  cpg-activity-type: diagnostic
  useContext: thần-kinh/nhiễm

- id: correctMetabolicCauses
  description: "Bù dịch, điều chỉnh điện giải, quản lý đường huyết và thận trọng với thuốc."
  type: intervention
  cpg-activity-type: supportive-care
  useContext: nội-khoa

- id: administerAntidoteIfAvailable
  description: "Dùng naloxone, flumazenil hoặc antidote phù hợp khi có chỉ định."
  type: intervention
  cpg-activity-type: medication
  useContext: ngộ-độc

- id: startAntibioticsIfSepsisSuspected
  description: "Khởi đầu kháng sinh theo protocol nếu nghi sốc nhiễm trùng."
  type: intervention
  cpg-activity-type: medication
  useContext: nhiễm-trùng

- id: manageDeliriumNonPharmAndPharmIfSevere
  description: "Ưu tiên biện pháp phi dược, sử dụng thuốc an thần thận trọng nếu cần."
  type: action
  cpg-activity-type: therapy
  useContext: deliriu

- id: admitForObservationAndWorkup
  description: "Nhập viện để điều tra nguyên nhân gây lú lẫn tích cực."
  type: intervention
  cpg-activity-type: inpatient-care
  useContext: nhập-viện

- id: dischargeWithSafetyPlan
  description: "Xuất viện với kế hoạch an toàn, người giám sát và hẹn theo dõi."
  type: action
  cpg-activity-type: outpatient-care
  useContext: ngoại-trú

- id: implementSafetyPrecautions
  description: "Thực hiện biện pháp an toàn: giám sát, thu dọn vật nguy hiểm."
  type: action
  cpg-activity-type: patient-safety
  useContext: an-toàn

- id: arrangeCognitiveFollowup
  description: "Sắp xếp phục hồi nhận thức hoặc khám thần kinh/ tâm thần."
  type: action
  cpg-activity-type: administrative
  useContext: follow-up

- id: planFollowup
  description: "Lên kế hoạch theo dõi và đánh giá lại khi cần."
  type: action
  cpg-activity-type: administrative
  useContext: follow-up

## Bảng phân loại nguyên nhân lú lẫn

| Loại | Ví dụ |
|------|------|
| Nhiễm trùng | UTI, pneumonia |
| Độc chất/ thuốc | Opioid, benzodiazepine |
| Nội tiết/ chuyển hóa | Đường huyết, điện giải |

## Ghi chú

- Generated from `diagrams/confusion-diagram.png`
