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

- actionId: observe_and_followup
  title: Quan sát và tái khám
  description: Theo dõi lâm sàng, hướng dẫn bệnh nhân quay lại nếu triệu chứng tiến triển; sắp xếp đánh giá sâu hơn nếu cần.

- actionId: diagnose_TIA
  title: Chẩn đoán CTMNTQ (TIA)
  description: Triệu chứng hồi phục <24 giờ và không có tổn thương DWI. Xem xét đánh giá nguy cơ (ABCD2) và bắt đầu can thiệp phòng ngừa:
    - Nếu ABCD2 < 4: aspirin 81-325 mg/ngày (sau đó duy trì 81-100 mg/ngày) hoặc clopidogrel nếu dị ứng với aspirin.
    - Nếu ABCD2 ≥ 4: xem xét điều trị sớm tích cực (xem `early_DAPT_if_high_risk`).
  todo: Map to ICD/SNOMED codes (TODO)

- actionId: single_antiplatelet_low_risk
  title: Chống kết tập tiểu cầu đơn
  description: Aspirin 81-325 mg/ngày (sau đó duy trì 81-100 mg/ngày). Nếu dị ứng: clopidogrel 75 mg/ngày hoặc aspirin + dipyridamole hoặc cilostazol.
  todo: Verify medication codes and contra-indications (TODO)

- actionId: early_DAPT_if_high_risk
  title: Điều trị kết hợp sớm (DAPT) cho CTMNTQ/đột quỵ nhẹ có nguy cơ cao
  description: Trong vòng 24 giờ đầu, cho phối hợp aspirin + clopidogrel (nạp clopidogrel 300-600 mg, duy trì 75 mg/ngày) trong 21-90 ngày tùy kịch bản; hoặc aspirin + ticagrelor (nạp 180 mg, sau 12 giờ 90 mg, duy trì 90 mg x2/ngày) trong các chỉ định phù hợp. Thời gian tối đa 7 ngày cho một số hướng dẫn sớm.
  caution: Chú ý nguy cơ chảy máu. Cân nhắc chống chỉ định.
  todo: Add SNOMED/ATC codes for medications (TODO)

- actionId: antiplatelet_or_consider_risk
  title: Chống kết tập tiểu cầu hoặc cân nhắc nguy cơ
  description: Với đột quỵ nhẹ (NIHSS ≤5) có thể bắt đầu thuốc chống kết tập tiểu cầu đơn; cân nhắc DAPT nếu có yếu tố nguy cơ cao.

- actionId: stroke_management_refer
  title: Quản lý đột quỵ nặng / chuyển viện chuyên khoa
  description: NIHSS >5 → đánh giá cấp cứu đột quỵ, can thiệp tái thông nếu phù hợp, nhập khoa thăm dò/chuyên khoa.

- actionId: antiplatelet_pathway
  title: Đường điều trị chống kết tập tiểu cầu
  description: Nếu không có AF và không có chống chỉ định, theo chu trình chống kết tập tiểu cầu theo mức độ nguy cơ.

- actionId: anticoagulation_for_af
  title: Kháng đông cho rung nhĩ
  description: Nếu rung nhĩ không do van tim → ưu tiên thuốc chống đông đường uống thế hệ mới (DOAC): dabigatran, rivaroxaban, apixaban, edoxaban. Nếu có van cơ học hoặc hẹp van 2 lá trung bình-nặng → dùng kháng vitamin K (VKA) với mục tiêu INR 2,5-3,5.
  todo: Map DOAC and VKA meds to codes (TODO)

- actionId: anticoagulation_vka_mechanical_valve
  title: Kháng vitamin K cho van cơ học
  description: Dùng VKA với mục tiêu INR 2,5-3,5; đánh giá nguy cơ chảy máu và theo dõi INR.

- actionId: anticoagulation_or_antiplatelet_decision
  title: Quyết định kháng đông hoặc kháng kết tập tiểu cầu
  description: Dựa trên nguyên nhân (tim hay mạch), nguy cơ chảy máu, và đặc điểm bệnh nhân.

- actionId: consider_carotid_revascularization
  title: Cân nhắc tái thông động mạch cảnh (stent hoặc CEA)
  description: Hẹp động mạch cảnh ngoại sọ triệu chứng 50–99% → xem xét can thiệp tái thông phối hợp điều trị nội khoa; tham vấn chuyên gia mạch máu.

- actionId: medical_management
  title: Điều trị nội khoa tối ưu
 description: Quản lý nội khoa tích cực: chống kết tập tiểu cầu/kháng đông phù hợp, kiểm soát huyết áp, lipid, đường huyết; cân nhắc can thiệp nếu cần.

- actionId: consult_specialist
  title: Tham vấn chuyên gia
  description: Các trường hợp phức tạp (moyamoya, lóc tách nặng, chỉ định phẫu thuật) cần hội chẩn chuyên gia thần kinh mạch máu hoặc can thiệp.

- actionId: risk_factor_management
  title: Kiểm soát yếu tố nguy cơ
  description: 
    - Huyết áp mục tiêu < 130/80 mmHg; lựa chọn thuốc: chẹn thụ thể AT1 / ức chế men chuyển ± lợi tiểu.
    - LDL-C mục tiêu < 70 mg/dL; liệu pháp statin ± thêm thuốc nếu cần.
    - Đái tháo đường: mục tiêu HbA1c < 7%.
    - Giảm cân BMI mục tiêu < 23, ngưng hút thuốc, CPAP cho ngưng thở khi ngủ.
  todo: Add LOINC/SNOMED for lab targets (TODO)

- actionId: schedule_followup
  title: Sắp xếp tái khám
  description: Lên lịch tái khám để theo dõi tái phát, tác dụng phụ, điều chỉnh thuốc.

- actionId: arrange_followup
  title: Sắp xếp tái khám khẩn
  description: Nếu chưa có lịch, sắp xếp tái khám sớm trong 1-2 tuần hoặc theo mức độ nguy cơ.

## Notes / TODO

- Mã hóa: Nhiều mục cần ánh xạ tới hệ mã chuẩn (ICD-10, SNOMED CT, ATC cho thuốc, LOINC cho xét nghiệm). Chỗ nào cần mã đã được đánh dấu `TODO`.
- Các liều thuốc được ghi dựa trên văn bản nguồn; cần xác minh lại với tài liệu nguồn/thuốc địa phương trước khi triển khai lâm sàng.
- Bản MD này là nguồn để sinh `Bundle` (PlanDefinition, Library, Questionnaire, ActivityDefinition). Các `stepId` tương ứng sẽ trở thành `linkId` trong Questionnaire.

---

Generated from `diagrams/dieu-tri-chan-doan-dot-quy.txt` using project rule `SYSTEM_RULE.md`.
