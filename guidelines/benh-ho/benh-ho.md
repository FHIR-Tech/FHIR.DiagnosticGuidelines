---
id: benh-ho
title: Evaluation of Cough (Adult Ambulatory)
description: Structured diagnostic pathway for evaluating cough in ambulatory care, focusing on alarm features, duration-based classification, and common etiologies (UACS, asthma, GERD, ACE inhibitor cough, pneumonia, bronchiectasis).
version: 1.0.0
date: 2025-10-27
authors:
  - name: Auto-generated via rule v2.6.4
fhirVersion: "4.0.1"
source-type: text
source-file: diagrams/benh-ho.txt
clinical-risk: medium
---

## Context / Scope
Cough is a ubiquitous symptom with a broad differential. This guideline encodes an evidence-based, duration-anchored approach that first screens for alarm features, then characterizes cough and directs attention to the most common etiologies in ambulatory settings. It does not replace clinical judgment.

## Flow

1. stepId: hemoptysis
   question: "Have you coughed up any blood (hemoptysis)?"
   type: boolean
   next:
     true: action=urgent-evaluation
     false: stepId=fever-purulent-sputum

2. stepId: fever-purulent-sputum
   question: "Fever with purulent sputum?"
   type: boolean
   notes: "Consider pneumonia or lung abscess when true; could be acute sinusitis/bronchitis in some cases."
   next:
     true: action=consider-pneumonia-eval
     false: stepId=wheezing-sob

3. stepId: wheezing-sob
   question: "Wheezing or shortness of breath?"
   type: boolean
   notes: "Consider asthma, COPD, or CHF when true."
   next:
     true: action=consider-airflow-obstruction
     false: stepId=chest-pain

4. stepId: chest-pain
   question: "Chest pain present?"
   type: boolean
   notes: "Consider PE or ACS if concerning chest pain."
   next:
     true: action=urgent-evaluation
     false: stepId=weight-loss

5. stepId: weight-loss
   question: "Unintentional weight loss?"
   type: boolean
   notes: "Consider malignancy or TB when true."
   next:
     true: action=consider-serious-underlying
     false: stepId=orthopnea-pnd-edema

6. stepId: orthopnea-pnd-edema
   question: "Orthopnea, PND, or peripheral edema present?"
   type: boolean
   notes: "Suggests CHF; also consider OSA or GERD in different contexts."
   next:
     true: action=consider-chf-eval
     false: stepId=cough-duration

7. stepId: cough-duration
   question: "Duration of cough"
   type: choice
   answers:
     - code: lt3w
       display: "< 3 weeks (Acute)"
     - code: w3to8
       display: "3–8 weeks (Subacute)"
     - code: gt8w
       display: "> 8 weeks (Chronic)"
   next:
     lt3w: stepId=characterize-cough
     w3to8: stepId=characterize-cough
     gt8w: stepId=characterize-cough

8. stepId: characterize-cough
   question: "Characterize the cough (collect key features)"
   type: group
   notes: "Collect onset, frequency, timing, quality (dry vs productive), associated symptoms, and triggers."
   next:
     else: stepId=etiology-screen

9. stepId: productive-cough
   question: "Is the cough productive (brings up sputum)?"
   type: boolean
   next:
     true: stepId=sputum-qualities
     false: stepId=mucus-postnasal-drip

10. stepId: sputum-qualities
    question: "If productive: is sputum purulent or foul-smelling?"
    type: boolean
    notes: "Purulent/foul suggests bronchiectasis, abscess, or pneumonia."
    next:
      true: action=consider-bronchiectasis-workup
      false: stepId=mucus-postnasal-drip

11. stepId: mucus-postnasal-drip
    question: "Does mucus drip in the back of the throat (postnasal drip)?"
    type: boolean
    next:
      true: action=propose-uacs
      false: stepId=wheeze-exertion

12. stepId: wheeze-exertion
    question: "Wheezing or chest tightness with exertion?"
    type: boolean
    next:
      true: action=propose-asthma
      false: stepId=heartburn-regurgitation

