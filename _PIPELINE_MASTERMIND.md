# Activity Pipeline Mastermind

## Source Registry Summary
Total unique sources evaluated: 231

- **OK (Eligible for pilot)**: 78
- **RESTRICTED**: 152
- **UNKNOWN**: 1

> All RESTRICTED and UNKNOWN sources are DISABLED for scraping. 
> Dainik Bhaskar is flagged as RESTRICTED by default due to its terms against automated collection and AI/LLM training.

## Sync Mechanism & Repository Rules
This repository (`activity-pipeline`) is now the **canonical sync point** between the Mac (primary dev) and the Windows machine (local LLM extraction). 
- **`raw/` never syncs:** Bulky per-article HTML/JSON stays local to whichever machine scraped it. It is excluded via `.gitignore`.
- **`processed/` and control files sync:** All extracted entity data, summary CSVs, `_MASTERMIND.md` references, `_PROGRESS.md`, `_SCHEMA.md`, and `sources/` always sync across machines via this Git repository.
