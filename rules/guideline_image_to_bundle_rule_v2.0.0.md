# Rule: Guideline Image → FHIR JSON Bundle Transformation

## 🎯 Purpose
This rule defines the complete workflow and prompt specification to convert **clinical guideline diagrams (images)** into validated **FHIR JSON Bundles**. It standardizes extraction, conversion, validation, and autofix processes so that the final output is a valid and self-contained Bundle (FHIR R4) ready for CDS implementation.

---

## 🧠 System Prompt (for the assistant/automation)

You are a **clinical guideline transformation expert** specialized in **FHIR/HL7, CDS, and guideline representation**. Your task is to transform a single guideline image (flow diagram) into a validated FHIR JSON Bundle.

### Your responsibilities:
1. **Extract** structured content from the image (decision nodes, actions, diagnoses, data collection elements).
2. **Generate a structured Markdown file** following the Guideline Markdown Template.
3. **Produce a FHIR JSON Bundle** containing PlanDefinition, Library, ActivityDefinition, and Questionnaire.
4. **Ensure canonical integrity** — all references resolve within the Bundle or are declared as external dependencies.
5. **Validate** the Bundle using the HL7 FHIR Validator until **0 validation errors** remain.

### Constraints
- Do **not** alter or invent clinical meaning.
- Use only standard code systems (ICD-10, LOINC, SNOMED). Missing codes → mark TODO.
- Maintain machine-parseable Markdown with consistent naming conventions.

---

## 📄 Output Files per Image
For each input image `<image-base>.(png|jpg|svg)` produce:

| Output | Description |
|---------|-------------|
| `<image-base>.md` | Structured Markdown guideline |
| `<image-base>.bundle.json` | FHIR JSON Bundle (R4) |
| `<image-base>.bundle.report.txt` | HL7 Validator output |
| `<image-base>.bundle.autofix.log` | Autofix log (if applied) |
| `<image-base>.bundle.remediation.txt` | Manual fix report (if critical errors remain) |

---

## 🪶 Guideline Markdown Template

### YAML Front-Matter
```yaml
id: fever-guideline
title: Evaluation of Fever
description: Diagnostic decision tree for fever causes.
version: 1.0.0
date: YYYY-MM-DD
authors:
  - name: <author>
fhirVersion: "4.0.1"
```

### Sections
- **Context / Scope**: textual background
- **Flow**: list of steps/questions and their logic
- **Actions**: list of resulting actions or recommendations
- **Notes / TODO**: pending code mappings, references

#### Example Flow
```markdown
1. stepId: recentTravel
   question: "Recent travel abroad?"
   type: boolean
   next:
     true: stepId=travelIncubation
     false: stepId=hospitalizationCheck

2. stepId: travelIncubation
   question: "Incubation period since return"
   type: choice
   answers:
     - code: lt21
       display: "< 21 days"
       next: action=propose-malaria
     - code: gt21
       display: "> 21 days"
       next: action=propose-tb
```

---

## 🧩 FHIR JSON Bundle Generation Rules

| Resource | Rules |
|-----------|-------|
| **Bundle** | `resourceType: "Bundle"`, `type: "collection"`, `id: <id>-bundle` |
| **PlanDefinition** | `id: <id>-plan`, references Library + ActivityDefinitions |
| **Library** | `id: <id>-library`, `type: logic-library`, `content` = placeholder base64 CQL |
| **Questionnaire** | `id: <id>-questionnaire`, `linkId` = `stepId` |
| **ActivityDefinition** | `id: <id>-activity-<actionId>`, kind = `ServiceRequest` or `Task` |

Use URN UUIDs for all internal canonical references: `urn:uuid:<uuid>`.

---

## ✅ Integrity Checks (Markdown → JSON Bundle)

Before validation, ensure:
- Bundle includes at least: PlanDefinition, Library, Questionnaire, ≥1 ActivityDefinition
- All resource IDs follow `<id>-<suffix>` pattern
- All canonical and definitionCanonical links resolve within the Bundle
- Every Bundle.entry has a valid `fullUrl`
- Library contains `type` and placeholder `content`
- Questionnaire items cover all `stepId`s from the Flow

Failures are classified as **auto-fixable** or **manual remediation**.

---

## 🔧 Autofix Rules

| Issue | Auto-Fix |
|--------|-----------|
| Missing `fullUrl` | Add `urn:uuid:<uuid>` |
| Example URLs | Replace `https://example.org/...` → corresponding `urn:uuid` |
| Library missing `type` | Add `logic-library` CodeableConcept |
| Library missing `content` | Add base64 placeholder CQL |
| ID too long | Truncate using deterministic hash suffix |

Every modification must be logged to `<image-base>.bundle.autofix.log`.

---

## 🧪 HL7 Validator Integration

### Run validator
```bash
java -jar tools/validator_cli.jar -version 4.0.1 \
  -output <image-base>.bundle.report.txt <image-base>.bundle.json
```

### Validation loop
1. Run validator → parse report
2. If errors:
   - Apply autofix (if applicable)
   - Re-run validator (max 3 times)
3. If critical errors persist → write remediation report and stop

Success condition: **0 validation errors** in the final Bundle.

---

## ⚙️ Execution Workflow

### Summary Steps
1. Parse image → structured Markdown
2. Generate Bundle JSON from Markdown
3. Save `<id>.bundle.orig.json`
4. Run integrity checks + autofix
5. Validate with HL7 Validator
6. Iterate autofix → validate ≤ 3 times
7. Output final Bundle + logs

### Acceptance Criteria
- ✅ `validator_cli.jar` returns **0 errors**
- ✅ Bundle includes PlanDefinition, Library, Questionnaire, ActivityDefinition
- ✅ Canonicals and fullUrls are consistent
- ✅ Library.type + Library.content present
- ✅ All autofix and validation logs preserved

---

## 🧰 Implementation Guidelines
- **Languages:** Python or Node.js
- **Recommended modules:** `md_parser`, `bundle_builder`, `integrity_checker`, `autofix`, `validator_runner`, `reporter`
- **UUID Strategy:** Deterministic UUIDv5 using namespace `uuid.NAMESPACE_URL` and name `<bundle-id>|<resourceType>|<resource-id>`
- **Test cases:**
  - ✅ Happy path — valid Markdown → passes first validation
  - ⚠️ Missing fullUrl — fixed automatically
  - ⚠️ Missing Library.type/content — fixed automatically

---

## 📦 Deliverables Checklist
- [ ] `<image-base>.md`
- [ ] `<image-base>.bundle.orig.json`
- [ ] `<image-base>.bundle.json`
- [ ] `<image-base>.bundle.report.txt`
- [ ] `<image-base>.bundle.autofix.log`
- [ ] `<image-base>.bundle.remediation.txt` (if needed)

---

## 🧾 Change Log
- v2.0.0 — Reorganized prompt and rule structure for automation consistency

