---
id: dieu-tri-chan-doan-dot-quy
title: Chẩn đoán và Điều trị - Đột quỵ / Cơn thiếu máu não thoáng qua
description: Hướng dẫn tóm tắt chẩn đoán và điều trị cơn thiếu máu não thoáng qua (CTMNTQ) và đột quỵ nhẹ theo nội dung văn bản nguồn.
version: 1.0.0
date: 2025-10-09
authors:
  - name: Dự thảo AI (từ `diagrams/dieu-tri-chan-doan-dot-quy.txt`)
fhirVersion: "4.0.1"
---

## Context / Scope

Tài liệu này tóm tắt các phần Chẩn đoán và Điều trị liên quan tới cơn thiếu máu não thoáng qua (CTMNTQ) và đột quỵ nhẹ từ nguồn cung cấp. Mục tiêu: giảm nguy cơ tái phát, xử trí cấp sớm các tình huống có nguy cơ cao, và kiểm soát các yếu tố nguy cơ thay đổi được.

Áp dụng cho bệnh nhân nghi ngờ CTMNTQ hoặc đột quỵ nhẹ; không thay thế phán đoán lâm sàng của chuyên gia. Một số mã chuẩn (ICD-10, SNOMED, LOINC) cần được điền — đánh dấu TODO bên dưới.

## Flow

1. stepId: clinical_neurological_signs
   question: "Có dấu hiệu thần kinh khu trú (ví dụ: méo miệng, nói khó, liệt một chi, chóng mặt nghi ngờ tổn thương một bên)?"
   type: boolean
   next:
     true: stepId=imaging_and_classification
     false: action=observe_and_followup

2. stepId: imaging_and_classification
   question: "Đã thực hiện hình ảnh học (CT/MRI) để tìm tổn thương? (DWI MRI hoặc CT scan)"
   type: choice
   answers:
     - code: dwi_pos
       display: "DWI dương (tổn thương trên MRI)"
       next: stepId=classify_by_nihss
     - code: dwi_neg
       display: "DWI âm (không thấy tổn thương)"
       next: stepId=assess_tia_vs_minor

3. stepId: assess_tia_vs_minor
   question: "Triệu chứng kéo dài < 24 giờ và không có tổn thương trên DWI → Cân nhắc CTMNTQ?"
   type: boolean
   next:
     true: action=diagnose_TIA
     false: stepId=classify_by_nihss

4. stepId: classify_by_nihss
   question: "Điểm NIHSS hiện tại là bao nhiêu?"
   type: numeric
   next:
     "<=3": action=early_DAPT_if_high_risk
     "<=5": action=antiplatelet_or_consider_risk
     ">5": action=stroke_management_refer

5. stepId: abc_d2_score
   question: "ABCD2 score (điểm)"
   type: numeric
   next:
     "<4": action=single_antiplatelet_low_risk
     ">=4": stepId=consider_early_dual_antiplatelet

6. stepId: consider_early_dual_antiplatelet
   question: "Trong vòng 24 giờ đầu và ABCD2 >=4 hoặc NIHSS phù hợp: có chỉ định điều trị sớm kết hợp (DAPT)?"
   type: boolean
   next:
     true: action=early_DAPT_if_high_risk
     false: action=single_antiplatelet_low_risk

7. stepId: atrial_fibrillation_check
   question: "Có rung nhĩ (AF) hoặc tiền sử AF trên ECG/Holter?"
   type: boolean
   next:
     true: action=anticoagulation_for_af
     false: action=antiplatelet_pathway

8. stepId: valvular_heart_disease_check
   question: "Có bệnh van tim (van 2 lá cơ học hoặc hẹp van 2 lá trung bình-nặng)?"
   type: boolean
   next:
     true: action=anticoagulation_vka_mechanical_valve
     false: action=anticoagulation_or_antiplatelet_decision

9. stepId: carotid_stenosis_assessment
   question: "Hẹp động mạch cảnh ngoại sọ triệu chứng ≥ 50%?"
   type: numeric
   next:
     ">=50": action=consider_carotid_revascularization
     "<50": action=medical_management

10. stepId: intracranial_stenosis_or_dissection
    question: "Hẹp mạch nội sọ do xơ vữa hoặc lóc tách?"
    type: choice
    answers:
      - code: dissection
        display: "Lóc tách - cân nhắc aspirin hoặc kháng vitamin K"
        next: action=consult_specialist
      - code: intracranial_atherosclerosis
        display: "Hẹp mạch nội sọ do xơ vữa - điều trị nội khoa"
        next: action=medical_management

11. stepId: risk_factors_review
    question: "Đã đánh giá và có kế hoạch kiểm soát: huyết áp, lipid, đái tháo đường, hút thuốc, béo phì?"
    type: checklist
    next:
      completed: action=risk_factor_management

