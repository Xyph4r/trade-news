# Security

This repository publishes a public website that is written automatically by a
scheduled Claude Code routine.

To report a security problem, please use GitHub's private vulnerability reporting
(Security tab > Report a vulnerability) instead of opening a public issue.

What is in place:

- The routine may only write files in `_posts/` and push to `main`; force-pushes are denied.
- `scripts/check_posts.py` runs before every commit and in CI. It blocks ISINs,
  personal-holdings wording, tokens, scripts, iframes, external images and non-HTTPS links.
- The site sends a strict Content Security Policy: only its own scripts and styles load.
- Personal data (holdings, amounts) is never stored in this repository.
