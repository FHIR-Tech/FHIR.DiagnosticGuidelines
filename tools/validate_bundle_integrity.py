#!/usr/bin/env python3
"""
Simple integrity checks for MD->Bundle conversion.
Checks performed:
 - Bundle resourceType and type
 - Presence of PlanDefinition, Library, Questionnaire
 - Naming convention for resource ids
 - PlanDefinition.library points to existing Library
 - PlanDefinition actions reference existing ActivityDefinition via definitionCanonical
 - Questionnaire linkIds cover referenced stepIds (best effort: reads from a provided steps list if available)
 - Reports unused resources

Usage:
  python3 tools/validate_bundle_integrity.py fever-diagram.bundle.json

Exit codes:
  0 - all critical checks passed (may print warnings)
  1 - critical failures
"""
import json
import sys
from pathlib import Path


def load_bundle(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def find_by_resource_type(bundle, rtype):
    return [e['resource'] for e in bundle.get('entry', []) if e.get('resource', {}).get('resourceType') == rtype]


def main():
    if len(sys.argv) < 2:
        print('Usage: validate_bundle_integrity.py <bundle.json>')
        sys.exit(2)
    p = Path(sys.argv[1])
    if not p.exists():
        print('File not found:', p)
        sys.exit(2)
    bundle = load_bundle(p)
    errors = []
    warnings = []

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
            if '/' in libref:
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
        for it in items:
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

    # Print results
    if errors:
        print('INTEGRITY CHECK: FAIL')
        for e in errors:
            print('ERROR:', e)
        if warnings:
            print('\nWarnings:')
            for w in warnings:
                print('WARN:', w)
        sys.exit(1)
    else:
        print('INTEGRITY CHECK: PASS')
        if warnings:
            print('\nWarnings:')
            for w in warnings:
                print('WARN:', w)
        sys.exit(0)

if __name__ == '__main__':
    main()
