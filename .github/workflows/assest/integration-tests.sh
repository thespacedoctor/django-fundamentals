#!/usr/bin/env bash
# INVOKED BY thespacedoctor/reusable-workflows/.github/workflows/integration-tests.yml
# NOTE: THE "assest" DIRECTORY NAME (NOT "assets") MATCHES A TYPO IN THAT REUSABLE WORKFLOW
set -euo pipefail

pip install -e ".[tests]"
pytest -q
