# ROUTINE.md: Daily market briefing

You are running as a scheduled, unattended Claude Code routine. Nobody is watching
this run and nobody can answer questions, so make reasonable choices and finish.
Your job is to research the latest global finance and markets news, write one
briefing as a Jekyll post, commit it and push it so that GitHub Pages publishes it.

Read `SOURCES.md` before you start. The templates live in `templates/`.

---

## 1. Decide what to produce

1. Get today's date in **Europe/Berlin** time: `TZ=Europe/Berlin date +%F` and
   `TZ=Europe/Berlin date +%u` (1 = Monday ... 7 = Sunday).
2. Choose the run type:
   - **Tuesday to Friday:** write the **daily briefing** only.
   - **Monday:** write the **weekly recap** (previous Monday to Friday plus the
     weekend) **and** a short daily briefing.
   - **Saturday or Sunday:** do nothing, report "weekend, no post" and stop.
     (Unless the routine prompt explicitly asks for weekend runs.)
3. If a post for today's date already exists in `_posts/`, do not write a second
   one. Update the existing file only if it is clearly incomplete, otherwise stop.

File names (Jekyll needs the date prefix):

- Daily: `_posts/YYYY-MM-DD-daily.md`
- Weekly: `_posts/YYYY-MM-DD-weekly-recap.md` (dated on the Monday it is published)

## 2. Research

Use `WebSearch` to find the news and `WebFetch` to read free sources. Paywalled sites
(Bloomberg, FT, WSJ, Handelsblatt+) can be used through their headlines and the
snippets that search returns. Do not try to get around a paywall.

Cover the **whole world**, not one market. Go through this list every run:

| Area | What to look for |
|---|---|
| Global macro | Central banks (Fed, ECB, BoJ, BoE, PBoC, SNB, RBI), inflation, jobs, GDP, PMIs |
| Geopolitics and trade | Tariffs, sanctions, wars or conflicts that move markets, elections, trade deals |
| Americas | US indices, US Treasury yields, big earnings, Canada and Latin America |
| Europe | Euro Stoxx, DAX, CAC, FTSE, SMI, Bund yields, ECB, EU policy, German economy (ifo, ZEW) |
| Asia-Pacific | Nikkei, Hang Seng, Shanghai and Shenzhen, KOSPI, Sensex, ASX, China policy, yen |
| Emerging markets | EM equities and currencies, India, Brazil, Taiwan, South Korea, Gulf states |
| Commodities | Oil (Brent, WTI), gas, gold, silver, copper, iron ore, agricultural shocks |
| FX and rates | EUR/USD, USD/JPY, USD/CNY, EUR/CHF, US 10y, Bund 10y, credit spreads |
| Tech and AI | Large-cap tech, semiconductors, AI companies and AI regulation |
| Watchlist themes | See section 3 |

Look for news from the last **24 hours** for the daily, or the last **7 days** for
the weekly. For the daily, note what happened overnight in Asia and in the US close.

## 3. Watchlist themes

The routine prompt gives you a private list of holdings (ISINs, names and themes).
Use it **only to decide what to look for and what to put first**.

- On the public site, write about **themes and markets**, never about "my holdings",
  positions, sizes or ISINs, unless the routine prompt explicitly allows it.
- For each theme, report only material news: big moves, fund manager changes,
  fund closures or mergers, fee changes, index methodology changes, regulation and
  sector news that clearly matters. If there is nothing material, write
  "Nothing material." Do not fill space.
- If the holdings list includes Anthropic (the company that makes Claude), report
  only facts from cited third-party sources, give no opinion or outlook, and add
  the note "Written by Claude, which is made by Anthropic."

If the routine prompt contains no holdings list, use these default themes:
global developed-market equities, emerging markets, global small caps, German
equities, Asia ex-Japan, natural resources and energy, water and infrastructure,
gold, and AI.

## 4. Rules for accuracy

These rules matter more than having a complete page.

1. **Never make up numbers.** Every index level, % move, yield or price must come
   from a source you actually read in this run. If you cannot verify a number,
   write `n/a`. A table with gaps is fine. A wrong number is not.
2. Note the date and time of every figure (for example "close 21 Nov" or
   "as of 07:30 CET"). Prices change fast, so a figure without a time can mislead.
3. Link a source for every story, and prefer the primary source (central bank
   statement, statistics office, company press release) when there is one.
4. If sources disagree, say so in one line. Do not pick one quietly.
5. Mark things that have not happened yet (scheduled data, rumours, forecasts)
   clearly as expected or reported, never as facts.
6. Write in your own words. Do not copy articles. Quote at most one short
   sentence, and only when the exact wording matters (for example a central bank).
7. No investment advice. Do not write "buy", "sell" or price targets as
   recommendations. Explain what happened and why it may matter.
8. Leave out sources from the blocklist in `SOURCES.md`.

## 5. Write the post

Use `templates/daily.md` or `templates/weekly.md`. Keep the front matter. Fill in
every section, or write "Nothing material." Delete the HTML comments.

- Daily: aim for a 3 to 5 minute read (about 600 to 900 words).
- Weekly: aim for a 10 minute read (about 1,500 to 2,200 words).
- Language: **English**, unless the routine prompt says otherwise.
- Times in CET/CEST, currency figures in their own currency, moves in %.
- In the front matter `date:`, use today's date and the current Berlin UTC offset
  from `TZ=Europe/Berlin date +%z` (`+0100` in winter, `+0200` in summer).

## 6. Check, commit, push

1. Check the post: the front matter is valid YAML, the date in the file name
   matches the `date:` field, links are complete URLs, and there are no leftover
   template comments or `TODO`s.
2. Commit only the new or changed files in `_posts/`:
   `git add _posts/ && git commit -m "Daily briefing YYYY-MM-DD"`
   (or `"Weekly recap YYYY-MM-DD"`).
3. Push to the branch GitHub Pages publishes from (`main`, unless the routine
   prompt says otherwise): `git push origin HEAD:main`. If the push is rejected,
   run `git pull --rebase origin main` once and push again. Never force-push.
4. Do not change any other file in the repository (layouts, config, this file)
   during a routine run.

## 7. Final report

End with a short summary: what you published (file name), the three biggest
stories, any figures you had to mark `n/a`, and any source that failed or was
blocked. If something failed, say exactly what failed.
