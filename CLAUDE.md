# Claude's Home — zin

This repository is my persistent home base. It contains my skills, memory seeds, and setup scripts so I can be fully functional on any new system after a single `git clone` + `./setup.sh`.

## What's here

| Path | Purpose |
|------|---------|
| `setup.sh` | Bootstrap a new system — run this first |
| `scripts/gh-token.sh` | Generate GitHub App installation tokens |
| `.claude/skills/github/` | Skill for authenticated GitHub operations |
| `memory/` | Seed memory and notes carried across sessions |

## GitHub authentication

Credentials live at `~/.config/github-app/`:
- `credentials` — `GITHUB_APP_ID`, `GITHUB_APP_CLIENT_ID`, `GITHUB_APP_CLIENT_SECRET`
- `private-key.pem` — RSA private key for JWT signing

Use `~/.local/bin/gh-token <owner>` to get an installation token. The `/github` skill encapsulates this workflow.

## Setting up on a new system

```bash
git clone https://github.com/albertpurnama/zin ~/Documents/dev/zin
cd ~/Documents/dev/zin
./setup.sh
```

`setup.sh` will:
1. Install `gh-token` to `~/.local/bin/`
2. Symlink skills into `~/.claude/skills/`
3. Print instructions for placing GitHub App credentials

## Cloning private repos

For private repos, use the `/github` skill or run:
```bash
TOKEN=$(~/.local/bin/gh-token <owner>)
git clone https://x-access-token:$TOKEN@github.com/<owner>/<repo>
```
