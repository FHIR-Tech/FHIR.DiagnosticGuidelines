---
id: vaginal_bleeding-diagram
title: Hướng dẫn đánh giá chảy máu âm đạo
description: Quy trình phân loại và xử trí ban đầu đối với chảy máu âm đạo bất thường ở mọi lứa tuổi, bao gồm đánh giá khẩn cấp vs. theo dõi ngoại trú.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
  - name: Reviewer Needed
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/vaginal_bleeding-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho bệnh nhân nữ than chảy máu âm đạo bất thường (không đúng kỳ kinh, sau giao hợp, giữa chu kỳ hoặc chảy máu nặng). Mục tiêu phân loại mức độ khẩn cấp, xác định nguyên nhân có khả năng và hướng xử trí ban đầu.

## Flow

1. stepId: start
   question: "Bệnh nhân có dấu hiệu mất máu nặng (choáng, da lạnh, huyết áp thấp) không?"
   type: boolean
   next:
     true: action=refer-urgent
     false: stepId=menstrualStatus

2. stepId: menstrualStatus
   question: "Bệnh nhân có đang trong chu kỳ kinh nguyệt hoặc mới sinh con (postpartum)?"
   type: choice
   answers:
     - code: menstrual
       display: "Kinh nguyệt"
       next: action=menstrual-related
     - code: postpartum
       display: "Sau sinh"
       next: action=postpartum-eval
     - code: intermenstrual
       display: "Giữa chu kỳ / sau giao hợp"
       next: stepId=assessInfectionCancer

3. stepId: assessInfectionCancer
   question: "Có triệu chứng kèm theo: đau, tiết dịch mùi, sụt cân, hay khối vùng chậu không?"
   type: boolean
   next:
     true: action=investigateInfectionOrMalignancy
     false: action=outpatient-eval

4. stepId: hemodynamicStatus
   question: "Bệnh nhân có dấu hiệu mất nhiều máu (nhịp nhanh, huyết áp thấp, choáng) không?"
   type: boolean
   next:
     true: action=refer-urgent
     false: stepId=contraceptionAndMeds

5. stepId: contraceptionAndMeds
   question: "Bệnh nhân có dùng thuốc tránh thai, thuốc chống đông hay thuốc có thể gây xuất huyết không?"
   type: boolean
   next:
     true: action=reviewMedications
     false: stepId=imagingConsider

6. stepId: imagingConsider
   question: "Cần siêu âm vùng chậu hoặc nội soi để đánh giá không?"
   type: boolean
   next:
     true: action=orderImaging
     false: action=conservativeManagement

7. stepId: sexualHistory
   question: "Có quan hệ tình dục gần đây, giao hợp đau, hoặc nguy cơ lây truyền không?"
   type: boolean
   next:
     true: action=investigateSTI
     false: stepId=followUp

8. stepId: followUp
   question: "Triệu chứng kéo dài hay tái phát không?"
   type: boolean
   next:
     true: action=referGynae
     false: action=conservativeManagement

9. stepId: labTests
   question: "Có cần xét nghiệm máu (HB, công thức máu, chức năng đông) không?"
   type: boolean
   next:
     true: action=orderLabTests
     false: action=monitorAndPlan

10. stepId: dispositionCheck
    question: "Cần nhập viện hoặc chuyển chuyên khoa không?"
    type: choice
    answers:
      - code: admit
        display: "Nhập viện"
        next: action=refer-urgent
      - code: outpatient
        display: "Ngoại trú"
        next: action=conservativeManagement

## Hành động

- id: refer-urgent
  description: "Chuyển cấp cứu hoặc xử trí ngay nếu mất máu nhiều hoặc biểu hiện sốc."
  type: referral
  cpg-activity-type: emergency
  useContext: cấp cứu

- id: menstrual-related
  description: "Tư vấn theo dõi nếu chảy máu phù hợp chu kỳ; đánh giá tình trạng rối loạn chu kỳ nếu cần."
  type: advice
  cpg-activity-type: patient-education
  useContext: kinh nguyệt

- id: postpartum-eval
  description: "Đánh giá nguyên nhân chảy máu sau sinh (tổn thương tầng sinh môn, sót nhau, rối loạn đông)."
  type: investigation
  cpg-activity-type: clinical-assessment
  useContext: sau sinh

- id: investigateInfectionOrMalignancy
  description: "Lấy mẫu, soi cổ tử cung, siêu âm vùng chậu và xét nghiệm cần thiết để loại trừ nhiễm trùng hoặc nguyên nhân ác tính."
  type: investigation
  cpg-activity-type: diagnostic
  useContext: nghi ngờ nhiễm/ác tính

- id: reviewMedications
  description: "Rà soát và điều chỉnh thuốc có thể gây xuất huyết (chống đông, NSAID, thuốc tránh thai)."
  type: action
  cpg-activity-type: medication-review
  useContext: dược

- id: orderImaging
  description: "Yêu cầu siêu âm vùng chậu hoặc nội soi theo chỉ định để xác định nguyên nhân tại tử cung hoặc buồng trứng."
  type: investigation
  cpg-activity-type: imaging
  useContext: imaging

- id: investigateSTI
  description: "Lấy mẫu chẩn đoán bệnh lây truyền qua đường tình dục nếu nghi ngờ (NAAT, cấy)."
  type: investigation
  cpg-activity-type: laboratory
  useContext: STI

- id: orderLabTests
  description: "Yêu cầu Hb, Hct, công thức máu và xét nghiệm đông máu khi nghi mất máu."
  type: investigation
  cpg-activity-type: laboratory
  useContext: huyết học

- id: monitorAndPlan
  description: "Theo dõi biểu hiện lâm sàng và hẹn tái khám theo dõi nếu không nặng."
  type: follow-up
  cpg-activity-type: follow-up
  useContext: theo dõi

- id: referGynae
  description: "Chuyển tư vấn chuyên khoa sản phụ khoa nếu có dấu hiệu nghi ngờ tổn thương nghiêm trọng hoặc chảy máu tái diễn."
  type: referral
  cpg-activity-type: referral
  useContext: chuyên khoa

- id: conservativeManagement
  description: "Điều trị ngoại trú, bổ sung sắt nếu cần, hẹn tái khám; hướng dẫn theo dõi."
  type: management
  cpg-activity-type: outpatient-care
  useContext: theo dõi

## Ghi chú / TODO

- Generated from diagrams/vaginal_bleeding-diagram.png

- Bảng phân loại nguyên nhân chảy máu âm đạo:

| Loại nguyên nhân    | Đặc điểm / Ví dụ                                  |
|---------------------|---------------------------------------------------|
| Kinh nguyệt          | Chu kỳ bình thường, rong kinh                      |
| Sau sinh             | Tổn thương tầng sinh môn, sót nhau                  |
| Bệnh lý tử cung       | U xơ, polyp, ung thư                                |
| Rối loạn đông máu     | Hemophilia, dùng thuốc chống đông                   |
| Nhiễm trùng / STI     | Viêm cổ tử cung, nhiễm khuẩn                         |

