# zin — Claude's home base

Skills, helpers, and setup for a fully configured Claude Code environment.

---

## Fresh install (no GitHub access yet)

On a new system, credentials aren't set up yet so you can't use the normal
clone flow. Bootstrap manually:

### 1. Place GitHub App credentials

```bash
mkdir -p ~/.config/github-app
chmod 700 ~/.config/github-app

# Create ~/.config/github-app/credentials:
cat > ~/.config/github-app/credentials <<'EOF'
GITHUB_APP_ID=<your-app-id>
GITHUB_APP_CLIENT_ID=<your-client-id>
GITHUB_APP_CLIENT_SECRET=<your-client-secret>
EOF

# Copy your private key:
cp /path/to/private-key.pem ~/.config/github-app/private-key.pem

chmod 600 ~/.config/github-app/credentials ~/.config/github-app/private-key.pem
```

### 2. Generate a token and clone this repo

No tooling needed — pure bash + openssl + curl:

```bash
source ~/.config/github-app/credentials

b64url() { openssl base64 -A | tr '+/' '-_' | tr -d '='; }
NOW=$(date +%s)
H=$(echo -n '{"alg":"RS256","typ":"JWT"}' | b64url)
P=$(echo -n "{\"iat\":$((NOW-60)),\"exp\":$((NOW+600)),\"iss\":\"$GITHUB_APP_ID\"}" | b64url)
SIG=$(echo -n "$H.$P" | openssl dgst -sha256 -sign ~/.config/github-app/private-key.pem | b64url)
JWT="$H.$P.$SIG"

INSTALL_ID=$(curl -s -H "Authorization: Bearer $JWT" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/app/installations \
  | python3 -c "import sys,json; [print(i['id']) for i in json.load(sys.stdin) if i['account']['login']=='albertpurnama']")

TOKEN=$(curl -s -X POST \
  -H "Authorization: Bearer $JWT" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/app/installations/$INSTALL_ID/access_tokens \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

git clone https://x-access-token:$TOKEN@github.com/albertpurnama/zin ~/Documents/dev/zin
```

### 3. Install

```bash
cd ~/Documents/dev/zin
make install
```

---

## Subsequent use (already set up)

```bash
make install    # install / re-link everything
make check      # verify credentials and installation
make uninstall  # remove installed files
```

---

## What gets installed

| Item | Destination | Purpose |
|------|-------------|---------|
| `gh-token` | `~/.local/bin/gh-token` | Generate GitHub App installation tokens |
| `/github` skill | `~/.claude/skills/github/` | Authenticated GitHub ops inside Claude |

---

## Using the /github skill in Claude

Once installed, Claude can perform authenticated GitHub operations:

- *"clone https://github.com/org/private-repo"*
- *"push my changes to origin"*
- *"create a PR for this branch"*
- *"list open issues on owner/repo"*
