# Tools

This folder contains helper scripts used by the guideline conversion workflow.

- `validate_bundle_integrity.py` - integrity and cross-checks for Markdown -> Bundle conversions. Usage:

  - Legacy bundle-only invocation:
    ```
    python3 tools/validate_bundle_integrity.py <bundle.json>
    ```

  - New recommended invocation (validates Markdown and optionally Bundle):
    ```
    python3 tools/validate_bundle_integrity.py --md <guideline.md> [--bundle <guideline.bundle.json>] [--output <report.txt>]
    ```

  The script now extracts YAML front-matter from the Markdown, finds stepIds and compares them to Questionnaire linkIds in the bundle (if provided), and performs the previous bundle integrity checks.

- `post_md_checks.py` - lightweight wrapper to call `validate_bundle_integrity.py` after a converter has generated the `.md` (and optionally `.bundle.json`). It writes `<base>.integrity.report.txt` next to the Markdown file.

Example:

```bash
python3 tools/post_md_checks.py --md guidelines/fever-diagram/fever-diagram.md --bundle guidelines/fever-diagram/fever-diagram.bundle.json
```