12. stepId: followup_management
    question: "Sắp xếp tái khám và theo dõi tác dụng phụ/biến chứng của thuốc?"
    type: boolean
    next:
      true: action=schedule_followup
      false: action=arrange_followup

## Actions

- id: observeAndFollowup
  description: "Theo dõi lâm sàng, hướng dẫn bệnh nhân quay lại nếu triệu chứng tiến triển; sắp xếp đánh giá sâu hơn nếu cần."
  type: follow-up
  cpg-activity-type: follow-up
  useContext: monitoring

- id: diagnoseTIA
  description: "Chẩn đoán CTMNTQ (TIA) khi triệu chứng hồi phục <24 giờ và không có tổn thương DWI; đánh giá ABCD2 và bắt đầu can thiệp phòng ngừa phù hợp."
  type: action
  cpg-activity-type: diagnosis
  useContext: tia

- id: singleAntiplatelet
  description: "Bắt đầu aspirin hoặc clopidogrel nếu chỉ định (liều theo hướng dẫn địa phương) cho bệnh nhân nguy cơ thấp."
  type: intervention
  cpg-activity-type: medication
  useContext: antiplatelet

- id: earlyDAPT
  description: "Phối hợp aspirin + clopidogrel trong 21-90 ngày cho bệnh nhân có nguy cơ cao trong 24 giờ đầu, theo cân nhắc nguy cơ chảy máu."
  type: intervention
  cpg-activity-type: medication
  useContext: DAPT

- id: strokeManagementRefer
  description: "Chuyển và xử trí đột quỵ nặng: can thiệp tái thông nếu phù hợp, nhập viện, hội chẩn chuyên khoa."
  type: referral
  cpg-activity-type: acute-management
  useContext: stroke

- id: antiplateletPathway
  description: "Theo dõi và điều chỉnh phác đồ kháng kết tập tiểu cầu theo mức độ nguy cơ khi không có AF."
  type: action
  cpg-activity-type: medication
  useContext: antiplatelet

- id: anticoagulationForAF
  description: "Khởi kháng đông cho bệnh nhân có rung nhĩ phù hợp; ưu tiên DOAC nếu không có chống chỉ định."
  type: intervention
  cpg-activity-type: medication
  useContext: anticoagulation

- id: anticoagulationVKA
  description: "Sử dụng VKA cho bệnh nhân có van cơ học hoặc chống chỉ định DOAC; theo dõi INR."
  type: intervention
  cpg-activity-type: medication
  useContext: anticoagulation

- id: considerCarotidRevascularization
  description: "Cân nhắc can thiệp động mạch cảnh (CEA hoặc stent) cho hẹp triệu chứng 50–99% theo chỉ định chuyên gia."
  type: referral
  cpg-activity-type: procedure
  useContext: vascular

- id: medicalManagement
  description: "Quản lý nội khoa tối ưu: kiểm soát huyết áp, lipid, đường huyết; sử dụng thuốc phù hợp và quản lý yếu tố nguy cơ."
  type: management
  cpg-activity-type: chronic-care
  useContext: secondary-prevention

- id: consultSpecialist
  description: "Hội chẩn chuyên gia cho các trường hợp phức tạp (lóc tách, moyamoya, chỉ định phẫu thuật)."
  type: referral
  cpg-activity-type: referral
  useContext: specialist

- id: riskFactorManagement
  description: "Thiết lập mục tiêu kiểm soát huyết áp, LDL, HbA1c và các yếu tố lối sống; lập kế hoạch theo dõi."
  type: action
  cpg-activity-type: prevention
  useContext: risk-management

- id: scheduleFollowup
  description: "Sắp xếp tái khám để theo dõi nguy cơ tái phát, điều chỉnh thuốc và theo dõi biến chứng."
  type: action
  cpg-activity-type: administrative
  useContext: follow-up

## Notes / TODO

- Mã hóa: Nhiều mục cần ánh xạ tới hệ mã chuẩn (ICD-10, SNOMED CT, ATC cho thuốc, LOINC cho xét nghiệm). Chỗ nào cần mã đã được đánh dấu `TODO`.
- Các liều thuốc được ghi dựa trên văn bản nguồn; cần xác minh lại với tài liệu nguồn/thuốc địa phương trước khi triển khai lâm sàng.
- Bản MD này là nguồn để sinh `Bundle` (PlanDefinition, Library, Questionnaire, ActivityDefinition). Các `stepId` tương ứng sẽ trở thành `linkId` trong Questionnaire.

---

Generated from `diagrams/dieu-tri-chan-doan-dot-quy.txt` using project rule `SYSTEM_RULE.md`.
