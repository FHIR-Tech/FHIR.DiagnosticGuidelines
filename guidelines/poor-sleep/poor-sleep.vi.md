---
id: poor-sleep
title: Đánh giá tình trạng ngủ kém / Mất ngủ
description: >-
  Luồng ra quyết định cho việc đánh giá bệnh nhân trình bày tình trạng ngủ kém hoặc mất ngủ. Trích xuất từ sơ đồ "poor_sleep".
version: 1.0.0
date: 2025-10-16
authors:
  - name: automated-converter
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/poor_sleep.png
translated_from:
  file: guidelines/poor-sleep/poor-sleep.md
  language: en
  detection_confidence: 0.99
translation_tool:
  name: "auto-translator"
  version: "v1"
translation_date: 2025-10-16T00:00:00Z
translation_checksum: TODO
---

Bối cảnh / Phạm vi:

Hướng dẫn này mô tả cách tiếp cận chẩn đoán bệnh nhân trình bày triệu chứng ngủ kém hoặc mất ngủ. Nó phân biệt các vấn đề ngủ ngắn hạn/chuyển tiếp với mất ngủ mạn tính, sàng lọc rối loạn tâm thần, sử dụng chất, các bệnh nội khoa góp phần, rối loạn giấc ngủ phổ biến (ngưng thở khi ngủ, RLS, PLMD) và rối loạn nhịp sinh học. Các khuyến nghị bao gồm biện pháp bảo tồn, chuyển tuyến, điều trị nguyên nhân, và giới thiệu chuyên khoa.

Flow (Luồng):

1. stepId: defineComplaint
   question: "Bệnh nhân có trình bày vấn đề ngủ kém không?"
   type: boolean
   next:
     true: stepId=assessDaytimeImpact
     false: action=none

2. stepId: assessDaytimeImpact
   question: "Đánh giá hậu quả ban ngày, yếu tố kích hoạt và vệ sinh giấc ngủ"
   type: collect-information
   next:
     continue: stepId=defineDuration

3. stepId: defineDuration
   question: "Triệu chứng kéo dài bao lâu?"
   type: choice
   answers:
     - code: transient
       display: "Ngắn hạn (< 3 tuần)"
       next: action=considerShortSleeper
     - code: chronic
       display: "Mạn tính (> 3 tuần)"
       next: stepId=screenMentalHealth

4. stepId: considerShortSleeper
   action: consider-short-sleeper
   description: "Cân nhắc người ngủ ngắn / biến thể bình thường; xem xét stress cấp tính, bệnh cấp, lệch múi giờ, tác dụng thuốc/chất"
   next:
     done: action=conservativeAdvice

5. stepId: screenMentalHealth
   question: "Có bằng chứng về rối loạn sức khỏe tâm thần không?"
   type: boolean
   next:
     true: action=considerInsomniaDueToMentalHealth
     false: stepId=reviewSubstanceUse

6. stepId: considerInsomniaDueToMentalHealth
   action: consider-insomnia-mental-health
   description: "Cân nhắc mất ngủ do rối loạn tâm thần; đánh giá và điều trị, cân nhắc chuyển tuyến"
   next:
     done: action=referMentalHealth

7. stepId: reviewSubstanceUse
   question: "Có bằng chứng sử dụng chất (thuốc kê đơn, OTC, caffein, nicotine, rượu, chất bất hợp pháp) góp phần không?"
   type: boolean
   next:
     true: action=considerInsomniaSubstance
     false: stepId=reviewMedicalDisorders

8. stepId: considerInsomniaSubstance
   action: consider-insomnia-substance
   description: "Cân nhắc mất ngủ do sử dụng chất hoặc cai; thay đổi/dừng thuốc, đánh giá lạm dụng/cai, cân nhắc chuyển tuyến"
   next:
     done: action=manageSubstance

