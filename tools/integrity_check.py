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
        # stepId tokens (simple) and more structured Flow parsing
        for m in re.finditer(r"stepId\s*[:=]\s*([A-Za-z0-9_\-]+)", text):
            step_ids.append(m.group(1))

        # Attempt to parse Flow section for steps and actions (best-effort)
        # Flow steps: look for lines like '1. stepId: initialAssessment' or 'stepId: xyz' within the Flow block
        flow_steps = {}
        actions = {}
        # find Flow section
        mflow = re.search(r"^## Flow\s*\n(.*?)(?:\n## |\Z)", text, flags=re.S | re.M)
        if mflow:
            flow_text = mflow.group(1)
            # split into step blocks by numbering like '1.' or blank lines
            flow_steps = {}
            # naive split: look for lines starting with a number and a dot
            blocks = re.split(r"\n(?=\s*\d+\.)", flow_text)
            # compute the starting line number of the flow section in the full text
            flow_section_start_line = text[:mflow.start()].count('\n') + 1
            for blk in blocks:
                mstep = re.search(r"stepId\s*[:=]\s*([A-Za-z0-9_\-]+)", blk)
                if mstep:
                    sid = mstep.group(1)
                    # extract question
                    qmatch = re.search(r"question\s*:\s*\"([^\"]+)\"|question\s*:\s*([^\n]+)", blk)
                    q = qmatch.group(1) if qmatch and qmatch.group(1) else (qmatch.group(2).strip() if qmatch and qmatch.group(2) else None)
                    # extract type
                    tmatch = re.search(r"type\s*:\s*([A-Za-z]+)", blk)
                    typ = tmatch.group(1) if tmatch else None
                    # extract answers (list of dicts)
                    answers = []
                    for am in re.finditer(r"-\s*code\s*:\s*([A-Za-z0-9_\-]+)\s*\n\s*display\s*:\s*\"?([^\n\"]+)\"?\s*(?:\n\s*next\s*:\s*([^\n]+))?", blk):
                        code = am.group(1)
                        display = am.group(2).strip()
                        nxt = am.group(3).strip() if am.group(3) else None
                        answers.append({'code': code, 'display': display, 'next': nxt})
                    # also look for inline answers under 'answers:'
                    if not answers:
                        # capture indented answer list after 'answers:'
                        mans = re.search(r"answers\s*:\s*\n(.*?)($|\n\s*\n)", blk, flags=re.S)
                        if mans:
                            for line in mans.group(1).splitlines():
                                m2 = re.search(r"-\s*code\s*:\s*([A-Za-z0-9_\-]+)\s*$", line)
                                if m2:
                                    answers.append({'code': m2.group(1), 'display': None, 'next': None})

                    # extract next mappings
                    next_map = {}
                    for nm in re.finditer(r"^(\s*[a-zA-Z0-9_\-]+)\s*:\s*(.*)$", blk, flags=re.M):
                        key = nm.group(1).strip()
                        val = nm.group(2).strip()
                        if key in ('next', 'true', 'false') or re.match(r"^\s*[0-9]+\s*:", key) or key.endswith(':'):
                            # normalize
                            next_map[key.rstrip(':')] = val
                    # determine start line of this block within flow_text
                    pos = flow_text.find(blk)
                    start_line = flow_section_start_line + (flow_text[:pos].count('\n') if pos != -1 else 0)
                    flow_steps[sid] = {'raw': blk.strip(), 'question': q, 'type': typ, 'answers': answers, 'next': next_map, 'start_line': start_line}
                    if sid not in step_ids:
                        step_ids.append(sid)

        # Actions section
        ma = re.search(r"^## Actions\s*\n(.*?)(?:\n## |\Z)", text, flags=re.S | re.M)
        if ma:
            actions_text = ma.group(1)
            # find actionId: tokens and descriptions
            actions = {}
            # split on blank lines into chunks
            for chunk in re.split(r"\n\s*\n", actions_text):
                mact = re.search(r"actionId\s*[:=]\s*([A-Za-z0-9_\-]+)", chunk)
                if mact:
                    aid = mact.group(1)
                    # description is rest of chunk without the actionId line
                    desc = re.sub(r".*actionId\s*[:=]\s*%s\s*" % re.escape(aid), '', chunk, flags=re.S).strip()
                    actions[aid] = {'raw': chunk.strip(), 'description': desc}

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

    return {'front': front, 'step_ids': list(dict.fromkeys(step_ids)), 'generated_from': generated_from, 'checksum_token': checksum_token, 'flow_steps': flow_steps, 'actions': actions}


