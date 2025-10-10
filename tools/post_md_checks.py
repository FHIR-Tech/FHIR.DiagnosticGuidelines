#!/usr/bin/env python3
"""
Helper to run integrity checks immediately after generating Markdown (and bundle if available).

Usage:
  python3 tools/post_md_checks.py --md <guideline.md> [--bundle <guideline.bundle.json>]

This script calls validate_bundle_integrity.py with appropriate flags and writes the integrity report
next to the guideline files (e.g., <base>.integrity.report.txt).
"""
import argparse
import subprocess
from pathlib import Path
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--md', required=True)
    parser.add_argument('--bundle', required=False)
    args = parser.parse_args()

    pmd = Path(args.md)
    if not pmd.exists():
        print('Markdown not found:', pmd)
        sys.exit(2)

    base = pmd.stem
    report_file = pmd.with_name(f'{base}.integrity.report.txt')

    cmd = ['python3', 'tools/validate_bundle_integrity.py', '--md', str(pmd), '--output', str(report_file)]
    if args.bundle:
        pb = Path(args.bundle)
        if not pb.exists():
            print('Bundle not found:', pb)
            sys.exit(2)
        cmd.extend(['--bundle', str(pb)])

    print('Running integrity checks:', ' '.join(cmd))
    subprocess.run(cmd, check=False)
    print('Report written to', report_file)


if __name__ == '__main__':
    main()
