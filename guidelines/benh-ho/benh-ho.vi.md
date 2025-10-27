---
id: benh-ho
title: Đánh giá ho (Người lớn ngoại trú)
description: Lộ trình chẩn đoán có cấu trúc để đánh giá triệu chứng ho trong bối cảnh ngoại trú, ưu tiên sàng lọc dấu hiệu báo động, phân loại theo thời gian và các căn nguyên thường gặp (UACS, hen, GERD, ho do ức chế men chuyển, viêm phổi, giãn phế quản).
version: 1.0.0
date: 2025-10-27
authors:
  - name: Bản dịch tự động theo rule v2.6.4
fhirVersion: "4.0.1"

# Language / translation metadata
language: vi
translated_from:
  file: diagrams/benh-ho.txt
  language: en
  detection_confidence: 0.99
translation_tool:
  name: "copilot-translation"
  version: "v1"
translation_date: 2025-10-27T00:00:00Z
translation_checksum: ""
translation_notes: |
  - preserve_codes: true
  - human_review_required: false
  - flagged_items: 0
---

## Context / Scope
Ho là một triệu chứng phổ biến với chẩn đoán phân biệt rộng. Hướng dẫn này mã hóa cách tiếp cận dựa trên bằng chứng, theo mốc thời gian, bắt đầu bằng sàng lọc dấu hiệu báo động, sau đó đặc trưng hóa ho và định hướng tới các căn nguyên thường gặp trong ngoại trú. Không thay thế cho phán đoán lâm sàng.

## Flow

1. stepId: hemoptysis
   question: "Bạn có ho ra máu (ho ra máu - hemoptysis) không?"
   type: boolean
   next:
     true: action=urgent-evaluation
     false: stepId=fever-purulent-sputum

2. stepId: fever-purulent-sputum
   question: "Sốt kèm đờm mủ?"
   type: boolean
   notes: "Khi có, cân nhắc viêm phổi hoặc áp-xe phổi; đôi khi là viêm xoang/viêm phế quản cấp."
   next:
     true: action=consider-pneumonia-eval
     false: stepId=wheezing-sob

3. stepId: wheezing-sob
   question: "Khò khè hoặc khó thở?"
   type: boolean
   notes: "Gợi ý hen, COPD hoặc suy tim khi có."
   next:
     true: action=consider-airflow-obstruction
     false: stepId=chest-pain

4. stepId: chest-pain
   question: "Có đau ngực không?"
   type: boolean
   notes: "Cân nhắc thuyên tắc phổi (PE) hoặc hội chứng vành cấp (ACS) nếu đau ngực đáng ngờ."
   next:
     true: action=urgent-evaluation
     false: stepId=weight-loss

5. stepId: weight-loss
   question: "Sụt cân không chủ ý?"
   type: boolean
   notes: "Khi có, cân nhắc ác tính hoặc lao."
   next:
     true: action=consider-serious-underlying
     false: stepId=orthopnea-pnd-edema

6. stepId: orthopnea-pnd-edema
   question: "Có khó thở khi nằm (orthopnea), cơn khó thở kịch phát về đêm (PND) hoặc phù ngoại biên?"
   type: boolean
   notes: "Gợi ý suy tim; cũng cân nhắc OSA hoặc GERD theo bối cảnh."
   next:
     true: action=consider-chf-eval
     false: stepId=cough-duration

7. stepId: cough-duration
   question: "Thời gian ho"
   type: choice
   answers:
     - code: lt3w
       display: "< 3 tuần (Cấp)"
     - code: w3to8
       display: "3–8 tuần (Bán cấp)"
     - code: gt8w
       display: "> 8 tuần (Mạn)"
   next:
     lt3w: stepId=characterize-cough
     w3to8: stepId=characterize-cough
     gt8w: stepId=characterize-cough

8. stepId: characterize-cough
   question: "Đặc trưng ho (thu thập các đặc điểm chính)"
   type: group
   notes: "Thu thập khởi phát, tần suất, thời điểm, tính chất (khô vs có đờm), triệu chứng liên quan và yếu tố khởi phát."
   next:
     else: stepId=etiology-screen

9. stepId: productive-cough
   question: "Ho có đờm (có khạc ra đờm) không?"
   type: boolean
   next:
     true: stepId=sputum-qualities
     false: stepId=mucus-postnasal-drip

10. stepId: sputum-qualities
    question: "Nếu có đờm: đờm có mủ hoặc mùi hôi không?"
    type: boolean
    notes: "Đờm mủ/hôi gợi ý giãn phế quản, áp-xe hoặc viêm phổi."
    next:
      true: action=consider-bronchiectasis-workup
      false: stepId=mucus-postnasal-drip

11. stepId: mucus-postnasal-drip
    question: "Có cảm giác nhầy chảy sau họng (postnasal drip) không?"
    type: boolean
    next:
      true: action=propose-uacs
      false: stepId=wheeze-exertion

12. stepId: wheeze-exertion
    question: "Khò khè hoặc tức ngực khi gắng sức?"
    type: boolean
    next:
      true: action=propose-asthma
      false: stepId=heartburn-regurgitation