def verify_integrity(md_path: Path, source_path: Path = None):
    errors = []
    warnings = []
    md_info = parse_markdown_minimal(md_path)

    front = md_info['front']
    step_ids = md_info['step_ids']
    generated_from = md_info['generated_from']
    checksum_token = md_info['checksum_token']
    # flow_steps and actions parsed (best-effort)
    # Note: parse_markdown_minimal populates these fields on the md_info if available
    flow_steps = md_info.get('flow_steps') if isinstance(md_info.get('flow_steps'), dict) else {}
    actions = md_info.get('actions') if isinstance(md_info.get('actions'), dict) else {}

    # If parse didn't return structured flow_steps/actions (older parser), try re-parsing quick
    if not flow_steps or not actions:
        # best-effort re-parse within this function (duplicate logic to be robust)
        text = md_path.read_text(encoding='utf-8')
        mflow = re.search(r"^## Flow\s*\n(.*?)(?:\n## |\Z)", text, flags=re.S | re.M)
        if mflow:
            flow_text = mflow.group(1)
            flow_steps = {}
            for chunk in re.split(r"\n\s*\n", flow_text):
                mstep = re.search(r"stepId\s*[:=]\s*([A-Za-z0-9_\-]+)", chunk)
                if mstep:
                    sid = mstep.group(1)
                    flow_steps[sid] = chunk.strip()
        ma = re.search(r"^## Actions\s*\n(.*?)(?:\n## |\Z)", text, flags=re.S | re.M)
        if ma:
            actions_text = ma.group(1)
            actions = {}
            for mact in re.finditer(r"actionId\s*[:=]\s*([A-Za-z0-9_\-]+)", actions_text):
                aid = mact.group(1)
                actions[aid] = True

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

    # Validate structured flow steps
    unresolved_refs = set()
    missing_fields = []
    for sid, chunk in flow_steps.items():
        # chunk may be a dict with 'raw' or a raw string
        chunk_str = chunk['raw'] if isinstance(chunk, dict) and 'raw' in chunk else (chunk if isinstance(chunk, str) else '')
        # check presence of question and type
        if not re.search(r"question\s*:\s*\"?[^\n\"]+\"?", chunk_str) and not re.search(r"question\s*:\s*[^\n]+", chunk_str):
            missing_fields.append((sid, 'question'))
        if not re.search(r"type\s*:\s*\"?[^\n\"]+\"?", chunk_str) and not re.search(r"type\s*:\s*[^\n]+", chunk_str):
            missing_fields.append((sid, 'type'))

        # find next references like 'next: stepId=foo' or 'next: action=bar' or 'next: actionId'
        for m in re.finditer(r"next\s*:\s*([^\n]+)", chunk_str):
            nxt = m.group(1).strip()
            # common patterns: 'true: stepId=severityAssessment' or 'true: action=prescribe'
            for token in re.split(r"[,;]\s*|\s+", nxt):
                # extract id-like tokens
                mm = re.search(r"(?:stepId|step|step_id)\s*[=:\s]\s*([A-Za-z0-9_\-]+)", token)
                if mm:
                    if mm.group(1) not in flow_steps:
                        unresolved_refs.add(mm.group(1))
                ma = re.search(r"(?:actionId|action|action_id)\s*[=:\s]\s*([A-Za-z0-9_\-]+)", token)
                if ma:
                    if ma.group(1) not in actions:
                        unresolved_refs.add(ma.group(1))

    if missing_fields:
        for sid, fld in missing_fields:
            warnings.append(f"step '{sid}' missing field: {fld}")

    if unresolved_refs:
        for ref in sorted(unresolved_refs):
            errors.append(f"unresolved next reference: {ref}")

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
    # Append errors/warnings
    if errors:
        lines.append('Errors:')
        for e in errors:
            lines.append('  - ' + e)
    if warnings:
        lines.append('Warnings:')
        for w in warnings:
            lines.append('  - ' + w)

    # Detailed per-step dump (if any flow_steps were parsed)
    if flow_steps:
        lines.append('')
        lines.append('Parsed Flow Steps:')
        for sid, obj in flow_steps.items():
            # obj may be dict or raw string
            if isinstance(obj, dict):
                q = obj.get('question')
                typ = obj.get('type')
                answers = obj.get('answers') or []
                next_map = obj.get('next') or {}
                lines.append(f"- stepId: {sid}")
                lines.append(f"    question: {q}")
                lines.append(f"    type: {typ}")
                if answers:
                    lines.append(f"    answers:")
                    for a in answers:
                        lines.append(f"      - code: {a.get('code')} display: {a.get('display')} next: {a.get('next')}")
                if next_map:
                    lines.append(f"    next:")
                    for k, v in next_map.items():
                        lines.append(f"      {k}: {v}")
            else:
                lines.append(f"- stepId: {sid} (raw)\n{str(obj)[:200]}")

    # If source provided, do a higher-level section mapping check: extract top-level headings from source and ensure their keywords appear in markdown
    if source_path and source_path.exists():
        try:
            stext = source_path.read_text(encoding='utf-8')
            # find lines that look like 'II. ...' or '1.' headings
            sects = []
            for ln in stext.splitlines():
                msec = re.match(r"^\s*([IVXLCDM]+\.|\d+\.)\s*(.+)$", ln)
                if msec:
                    title = msec.group(2).strip()
                    # normalize to short token but keep Unicode letters
                    token = re.sub(r"[^\w\s]+", ' ', title, flags=re.UNICODE).strip().lower()
                    if token:
                        sects.append((title, token))
            if sects:
                lines.append('')
                lines.append('Source sections detected: ' + ', '.join([t[0] for t in sects]))
                # Check each token presence in markdown text (best-effort)
                mtext = md_path.read_text(encoding='utf-8').lower()
                missing_sects = []
                for orig, token in sects:
                    # split token into words, ignore short words
                    words = [w for w in token.split() if len(w) > 2]
                    if not words:
                        continue
                    # consider present if any of the words appear in markdown (approximate)
                    found = any(w in mtext for w in words)
                    if not found:
                        missing_sects.append(orig)
                if missing_sects:
                    lines.append('Source->MD mapping: MISSING sections in markdown:')
                    for ms in missing_sects:
                        lines.append('  - ' + ms)
                else:
                    lines.append('Source->MD mapping: all detected source sections appear to be represented (approx).')
        except Exception as e:
            lines.append('\nSource section mapping failed: ' + str(e))

        # Compute and suggest source checksum to include in markdown front-matter
        try:
            checksum = sha256_file(source_path)
            lines.append('')
            lines.append('Suggested front-matter additions to assert provenance:')
            lines.append(f'  generated-from: `{str(source_path.as_posix())}`')
            lines.append(f'  source-checksum: {checksum}')
        except Exception as e:
            lines.append('\nCould not compute source checksum: ' + str(e))

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
