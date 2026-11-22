# trade-news

A GitHub Pages site with a daily global markets briefing, a weekend edition and a
weekly recap every Monday, in English with a German toggle, written by a scheduled
Claude Code routine.

| File | Purpose |
|---|---|
| `ROUTINE.md` | Step-by-step instructions the routine follows every run |
| `SOURCES.md` | Trusted sources by tier, plus a blocklist |
| `templates/` | Daily, weekend and weekly post templates (English and German blocks) |
| `scripts/check_posts.py` | Privacy and safety check run before every commit and in CI |
| `_posts/` | Published posts (`YYYY-MM-DD-daily.md`, `-weekend.md`, `-weekly-recap.md`) |
| `.claude/settings.json` | Permissions for the unattended routine run |

## Setup

1. GitHub: Settings > Pages > Source "Deploy from a branch", branch `main`, folder `/ (root)`.
2. Create a scheduled Claude Code task (every day, 06:40 Berlin time) on this
   repository whose prompt says: "Follow ROUTINE.md." plus the private watchlist.
   The task must be allowed to push to `main`, and its cloud environment needs network
   access to the news sites in `SOURCES.md`.

Not investment advice.
