# PoliticalChakra - Project Mastermind

This document is the **OPERATIONAL MASTERMIND** for the PoliticalChakra frontend site project. 
Any AI agent (Gemini, Claude Code, etc.) or developer picking up this project MUST read this file to gain zero-to-one context before proceeding.

---

## 1. Project Identity
- **Final Brand Name:** PoliticalChakra
---

## 2. Architecture Map
**Key Routes:**
- `/` - Homepage (marketing, stat counters, CTA).
- `/history/up` - Main Uttar Pradesh election history dashboard.
- `/history/up/compare/parties` - Head-to-head party performance comparison UI.
- `/history/up/compare/candidates` - Candidate comparison tool (currently incomplete).
- `/constituency/[id]` - Constituency-specific details page.
- `/state/up` - State landing page.

**Shared Components & Patterns:**
- `src/lib/constants.ts` (or equivalent) - The source of truth for **party colors** and global static references.
- `src/lib/formatters.ts` - Shared Indian currency/number formatters (e.g., `formatIndianNumber`).
- **Filter-bar Pattern:** A sticky filter bar used across dashboard pages to filter by year, district, and party.
- **Election Result Detail Sidebar:** Reused across pages to show granular details of an election (usually embedded or via a drawer/modal component).
- `src/data/up-elections.ts` - Centralized canonical data source that parses all local JSONs and normalizes party names cleanly before they hit the API routes or components.

---

## 3. Data Status Ledger
Tracking the status of major data surfaces across the app:

| Data Surface / Feature | Status | Notes |
| :--- | :--- | :--- |
| **MyNeta-scraped winner/affidavit data** (2007-2024 UP) | **REAL** | Sourced from local JSONs populated by the `politicalsetu-data` scraping sibling project. |
| **Avg Self-Declared Assets** (`compare/parties`) | **BROKEN-WIRING** | Currently shows ₹0.0 Cr despite real scraped asset data existing in the JSONs. Likely a wiring/aggregation bug in the data layer. |
| **Candidate Comparison** (`compare/candidates`) | **UNWIRED** | Awaiting real search logic implementation; currently incomplete. |
| **Alliances Section** | **DUMMY-PLACEHOLDER** | Dummy data per product owner. Needs real alliance-to-constituency mapping before it's meaningful. |
| **Homepage Stat Counters** | **BROKEN-WIRING** | Still hardcoded/showing broken zeros instead of live counts. |

*Note: The data scraping project (`politicalsetu-data`) lives in a sibling directory or is managed separately.*

---

## 4. Known Open Issues
- [ ] **Homepage zero counters:** The large metric counters on the landing page are hardcoded/broken.
- [ ] **Compare parties assets bug:** Avg Self-Declared Assets shows ₹0.0 Cr on the `compare/parties` route.
- [ ] **Compare candidates incomplete:** Search/comparison logic is unwired.
- [ ] **Alliances dummy:** Needs real mapping data to replace current dummy placeholders.
- [ ] **Results table UI:** Column width/wrapping needs fixing + inconsistent District column behavior.
- [ ] **Number formatting:** Non-Indian number grouping used on vote counts in some views.
- [ ] **Civic Disengagement widget:** Broken link + emoji usage needs refinement.
- [ ] **Winners-vs-runners-up table:** Needs refinement/cleanup.
- [ ] **Margin distribution chart:** Styling needs an overhaul.

---

## 5. DELEGATION PROTOCOL
**THIS IS A PERMANENT OPERATING RULE.**

Before starting any non-trivial task, assess whether it is **GRUNT WORK** (to be delegated) or **PRIMARY WORK** (to be done directly).

### When to Delegate (to Claude Code via OmniRouter):
Delegate mechanical and verifiable tasks to conserve budget:
- Bulk scraping
- Cross-checking scraped data against source pages
- Normalizing/cleaning already-collected data into the fixed schema
- Repetitive multi-file find/replace
- Generating audit reports
- Writing documentation
- Running large greps and summarizing results

### When to Keep In-House:
Do the work directly when it requires:
- Live product/UI judgment
- Touching fewer than ~5 files with real design nuance
- Final sign-off on data accuracy before shipping to users

### How to Delegate:
NEVER just describe the task in chat. **Produce a fully self-contained task brief formatted for direct paste into the Claude Code CLI.** (The Claude Code session has no access to this conversation).

Every brief MUST include:
1. `"Read _MASTERMIND.md at the repo root before doing anything."`
2. **Exact scope:** Which files/folders it may touch and which it must NOT touch.
3. **Exact input/output:** Source paths and exact output paths.
4. **Schema:** The fixed schema/format to follow, if data-related (reference `_SCHEMA.md` or CSV headers).
5. **Hard rules:** No fabricated data, no guessing missing values, cite what was verified vs left empty.
6. **Reporting:** Append a dated entry to `_PROGRESS.md` with the outcome (do not just reply in chat).

**Example Output:** Generate these briefs directly in the CLI response so they can be copy-pasted as-is.

---

## 6. Continuity Rule
**Nothing lives only in chat memory or on one machine.**
Any meaningful progress, decision, or blocker MUST be written to `_MASTERMIND.md` or `_PROGRESS.md` before the session ends. Opening the project on a different OS/machine tomorrow via `git pull` must be sufficient to resume with full context.

## 7. Activity Pipeline
A pilot project for UP political-activity tracking has been established in the `activity-pipeline/` subdirectory.
- **Source Registry & Status:** See [Pipeline Mastermind](activity-pipeline/_PIPELINE_MASTERMIND.md) for the latest counts of OK / RESTRICTED / UNKNOWN sources.
