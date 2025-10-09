# Rule: Convert guideline image -> Markdown -> FHIR JSON Bundle -> TTL (validated)

Purpose

This document defines the rules and step-by-step process to convert a clinical guideline diagram (image) into a validated FHIR JSON Bundle. It is designed to be used by an expert reviewer/engineer who will extract the guideline from an image, represent it in structured Markdown, generate FHIR resources (Bundle, PlanDefinition, ActivityDefinition, Questionnaire, Library, etc.) in JSON, and validate the result using the HL7 FHIR validator CLI (validator_cli.jar).

This rule file also defines the System Prompt to be used by any assistant/automation that performs the preliminary extraction and mapping.

---

## System Prompt (for the assistant/automation)

You are a clinical guideline transformation expert limited to the following domains: FHIR/HL7 resources, Clinical Decision Support (CDS), Clinical Guideline representation, and FHIR Bundle packaging. When given a single guideline image (diagram), you will:

- Read and parse the image content to extract the decision flow, questions, actions, possible diagnoses, and data collection elements.
- Produce a structured Markdown file that follows the Guideline Markdown Template (see below). The Markdown must be explicit about branching logic, conditions, and referenced codes (ICD-10, LOINC, SNOMED where applicable).
- From the Markdown, generate a FHIR JSON Bundle containing the required resources to implement the decision logic: at minimum PlanDefinition, Library (CQL or placeholder), ActivityDefinition for actions, Questionnaire for data collection, and any supporting CodeSystem/ValueSet references if available.
- Ensure all resource `id`, `url` and `canonical` links are consistent and self-contained inside the Bundle (or clearly state external canonical dependencies).
- Validate the generated JSON Bundle using the HL7 FHIR Validator CLI and iterate until there are no validation errors (warnings may be acceptable but should be reviewed).

Constraints & Safety

- Do not provide clinical diagnosis or treatment beyond mapping what is explicitly in the guideline image. Treat clinical content as informational; do not change clinical meaning.
- Use only standard code systems when possible (ICD-10, LOINC, SNOMED); if codes are not provided on the image, leave human-readable displays and include TODO comments for later code mapping.
- Produce machine-parseable Markdown following the template and naming conventions in this document.

---

## Files produced per image

For each guideline image named `<image-base>.png|jpg|svg` produce:

- `<image-base>.md` — the structured guideline markdown following the template below.
- `<image-base>.bundle.json` — the corresponding FHIR JSON Bundle (FHIR R4 recommended) with resources referenced by the PlanDefinition.
- `<image-base>.bundle.report.txt` — validator output (errors/warnings) after running `validator_cli.jar`.

Example: image `fever-diagram.png` -> `fever-diagram.md`, `fever-diagram.bundle.json`, `fever-diagram.bundle.report.txt`.

---

## Guideline Markdown Template

The Markdown must follow this structure to be machine-parseable and to guide JSON generation.

---
Metadata (YAML front-matter)

```yaml
id: <short-id>           # short identifier, used for resource ids
title: <Human title>
description: <Short description>
version: 1.0.0
date: YYYY-MM-DD
authors:
  - name: <author>
  - name: <reviewer>
fhirVersion: "4.0.1"
```

---

Content sections

- Context / Scope: textual
- Flow: a numbered or nested list describing steps/questions and branches. Each step must include:
  - id: unique step id
  - question/text
  - type: boolean/choice/choice-multiple/text
  - answers: for choices list code/display if known
  - next: mapping from answer -> next step id or final action
- Actions: list of actions (propose diagnosis, collect information, order test). Each action must map to an ActivityDefinition id and include suggested code (cpg-activity-type) and useContext if available.
- Major classification table (if any)
- Notes / TODO: mapping reminders (codes to add, references)

Example snippet (Flow):

```markdown
## Flow

1. stepId: recentTravel
   question: "Recent travel abroad?"
   type: boolean
   next:
     true: stepId=travelerIncubation
     false: stepId=hospitalizationCheck

2. stepId: travelerIncubation
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

## JSON Bundle generation rules

- Bundle.resourceType: "Bundle"
- Bundle.type: "collection"
- Bundle.id: use front-matter `id` + "-bundle"
- Each resource must have `id`, `url` for canonical items, and `meta.profile` if referencing a profile.
- PlanDefinition:
  - id: `<id>-plan`
  - url: `https://example.org/fhir/PlanDefinition/<id>-plan`
  - library: include `Library/<id>-library` canonical
  - actions: generated from Flow; use `condition.expression` (CQL placeholder strings) to map flow conditions (e.g., RecentTravelAbroad). Each action that issues a diagnosis should be of `code` with `propose-diagnosis` cpg code.
