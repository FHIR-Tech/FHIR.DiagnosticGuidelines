---
id: breast_mass-diagram
title: Hướng dẫn khối vú
description: Quy trình đánh giá khối vú ở nữ và nam, phân loại nguy cơ, chỉ định chẩn đoán hình ảnh và sinh thiết.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/breast_mass-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho bệnh nhân phát hiện khối vú; mục tiêu phân loại lành/ ác tính và quyết định chẩn đoán hình ảnh (US, mammography) và sinh thiết.

## Flow

1. stepId: immediateConcern
   question: "Có dấu hiệu đỏ nặng, chảy mủ, loét hoặc sờ thấy hạch cổ nách to không?"
   type: boolean
   next:
     true: action=urgentBreastUnitReferral
     false: stepId=historyExamination

2. stepId: historyExamination
   question: "Tiền sử khối, tuổi, tiền căn gia đình ung thư vú, thay đổi da/ núm vú?"
   type: info
   next:
     info: stepId=ageAndRisk

3. stepId: ageAndRisk
   question: "Bệnh nhân thuộc độ tuổi sàng lọc (>40) hoặc có nguy cơ cao không?"
   type: boolean
   next:
     true: action=orderMammography
     false: action=orderUltrasound

4. stepId: imagingResults
   question: "Hình ảnh gợi ý tổn thương đáng ngờ (BIRADS 4–5)?"
   type: boolean
   next:
     true: action=arrangeBiopsy
     false: action=monitorOrRefer

5. stepId: needleBiopsy
   question: "Sinh thiết kim hoặc core biopsy được thực hiện và giải phẫu bệnh cần?"
   type: boolean
   next:
     true: action=interpretPathology
     false: action=discussOptions

6. stepId: pathologyResults
   question: "Pathology dương tính ác tính?"
   type: boolean
   next:
     true: action=referOncologyAndSurgery
     false: action=followUp

7. stepId: maleBreastMass
   question: "Trường hợp nam giới cần đánh giá đặc biệt (gynecomastia vs malignancy)?"
   type: boolean
   next:
     true: action=targetedAssessment
     false: action=end

8. stepId: adjunctTests
   question: "Cần thêm xét nghiệm (hormone, genetic testing) không?"
   type: boolean
   next:
     true: action=orderGeneticTests
     false: action=end

9. stepId: psychoSupport
   question: "Cần hỗ trợ tâm lý/ tư vấn bệnh nhân và gia đình không?"
   type: boolean
   next:
     true: action=provideSupport
     false: action=end

10. stepId: documentation
    question: "Ghi chép, thông báo kết quả và lập kế hoạch tiếp theo?"
    type: boolean
    next:
      true: action=documentAndPlan
      false: action=end

## Hành động

- id: urgentBreastUnitReferral
  description: "Tham vấn nhanh đơn vị ung bướu vú nếu có dấu hiệu nghiêm trọng."
  type: referral
  cpg-activity-type: emergency
  useContext: ung bướu vú

- id: orderMammography
  description: "Yêu cầu chụp nhũ ảnh theo chuẩn để đánh giá tổn thương ở bệnh nhân đủ tuổi."
  type: investigation
  cpg-activity-type: imaging
  useContext: mammography

- id: orderUltrasound
  description: "Siêu âm vú cho phụ nữ trẻ hoặc đánh giá khối dạng đặc/ nang."
  type: investigation
  cpg-activity-type: imaging
  useContext: ultrasound

- id: arrangeBiopsy
  description: "Sắp xếp sinh thiết kim/core biopsy để chẩn đoán mô học."
  type: intervention
  cpg-activity-type: diagnostic-procedure
  useContext: sinh thiết

- id: interpretPathology
  description: "Nhận kết quả giải phẫu bệnh và thảo luận hướng điều trị."
  type: action
  cpg-activity-type: diagnostic
  useContext: pathology

- id: referOncologyAndSurgery
  description: "Tham vấn ung bướu và phẫu thuật khi chẩn đoán ác tính."
  type: referral
  cpg-activity-type: referral
  useContext: chuyên khoa

- id: followUp
  description: "Theo dõi nếu là lành tính, hẹn tái khám hoặc lâm sàng theo guideline."
  type: action
  cpg-activity-type: monitoring
  useContext: theo dõi

- id: targetAssessment
  description: "Đánh giá nam giới: loại trừ gynecomastia, hội chứng nội tiết và nghi ngờ ác tính."
  type: investigation
  cpg-activity-type: diagnostic
  useContext: male-breast

- id: orderGeneticTests
  description: "Xem xét xét nghiệm BRCA hoặc tư vấn di truyền khi phù hợp."
  type: investigation
  cpg-activity-type: genetic-testing
  useContext: genetics

- id: provideSupport
  description: "Hỗ trợ tâm lý, tư vấn và nguồn lực bệnh nhân khi cần."
  type: action
  cpg-activity-type: patient-education
  useContext: hỗ trợ

- id: documentAndPlan
  description: "Ghi chép kết quả và lập kế hoạch quản lý tiếp theo."
  type: action
  cpg-activity-type: administrative
  useContext: hồ sơ

- id: discussOptions
  description: "Thảo luận các lựa chọn theo kết quả hình ảnh và lâm sàng."
  type: action
  cpg-activity-type: shared-decision-making
  useContext: tư vấn

## Bảng phân loại nguyên nhân khối vú

| Loại | Ví dụ |
|------|------|
| Lành tính | Nang, u tuyến |
| Ác tính | Carcinoma |
| Thay đổi hormon | Gynecomastia |

## Ghi chú

- Generated from diagrams/breast_mass-diagram.png
