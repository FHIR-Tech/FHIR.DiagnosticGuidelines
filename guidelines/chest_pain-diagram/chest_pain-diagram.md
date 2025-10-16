---
id: chest_pain-diagram
title: Hướng dẫn đánh giá đau ngực
description: Quy trình phân loại và xử trí ban đầu đau ngực, bao gồm loại trừ bệnh lý tim mạch cấp tính và phân biệt các nguyên nhân khác.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/chest_pain-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho bệnh nhân đến khám vì đau ngực. Mục tiêu: nhận diện triệu chứng báo động (NMCT, thuyên tắc phổi, bóc tách động mạch chủ), phân loại nguy cơ và hướng xử trí cấp/ngoại trú.

## Flow

1. stepId: immediateThreat
   question: "Bệnh nhân có đau ngực dữ dội kèm khó thở nặng, vã mồ hôi, ngất, hoặc mất ý thức không?"
   type: boolean
   next:
     true: action=activateAcuteResponse
     false: stepId=historyAndRisk

2. stepId: historyAndRisk
   question: "Thu thập tiền sử: yếu tố nguy cơ tim mạch, tuổi, hút thuốc, đau lan hàm/cằm/chi trái, yếu tố giảm đau khi nghỉ?"
   type: info
   next:
     info: stepId=vitalSigns

3. stepId: vitalSigns
   question: "Huyết áp, nhịp tim, SpO2, nhiệt độ có bất thường không?"
   type: choice
   answers:
     - code: unstable
       display: "Mất ổn định huyết động"
       next: action=activateAcuteResponse
     - code: stable
       display: "Ổn định"
       next: stepId=ecgNeed

4. stepId: ecgNeed
   question: "Có chỉ định làm ECG ngay (đau ngực <12 giờ hoặc triệu chứng gợi ý)?"
   type: boolean
   next:
     true: action=orderECG
     false: stepId=considerNonCardiac

5. stepId: troponinAndLabs
   question: "ECG/triệu chứng gợi ý NMCT hoặc cần xét nghiệm troponin?"
   type: boolean
   next:
     true: action=orderTroponinAndLabs
     false: stepId=imaging

6. stepId: imaging
   question: "Cân nhắc X-quang ngực, CT pulmonary angiography, hoặc siêu âm tim?"
   type: choice
   answers:
     - code: cta
       display: "Nghi thuyên tắc phổi"
       next: action=orderCTPA
     - code: cxr
       display: "X-quang ngực"
       next: action=orderCXR
     - code: echo
       display: "Siêu âm tim"
       next: action=orderEcho

7. stepId: considerGIorMusculoskeletal
   question: "Triệu chứng gợi ý nguyên nhân tiêu hóa, cơ xương hay thần kinh (đau tăng khi thay đổi tư thế, ăn uống)?"
   type: boolean
   next:
     true: action=manageNonCardiac
     false: action=monitorAndRepeat

8. stepId: disposition
   question: "Cần nhập viện hay quản lý ngoại trú?"
   type: choice
   answers:
     - code: admit
       display: "Nhập viện"
       next: action=admitAndManage
     - code: outpatient
       display: "Ngoại trú"
       next: action=dischargeWithPlan

9. stepId: followUp
   question: "Sắp xếp tái khám và theo dõi triệu chứng không?"
   type: boolean
   next:
     true: action=scheduleFollowup
     false: action=end

10. stepId: safetyNet
    question: "Hướng dẫn bệnh nhân khi nào cần quay lại (tăng đau, khó thở, môi tím) không?"
    type: boolean
    next:
      true: action=provideSafetyNet
      false: action=end

## Hành động

- id: activateAcuteResponse
  description: "Kích hoạt xử trí cấp cứu: ABC, oxy, đường truyền, ECG liên tục, gọi đội tim mạch/CCU." 
  type: intervention
  cpg-activity-type: acute-management
  useContext: cấp cứu

- id: orderECG
  description: "Ghi ECG 12 đạo ngay tại giường và so sánh với ECG trước đó nếu có."
  type: investigation
  cpg-activity-type: diagnostic
  useContext: ECG

- id: orderTroponinAndLabs
  description: "Yêu cầu Troponin I/T, công thức máu, điện giải, D-dimer nếu cần, chức năng thận, men gan."
  type: investigation
  cpg-activity-type: laboratory
  useContext: xét nghiệm

- id: orderCTPA
  description: "Yêu cầu CT pulmonary angiography khi nghi ngờ thuyên tắc phổi và bệnh nhân đủ điều kiện."
  type: investigation
  cpg-activity-type: imaging
  useContext: thuyên tắc phổi

- id: orderCXR
  description: "Chụp X-quang ngực thẳng để đánh giá phổi, tim và ổ bụng trên nếu cần."
  type: investigation
  cpg-activity-type: imaging
  useContext: chest-imaging

- id: orderEcho
  description: "Siêu âm tim khi nghi ngờ nguyên nhân cơ tim, giảm chức năng thất, tràn dịch màng ngoài tim."
  type: investigation
  cpg-activity-type: imaging
  useContext: echo

- id: manageNonCardiac
  description: "Xử trí đau do cơ xương: NSAID, vật lý trị liệu; tiêu hóa: PPI, đánh giá loét/viêm dạ dày; tư vấn chế độ ăn."
  type: intervention
  cpg-activity-type: management
  useContext: noncardiac

- id: admitAndManage
  description: "Nhập viện theo dõi và điều trị theo nguyên nhân (NMCT, PE, bóc tách)."
  type: intervention
  cpg-activity-type: inpatient-care
  useContext: nhập viện

- id: dischargeWithPlan
  description: "Xuất viện với kế hoạch khám lại, thuốc và hướng dẫn an toàn nếu không có dấu hiệu nặng."
  type: action
  cpg-activity-type: outpatient-care
  useContext: ngoại trú

- id: scheduleFollowup
  description: "Sắp xếp tái khám chuyên khoa tim mạch hoặc nội tổng quát trong 1–2 tuần tuỳ nguy cơ."
  type: action
  cpg-activity-type: administrative
  useContext: follow-up

- id: provideSafetyNet
  description: "Hướng dẫn bệnh nhân quay lại nếu xuất hiện khó thở trầm trọng, đổ mồ hôi lạnh, mất ý thức, đau tăng." 
  type: action
  cpg-activity-type: patient-education
  useContext: an toàn

## Bảng phân loại nguyên nhân đau ngực

| Loại nguyên nhân    | Đặc điểm / Ví dụ                                  |
|---------------------|---------------------------------------------------|
| Tim mạch            | NMCT, đau thắt ngực do thiếu máu cục bộ, bóc tách động mạch chủ |
| Hô hấp              | Thuyên tắc phổi, viêm màng phổi, viêm phổi          |
| Tiêu hóa            | Trào ngược, loét dạ dày, viêm tuỵ                    |
| Cơ xương            | Viêm cơ, gãy xương sườn, đau thành ngực             |
| Tâm lý              | Lo âu, cơn hoảng loạn                                |

## Ghi chú / TODO

- Generated from diagrams/chest_pain-diagram.png
