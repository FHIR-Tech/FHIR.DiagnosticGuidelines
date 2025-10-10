#!/usr/bin/env python3
"""
Integrity loop tool for Step 2 (MD integrity + autofix) and Step 4 (MD->Bundle integrity + autofix)

Usage examples:
  # Step 2: check and attempt to autofix Markdown
  python3 tools/integrity_loop.py --md guidelines/fever-diagram/fever-diagram.md --source diagrams/fever-diagram.png --step2

  # Step 4: run bundle integrity checks and autofix loop
  python3 tools/integrity_loop.py --md guidelines/fever-diagram/fever-diagram.md --bundle guidelines/fever-diagram/fever-diagram.bundle.json --step4

The tool implements a conservative set of autofixes described in SYSTEM_RULE.md:
- For Markdown: ensure required front-matter keys (id, title, fhirVersion, date) are present; optionally inject source-checksum if --source provided.
- For Bundle: add missing fullUrl entries, ensure Library.type and Library.content present (base64 placeholder), ensure Bundle.id/type present.

All autofix actions are logged to `<base>.bundle.autofix.log` when operating on bundles.
"""
import argparse
import re
from pathlib import Path
import sys
import hashlib
import json
import base64
import uuid
import datetime
import subprocess


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def read_front_matter(text: str):
    m = re.search(r"^---\s*\n(.*?)\n---\s*\n", text, flags=re.S)
    if not m:
        return None, text
    return m.group(1), text[m.end():]


def parse_front_to_dict(fm_text: str):
    d = {}
    lines = fm_text.splitlines()
    # naive parse: key: value (no complex YAML)
    key = None
    for ln in lines:
        if not ln.strip():
            continue
        if ':' in ln and not ln.startswith('  '):
            k, v = ln.split(':', 1)
            key = k.strip()
            d[key] = v.strip().strip('"')
        else:
            # ignore nested structures for now
            continue
    return d


def dict_to_front_text(d: dict):
    lines = ['---']
    for k, v in d.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            for it in v:
                if isinstance(it, dict):
                    # support authors list of dicts
                    lines.append(f"  - name: {it.get('name')}")
                else:
                    lines.append(f"  - {it}")
        else:
            lines.append(f"{k}: {v}")
    lines.append('---')
    return '\n'.join(lines) + '\n\n'


def autofix_markdown(md_path: Path, source_path: Path = None):
    text = md_path.read_text(encoding='utf-8')
    fm_text, rest = read_front_matter(text)
    changed = False
    log = []
    if fm_text is None:
        # create minimal front-matter
        fm = {}
        fm['id'] = md_path.stem
        fm['title'] = md_path.stem
        fm['date'] = datetime.date.today().isoformat()
        fm['fhirVersion'] = '4.0.1'
        fm['authors'] = [{'name': 'AutoFix'}]
        new_text = dict_to_front_text(fm) + rest
        md_path.write_text(new_text, encoding='utf-8')
        log.append('Inserted missing front-matter block with id/title/date/fhirVersion/authors')
        changed = True
    else:
        fm = parse_front_to_dict(fm_text)
        if not fm.get('id'):
            fm['id'] = md_path.stem
            log.append('Added missing id to front-matter')
            changed = True
        if not fm.get('title'):
            fm['title'] = md_path.stem
            log.append('Added missing title to front-matter')
            changed = True
        if not fm.get('fhirVersion'):
            fm['fhirVersion'] = '4.0.1'
            log.append('Added missing fhirVersion to front-matter')
            changed = True
        if not fm.get('date'):
            fm['date'] = datetime.date.today().isoformat()
            log.append('Added missing date to front-matter')
            changed = True
        # authors - if missing, add AutoFix
        if not fm.get('authors'):
            fm['authors'] = [{'name': 'AutoFix'}]
            log.append('Added missing authors to front-matter')
            changed = True

        if changed:
            new_text = dict_to_front_text(fm) + rest
            md_path.write_text(new_text, encoding='utf-8')

    # optional: add checksum token
    if source_path and source_path.exists():
        checksum = sha256_file(source_path)
        # check if checksum present in front-matter already
        text2 = md_path.read_text(encoding='utf-8')
        if 'source-checksum' not in text2:
            # insert source-checksum into existing front-matter (best-effort)
            fm_text2, rest2 = read_front_matter(text2)
            if fm_text2 is None:
                # create new front-matter
                fm2 = {'id': md_path.stem, 'title': md_path.stem, 'fhirVersion': '4.0.1', 'date': datetime.date.today().isoformat(), 'source-checksum': checksum}
                md_path.write_text(dict_to_front_text(fm2) + rest2, encoding='utf-8')
                log.append('Inserted source-checksum into new front-matter')
                changed = True
            else:
                # append checksum line to fm_text2
                new_fm_text = fm_text2 + '\nsource-checksum: ' + checksum + '\n'
                new_text = '---\n' + new_fm_text + '---\n\n' + rest2
                md_path.write_text(new_text, encoding='utf-8')
                log.append('Appended source-checksum to front-matter')
                changed = True

    return changed, log


