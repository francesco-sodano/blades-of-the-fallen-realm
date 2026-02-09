#!/usr/bin/env bash
# Run Blades of the Fallen Realm
set -euo pipefail

cd "$(dirname "$0")/.."
python -m blades_of_the_fallen_realm
