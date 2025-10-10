#!/usr/bin/env python3
"""
Lightweight integrity checker for generated guideline Markdown files.

Checks performed:
- Parse minimal YAML front-matter from the Markdown and extract keys (id, title, date, authors, fhirVersion).
- Extract stepIds from the Markdown flow section.
- If a source file is provided (e.g. a .txt guideline or diagram filename), compute a SHA256 checksum of the source and compare with a checksum token found in the Markdown (optional).
- Verify that the Markdown contains an explicit "Generated from `<source>`" line (best-effort) and that the front-matter id matches expectations.

Usage:
  python3 tools/integrity_check.py --md <guideline.md> [--source <diagrams/xxx.txt|diagrams/xxx.png>] [--report <report.txt>]

Exit codes:
  0 - all critical checks passed
  1 - critical failures
  2 - usage / file missing
"""
import argparse
import hashlib
import re
from pathlib import Path
import sys


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def parse_markdown_minimal(path: Path):
    """Return dict: front (dict), step_ids (list), generated_from (str or None), checksum_token (str or None)"""
    text = path.read_text(encoding='utf-8')
    front = {}
    step_ids = []
    generated_from = None
    checksum_token = None

    # YAML front-matter
    m = re.search(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.S)
    fm_text = None
    if m:
        fm_text = m.group(1)
        for ln in fm_text.splitlines():
            if ':' in ln:
                k, v = ln.split(':', 1)
                front[k.strip()] = v.strip().strip('"')

    # stepId tokens
    for m in re.finditer(r"stepId\s*[:=]\s*([A-Za-z0-9_\-]+)", text):
        step_ids.append(m.group(1))

    # look for generated-from line (common pattern in this repo)
    # e.g., "Generated from `diagrams/dieu-tri-chan-doan-dot-quy.txt`"
    m2 = re.search(r"Generated from [`']([^`']+)[`']", text)
    if m2:
        generated_from = m2.group(1)

    # look for explicit checksum token like: source-checksum: <hex>
    if fm_text:
        for ln in fm_text.splitlines():
            if 'checksum' in ln.lower() or 'source-checksum' in ln.lower():
                if ':' in ln:
                    _, v = ln.split(':', 1)
                    token = v.strip()
                    # basic hex check
                    if re.fullmatch(r'[0-9a-fA-F]{64}', token):
                        checksum_token = token.lower()

    return {'front': front, 'step_ids': list(dict.fromkeys(step_ids)), 'generated_from': generated_from, 'checksum_token': checksum_token}


def verify_integrity(md_path: Path, source_path: Path = None):
    errors = []
    warnings = []
    md_info = parse_markdown_minimal(md_path)

    front = md_info['front']
    step_ids = md_info['step_ids']
    generated_from = md_info['generated_from']
    checksum_token = md_info['checksum_token']

    # Basic front-matter checks
    if not front.get('id'):
        errors.append('front-matter missing id')
    if not front.get('title'):
        warnings.append('front-matter missing title')
    if not front.get('fhirVersion'):
        warnings.append('front-matter missing fhirVersion')

    # stepIds presence
    if not step_ids:
        warnings.append('no stepId tokens found in markdown')

    # source checks
    if source_path:
        if not source_path.exists():
            errors.append(f'source file not found: {source_path}')
        else:
            # check generated_from mentions source (best-effort)
            rel_source = str(source_path.as_posix())
            if generated_from:
                if rel_source not in generated_from and source_path.name not in generated_from:
                    warnings.append(f"Markdown 'Generated from' line does not mention provided source ({rel_source}); found: {generated_from}")
            else:
                warnings.append('Markdown does not contain a "Generated from <source>" line')

            # checksum compare if token present
            if checksum_token:
                actual = sha256_file(source_path)
                if actual != checksum_token:
                    errors.append('checksum token in markdown does not match actual source checksum')
            else:
                warnings.append('no checksum token found in markdown; cannot verify exact source match')

    # Construct report
    ok = not errors
    lines = []
    lines.append('INTEGRITY CHECK: ' + ('PASS' if ok else 'FAIL'))
    lines.append('')
    lines.append('Markdown: ' + str(md_path))
    if source_path:
        lines.append('Source: ' + str(source_path))
    lines.append('')
    lines.append('Front-matter keys: ' + ', '.join(front.keys()))
    lines.append('StepIds: ' + (', '.join(step_ids) or '<none>'))
    if generated_from:
        lines.append('Generated-from: ' + generated_from)
    if checksum_token:
        lines.append('Checksum token present (sha256): ' + checksum_token)
    lines.append('')
    if errors:
        lines.append('Errors:')
        for e in errors:
            lines.append('  - ' + e)
    if warnings:
        lines.append('Warnings:')
        for w in warnings:
            lines.append('  - ' + w)

    return {'ok': ok, 'text': '\n'.join(lines), 'errors': errors, 'warnings': warnings}


def main():
    parser = argparse.ArgumentParser(description='Integrity checker for guideline Markdown files')
    parser.add_argument('--md', required=True, help='Path to generated guideline markdown file')
    parser.add_argument('--source', required=False, help='Original source file used to generate the md (txt or image)')
    parser.add_argument('--report', required=False, help='Write report to this file')

    args = parser.parse_args()
    pmd = Path(args.md)
    if not pmd.exists():
        print('Markdown file not found:', pmd)
        sys.exit(2)

    psrc = Path(args.source) if args.source else None

    res = verify_integrity(pmd, psrc)
    print(res['text'])
    if args.report:
        Path(args.report).write_text(res['text'], encoding='utf-8')
        print('Report written to', args.report)

    sys.exit(0 if res['ok'] else 1)


if __name__ == '__main__':
    main()