def ensure_bundle_structure(bundle: dict, bundle_path: Path, log_lines: list):
    # Ensure top-level basics
    if bundle.get('resourceType') != 'Bundle':
        bundle['resourceType'] = 'Bundle'
        log_lines.append('Set resourceType=Bundle')
    if bundle.get('type') != 'collection':
        bundle['type'] = 'collection'
        log_lines.append('Set Bundle.type=collection')
    if not bundle.get('id'):
        bundle['id'] = bundle_path.stem + '-bundle'
        log_lines.append(f"Set Bundle.id={bundle['id']}")


def generate_fullurl(bundle_id: str, r: dict):
    rt = r.get('resourceType', 'Resource')
    rid = r.get('id') or str(uuid.uuid4())
    name = f"{bundle_id}|{rt}|{rid}"
    u = uuid.uuid5(uuid.NAMESPACE_URL, name)
    return 'urn:uuid:' + str(u)


def autofix_bundle(bundle_path: Path, log_path: Path):
    text = bundle_path.read_text(encoding='utf-8')
    bundle = json.loads(text)
    log_lines = []

    ensure_bundle_structure(bundle, bundle_path, log_lines)

    entries = bundle.get('entry', [])
    changed = False
    # ensure all entries have fullUrl and resource ids
    for idx, e in enumerate(entries):
        if not e.get('resource'):
            continue
        r = e['resource']
        rt = r.get('resourceType', 'Resource')
        if not r.get('id'):
            # generate deterministic id
            new_id = f'{rt.lower()}-{idx+1}'
            r['id'] = new_id
            log_lines.append(f'Generated id for {rt}: {new_id}')
            changed = True
        if not e.get('fullUrl'):
            fu = generate_fullurl(bundle.get('id', bundle_path.stem), r)
            e['fullUrl'] = fu
            log_lines.append(f'Added fullUrl {fu} for resource {r.get("resourceType")}/{r.get("id")}')
            changed = True

        # Library specific fixes
        if r.get('resourceType') == 'Library':
            if not r.get('type'):
                r['type'] = {'coding': [{'system': 'http://terminology.hl7.org/CodeSystem/library-type', 'code': 'logic-library'}]}
                log_lines.append(f'Added Library.type for {r.get("id")}')
                changed = True
            if not r.get('content'):
                placeholder = base64.b64encode(b'/* placeholder CQL */').decode('ascii')
                r['content'] = [{'contentType': 'text/cql', 'data': placeholder}]
                log_lines.append(f'Added Library.content placeholder for {r.get("id")}')
                changed = True

    # ensure fullUrls for any leftover missing ones
    if changed:
        # backup original
        orig_path = bundle_path.with_name(bundle_path.stem + '.bundle.orig.json')
        if not orig_path.exists():
            orig_path.write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding='utf-8')
            log_lines.append(f'Wrote backup original bundle to {orig_path.name}')
        # write updated bundle
        bundle_path.write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding='utf-8')
        log_lines.append('Wrote autofixed bundle to disk')
        # append log
        log_path.write_text('\n'.join(log_lines) + '\n', encoding='utf-8')

    return changed, log_lines