- ActivityDefinition: one per action defined in Flow. Use `kind: ServiceRequest` for propose-diagnosis activities, `kind: Task` for collect-information activities.
- Library: include a content entry with `contentType: text/cql` and a small placeholder CQL or encoded content. Define booleans referenced by PlanDefinition conditions (like RecentTravelAbroad, TravelerIncubationLessThan21Days).
- Questionnaire: generate items for each data collection node in Flow. Use linkIds equal to stepIds.

---

## Data integrity checks (MD -> Bundle)

When converting from the structured Markdown to the JSON Bundle, the following integrity checks MUST be performed automatically and reported. These checks help ensure the Bundle is self-consistent and that the PlanDefinition can reference the generated resources.

- Resource presence: verify that the Bundle contains at minimum a PlanDefinition, a Library, a Questionnaire, and one or more ActivityDefinition resources when referenced by the PlanDefinition.
- ID naming convention: ensure resource ids follow naming conventions (e.g., `<id>-plan`, `<id>-library`, `<id>-questionnaire`, `<id>-activity-<action-id>`). Report mismatches.
- Canonical references: verify canonical URLs in PlanDefinition.library and any definitionCanonical fields point to a resource present in the same Bundle (or explicitly declared external dependencies). Report broken canonicals.
- Action link integrity: for each PlanDefinition.action.definitionCanonical (or `definitionUri`), confirm the referenced ActivityDefinition id exists in the Bundle.
- Questionnaire linkIds: ensure each stepId referenced in the Markdown Flow that requires data collection has a corresponding `linkId` in the Questionnaire.
- Library symbols: check the Library content (placeholder CQL) includes definitions referenced in PlanDefinition.condition.expression strings (e.g., RecentTravelAbroad, TravelerIncubationLessThan21Days). If the Library is a placeholder, report which booleans/identifiers are missing.
- Unused resources: report resources present in the Bundle that are not referenced by PlanDefinition or Questionnaire (may be OK but should be flagged).
- JSON schema: ensure the top-level Bundle has resourceType `Bundle`, `type` set to `collection`, and an `id` equal to the Markdown front-matter id + `-bundle`.

Each check should output pass/fail and a human-readable message. The conversion pipeline should fail fast on critical integrity errors (missing PlanDefinition, broken canonical), and warn for non-critical issues (unused resources, missing codes).


Naming conventions

- Resource ids: `<id>-plan`, `<id>-library`, `<id>-questionnaire`, `<id>-activity-<action-id>`
- Canonical URLs: `https://example.org/fhir/<ResourceType>/<id>-<suffix>`

---

## Validation loop (how to run validator and remediate)

1. Run validator:

```bash
java -jar tools/validator_cli.jar -version 4.0.1 -output <image-base>.bundle.report.txt <image-base>.bundle.json
```

2. Inspect `<image-base>.bundle.report.txt`.
  - If errors: fix the JSON Bundle (missing required fields, incorrect types, missing required references), re-run validator.
  - If warnings: review them manually and decide whether to address.

3. Repeat until zero errors. The final output expected: `<image-base>.bundle.json` with 0 validation errors.

Common validator errors and fixes

- Missing resourceType or id: add required fields.
- Incorrect cardinality on nested elements: ensure arrays vs single objects match FHIR spec.
- Unknown code system or invalid coding entries: temporarily use text displays and add TODO for code mapping.
- Broken canonical references: ensure `PlanDefinition.library` points to an existing Library canonical in the Bundle.

---

## Example file naming & deliverables

For `fever-diagram.png` produce:
- `fever-diagram.md`
- `fever-diagram.bundle.json`
- `fever-diagram.bundle.report.txt`

---

## Automation considerations

- Prefer generating an intermediate JSON object model (Python dict or JS object) from the Markdown template then serializing to JSON. This allows programmatic validation of resource IDs/links before using validator CLI.
- Provide mapping helpers for common patterns (PlanDefinition.action → ActivityDefinition resource creation, Questionnaire item generation).

## Best practices to produce a "clean" Bundle (minimise manual fixes)

These are practical suggestions to follow in the generator so the initial Bundle needs fewer manual edits and passes validation faster:

