---
id: chan-doan-dieu-tri-cum-mua
title: Cúm mùa — Chẩn đoán và điều trị
description: Hướng dẫn chẩn đoán, phân loại mức độ, và điều trị người bệnh cúm mùa (seasonal influenza).
version: 1.0.0
date: 2025-10-10
authors:
  - name: Bộ Y tế (tổng hợp)
fhirVersion: "4.0.1"
source-type: text
source-file: diagrams/chan-doan-dieu-tri-cum-mua.txt
source-checksum: TODO:sha256
generated-from: diagrams/chan-doan-dieu-tri-cum-mua.txt
---

## Context / Scope
Hướng dẫn tóm tắt chẩn đoán và điều trị người bệnh nhiễm cúm mùa, bao gồm phân độ nặng, các xét nghiệm chẩn đoán, và chỉ định sử dụng thuốc kháng vi rút cũng như điều trị hỗ trợ.

## Flow
- id: prescribeOseltamivir
  description: "Sử dụng Oseltamivir càng sớm càng tốt; liều theo tuổi và cân nặng. Thời gian thường 5 ngày, có thể kéo dài ở bệnh nặng hoặc suy giảm miễn dịch."
  type: intervention
  cpg-activity-type: medication
  useContext: antiviral

- id: outpatientManagement
  description: "Điều trị hỗ trợ ngoại trú: bù nước, hạ sốt, nghỉ ngơi, theo dõi; không khuyến cáo kháng sinh trừ khi có nghi ngờ bội nhiễm."
  type: management
  cpg-activity-type: outpatient-care
  useContext: supportive-care

- id: admitAndEscalate
  description: "Nhập viện và xử trí nâng cao: oxy, HFNC/NIV/intubation, xét nghiệm và điều trị bội nhiễm, cân nhắc ECMO trong trường hợp thất bại các biện pháp khác."
  type: referral
  cpg-activity-type: acute-management
  useContext: hospital-care

- id: end
  description: "Kết thúc hướng dẫn khi không còn hành động tiếp theo cần thực hiện."
  type: action
  cpg-activity-type: administrative
  useContext: end-flow

- id: diagnosticTests
  description: "Yêu cầu test nhanh hoặc RT-PCR để xác định chủng virus và hướng quản lý; lấy mẫu theo quy định."
  type: investigation
  cpg-activity-type: laboratory
  useContext: diagnostic

- id: supportiveCare
  description: "Quản lý triệu chứng: acetaminophen cho sốt/đau, bù nước, tư vấn dinh dưỡng và nghỉ ngơi."
  type: intervention
  cpg-activity-type: symptom-management
  useContext: supportive-care

- id: monitorAndFollowUp
  description: "Theo dõi tại nhà hoặc ngoại trú, cảnh báo dấu hiệu nặng và sắp xếp tái khám khi cần."
  type: follow-up
  cpg-activity-type: follow-up
  useContext: monitoring

- id: antiviralAlternatives
  description: "Cân nhắc Baloxavir hoặc Zanamivir khi Oseltamivir không phù hợp hoặc chống chỉ định."
  type: intervention
  cpg-activity-type: medication
  useContext: antiviral

- id: infectionControl
  description: "Áp dụng biện pháp phòng lây: khẩu trang, rửa tay, cách ly theo mức độ; thông báo cho đơn vị y tế nếu cần."
  type: action
  cpg-activity-type: infection-control
  useContext: public-health

- id: vaccinationAdvice
  description: "Khuyến cáo tiêm vắc-xin mùa cúm theo độ tuổi và nhóm nguy cơ; tư vấn lợi ích và chống chỉ định."
  type: action
  cpg-activity-type: prevention
  useContext: vaccination

- id: riskCommunication
  description: "Giải thích nguy cơ tiến triển nặng và hướng dẫn khi nào tìm chăm sóc y tế ngay lập tức."
  type: action
  cpg-activity-type: patient-education
  useContext: communication
     true: action=prescribeOseltamivir
     false: stepId=outpatientSupport

