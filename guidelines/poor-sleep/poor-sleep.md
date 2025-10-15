---
id: poor-sleep
title: Evaluation of Poor Sleep / Insomnia
description: >-
  Decision pathway for patients presenting with poor sleep or insomnia symptoms. Extracted from diagram image "poor_sleep".
version: 1.0.0
date: 2025-10-15
authors:
  - name: automated-converter
fhirVersion: "4.0.1"
source-type: image
source-file: diagrams/poor_sleep.png
source-checksum: TODO
---

Context / Scope:

This guideline describes a diagnostic approach to patients presenting with complaints of poor sleep or insomnia. It distinguishes transient/short-term sleep problems from chronic insomnia, screens for mental health disorders, substance use, contributing medical disorders, common sleep disorders (sleep apnea, RLS, PLMD), and circadian rhythm disorders. Recommendations include conservative measures, referral, treating underlying causes, and specialist referral.

Flow:

1. stepId: defineComplaint
   question: "Does the patient present with a complaint of poor sleep?"
   type: boolean
   next:
     true: stepId=assessDaytimeImpact
     false: action=none

2. stepId: assessDaytimeImpact
   question: "Assess daytime consequences, precipitating factors, and sleep hygiene"
   type: collect-information
   next:
     continue: stepId=defineDuration

3. stepId: defineDuration
   question: "What is the duration of symptoms?"
   type: choice
   answers:
     - code: transient
       display: "Transient or short-term (< 3 wks)"
       next: action=considerShortSleeper
     - code: chronic
       display: "Chronic (> 3 wks)"
       next: stepId=screenMentalHealth

4. stepId: considerShortSleeper
   action: consider-short-sleeper
   description: "Consider short sleeper / normal variant; review for acute life stress, acute illness, jet lag, substance/medication effect"
   next:
     done: action=conservativeAdvice

5. stepId: screenMentalHealth
   question: "Is there evidence of mental health disorder?"
   type: boolean
   next:
     true: action=considerInsomniaDueToMentalHealth
     false: stepId=reviewSubstanceUse

6. stepId: considerInsomniaDueToMentalHealth
   action: consider-insomnia-mental-health
   description: "Consider insomnia due to mental health disorder; evaluate and treat mental health disorder and consider referral"
   next:
     done: action=referMentalHealth

7. stepId: reviewSubstanceUse
   question: "Is there evidence of substance use that could contribute? (prescription meds, OTC, caffeine, nicotine, alcohol, illicit drugs)"
   type: boolean
   next:
     true: action=considerInsomniaSubstance
     false: stepId=reviewMedicalDisorders

8. stepId: considerInsomniaSubstance
   action: consider-insomnia-substance
   description: "Consider insomnia due to substance use or withdrawal; change/stop medications, evaluate for substance abuse/withdrawal, consider referral"
   next:
     done: action=manageSubstance

9. stepId: reviewMedicalDisorders
   question: "Evidence of contributing medical or neurologic disorders? (e.g., CHF, CAD, COPD, asthma, PUD, GERD, renal or neurologic diseases)"
   type: boolean
   next:
     true: action=considerInsomniaMedical
     false: stepId=reviewSleepDisorders

10. stepId: considerInsomniaMedical
    action: consider-insomnia-medical
    description: "Consider insomnia due to medical or neurologic disorder; evaluate and treat underlying medical disorder. Consider referral or urgent referral for alarm symptoms"
    next:
      done: action=manageMedical

11. stepId: reviewSleepDisorders
    question: "Evidence of common sleep disorders? (sleep apnea, RLS, PLMD)"
    type: boolean
    next:
      true: action=considerInsomniaSleepDisorder
      false: stepId=reviewCircadian

12. stepId: considerInsomniaSleepDisorder
    action: consider-insomnia-sleep-disorder
    description: "Consider insomnia due to sleep disorder; refer to sleep specialist to confirm sleep apnea, PLMD, RLS. Treat RLS if present."
    next:
      done: action=referSleepSpecialist

13. stepId: reviewCircadian
    question: "Evidence of circadian rhythm disorder?"
    type: boolean
    next:
      true: action=considerAdvancedOrDelayedSleepPhase
      false: stepId=noSecondaryCause

14. stepId: considerAdvancedOrDelayedSleepPhase
    action: consider-advanced-delayed-sleep-phase
    description: "Consider advanced or delayed sleep phase disorders; referral to sleep specialist"
    next:
      done: action=referSleepSpecialist