- Use stable, short resource ids that follow the naming convention in this document and keep them under 64 characters.
- Do not embed example hostnames (for example `https://example.org`) in canonical fields used for internal references. For local, in-bundle canonical references prefer urn-based identifiers (for example `urn:uuid:<uuid>` or `urn:uuid:<short-id>`) and ensure the corresponding resource in the Bundle uses the same id/fullUrl. This avoids the validator error "Example URLs are not allowed in this context".
- Always populate `Bundle.entry[].fullUrl` for each entry (for non-transaction/batch bundles). A robust pattern is to set `fullUrl` to `urn:uuid:<uuid>` and use the same `urn:uuid` where a canonical/reference is required.
- Include required resource fields: `resourceType`, `id`, `status` (when applicable), and minimal `meta`/`url`/`version` for canonical resources (PlanDefinition, Library, ActivityDefinition, Questionnaire).
- Library resources must include the `type` element (CodeableConcept) and at least one content item (`content` with `contentType` and `data` or `attachment`). Provide a minimal CQL placeholder encoded in base64 when generating automatically.
- Add a minimal narrative to DomainResource instances (a `text` element with `status` and `div`) to satisfy best-practice validators (dom-6). The narrative can be small (a 1-2 sentence human-readable summary).
- Keep ActivityDefinition ids short and use a stable suffix pattern like `<id>-activity-<short-action-id>`.
- For PlanDefinition.action references, prefer `definitionCanonical`/`definitionUri` values that match the Library/ActivityDefinition resource canonical you put in the Bundle (use the same `urn:uuid` values if you are using urns).
- Populate `Questionnaire.item.linkId` exactly with the `stepId` values used in the Markdown to make cross-checking easy.
- Add `meta.profile` when your resources must conform to a specific profile; otherwise leave it absent to avoid profile-related validation noise.
- Validate the generated JSON object model programmatically (lightweight checks) before writing the file to detect obvious problems (missing fullUrl, canonical mismatch, id length, missing Library.type).

## Automated post-validation remediation workflow

You should implement an automated remediation step that runs immediately after the validator and attempts safe, deterministic fixes for common, easily-corrected errors. The following is a recommended sequence and mapping from validator issues to automatic fixes:

1. Run the HL7 FHIR validator on the generated Bundle and capture the OperationOutcome (XML or JSON).
2. Parse the OperationOutcome and classify issues into: Critical (must fix before re-running), Auto-fixable, and Manual review.

Auto-fixable patterns and how to fix them automatically:

- "Except for transactions and batches, each entry in a Bundle must have a fullUrl":
  - Fix: For each Bundle.entry missing `fullUrl`, set `fullUrl` = `urn:uuid:<resourceType>-<id>` (or generate a uuid). Also ensure the resource's `id` matches the id used in the urn if you choose that pattern.

- "Example URLs are not allowed in this context":
  - Fix: Replace `https://example.org/...` or other example hostnames in canonical fields (PlanDefinition.library, action.definitionCanonical, ActivityDefinition.url, Library.url, Questionnaire.url) with the corresponding `urn:uuid:<id>` value that matches the target resource's `fullUrl` / id. Update all matching references across the Bundle.

- "Library.type: minimum required = 1, but only found 0":
  - Fix: Add a minimal `type` CodeableConcept to the Library, for example using coding `{ system: "http://terminology.hl7.org/CodeSystem/library-type", code: "logic-library", display: "Logic Library" }`.

- "Invalid Resource id: Too long":
  - Fix: Truncate or re-generate the offending id using a deterministic algorithm (e.g., take a short prefix of the action id and a hash suffix) ensuring uniqueness within the Bundle. Update any references to that id accordingly.

Automated remediation steps (ordered):

- Load bundle JSON into memory as an object model.
- Run a pre-validator integrity check (id length, missing fullUrl, missing Library.type, missing Library.content, canonical patterns). Apply the auto-fixes listed above.
- Serialize and re-run the validator. If errors remain, parse them again.
- For remaining non-auto-fixable critical errors (missing required fields not covered above, structural mismatches), collect them into a short report and flag for manual correction.

Logging and safety:

- Keep a copy of the original generated Bundle before any automated edits (write to `<image-base>.bundle.orig.json`).
- Log the exact changes applied (file `<image-base>.bundle.autofix.log`) with OperationOutcome issue references and diffs for traceability.
- Limit auto-fixes to deterministic, reversible changes (id/canonical/fullUrl fixes, add minimal required fields). Do not automatically invent clinical codes, expand CQL, or remove resources.

Exit criteria and iteration:

- Repeat auto-fix → validate up to N times (recommended N = 3).
- If after N attempts there are still critical validation errors, stop and produce a remediation report (`<image-base>.bundle.remediation.txt`) that lists each remaining error and suggested manual steps.

Integration tips for implementers:

- Implement the pre-checks as a small library/module so other guideline converters can reuse it.
- Use stable deterministic UUIDs or a canonical naming helper to avoid changing ids on each run (helps with diffs and reviews).
- When possible, include unit tests that generate minimal example Bundles and verify the auto-fix routine resolves known validator errors.


---

## Change log
- v1.0.0 — Initial rule file
