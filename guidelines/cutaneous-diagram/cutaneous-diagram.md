---
id: cutaneous-diagram
title: Hướng dẫn các bệnh da (cutaneous)
description: Quy trình đánh giá tổn thương da cấp và mạn: phát ban, ban đỏ, mụn nước, nhiễm trùng, dị ứng và hướng xử trí ban đầu.
version: 1.0.0
date: 2025-10-16
authors:
  - name: AI Draft
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/cutaneous-diagram.png
source-checksum: TODO
---

## Bối cảnh / Phạm vi

Áp dụng cho bệnh nhân có tổn thương da; mục tiêu phân loại viêm, nhiễm trùng, dị ứng, tự miễn và đề xuất điều trị ban đầu hoặc tham vấn da liễu.

## Flow

1. stepId: severeReaction
   question: "Có dấu hiệu phản vệ, khó thở, phù mặt, loạn ý thức không?"
   type: boolean
   next:
     true: action=manageAnaphylaxis
     false: stepId=onsetAndDistribution

2. stepId: onsetAndDistribution
   question: "Tổn thương khởi phát đột ngột hay mạn; phân bố khu trú hay toàn thân?"
   type: choice
   answers:
     - code: local
       display: "Khu trú"
       next: stepId=considerInfectionOrContact
     - code: generalized
       display: "Toàn thân"
       next: stepId=considerSystemicCauses

3. stepId: considerInfectionOrContact
   question: "Có bội nhiễm, mủ, yếu tố tiếp xúc (hoa quả, kim loại) hay chấn thương?"
   type: boolean
   next:
     true: action=manageLocalInfectionOrContactDermatitis
     false: action=topicalManagement

4. stepId: considerSystemicCauses
   question: "Liệu là phản ứng thuốc, nhiễm virus (measles), hay bệnh tự miễn?"
   type: boolean
   next:
     true: action=orderSystemicInvestigations
     false: action=conservativeCare

5. stepId: biopsyIndication
   question: "Cần sinh thiết khi nghi ung thư da hoặc bệnh mạn không giải thích được không?"
   type: boolean
   next:
     true: action=arrangeSkinBiopsy
     false: action=monitor

6. stepId: topicalOrSystemicTherapy
   question: "Cân nhắc corticoid tại chỗ, kháng sinh tại chỗ/ toàn thân hoặc thuốc ức chế miễn dịch?"
   type: choice
   answers:
     - code: topical
       display: "Corticoid tại chỗ, chăm sóc da"
       next: action=prescribeTopicalTherapy
     - code: systemic
       display: "Kháng sinh/ corticoid toàn thân"
       next: action=prescribeSystemicTherapy

7. stepId: allergyTesting
   question: "Cần test dị ứng (patch test) hay test IgE không?"
   type: boolean
   next:
     true: action=arrangeAllergyTesting
     false: action=education

8. stepId: referral
   question: "Cần tham vấn da liễu khi không đáp ứng hoặc nghi ngờ bệnh hiếm không?"
   type: boolean
   next:
     true: action=referDermatology
     false: action=continueManagement

9. stepId: disposition
   question: "Cần nhập viện hay quản lý ngoại trú?"
   type: choice
   answers:
     - code: admit
       display: "Nhập viện"
       next: action=admitForIVTherapy
     - code: outpatient
       display: "Ngoại trú"
       next: action=dischargeWithTopicalPlan

10. stepId: followUp
    question: "Sắp xếp theo dõi và đánh giá hiệu quả điều trị không?"
    type: boolean
    next:
      true: action=scheduleFollowup
      false: action=end

## Hành động

- id: manageAnaphylaxis
  description: "Tiêm adrenaline theo algorithm, oxy, đặt đường truyền và chuyển cấp cứu."
  type: intervention
  cpg-activity-type: emergency
  useContext: phản vệ

- id: manageLocalInfectionOrContactDermatitis
  description: "Làm sạch, kháng sinh/ steroid tại chỗ, tránh tác nhân tiếp xúc."
  type: intervention
  cpg-activity-type: management
  useContext: nhiễm trùng/ dị ứng

- id: prescribeTopicalTherapy
  description: "Kê corticoid tại chỗ, kem dưỡng ẩm và hướng dẫn chăm sóc da."
  type: intervention
  cpg-activity-type: medication
  useContext: bôi tại chỗ

- id: prescribeSystemicTherapy
  description: "Kê kháng sinh/ corticosteroid toàn thân hoặc ức chế miễn dịch khi cần."
  type: intervention
  cpg-activity-type: medication
  useContext: toàn thân

- id: arrangeSkinBiopsy
  description: "Sắp xếp sinh thiết da khi nghi ngờ ác tính hoặc bệnh đặc hiệu."
  type: investigation
  cpg-activity-type: diagnostic-procedure
  useContext: pathology

- id: arrangeAllergyTesting
  description: "Sắp xếp patch test hoặc test dị ứng khi nghi ngờ dị ứng tiếp xúc."
  type: investigation
  cpg-activity-type: diagnostic
  useContext: dị ứng

- id: referDermatology
  description: "Giới thiệu chuyên khoa da liễu cho chẩn đoán và điều trị chuyên sâu."
  type: referral
  cpg-activity-type: referral
  useContext: chuyên khoa

- id: admitForIVTherapy
  description: "Nhập viện để truyền kháng sinh IV hoặc theo dõi bệnh nhân nặng."
  type: intervention
  cpg-activity-type: inpatient-care
  useContext: nhập viện

- id: dischargeWithTopicalPlan
  description: "Xuất viện với kế hoạch điều trị bôi tại nhà và theo dõi."
  type: action
  cpg-activity-type: outpatient-care
  useContext: ngoại trú

- id: education
  description: "Giáo dục về tránh tác nhân, chăm sóc da và sử dụng thuốc đúng cách."
  type: action
  cpg-activity-type: patient-education
  useContext: tự chăm sóc

- id: continueManagement
  description: "Tiếp tục điều trị và đánh giá đáp ứng trước khi chuyển chuyên khoa."
  type: action
  cpg-activity-type: monitoring
  useContext: theo dõi

- id: scheduleFollowup
  description: "Sắp xếp tái khám để đánh giá đáp ứng và điều chỉnh kế hoạch."
  type: action
  cpg-activity-type: administrative
  useContext: follow-up

## Bảng phân loại tổn thương da

| Loại | Ví dụ |
|------|------|
| Dị ứng | Viêm da tiếp xúc, urticaria |
| Nhiễm trùng | Cellulitis, impetigo |
| Tự miễn | Psoriasis, lupus |

## Ghi chú

- Generated from diagrams/cutaneous-diagram.png