4. stepId: mildCaseManagement
   action: outpatient-management
   question: "Người bệnh cúm nhẹ không có yếu tố nguy cơ - điều trị hỗ trợ và theo dõi" 
   type: info
   next:
     default: action=end

5. stepId: outpatientSupport
   action: supportive-care
   question: "Cung cấp điều trị hỗ trợ (bù nước, hạ sốt, dinh dưỡng), tư vấn theo dõi dấu hiệu nặng" 
   type: info
   next:
     default: action=end

6. stepId: severeCase
   question: "Người bệnh có biểu hiện nặng (khó thở, thiếu oxy, suy cơ quan, shock)?"
   type: boolean
   next:
     true: stepId=admitAndEscalate
     false: action=end

7. stepId: diagnosticTests
   question: "Cần xét nghiệm khẳng định (RT-PCR) hoặc test nhanh để sàng lọc?"
   type: choice
   answers:
     - code: rapid
       display: "Test nhanh (sàng lọc)"
       next: stepId=interpretation
     - code: pcr
       display: "RT-PCR / Multiplex-PCR (khẳng định)"
       next: stepId=interpretation

8. stepId: interpretation
   question: "Kết quả xét nghiệm dương tính cho vi rút cúm?"
   type: boolean
   next:
     true: stepId=confirmCase
     false: stepId=differentialDiagnosis

9. stepId: confirmCase
   action: confirm-diagnosis
   question: "Ca bệnh khẳng định - tiến hành phân mức độ và điều trị phù hợp" 
   type: info
   next:
     default: stepId=riskAssessment

10. stepId: differentialDiagnosis
    action: consider-other-pathogens
    question: "Cân nhắc nguyên nhân khác nếu nghi ngờ và xét nghiệm cúm âm tính" 
    type: info
    next:
      default: action=end

11. stepId: admitAndEscalate
    action: admit
    question: "Nhập viện, cân nhắc hỗ trợ hô hấp (oxy, HFNC, NIV, intubation, ECMO) và điều trị kháng vi rút kéo dài/kháng khuẩn nếu nghi ngờ bội nhiễm" 
    type: info
    next:
      default: action=end

## Actions
- actionId: prescribeOseltamivir
  title: "Kê Oseltamivir"
  description: "Sử dụng Oseltamivir càng sớm càng tốt; liều dùng theo hướng dẫn tuổi và cân nặng. Thời gian: 5 ngày, có thể kéo dài đến 10 ngày ở bệnh nặng hoặc suy giảm miễn dịch. Thay thế: Baloxavir hoặc Zanamivir nếu cần."
  resource: ActivityDefinition

- actionId: outpatient-management
  title: "Điều trị ngoại trú hỗ trợ"
  description: "Bù nước, hạ sốt (không dùng aspirin), dinh dưỡng, theo dõi tái khám khi có dấu hiệu nặng. Không khuyến cáo kháng sinh nếu nhẹ."
  resource: ActivityDefinition

-- actionId: admitAndEscalate
  title: "Nhập viện và điều trị nâng cao"
  description: "Nhập viện, theo dõi và thực hiện điều trị hỗ trợ suy hô hấp (oxy, HFNC, NIV, thở máy), điều trị kháng vi rút kéo dài/kháng khuẩn nếu nghi ngờ bội nhiễm; cân nhắc ECMO nếu thất bại các biện pháp khác."
  resource: ActivityDefinition

- actionId: end
  title: "Kết thúc hướng dẫn"
  description: "Không có hành động tiếp theo - kết thúc luồng điều trị/định hướng." 
  resource: ActivityDefinition

## Notes / TODO
- Map drug codes (Oseltamivir, Zanamivir, Baloxavir) to RxNorm or ATC codes: TODO
- Map tests to LOINC codes (Influenza RNA PCR, rapid antigen): TODO
- source-checksum: TODO - compute SHA256 of original text file and set above