15. stepId: noSecondaryCause
    question: "No evidence of secondary cause?"
    type: boolean
    next:
      true: action=considerIdiopathicInsomnia
      false: action=reviewFurther

16. stepId: considerIdiopathicInsomnia
    action: consider-idiopathic-insomnia
    description: "Consider idiopathic insomnia, psychophysiologic (conditioned) insomnia, or sleep-state misperception. Provide behavioral interventions and consider CBT-i or specialist referral where appropriate."
    next:
      done: action=conservativeAdvice

Actions:

- actionId: conservativeAdvice
  title: "Conservative measures"
  description: "Provide sleep hygiene advice, assess precipitating factors, consider short course of short-acting hypnotic if indicated, and review daytime routines."
  resourceKind: ActivityDefinition

- actionId: referSleepSpecialist
  title: "Refer to sleep specialist"
  description: "Referral to sleep clinic for assessment and management of suspected sleep disorders."
  resourceKind: ReferralRequest

- actionId: referMentalHealth
  title: "Refer to mental health services"
  description: "Refer for assessment and treatment of mental health disorder where relevant."
  resourceKind: ReferralRequest

- actionId: manageSubstance
  title: "Manage substance-related causes"
  description: "Change or stop medications, evaluate and treat substance abuse or withdrawal, consider referral."
  resourceKind: ActivityDefinition

- actionId: manageMedical
  title: "Manage underlying medical disorder"
  description: "Evaluate and treat underlying medical or neurologic disorder; urgent referral for alarm symptoms."
  resourceKind: ActivityDefinition

- actionId: considerInsomniaDueToMentalHealth
  title: "Consider insomnia due to mental health disorder"
  description: "Consider insomnia as secondary to mental health conditions."

- actionId: considerInsomniaSubstance
  title: "Consider insomnia due to substance use"
  description: "Consider insomnia related to substance or medication effects."

- actionId: considerInsomniaMedical
  title: "Consider insomnia due to medical/neurologic disorder"
  description: "Consider medical or neurologic causes for insomnia."

- actionId: considerInsomniaSleepDisorder
  title: "Consider insomnia due to sleep disorder"
  description: "Consider common sleep disorders (sleep apnea, RLS, PLMD)"

- actionId: considerAdvancedOrDelayedSleepPhase
  title: "Consider circadian rhythm disorder"
  description: "Consider advanced or delayed sleep phase disorders."

Notes / TODO:

- Clinical codes (SNOMED/ICD/LOINC) not assigned. Marked as TODO where appropriate.
- `source-checksum` left as TODO; compute sha256 of source image if available.
- Review wording with a clinician before publication to avoid altering clinical meaning.

Generated from diagram "poor_sleep".

Codes (proposed):

- Concept: Insomnia / Poor sleep
  - SNOMED CT: 193462001 (Insomnia disorder)  # verify exact preferred concept
  - ICD-10: G47.0 (Insomnia)

- Concept: Sleep apnea (suspected)
  - SNOMED CT: 73430006 (Sleep apnea)
  - ICD-10: G47.3

- Concept: Restless legs syndrome (RLS)
  - SNOMED CT: 40930008 (Restless legs syndrome)
  - ICD-10: G25.81

- Concept: Periodic limb movement disorder (PLMD)
  - SNOMED CT: TODO
  - ICD-10: G47.61 (Periodic limb movement disorder)

- Concept: Circadian rhythm sleep disorder
  - SNOMED CT: 40919007 (Circadian rhythm sleep disorder)  # confirm subtype
  - ICD-10: G47.2

- Concept: Substance-related sleep disturbance
  - SNOMED CT: TODO (search for substance-induced sleep disorder)
  - ICD-10: F10-F19 range for substance-related disorders (choose specific)

- Observations / tests:
  - Sleep study / polysomnography: LOINC: 63772-7 (Polysomnography study)  # verify LOINC code
  - Epworth Sleepiness Scale: LOINC: 89270-2 (Epworth Sleepiness Scale)  # verify

Notes on codes:
- I suggested common mappings for major clinical concepts. Please review each mapping with a clinician and change to the precise SNOMED/ICD/LOINC codes preferred in your setting.
- Items marked TODO need manual lookup/confirmation.

