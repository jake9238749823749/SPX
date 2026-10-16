# Plan: a simpler, better clone of Interval News

2026-10-16. Status: plan only, nothing built. Working name **Gap** (a placeholder of ours, not Interval's).

## What Interval is
These facts come from its App Store listing and two review sites, read on 2026-10-16 (links at the end).
- It is a news app from Interval Collective Inc. for iPhone, and an Android build is listed on apkcombo. Its journalists pick the day's key stories, "especially the ones that are being censored and suppressed".
- Features:
  - daily headlines, with summaries and key takeaways
  - evidence and original sources (footage, court and UN documents, social posts)
  - coverage and visibility indicators
  - a misinformation section
  - a daily audio podcast and staff picks
- Price: the free tier gives 5 full articles. Premium costs $11.99/month or $79.99/year. Rated 4.8 stars from 150 ratings.
- Users praise it as easy to digest and balanced. They like the misinformation tab, the coverage meter and the UI.
- Users complain about four things:
  - the price
  - "I have to google to find an article on the story"
  - they couldn't work out how to cancel the trial
  - they want more international news
- Not public: how the coverage and visibility indicators are calculated.

## The idea
For each day, Interval gives a short list of stories. Each story has a plain summary, its sources, and a sense of how widely it was covered. A daily script and a static web page can deliver all three.

**Why it is simpler:** it has no accounts, paywall, App Store listing, server or video.

**Why it is better:**
- The coverage figure is a published formula (counts of named outlets), not an unexplained editorial call.
- Every summary sentence links to the article it came from.
- International outlets are in the source list from day one.
- It is free.

## Feature by feature

| Interval | Clone | Why it's better or simpler |
|---|---|---|
| Staff journalists pick stories | A published formula ranks stories across about 40 named outlets. Jake approves each edition before it goes live. | Reproducible, and one person can run it |
| Summaries and key takeaways | Same, written by Claude from the source articles, with a citation on every sentence | Can be checked line by line |
| Coverage and visibility indicators (method not published) | A coverage bar that names every outlet that ran the story, grouped as wire, US major, US independent and international | Transparent, and it fixes "I have to google to find the article" |
| "Censored and suppressed" | A **Gaps** tab: stories that many outlets covered but US major outlets mostly didn't | Measures coverage instead of asserting censorship |
| Evidence and original sources | Every source article, plus the primary documents those articles link to (.gov, court and UN sites) | Automatic, so no in-house research is needed |
| Misinformation section (written in-house) | A **Fact-checks** tab with recent reviews by professional fact-checkers from the Google Fact Check Tools API, each linked | Makes no in-house calls on what is true |
| Daily audio and video | Not in v1 (text-to-speech can come later) | The most work, and the least central |
| 5 free articles, then $79.99/yr | Free, with no account | Removes the top complaint and the trial-cancelling problem |
| App Store app | An installable web app (PWA) for phone and desktop | No App Store review and no $99/yr developer account |

## What it looks like
Three tabs and a story page.
- **Today:** the 8 most-covered stories. Each row shows the headline, a one-line summary and the outlet count (e.g. "23 outlets").
- **Gaps:** up to 5 stories that pass the gap rule below, each with a line like "covered by 9 international outlets, 0 US major".
- **Fact-checks:** the 10 most recent claim reviews, each with the claim, rating, fact-checker and link.
- **Story page:**
  - the headline
  - a 3–5 sentence summary with numbered citations
  - 3 key takeaways
  - the coverage bar, with every outlet named and linked
  - links to primary documents
- **About page:** the outlet list, the formulas, the model used and how editions are approved.

## How it works

### Daily pipeline (one Python script, about 06:00 ET)
1. **Fetch.** Pull the last 24 hours from about 40 RSS feeds, which should give 500–1,000 items. Each feed carries one group tag: wire, US major, US independent or international. The tags describe what an outlet is; they are not political ratings, which need licensed data and invite disputes.
2. **Cluster.** Send all headlines and RSS descriptions to Claude in one call. It returns groups of items about the same story as structured output. Code then checks that each item sits in at most one group, and drops any group covered by only one outlet.
3. **Score (plain code, no AI).**
   - Coverage is the number of distinct outlets.
   - **Today** is the 8 stories with the highest coverage.
   - **Gaps** are stories with 4 or more outlets of which at most 1 is US major, ranked by coverage, excluding stories already in Today, with at most 5 shown.
4. **Read.** For each picked story, fetch the text of the source articles that are free to read. Use the RSS description for paywalled ones. Collect outbound links that point to primary-source domains on an allowlist (.gov, .mil, un.org, courtlistener.com, supremecourt.gov and similar).
5. **Summarize.** Make one Claude call per story with the source texts as documents and citations turned on. It returns a headline, a 3–5 sentence summary and 3 takeaways. Citations can't be combined with structured output, so the reply comes as fixed-format text that code parses.
6. **Check (plain code).** Every summary sentence must have at least one citation, and every citation must point to one of the story's sources. A story that fails is dropped and logged, never published.
7. **Fact-checks.** Query the Google Fact Check Tools API for claims reviewed in the last 2 days. The API is `v1alpha1`; Phase 0 confirms it is live and which query parameters it requires.
8. **Publish with approval.** Write `editions/YYYY-MM-DD.json` and open a pull request. Jake reads the preview and merges it, and the merge publishes the edition. If nothing is merged, the previous edition stays up.

### Front end
- It is one static page: `index.html`, `app.js`, `style.css`, `manifest.json` and a service worker (`sw.js`).
- It reads the latest edition's JSON.
- No framework and no build step.
- Hosting: GitHub Pages or Cloudflare Pages, both free.

### Layout
```
pipeline/
  feeds.yaml        outlet list: name, feed URL, group
  build.py          steps 1–8
  test_build.py     offline tests on saved fixture days
  fixtures/
site/
  index.html  app.js  style.css  manifest.json  sw.js
editions/           one JSON file per day
.github/workflows/daily.yml
```

### Edition file (abbreviated)
```json
{
  "date": "2026-10-17",
  "stories": [{
    "id": "s1", "section": "today",
    "headline": "...",
    "summary": [{"text": "...", "cites": [2, 5]}],
    "takeaways": ["...", "...", "..."],
    "coverage": {"total": 23, "wire": 2, "us_major": 9, "us_independent": 4, "international": 8},
    "sources": [{"n": 2, "outlet": "BBC", "title": "...", "url": "...", "published": "..."}],
    "primary_docs": ["https://..."]
  }],
  "factchecks": [{"claim": "...", "rating": "False", "publisher": "...", "url": "..."}]
}
```

## Cost (estimate; Phase 1 measures the real figure)
Claude Opus 5.5 costs $4 per million input tokens and $20 per million output tokens (price checked 2026-10-16). Thinking tokens bill as output.

| Step | Per day | Tokens in | Tokens out | $/day |
|---|---|---|---|---|
| Clustering | 1 call | ~40k | ~8k | ~$0.32 |
| Summaries | 13 calls | ~8k each | ~3k each | ~$1.20 |
| **Total** | | | | **~$1.50 (~$45/month)** |

- The Batch API halves this to about $23/month. Results take minutes to hours rather than seconds, which is fine for a job that runs at 06:00.
- Hosting, RSS and the Fact Check API cost $0. A domain is optional, at about $12/year.
- Cheaper models (Sonnet 5.5, Haiku 5.5) are an option once the quality check passes. That's Jake's call.

## Phases
| Phase | Work | Size | Done when |
|---|---|---|---|
| 0 Decide | Build `feeds.yaml` (about 40 outlets, each feed URL tested). Confirm the Fact Check API. Get API keys, pick a name, create the repo. | 1 session | Jake approves the outlet list. The list is the app's editorial stance, so it's his call. |
| 1 Pipeline | Write steps 1–7 against live feeds. Run 3 days and save them as fixtures. Tests run offline against the fixtures. | 1–2 sessions | 3 editions pass the step-6 check, with the real cost logged from API `usage` |
| 2 App | Build the three tabs, the story page, the About page, PWA install and dark mode. | 1 session | Loads in under 1 s on a phone and works offline for the last edition |
| 3 Daily run | A scheduled GitHub Action opens the PR, and merging publishes. | 1 session | Jake approves going public (repo rule: nothing is published without his approval) |
| 4 Trial | Run for 30 days and score against the criteria below. Extras come only after that: email digest, push alerts, audio, search, a native wrapper. | 30 days | Criteria met |

## Success criteria (fixed now, before building)
1. The edition is ready by 07:00 ET on at least 28 of 30 days.
2. 100% of published summary sentences carry a citation (the step-6 check).
3. Jake spot-checks 3 random stories a day and finds no more than 2 factual errors in 90 stories.
4. The Gaps tab has at least 3 stories on at least 25 of 30 days. If not, either the rule or the outlet list (too heavy on US outlets) is wrong.
5. Cost stays at or below $2/day.
6. At day 30, Jake still opens it by choice (one yes/no).

If criterion 2 or 3 fails, the app doesn't go public.

## Risks
- **AI summary errors.** Covered by a citation on every sentence, the automated check, and Jake's approval of each edition.
- **Copyright.** The app shows only headlines, its own summaries, short quotes and links. It never republishes article text, skips paywalled pages and respects robots.txt. This is not legal advice; get it checked before going public.
- **Outlet-list bias.** The list decides what counts as a gap. Publish it, balance US outlets across the spectrum, include non-US outlets, and review it monthly.
- **Gap-rule noise.** Requiring 4 or more outlets keeps single-outlet scoops and press releases out.
- **Feeds breaking.** Log each feed's health daily. A story needs at least 2 outlets anyway, so one dead feed doesn't sink an edition.
- **Name and look.** Use none of Interval's name, logo, wording or screens. "Clone" means the same job, not the same assets.
- **Off-goal.** This doesn't grow the Robinhood account (GOAL.md). It's a side project, so keep its code in its own repo.

## Decisions for Jake (each with a recommendation)
1. Web app or native iPhone app? Recommendation: a web app (PWA) first, wrapped later if the App Store matters.
2. Free or paid? Recommendation: free for the 30-day trial, then decide.
3. Where does the code live? Recommendation: a new repo. This plan stays here until it exists.
4. Name? "Gap" is a placeholder; choose a name before Phase 3.
5. Which model? Recommendation: Opus 5.5 to start, and try cheaper models after the quality check.

## Sources
- [Interval News, App Store listing](https://apps.apple.com/us/app/-/id6756529560)
- [Interval News reviews (justuseapp)](https://justuseapp.com/en/app/6756529560/interval-news/reviews)
- [Interval News, Android listing (apkcombo)](https://apkcombo.com/interval-news/com.intervalcollective.news/)
- [Google Fact Check Tools API](https://developers.google.com/fact-check/tools/api)
