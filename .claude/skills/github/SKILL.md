---
name: github
description: Perform GitHub operations (clone, push, PR, API calls) authenticated via the configured GitHub App. Use when the user asks to clone, push, pull, or interact with private GitHub repositories.
argument-hint: <operation> [repo-url or owner/repo]
allowed-tools: Bash, Read
---

Perform the requested GitHub operation using the GitHub App credentials.

## Credential locations
- `~/.config/github-app/credentials` — contains `GITHUB_APP_ID`, `GITHUB_APP_CLIENT_ID`, `GITHUB_APP_CLIENT_SECRET`
- `~/.config/github-app/private-key.pem` — RSA private key for JWT signing

## Helper: gh-token
`~/.local/bin/gh-token` generates installation access tokens.

```
gh-token                    # list all installations (id, owner, type)
gh-token <owner>            # token for all repos of that owner
gh-token <owner>/<repo>     # token scoped to a single repo
```

## Common patterns

### Clone a private repository
```bash
TOKEN=$(~/.local/bin/gh-token <owner>)
git clone https://x-access-token:$TOKEN@github.com/<owner>/<repo> [destination]
```

### Push to a private repository
```bash
TOKEN=$(~/.local/bin/gh-token <owner>)
git -C <repo-path> remote set-url origin https://x-access-token:$TOKEN@github.com/<owner>/<repo>
git -C <repo-path> push
```

### Use gh CLI with app auth
```bash
TOKEN=$(~/.local/bin/gh-token <owner>)
GITHUB_TOKEN=$TOKEN gh pr create ...
GITHUB_TOKEN=$TOKEN gh issue list --repo <owner>/<repo>
GITHUB_TOKEN=$TOKEN gh api repos/<owner>/<repo>
```

### Create a pull request
```bash
TOKEN=$(~/.local/bin/gh-token <owner>)
GITHUB_TOKEN=$TOKEN gh pr create --repo <owner>/<repo> --title "..." --body "..."
```

## Notes
- Tokens expire after ~1 hour; regenerate if you get 401 errors
- The app is installed on: run `gh-token` with no args to see all installations
- For `git push`, always set the remote URL with the fresh token before pushing

## Task
$ARGUMENTS
