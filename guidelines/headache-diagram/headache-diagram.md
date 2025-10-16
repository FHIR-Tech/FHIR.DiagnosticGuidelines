---
id: headache-diagram
title: Sơ đồ chẩn đoán và xử trí đau đầu
description: Quy trình có cấu trúc để đánh giá đau đầu cấp và mạn ở người lớn, bao gồm các dấu hiệu báo động, phân loại nguyên nhân, đề xuất điều trị cấp và dự phòng, cùng các bước theo dõi.
version: 1.0.1
date: 2025-10-16
authors:
  - name: AI Draft
  - name: Reviewer Needed
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/headache-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Hướng dẫn này áp dụng cho bệnh nhân trưởng thành đến khám vì đau đầu. Mục tiêu là:
- Nhận diện dấu hiệu báo động (red flags) cần can thiệp cấp cứu.
- Phân loại đau đầu (primary vs secondary).
- Đề xuất bước đánh giá, xét nghiệm, điều trị cấp và dự phòng.

## Quy trình (Flow)

1. stepId: headacheStart
   question: "Bệnh nhân có triệu chứng đau đầu chính không?"
   type: boolean
   next:
     true: stepId=redFlags
     false: action=exit-no-headache

2. stepId: redFlags
   question: "Có dấu hiệu báo động (khởi phát dữ dội, sốt, mất ý thức, liệt khu trú, thay đổi thị lực, co giật) không?"
   type: boolean
   next:
     true: stepId=urgentAssessment
     false: stepId=historyAndPattern

3. stepId: urgentAssessment
   question: "Bệnh nhân có cần can thiệp cấp cứu hay xét nghiệm khẩn (CT/MRI, LP) ngay không?"
   type: boolean
   next:
     true: action=manageAcuteNeurologicalCause
     false: stepId=historyAndPattern

4. stepId: historyAndPattern
   question: "Thu thập tiền sử: thời gian khởi phát, tính chất đau, vị trí, yếu tố kích hoạt, triệu chứng kèm theo (buồn nôn, ánh sáng, âm thanh)."
   type: info
   next:
     info: stepId=primaryVsSecondary

5. stepId: primaryVsSecondary
   question: "Triệu chứng gợi ý nguyên nhân chính (migraine, tension-type, cluster) hay nguyên nhân thứ phát?"
   type: choice
   answers:
     - code: primary
       display: "Nghi primary headache (migraine/tension/cluster)"
       next: stepId=managePrimary
     - code: secondary
       display: "Nghi secondary (khối, nhiễm trùng, chấn thương, tăng áp lực nội sọ)"
       next: stepId=investigateSecondary

6. stepId: managePrimary
   question: "Xác định subtype và lựa chọn chiến lược điều trị cấp và dự phòng"
   type: choice
   answers:
     - code: migraine
       display: "Migraine"
       next: action=manageMigraine
     - code: tension
       display: "Tension-type"
       next: action=manageTensionHeadache
     - code: cluster
       display: "Cluster"
       next: action=manageCluster
     - code: other
       display: "Khác (cervicogenic, medication-overuse)"
       next: action=considerOtherPrimary

7. stepId: investigateSecondary
   question: "Cần làm xét nghiệm hình ảnh hoặc xét nghiệm máu/CSF không?"
   type: choice
   answers:
     - code: imaging
       display: "Chụp CT/MRI"
       next: action=orderImaging
     - code: labs
       display: "Xét nghiệm máu, ESR/CRP, xét nghiệm miễn dịch"
       next: action=orderLabs
     - code: lp
       display: "Chọc dịch não tuỷ (LP) nếu nghi viêm/ xuất huyết tiềm ẩn"
       next: action=performLP

8. stepId: acuteVsPreventive
   question: "Bệnh nhân cần điều trị cấp tính hay dự phòng dựa trên tần suất và mức độ nặng?"
   type: choice
   answers:
     - code: acute
       display: "Điều trị cấp tính"
       next: action=acuteTreatmentOptions
     - code: preventive
       display: "Điều trị dự phòng"
       next: action=preventiveTreatmentOptions

9. stepId: monitor
   question: "Khuyến nghị ghi nhật ký đau đầu (headache diary) và theo dõi hiệu quả điều trị trong 1-3 tháng?"
   type: boolean
   next:
     true: action=useDiaryForManagement
     false: action=adviseStartDiary

10. stepId: followUp
    question: "Đã cải thiện sau can thiệp hay cần chuyển chuyên khoa?"
    type: boolean
    next:
      true: action=continueManagement
      false: action=referSpecialist

11. stepId: medicationOveruse
    question: "Có nguy cơ lạm dụng thuốc giảm đau (>=10-15 ngày/tháng) không?"
    type: boolean
    next:
      true: action=addressMedicationOveruse
      false: action=continueManagement

12. stepId: secondaryFollow
    question: "Sau điều tra hình ảnh/xét nghiệm, cần can thiệp phẫu thuật hay điều trị đặc hiệu không?"
    type: choice
    answers:
      - code: surgical
        display: "Cần can thiệp phẫu thuật"
        next: action=referNeurosurgery
      - code: medical
        display: "Điều trị nội khoa đặc hiệu"
        next: action=targetedMedicalTreatment

## Hành động (Actions)

