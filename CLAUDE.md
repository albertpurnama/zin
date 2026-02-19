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

See `README.md` for the full fresh-install bootstrap (credentials must be placed manually first, then clone, then install).

```bash
cd ~/Documents/dev/zin
make install   # installs gh-token and links all skills
make check     # verify everything is wired up
```

## Cloning private repos

For private repos, use the `/github` skill or run:
```bash
TOKEN=$(~/.local/bin/gh-token <owner>)
git clone https://x-access-token:$TOKEN@github.com/<owner>/<repo>
```
