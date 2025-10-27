#!/usr/bin/env python3
"""
Extended integrity checks for MD->Bundle conversion and Markdown validation.

Usage:
  # legacy bundle-only usage (keeps compatibility):
  python3 tools/validate_bundle_integrity.py <bundle.json>

  # new usage with flags:
  python3 tools/validate_bundle_integrity.py --bundle <bundle.json> [--md <file.md>] [--output <report.txt>]
  python3 tools/validate_bundle_integrity.py --md <file.md> [--output <report.txt>]

Exit codes:
  0 - all critical checks passed (may print warnings)
  1 - critical failures
  2 - usage / file missing
"""
import json
import sys
import argparse
import re
from pathlib import Path


def load_bundle(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def find_by_resource_type(bundle, rtype):
    return [e['resource'] for e in bundle.get('entry', []) if e.get('resource', {}).get('resourceType') == rtype]


def parse_markdown(path):
    """Simple parser to extract minimal YAML front-matter keys and stepIds from the Markdown guideline.

    Returns: dict with keys: front (dict), step_ids (list)
    """
    front = {}
    step_ids = []
    p = Path(path)
    text = p.read_text(encoding='utf-8')

    # Try YAML front-matter between --- markers
    m = re.search(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.S)
    fm_text = None
    if m:
        fm_text = m.group(1)
    else:
        # Fallback: look at the top continuous block of lines containing ':' (key: value)
        lines = text.splitlines()
        acc = []
        for ln in lines[:40]:
            if ln.strip() == '':
                break
            if ':' in ln:
                acc.append(ln)
            else:
                break
        if acc:
            fm_text = '\n'.join(acc)

    if fm_text:
        for ln in fm_text.splitlines():
            if ':' in ln:
                k, v = ln.split(':', 1)
                front[k.strip()] = v.strip()

    # Find stepId occurrences in flow blocks: look for 'stepId:' tokens
    for m in re.finditer(r"stepId\s*:\s*([A-Za-z0-9_\-]+)", text):
        step_ids.append(m.group(1))

    # Also support lines like '1. stepId: recentTravel' or '- stepId: xyz'
    for m in re.finditer(r"stepId\s*=\s*([A-Za-z0-9_\-]+)", text):
        step_ids.append(m.group(1))

    # dedupe
    step_ids = list(dict.fromkeys(step_ids))

    return {'front': front, 'step_ids': step_ids}


def flatten_questionnaire_items(items):
    out = []
    for it in items:
        out.append(it)
        if 'item' in it and isinstance(it['item'], list):
            out.extend(flatten_questionnaire_items(it['item']))
    return out


def run_bundle_checks(bundle, errors, warnings):
    # Top-level checks
    if bundle.get('resourceType') != 'Bundle':
        errors.append('Top-level resourceType is not Bundle')
    if bundle.get('type') != 'collection':
        warnings.append('Bundle.type is not "collection"')
    if not bundle.get('id'):
        errors.append('Bundle.id is missing')

    # Resource presence
    plans = find_by_resource_type(bundle, 'PlanDefinition')
    libs = find_by_resource_type(bundle, 'Library')
    qrs = find_by_resource_type(bundle, 'Questionnaire')
    acts = find_by_resource_type(bundle, 'ActivityDefinition')

    if not plans:
        errors.append('No PlanDefinition found in Bundle')
    if not libs:
        errors.append('No Library found in Bundle')
    if not qrs:
        warnings.append('No Questionnaire found in Bundle')

    # Build index by resourceType/id
    index = {}
    for e in bundle.get('entry', []):
        r = e.get('resource', {})
        rt = r.get('resourceType')
        rid = r.get('id')
        if rt and rid:
            index[f'{rt}/{rid}'] = r

    # ID naming convention (best-effort: read bundle.id prefix)
    bundle_id = bundle.get('id', '')
    prefix = bundle_id.replace('-bundle', '') if bundle_id.endswith('-bundle') else bundle_id
    if prefix:
        # expect plan id prefix
        expected_plan_id = f'{prefix}-plan'
        if plans:
            actual_plan_id = plans[0].get('id')
            if actual_plan_id != expected_plan_id:
                warnings.append(f'PlanDefinition.id "{actual_plan_id}" does not match expected "{expected_plan_id}"')

    # PlanDefinition references
    for plan in plans:
        # library
        libs_in_plan = plan.get('library', [])
        for libref in libs_in_plan:
            # libref like Library/fever-diagram-library or full canonical
            if isinstance(libref, str) and libref.startswith('http'):
                # try to resolve by suffix 'Library/<id>' if full canonical provided
                suffix = '/'.join(libref.split('/')[-2:])
                if suffix not in index and libref not in index:
                    errors.append(f'PlanDefinition references library {libref} but it is not present in the Bundle')
            elif '/' in str(libref):
                if libref not in index:
                    errors.append(f'PlanDefinition references library {libref} but it is not present in the Bundle')
            else:
                # canonical without slash: warn
                warnings.append(f'PlanDefinition.library contains unexpected value: {libref}')
        # actions
        for action in plan.get('action', []):
            defc = action.get('definitionCanonical') or action.get('definitionUri')
            if defc:
                # canonical may be like ActivityDefinition/xxx or full URL ending with ActivityDefinition/xxx
                key = defc
                if defc.startswith('http') and '/' in defc:
                    # extract resourceType/id suffix
                    suffix = '/'.join(defc.split('/')[-2:])
                    key = suffix
                if key not in index:
                    errors.append(f'PlanDefinition.action {action.get("id")} references {defc} which is not present in Bundle')

    # Questionnaire linkIds - best effort check: ensure linkIds are non-empty
    for qr in qrs:
        items = qr.get('item', [])
        for it in flatten_questionnaire_items(items):
            if not it.get('linkId'):
                warnings.append(f'Questionnaire item missing linkId: {it}')

    # Unused resources
    referenced = set()
    # from plan libraries
    for plan in plans:
        for libref in plan.get('library', []):
            if '/' in libref:
                referenced.add(libref)
    # from plan actions
    for plan in plans:
        for action in plan.get('action', []):
            defc = action.get('definitionCanonical') or action.get('definitionUri')
            if defc:
                key = defc
                if defc.startswith('http') and '/' in defc:
                    suffix = '/'.join(defc.split('/')[-2:])
                    key = suffix
                referenced.add(key)
    # from questionnaire
    for qr in qrs:
        referenced.add(f"Questionnaire/{qr.get('id')}")

    unused = []
    for k in index.keys():
        if k not in referenced:
            unused.append(k)

    if unused:
        warnings.append('Unused resources present in Bundle: ' + ', '.join(unused))

    return plans, qrs


def main():
    parser = argparse.ArgumentParser(description='Integrity checks for Markdown->Bundle conversion')
    parser.add_argument('--bundle', help='Path to bundle.json', required=False)
    parser.add_argument('--md', help='Path to guideline markdown file', required=False)
    parser.add_argument('--output', help='Write report to this file', required=False)
    # For backward compatibility allow positional bundle path
    parser.add_argument('positional', nargs='?', help=argparse.SUPPRESS)

    args = parser.parse_args()

    bundle_path = args.bundle or args.positional
    md_path = args.md
    out_path = args.output

    errors = []
    warnings = []
    report_lines = []

    md_info = None
    if md_path:
        pmd = Path(md_path)
        if not pmd.exists():
            print('Markdown file not found:', pmd)
            sys.exit(2)
        md_info = parse_markdown(pmd)
        front = md_info.get('front', {})
        step_ids = md_info.get('step_ids', [])

        # Basic front-matter checks
        if not front.get('id'):
            errors.append('Markdown front-matter missing "id"')
        if not front.get('title'):
            warnings.append('Markdown front-matter missing "title"')
        if not front.get('fhirVersion'):
            warnings.append('Markdown front-matter missing "fhirVersion"')

        report_lines.append('MARKDOWN CHECKS')
        report_lines.append(f'  Found front-matter keys: {", ".join(front.keys())}')
        report_lines.append(f'  Extracted stepIds: {step_ids or []}')

    plans = []
    qrs = []
    if bundle_path:
        pb = Path(bundle_path)
        if not pb.exists():
            print('Bundle file not found:', pb)
            sys.exit(2)
        bundle = load_bundle(pb)
        report_lines.append('\nBUNDLE CHECKS')
        p, q = run_bundle_checks(bundle, errors, warnings)
        plans = p
        qrs = q
        report_lines.append(f'  Bundle id: {bundle.get("id")}')

    # Cross-checks when both present
    if md_info and qrs:
        # collect all linkIds from questionnaire(s)
        q_linkids = set()
        for qr in qrs:
            items = qr.get('item', [])
            for it in flatten_questionnaire_items(items):
                if it.get('linkId'):
                    q_linkids.add(str(it.get('linkId')))
        report_lines.append('\nCROSS-CHECKS')
        report_lines.append(f'  Questionnaire linkIds: {sorted(q_linkids)}')
        missing = [s for s in md_info.get('step_ids', []) if s not in q_linkids]
        if missing:
            warnings.append(f'StepIds from Markdown not found in Questionnaire linkIds: {missing}')
            report_lines.append(f'  Missing stepIds in Questionnaire: {missing}')
        else:
            report_lines.append('  All Markdown stepIds present in Questionnaire linkIds')

    # If only md provided and no bundle, still pass if no critical errors
    # Prepare final report
    if errors:
        header = 'INTEGRITY CHECK: FAIL'
    else:
        header = 'INTEGRITY CHECK: PASS'

    out = [header]
    if errors:
        out.append('\nErrors:')
        for e in errors:
            out.append('  - ' + e)
    if warnings:
        out.append('\nWarnings:')
        for w in warnings:
            out.append('  - ' + w)
    out.append('\nDetails:')
    out.extend(report_lines)

    text = '\n'.join(out)
    print(text)
    if out_path:
        Path(out_path).write_text(text, encoding='utf-8')

    if errors:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