- id: manageAcuteNeurologicalCause
  description: "Ổn định và quản lý nguyên nhân thần kinh cấp tính (đột quỵ, xuất huyết, viêm màng não): nhập viện, chụp ảnh, điều trị hỗ trợ."
  type: action
  cpg-activity-type: acute-management
  useContext: thần kinh, dấu hiệu báo động

- id: orderImaging
  description: "Yêu cầu chụp CT/MRI sọ não theo chỉ định để loại trừ nguyên nhân cấu trúc hoặc xuất huyết."
  type: investigation
  cpg-activity-type: imaging
  useContext: chẩn đoán hình ảnh

- id: orderLabs
  description: "Yêu cầu xét nghiệm máu cơ bản: CBC, điện giải, chức năng gan/thận, ESR/CRP, xét nghiệm miễn dịch nếu cần."
  type: investigation
  cpg-activity-type: laboratory
  useContext: xét nghiệm

- id: performLP
  description: "Thực hiện chọc dò dịch não tủy khi nghi viêm/ xuất huyết tiềm ẩn và kết quả hình ảnh không đủ rõ ràng."
  type: investigation
  cpg-activity-type: procedure
  useContext: chọc dịch não tuỷ

- id: manageMigraine
  description: "Điều trị migraine cấp tính và xem xét phòng ngừa: triptan khi phù hợp, NSAIDs, chống nôn, và đánh giá dự phòng khi tái phát."
  type: intervention
  cpg-activity-type: management
  useContext: migraine

- id: manageTensionHeadache
  description: "Quản lý đau đầu do căng thẳng: NSAIDs, vật lý trị liệu, kỹ thuật thư giãn, điều chỉnh hành vi."
  type: intervention
  cpg-activity-type: management
  useContext: tension-type

- id: manageCluster
  description: "Quản lý đau đầu cụm: oxy liệu pháp, sumatriptan tiêm, prophylaxis đặc hiệu."
  type: intervention
  cpg-activity-type: management
  useContext: cluster

- id: considerOtherPrimary
  description: "Xem xét các nguyên nhân đau đầu nguyên phát khác: cervicogenic, medication-overuse headache."
  type: investigation
  cpg-activity-type: differential-diagnosis
  useContext: nguyên nhân khác

- id: acuteTreatmentOptions
  description: "Các lựa chọn điều trị cấp tính: NSAIDs, paracetamol, triptan, antiemetic, steroid ngắn ngày trong một số trường hợp."
  type: intervention
  cpg-activity-type: acute-management
  useContext: điều trị cấp

- id: preventiveTreatmentOptions
  description: "Các lựa chọn điều trị phòng ngừa: beta-blocker, topiramate, amitriptyline, CGRP inhibitors nếu phù hợp."
  type: intervention
  cpg-activity-type: preventive-management
  useContext: điều trị dự phòng

- id: useDiaryForManagement
  description: "Khuyến khích sử dụng nhật ký đau đầu để theo dõi tần suất, yếu tố kích hoạt và hiệu quả điều trị."
  type: action
  cpg-activity-type: monitoring
  useContext: theo dõi

- id: adviseStartDiary
  description: "Hướng dẫn bệnh nhân bắt đầu ghi nhật ký đau đầu và theo dõi triệu chứng."
  type: action
  cpg-activity-type: patient-education
  useContext: giáo dục bệnh nhân

- id: addressMedicationOveruse
  description: "Xác định và điều chỉnh tình trạng lạm dụng thuốc giảm đau: giảm, thay đổi chiến lược điều trị, hỗ trợ theo dõi."
  type: intervention
  cpg-activity-type: medication-management
  useContext: medication-overuse

- id: referSpecialist
  description: "Tham vấn chuyên khoa (thần kinh, đau đầu) khi thất bại điều trị, chẩn đoán phức tạp hoặc cần can thiệp đặc hiệu."
  type: referral
  cpg-activity-type: referral
  useContext: tham vấn

- id: referNeurosurgery
  description: "Tham vấn phẫu thuật thần kinh khi có chỉ định phẫu thuật (u, chảy máu) theo kết quả hình ảnh."
  type: referral
  cpg-activity-type: referral
  useContext: phẫu thuật thần kinh

- id: targetedMedicalTreatment
  description: "Bắt đầu điều trị y tế đặc hiệu theo chẩn đoán (ví dụ: kháng sinh cho nhiễm trùng, điều trị nội khoa cho rối loạn nội tiết)."
  type: intervention
  cpg-activity-type: targeted-treatment
  useContext: điều trị đặc hiệu

## Bảng phân loại

| Nhóm nguyên nhân | Ví dụ / Đặc trưng |
|------------------|-------------------|
| Migraine         | Đau nửa đầu, buồn nôn, nhạy cảm ánh sáng/âm thanh |
| Tension-type     | Đau như dải băng, không nặng, liên quan stress |
| Cluster          | Đau quanh mắt, tái diễn theo chu kỳ, kèm rỉ nước mắt |
| Secondary        | Do u, xuất huyết, nhiễm trùng, tăng áp lực nội sọ |
| Cervicogenic     | Bắt nguồn từ cổ, thường kèm giới hạn vận động cổ |
| Medication-overuse| Do lạm dụng thuốc giảm đau (>=10-15 ngày/tháng) |

## Ghi chú / TODO

- Thêm mã ICD/SNOMED/LOINC cho các chẩn đoán và hành động.
- Cập nhật tác giả/phiên bản sau rà soát lâm sàng.
- Generated from diagrams/headache-diagram.png