13. stepId: heartburn-regurgitation
    question: "Heartburn or regurgitation symptoms?"
    type: boolean
    next:
      true: action=propose-gerd
      false: stepId=post-viral-illness

14. stepId: post-viral-illness
    question: "Did the cough begin after a viral illness?"
    type: boolean
    next:
      true: action=consider-postinfectious
      false: stepId=ace-inhibitor-use

15. stepId: ace-inhibitor-use
    question: "Is the patient taking an ACE inhibitor?"
    type: boolean
    next:
      true: action=propose-ace-cough
      false: stepId=night-worse-lying-down

16. stepId: night-worse-lying-down
    question: "Is the cough worse at night or when lying down?"
    type: boolean
    notes: "Suggests GERD, UACS, or CHF depending on context."
    next:
      true: stepId=etiology-screen
      false: stepId=etiology-screen

17. stepId: etiology-screen
    question: "Synthesize likely etiology based on collected answers"
    type: group
    next:
      any:
        - mucus-postnasal-drip=true
      then: action=propose-uacs
      else: stepId=etiology-screen-2

18. stepId: etiology-screen-2
    question: "Synthesize likely etiology (part 2)"
    type: group
    next:
      any:
        - wheeze-exertion=true
      then: action=propose-asthma
      else: stepId=etiology-screen-3

19. stepId: etiology-screen-3
    question: "Synthesize likely etiology (part 3)"
    type: group
    next:
      any:
        - heartburn-regurgitation=true
        - night-worse-lying-down=true
      then: action=propose-gerd
      else: stepId=etiology-screen-4

20. stepId: etiology-screen-4
    question: "Synthesize likely etiology (part 4)"
    type: group
    next:
      any:
        - sputum-qualities=true
      then: action=consider-bronchiectasis-workup
      else: stepId=end

21. stepId: end
    action: conclude-evaluation
    type: group
    notes: "End of pathway if no clear etiology identified; consider imaging or specialist referral based on clinician judgment."
    next: end

## Actions

- actionId: urgent-evaluation
  description: "Urgent evaluation for serious causes (e.g., PE, ACS, massive hemoptysis, severe pneumonia)."
  kind: Task

- actionId: consider-pneumonia-eval
  description: "Evaluate for pneumonia or lung abscess (vitals, exam, consider chest imaging)."
  kind: ServiceRequest

- actionId: consider-airflow-obstruction
  description: "Assess for asthma/COPD/CHF exacerbation; consider bronchodilator trial and further evaluation."
  kind: Task

- actionId: consider-serious-underlying
  description: "Consider malignancy, TB, or other serious conditions; arrange appropriate workup."
  kind: Task

- actionId: consider-chf-eval
  description: "Evaluate for congestive heart failure if orthopnea/PND/edema present."
  kind: ServiceRequest

- actionId: consider-bronchiectasis-workup
  description: "If sputum is purulent/foul-smelling, consider bronchiectasis workup and sputum studies."
  kind: ServiceRequest

- actionId: propose-uacs
  description: "Propose diagnosis: Upper Airway Cough Syndrome (UACS)."
  kind: ServiceRequest

- actionId: propose-asthma
  description: "Propose diagnosis: Asthma (including cough-variant)."
  kind: ServiceRequest

- actionId: propose-gerd
  description: "Propose diagnosis: Gastroesophageal Reflux Disease (GERD)."
  kind: ServiceRequest

- actionId: consider-postinfectious
  description: "Consider postinfectious cough in subacute phase post-viral illness."
  kind: Task

- actionId: propose-ace-cough
  description: "Propose ACE inhibitor–induced cough; consider medication review/switch."
  kind: Task

- actionId: conclude-evaluation
  description: "Conclude evaluation; if persistent unexplained, consider imaging or referral."
  kind: Task

## Notes / TODO
- Codes (ICD-10/LOINC/SNOMED) mapping: TODO.
- Thresholds are qualitative in this pathway; add units if numeric thresholds are later introduced.
- This Markdown was generated from a textual guideline source; downstream tools should validate cross-artifact integrity.

Generated from diagrams/benh-ho.txt
