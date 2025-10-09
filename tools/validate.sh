#!/usr/bin/env bash
# sudo chmod +x ./tools/validate.sh
# Simple helper to run the FHIR validator and save report for a bundle
# Usage: ./tools/validate.sh <bundle.json>

set -euo pipefail
BUNDLE_FILE="$1"
if [ -z "$BUNDLE_FILE" ]; then
  echo "Usage: $0 <bundle.json>"
  exit 2
fi

JAR_PATH="tools/validator_cli.jar"
if [ ! -f "$JAR_PATH" ]; then
  echo "Validator jar not found at $JAR_PATH"
  echo "Please download the HL7 FHIR validator CLI and place it at $JAR_PATH"
  exit 3
fi

BASE_NAME=$(basename "$BUNDLE_FILE" .json)
REPORT_FILE="${BASE_NAME}.report.txt"

echo "Running validator on $BUNDLE_FILE -> $REPORT_FILE"
java -jar "$JAR_PATH" -version 4.0.1 -output "$REPORT_FILE" "$BUNDLE_FILE" || true

# Print summary: count errors/warnings
if [ -f "$REPORT_FILE" ]; then
  ERRORS=$(grep -c "\[error\]" "$REPORT_FILE" || true)
  WARNINGS=$(grep -c "\[warning\]" "$REPORT_FILE" || true)
  echo "Validation completed. Errors: $ERRORS  Warnings: $WARNINGS"
  echo "Report saved to $REPORT_FILE"
else
  echo "No report generated. Check validator invocation." 
fi
