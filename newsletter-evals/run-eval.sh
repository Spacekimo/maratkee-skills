#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# The runner stays on the host because the custom provider calls the installed Hermes CLI.
# --share uploads the completed matrix to the loopback-bound self-hosted Promptfoo service.
exec npx --yes promptfoo@latest eval --config promptfooconfig.yaml --share "$@"
