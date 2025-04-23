#!/usr/bin/env bash
set -euo pipefail

REPORT_DIR="reports"
mkdir -p "${REPORT_DIR}"

echo
echo "=== Running pytest with HTML report ==="
pytest \
  --html="${REPORT_DIR}/pytest_report.html" \
  --self-contained-html

echo
echo "=== Running flake8 style check ==="

# Check for flake8-html plugin
if python3 - <<EOF
import sys
try:
    import flake8_html
    sys.exit(0)
except ImportError:
    sys.exit(1)
EOF
then
  echo "flake8-html plugin detected; generating HTML report"
  flake8 . --format=html --htmldir="${REPORT_DIR}/flake8_html" || true
else
  echo "flake8-html plugin not found; generating plain-text report"
  flake8 . > "${REPORT_DIR}/flake8_report.txt" || true
fi