9. stepId: reviewMedicalDisorders
   question: "Có bằng chứng các bệnh nội khoa/thần kinh góp phần? (ví dụ CHF, CAD, COPD, asthma, PUD, GERD, thận hoặc bệnh thần kinh)"
   type: boolean
   next:
     true: action=considerInsomniaMedical
     false: stepId=reviewSleepDisorders

10. stepId: considerInsomniaMedical
    action: consider-insomnia-medical
    description: "Cân nhắc mất ngủ do bệnh nội/thần kinh; đánh giá và điều trị bệnh nền. Cân nhắc chuyển tuyến hoặc khẩn cấp nếu có triệu chứng báo động"
    next:
      done: action=manageMedical

11. stepId: reviewSleepDisorders
    question: "Có bằng chứng rối loạn giấc ngủ phổ biến? (ngưng thở khi ngủ, RLS, PLMD)"
    type: boolean
    next:
      true: action=considerInsomniaSleepDisorder
      false: stepId=reviewCircadian

12. stepId: considerInsomniaSleepDisorder
    action: consider-insomnia-sleep-disorder
    description: "Cân nhắc mất ngủ do rối loạn giấc ngủ; chuyển tuyến chuyên khoa giấc ngủ để xác nhận ngưng thở khi ngủ, PLMD, RLS. Điều trị RLS nếu có."
    next:
      done: action=referSleepSpecialist

13. stepId: reviewCircadian
    question: "Có bằng chứng rối loạn nhịp sinh học không?"
    type: boolean
    next:
      true: action=considerAdvancedOrDelayedSleepPhase
      false: stepId=noSecondaryCause

14. stepId: considerAdvancedOrDelayedSleepPhase
    action: consider-advanced-delayed-sleep-phase
    description: "Cân nhắc rối loạn pha ngủ tiến hoặc trễ; chuyển tuyến chuyên khoa giấc ngủ"
    next:
      done: action=referSleepSpecialist

15. stepId: noSecondaryCause
    question: "Không có bằng chứng nguyên nhân thứ phát?"
    type: boolean
    next:
      true: action=considerIdiopathicInsomnia
      false: action=reviewFurther

16. stepId: considerIdiopathicInsomnia
    action: consider-idiopathic-insomnia
    description: "Cân nhắc mất ngủ vô căn, mất ngủ tâm sinh lý, hoặc sai nhận thức trạng thái ngủ. Cung cấp can thiệp hành vi và cân nhắc CBT-i hoặc chuyển tuyến chuyên gia khi phù hợp."
    next:
      done: action=conservativeAdvice

Actions (Hành động):

- actionId: conservativeAdvice
  title: "Biện pháp bảo tồn"
  description: "Tư vấn vệ sinh giấc ngủ, đánh giá yếu tố kích hoạt, cân nhắc thuốc ngủ ngắn hạn nếu chỉ định, và xem xét thói quen ban ngày."
  resourceKind: ActivityDefinition

- actionId: referSleepSpecialist
  title: "Chuyển tới chuyên gia giấc ngủ"
  description: "Chuyển tới phòng khám giấc ngủ để đánh giá và quản lý rối loạn giấc ngủ nghi ngờ."
  resourceKind: ReferralRequest

- actionId: referMentalHealth
  title: "Chuyển tới dịch vụ sức khỏe tâm thần"
  description: "Chuyển để đánh giá và điều trị rối loạn tâm thần khi cần."
  resourceKind: ReferralRequest

- actionId: manageSubstance
  title: "Quản lý nguyên nhân do chất"
  description: "Thay đổi hoặc dừng thuốc, đánh giá và điều trị lạm dụng/cai, cân nhắc chuyển tuyến."
  resourceKind: ActivityDefinition

- actionId: manageMedical
  title: "Quản lý bệnh nền"
  description: "Đánh giá và điều trị bệnh nội/thần kinh nền; chuyển tuyến khẩn nếu triệu chứng báo động."
  resourceKind: ActivityDefinition

*** End of translation file
