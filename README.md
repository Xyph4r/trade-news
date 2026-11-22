# trade-news

A GitHub Pages site with a daily global markets briefing and a weekly recap every
Monday, written by a scheduled Claude Code routine.

| File | Purpose |
|---|---|
| `ROUTINE.md` | Step-by-step instructions the routine follows every run |
| `SOURCES.md` | Trusted sources by tier, plus a blocklist |
| `templates/` | Daily and weekly post templates |
| `_posts/` | Published briefings (`YYYY-MM-DD-daily.md`, `YYYY-MM-DD-weekly-recap.md`) |
| `.claude/settings.json` | Permissions for the unattended routine run |

## Setup

1. GitHub: Settings > Pages > Source "Deploy from a branch", branch `main`, folder `/ (root)`.
2. Create a scheduled Claude Code task (weekdays, early morning Berlin time) on this
   repository whose prompt says: "Follow ROUTINE.md." plus the private watchlist.
   The task must be allowed to push to `main`, and its cloud environment needs network
   access to the news sites in `SOURCES.md`.

Not investment advice.
