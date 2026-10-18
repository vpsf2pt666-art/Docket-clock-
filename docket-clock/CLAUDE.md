# Docket Clock

A litigation deadline tracker for New York Supreme Court class actions, built for an AI and corporate law course. It started as a Claude artifact. This folder is the handoff so the work can continue in Claude Code.

## What's here

- `index.html` is the whole app: markup, CSS and JavaScript in one file. No build step. Open it in a browser.
- `sample-filings/` holds four simulated PDF filings for the fictional case *Delgado v. Riverside Tower Management LLC* (Index No. 158204/2026). Every page carries a red "SIMULATED / NOT FILED IN ANY COURT" banner and watermark.
- `tools/make_sample_filings.py` regenerates those PDFs. Run `python3 tools/make_sample_filings.py sample-filings` (needs `reportlab`).

## How the app is organized (sections of the `<script>` in index.html)

- **Rule book (`EVENTS`)**: each trigger event lists the deadlines it starts as `{ t: title, d: days, c: citation }`. Negative `d` counts backward. `sched: true` marks a meeting and `sched: "deadline"` marks a court-ordered date; neither computes anything. All cases use New York CPLR rules (`juris: "ny"`). The federal FRCP events are still in the table but no case uses them any more.
- **Date math (`computeDue`, `roll`, `closedReason`)**: General Construction Law § 25-a. A deadline that falls on a weekend or New York public holiday (including Lincoln's Birthday and Election Day) moves to the next court day. Mail service adds 5 days (CPLR 2103(b)(2)).
- **State**: cases live in `localStorage` under `docketclock.v1`. `samplesV` versions the built-in sample cases (Okafor, Northfield, Delgado, Castellano). Version 5 added Castellano without resetting the other three. Sample dates are relative to today via `shift(n)`, `courtDay(n)` (next open court day) and `courtDayBack(n)` (previous open court day).
- **AI features**: "Read a filing", "Brief me" and the Gmail scan call Claude through `window.claude.use("sample")`. The Gmail scan also uses `window.claude.use("mcp")` with the Gmail connector's `search_threads` and `get_thread` tools. **These only exist inside the claude.ai artifact viewer.** Opened as a plain file, the page shows "AI features run when this page is opened in Claude", and the deadline calculator still works.
- **PDF reading**: pdf.js 3.11.174 from cdnjs extracts text in the browser, which then goes to the "Read a filing" prompt.

## AI outside Claude (OpenRouter key)

- Outside the claude.ai viewer, "Read a filing" and "Brief me" call OpenRouter (`https://openrouter.ai/api/v1/chat/completions`, model `anthropic/claude-sonnet-5.5`) through `callClaude(prompt, { signal, json, onText })`. Inside Claude, the same helper uses `window.claude` sampling.
- The user pastes their own OpenRouter key into the "Read a filing" panel. It is stored only in `localStorage` under `docketclock.openrouterKey`, and "Forget key" removes it. Never write a key into the file, a commit or a log. API calls bill the key owner's account, and the UI says so.
- Errors: 401 bad key, 402 out of credit, 429 rate limit, network failure, unreadable JSON.
- The Gmail panel is hidden outside Claude, because it needs Claude's Gmail connector.
- Hosted on Netlify, the page uses a server relay instead: `netlify/functions/claude.mjs` at `/api/claude` holds the site owner's key in the Netlify environment variable `OPENROUTER_API_KEY` (set in the Netlify dashboard, never in the repo). The page checks `GET /api/claude` at load; when the relay answers `{ok:true}`, the key box is hidden and visitors need no key. The relay fixes the model, caps prompt size (20k chars) and output (2000 tokens), rejects other websites by Origin, and rate-limits per IP (best effort). The real spending cap is the credit limit set on the key at openrouter.ai.
- Order of preference in `callClaude`: Claude sampling (artifact), then the relay (hosted site), then the visitor's own key (plain file).
- Published artifact: https://claude.ai/artifact/UxtFcMLUpBdQBTazzTGuZo (private; declares `sample` and Gmail `search_threads`/`get_thread`).

## Ground rules

- All cases, parties, counsel and justices are fictional. Keep anything shaped like a court document clearly marked as simulated.
- Deadlines are an educational approximation. Part rules, preliminary conference orders and stipulations can change them.
- Run a quick check after changing date math. For example, a 30-day CPLR 5513 clock from 2026-10-09 should land on Mon 2026-11-09, because Nov 8 is a Sunday.
