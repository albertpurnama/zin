#!/bin/bash
# Generate a GitHub App installation access token
# Usage:
#   gh-token.sh                  — list all installations
#   gh-token.sh <owner>          — get token for owner (org or user)
#   gh-token.sh <owner>/<repo>   — get token scoped to a single repo

set -e

CREDS=~/.config/github-app/credentials
PRIVATE_KEY=~/.config/github-app/private-key.pem

if [ ! -f "$CREDS" ] || [ ! -f "$PRIVATE_KEY" ]; then
  echo "ERROR: GitHub App credentials not found at ~/.config/github-app/" >&2
  echo "  Expected: $CREDS" >&2
  echo "  Expected: $PRIVATE_KEY" >&2
  exit 1
fi

# shellcheck source=/dev/null
source "$CREDS"

if [ -z "$GITHUB_APP_ID" ]; then
  echo "ERROR: GITHUB_APP_ID not set in $CREDS" >&2
  exit 1
fi

b64url() { openssl base64 -A | tr '+/' '-_' | tr -d '='; }

_make_jwt() {
  local now iat exp header payload h p sig
  now=$(date +%s)
  iat=$((now - 60))
  exp=$((now + 600))
  header='{"alg":"RS256","typ":"JWT"}'
  payload="{\"iat\":$iat,\"exp\":$exp,\"iss\":\"$GITHUB_APP_ID\"}"
  h=$(echo -n "$header" | b64url)
  p=$(echo -n "$payload" | b64url)
  sig=$(echo -n "$h.$p" | openssl dgst -sha256 -sign "$PRIVATE_KEY" | b64url)
  echo "$h.$p.$sig"
}

JWT=$(_make_jwt)

# No args — list installations
if [ -z "$1" ]; then
  curl -s \
    -H "Authorization: Bearer $JWT" \
    -H "Accept: application/vnd.github+json" \
    https://api.github.com/app/installations \
    | python3 -c "
import sys, json
for i in json.load(sys.stdin):
    print(i['id'], i['account']['login'], i['account']['type'])
"
  exit 0
fi

# Parse owner (and optional repo) from argument
INPUT="$1"
OWNER="${INPUT%%/*}"
REPO="${INPUT#*/}"
[ "$REPO" = "$INPUT" ] && REPO=""  # no slash found

# Find installation ID for owner
INSTALL_ID=$(curl -s \
  -H "Authorization: Bearer $JWT" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/app/installations \
  | python3 -c "
import sys, json
owner = '$OWNER'.lower()
for i in json.load(sys.stdin):
    if i['account']['login'].lower() == owner:
        print(i['id'])
        break
")

if [ -z "$INSTALL_ID" ]; then
  echo "ERROR: No installation found for owner '$OWNER'" >&2
  echo "Run without arguments to list available installations." >&2
  exit 1
fi

# Build request body (optionally scope to a single repo)
if [ -n "$REPO" ]; then
  BODY="{\"repositories\":[\"$REPO\"]}"
  EXTRA_ARGS=(-d "$BODY")
else
  EXTRA_ARGS=()
fi

# Get access token
curl -s -X POST \
  -H "Authorization: Bearer $JWT" \
  -H "Accept: application/vnd.github+json" \
  -H "Content-Type: application/json" \
  "${EXTRA_ARGS[@]}" \
  "https://api.github.com/app/installations/$INSTALL_ID/access_tokens" \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
if 'token' not in data:
    print('ERROR: ' + str(data), file=sys.stderr)
    sys.exit(1)
print(data['token'])
"
