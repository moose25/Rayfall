#!/usr/bin/env bash
# Toggle the Rayfall maintenance banner.
#
#   ./maintenance.sh on ["message"]   enable (optional custom message)
#   ./maintenance.sh off              disable
#   ./maintenance.sh status           show current state
#
# State is written to data/maintenance.json (override with RAYFALL_MAINTENANCE_FILE).
# The app reads it per request, so changes take effect without a restart.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FILE="${RAYFALL_MAINTENANCE_FILE:-$DIR/data/maintenance.json}"
mkdir -p "$(dirname "$FILE")"

case "${1:-}" in
  on)
    msg="${2:-Rayfall is undergoing maintenance. Back shortly.}"
    python3 - "$FILE" "$msg" <<'PY'
import json, sys
path, msg = sys.argv[1], sys.argv[2]
with open(path, "w", encoding="utf-8") as f:
    json.dump({"active": True, "message": msg}, f)
PY
    echo "Maintenance banner ON: $msg"
    ;;
  off)
    python3 - "$FILE" <<'PY'
import json, sys
with open(sys.argv[1], "w", encoding="utf-8") as f:
    json.dump({"active": False, "message": ""}, f)
PY
    echo "Maintenance banner OFF"
    ;;
  status)
    if [ -f "$FILE" ]; then cat "$FILE"; echo; else echo '{"active": false, "message": ""}'; fi
    ;;
  *)
    echo "usage: $0 {on [message]|off|status}" >&2
    exit 1
    ;;
esac