def run_validate_bundle_integrity(bundle_path: Path, md_path: Path, report_path: Path = None):
    cmd = ['python3', 'tools/validate_bundle_integrity.py', '--bundle', str(bundle_path), '--md', str(md_path)]
    if report_path:
        cmd.extend(['--output', str(report_path)])
    res = subprocess.run(cmd, check=False)
    return res.returncode


def step2_loop(md_path: Path, source_path: Path = None, max_iter: int = 3):
    # Run integrity_check.py and attempt autofix markdown if warnings/missing fields
    for i in range(1, max_iter + 1):
        print(f'Step2: integrity attempt {i} for {md_path}')
        rc = subprocess.run(['python3', 'tools/integrity_check.py', '--md', str(md_path)] + (['--source', str(source_path)] if source_path else []), check=False)
        if rc.returncode == 0:
            print('Step2: integrity PASS')
            return 0
        # If failed, try to autofix markdown
        changed, log = autofix_markdown(md_path, source_path)
        if changed:
            print('Step2: applied autofix to markdown:')
            for l in log:
                print('  -', l)
            continue
        else:
            print('Step2: no autofix applied; please correct markdown manually')
            return rc.returncode
    return 1


def step4_loop(md_path: Path, bundle_path: Path, max_iter: int = 3):
    base = md_path.stem
    autolog = bundle_path.with_name(base + '.bundle.autofix.log')
    report = bundle_path.with_name(base + '.integrity.report.txt')
    for i in range(1, max_iter + 1):
        print(f'Step4: bundle integrity attempt {i} for {bundle_path}')
        rc = run_validate_bundle_integrity(bundle_path, md_path, report)
        if rc == 0:
            print('Step4: integrity PASS')
            return 0
        # attempt autofix
        changed, logs = autofix_bundle(bundle_path, autolog)
        if changed:
            print('Step4: applied autofix to bundle:')
            for l in logs:
                print('  -', l)
            # re-run loop
            continue
        else:
            print('Step4: no autofix applied or autofix insufficient. Writing remediation report')
            # copy report to remediation
            remediation = bundle_path.with_name(base + '.bundle.remediation.txt')
            if report.exists():
                remediation.write_text(report.read_text(encoding='utf-8'), encoding='utf-8')
            return rc
    return 1


def main():
    parser = argparse.ArgumentParser(description='Run integrity loops for Step2 (MD) and Step4 (Bundle)')
    parser.add_argument('--md', required=True, help='Path to guideline markdown file')
    parser.add_argument('--bundle', required=False, help='Path to guideline bundle json')
    parser.add_argument('--source', required=False, help='Original source file (txt/png) used to generate md')
    parser.add_argument('--step2', action='store_true', help='Run Step 2: MD integrity loop')
    parser.add_argument('--step4', action='store_true', help='Run Step 4: Bundle integrity loop')
    parser.add_argument('--max-iter', type=int, default=3)
    args = parser.parse_args()

    md_path = Path(args.md)
    if not md_path.exists():
        print('Markdown file not found:', md_path)
        raise SystemExit(2)
    src = Path(args.source) if args.source else None

    if args.step2:
        rc = step2_loop(md_path, src, max_iter=args.max_iter)
        if rc != 0:
            print('Step2 loop finished with errors')
            raise SystemExit(rc)

    if args.step4:
        if not args.bundle:
            print('Step4 requires --bundle <path>')
            raise SystemExit(2)
        bundle_path = Path(args.bundle)
        if not bundle_path.exists():
            print('Bundle file not found:', bundle_path)
            raise SystemExit(2)
        rc = step4_loop(md_path, bundle_path, max_iter=args.max_iter)
        if rc != 0:
            print('Step4 loop finished with errors')
            raise SystemExit(rc)

    print('Requested steps completed')


if __name__ == '__main__':
    main()