13. stepId: heartburn-regurgitation
    question: "Ợ nóng hoặc trào ngược?"
    type: boolean
    next:
      true: action=propose-gerd
      false: stepId=post-viral-illness

14. stepId: post-viral-illness
    question: "Ho bắt đầu sau đợt nhiễm virus?"
    type: boolean
    next:
      true: action=consider-postinfectious
      false: stepId=ace-inhibitor-use

15. stepId: ace-inhibitor-use
    question: "Bệnh nhân có dùng thuốc ức chế men chuyển (ACE inhibitor) không?"
    type: boolean
    next:
      true: action=propose-ace-cough
      false: stepId=night-worse-lying-down

16. stepId: night-worse-lying-down
    question: "Ho nặng hơn về đêm hoặc khi nằm?"
    type: boolean
    notes: "Gợi ý GERD, UACS hoặc suy tim tùy bối cảnh."
    next:
      true: stepId=etiology-screen
      false: stepId=etiology-screen

17. stepId: etiology-screen
    question: "Tổng hợp căn nguyên khả dĩ dựa trên câu trả lời đã thu thập"
    type: group
    next:
      any:
        - mucus-postnasal-drip=true
      then: action=propose-uacs
      else: stepId=etiology-screen-2

18. stepId: etiology-screen-2
    question: "Tổng hợp căn nguyên (phần 2)"
    type: group
    next:
      any:
        - wheeze-exertion=true
      then: action=propose-asthma
      else: stepId=etiology-screen-3

19. stepId: etiology-screen-3
    question: "Tổng hợp căn nguyên (phần 3)"
    type: group
    next:
      any:
        - heartburn-regurgitation=true
        - night-worse-lying-down=true
      then: action=propose-gerd
      else: stepId=etiology-screen-4

20. stepId: etiology-screen-4
    question: "Tổng hợp căn nguyên (phần 4)"
    type: group
    next:
      any:
        - sputum-qualities=true
      then: action=consider-bronchiectasis-workup
      else: stepId=end

21. stepId: end
    action: conclude-evaluation
    type: group
    notes: "Kết thúc lộ trình nếu chưa xác định rõ căn nguyên; cân nhắc chẩn đoán hình ảnh hoặc chuyển tuyến tùy lâm sàng."
    next: end

## Actions

- actionId: urgent-evaluation
  description: "Đánh giá khẩn cấp cho các nguyên nhân nghiêm trọng (ví dụ: PE, ACS, ho ra máu ồ ạt, viêm phổi nặng)."
  kind: Task

- actionId: consider-pneumonia-eval
  description: "Đánh giá viêm phổi hoặc áp-xe phổi (dấu hiệu sinh tồn, khám, cân nhắc chụp X-quang ngực)."
  kind: ServiceRequest

- actionId: consider-airflow-obstruction
  description: "Đánh giá khả năng hen/COPD/suy tim; cân nhắc thử giãn phế quản và đánh giá thêm."
  kind: Task

- actionId: consider-serious-underlying
  description: "Cân nhắc ác tính, lao hoặc tình trạng nghiêm trọng khác; sắp xếp chẩn đoán phù hợp."
  kind: Task

- actionId: consider-chf-eval
  description: "Đánh giá khả năng suy tim khi có orthopnea/PND/phù."
  kind: ServiceRequest

- actionId: consider-bronchiectasis-workup
  description: "Nếu đờm mủ/hôi, cân nhắc đánh giá giãn phế quản và xét nghiệm đờm."
  kind: ServiceRequest

- actionId: propose-uacs
  description: "Đề xuất chẩn đoán: Hội chứng ho đường thở trên (UACS)."
  kind: ServiceRequest

- actionId: propose-asthma
  description: "Đề xuất chẩn đoán: Hen (bao gồm thể ho)."
  kind: ServiceRequest

- actionId: propose-gerd
  description: "Đề xuất chẩn đoán: Bệnh trào ngược dạ dày-thực quản (GERD)."
  kind: ServiceRequest

- actionId: consider-postinfectious
  description: "Cân nhắc ho sau nhiễm virus (giai đoạn bán cấp)."
  kind: Task

- actionId: propose-ace-cough
  description: "Đề xuất ho do thuốc ức chế men chuyển; cân nhắc xem xét/thay đổi thuốc."
  kind: Task

- actionId: conclude-evaluation
  description: "Kết thúc đánh giá; nếu kéo dài không rõ nguyên nhân, cân nhắc chẩn đoán hình ảnh hoặc chuyển tuyến."
  kind: Task

## Notes / TODO
- Mã chuẩn (ICD-10/LOINC/SNOMED): TODO.
- Các ngưỡng định lượng chưa đưa ra; sẽ bổ sung đơn vị nếu xuất hiện trong nguồn.
- Bản dịch chỉ áp dụng cho phần hiển thị; các identifier như stepId, linkId, actionId giữ nguyên.

Generated from diagrams/benh-ho.txt
