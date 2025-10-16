---
id: age-diagram
title: Hướng dẫn tổng quan theo độ tuổi
description: Quy trình đánh giá các vấn đề y tế phổ biến theo nhóm tuổi, giúp phân loại rủi ro và hướng chăm sóc phù hợp.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/age-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng để nhận diện yếu tố liên quan đến tuổi (trẻ em, người trưởng thành, cao tuổi) ảnh hưởng đến chẩn đoán, điều trị và phòng ngừa.

## Flow

1. stepId: identifyAgeGroup
   question: "Bệnh nhân thuộc nhóm tuổi nào? (trẻ em/ người lớn/ cao tuổi)"
   type: choice
   answers:
     - code: pediatric
       display: "Trẻ em"
       next: stepId=pediatricApproach
     - code: adult
       display: "Người lớn"
       next: stepId=adultApproach
     - code: elderly
       display: "Cao tuổi"
       next: stepId=geriatricApproach

2. stepId: pediatricApproach
   question: "Cân nhắc tiêm chủng, phát triển, cân nặng, các dấu cảnh báo (khó thở, bỏ bú)?"
   type: boolean
   next:
     true: action=urgentPediatricCare
     false: action=wellChildFollowup

3. stepId: adultApproach
   question: "Kiểm tra nguy cơ tim mạch, lối sống, khuyến cáo sàng lọc định kỳ?"
   type: boolean
   next:
     true: action=screeningAndPrevention
     false: action=riskModification

4. stepId: geriatricApproach
   question: "Đánh giá đa bệnh lý, thuốc nhiều, suy giảm chức năng, nguy cơ té ngã?"
   type: boolean
   next:
     true: action=comprehensiveGeriatricAssessment
     false: action=fallPreventionAdvice

5. stepId: medicationReview
   question: "Cần rà soát thuốc theo tuổi (dạng dùng, tương tác) không?"
   type: boolean
   next:
     true: action=performMedReview
     false: action=continuePlan

6. stepId: immunizationCheck
   question: "Kiểm tra tình trạng tiêm chủng phù hợp theo lứa tuổi không?"
   type: boolean
   next:
     true: action=updateImmunizations
     false: action=provideVaccineInfo

7. stepId: preventiveScreening
   question: "Cần sàng lọc ung thư/tiểu đường/huyết áp theo guideline không?"
   type: boolean
   next:
     true: action=orderScreeningTests
     false: action=education

8. stepId: functionalAssessment
   question: "Đánh giá chức năng (ADL/IADL) cho người cao tuổi cần không?"
   type: boolean
   next:
     true: action=referGeriatrics
     false: action=end

9. stepId: disposition
   question: "Cần can thiệp cấp cứu, theo dõi hay quản lý ngoại trú?"
   type: choice
   answers:
     - code: urgent
       display: "Cấp cứu"
       next: action=activateEmergency
     - code: outpatient
       display: "Ngoại trú"
       next: action=planOutpatientCare

10. stepId: followUp
    question: "Sắp xếp tái khám/giám sát theo lứa tuổi không?"
    type: boolean
    next:
      true: action=scheduleFollowup
      false: action=end

## Hành động

- id: urgentPediatricCare
  description: "Tham vấn nhi, ổn định đường thở/ dinh dưỡng, nhập viện nếu cần."
  type: intervention
  cpg-activity-type: acute-management
  useContext: pediatrics

- id: wellChildFollowup
  description: "Lên lịch khám theo mốc phát triển và tư vấn chăm sóc."
  type: action
  cpg-activity-type: preventive-care
  useContext: sức khoẻ trẻ em

- id: screeningAndPrevention
  description: "Áp dụng sàng lọc tim mạch, tiểu đường, cholesterol theo tuổi."
  type: action
  cpg-activity-type: screening
  useContext: phòng ngừa

- id: riskModification
  description: "Tư vấn thay đổi lối sống: dinh dưỡng, vận động, bỏ thuốc lá."
  type: action
  cpg-activity-type: lifestyle
  useContext: phòng ngừa

- id: comprehensiveGeriatricAssessment
  description: "Đánh giá đa chiều về chức năng, dinh dưỡng, tâm thần và môi trường."
  type: investigation
  cpg-activity-type: assessment
  useContext: lão khoa

- id: fallPreventionAdvice
  description: "Tư vấn dự phòng té ngã, môi trường an toàn, bài tập thăng bằng."
  type: action
  cpg-activity-type: preventive-care
  useContext: an toàn

- id: performMedReview
  description: "Rà soát đơn thuốc, loại bỏ thuốc không cần thiết, điều chỉnh liều theo tuổi."
  type: action
  cpg-activity-type: medication-review
  useContext: dược

- id: updateImmunizations
  description: "Cập nhật tiêm chủng theo phác đồ: MMR, influenza, pneumococcal, HPV."
  type: intervention
  cpg-activity-type: preventive-care
  useContext: tiêm chủng

- id: orderScreeningTests
  description: "Yêu cầu xét nghiệm sàng lọc: glucose, lipid, huyết áp, xét nghiệm liên quan."
  type: investigation
  cpg-activity-type: laboratory
  useContext: sàng lọc

- id: referGeriatrics
  description: "Tham vấn chuyên gia lão khoa khi cần tối ưu hóa chăm sóc."
  type: referral
  cpg-activity-type: referral
  useContext: lão khoa

- id: activateEmergency
  description: "Kích hoạt xử trí cấp cứu và chuyển viện nếu có dấu hiệu nguy kịch."
  type: intervention
  cpg-activity-type: emergency
  useContext: cấp cứu

- id: planOutpatientCare
  description: "Lập kế hoạch chăm sóc ngoại trú, hẹn tái khám, tư vấn."
  type: action
  cpg-activity-type: administrative
  useContext: ngoại trú

## Bảng phân loại theo tuổi

| Nhóm tuổi | Mối quan tâm chính |
|-----------|---------------------|
| Trẻ em    | Phát triển, tiêm chủng, dinh dưỡng |
| Người lớn | Sàng lọc tim mạch, tiểu đường |
| Cao tuổi  | Đa bệnh nền, sa sút chức năng, té ngã |

## Ghi chú

- Generated from diagrams/age-diagram.png
