# zin — Claude's home base

This repo bootstraps a fully configured Claude Code environment on any new system.

## Quick start

```bash
git clone https://github.com/albertpurnama/zin ~/Documents/dev/zin
cd ~/Documents/dev/zin
./setup.sh
```

Then place your GitHub App credentials:
```
~/.config/github-app/credentials     # APP_ID, CLIENT_ID, CLIENT_SECRET
~/.config/github-app/private-key.pem # RSA private key
```

## What gets installed

| Item | Destination | Purpose |
|------|-------------|---------|
| `gh-token` | `~/.local/bin/gh-token` | Generate GitHub App installation tokens |
| `/github` skill | `~/.claude/skills/github/` | Authenticated GitHub ops in Claude |

## Using the /github skill

Once set up, ask Claude to do anything GitHub-related and it will use the app credentials automatically. Examples:

- "clone https://github.com/org/private-repo"
- "push my changes to origin"
- "create a PR for this branch"
- "list open issues on owner/repo"
