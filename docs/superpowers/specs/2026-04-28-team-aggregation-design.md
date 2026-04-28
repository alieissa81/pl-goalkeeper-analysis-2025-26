# Team Aggregation Analysis — Design Spec

**Date:** 2026-04-28
**Project:** pl-goalkeeper-analysis-2025-26 (same repo as goalkeeper analysis)
**Dataset:** `data/premier_league_stats_gw31.csv` — 517 players, 99 columns, latin-1 encoding

---

## Goal

Produce a team-level aggregation analysis of all 20 Premier League clubs through GW31 of 2025–26, focused on **attack** (xG vs actual goals, shot efficiency, big chances) and **passing/build-up** (pass accuracy, progressive passing), finishing with a **composite team ranking**.

---

## Scope

Focus areas chosen: Attack + Passing & Build-up.
All 20 teams included — no minimum filter (team level data is complete for all clubs).

---

## Output Files

| File | Description |
|------|-------------|
| `team_analysis.py` | Main script — aggregation, 7 charts, composite ranking |
| `notebooks/team_analysis.ipynb` | Notebook with narrative markdown per section |
| `charts/team/` | Output directory for 7 PNG charts |
| `README_team_analysis.md` | Dedicated README with embedded charts + methodology |

The main `README.md` (goalkeeper analysis) is **not modified**.

---

## Data Aggregation Approach

All metrics are **summed** from player-level rows grouped by `team_name`.

Percentages are **re-computed from raw totals** — never averaged across players, which is statistically incorrect.

Key re-computations:
```python
team["pass_accuracy"]      = team["accuratePasses"] / team["totalPasses"] * 100
team["xg_diff"]            = team["goals"] - team["expectedGoals"]
team["conversion_rate"]    = team["goals"] / team["totalShots"] * 100
```

---

## Charts (7 total → saved to `charts/team/`)

### Chart 1 — Goals vs xG (Grouped Bar)
- Both actual goals (blue) and xG (orange) as side-by-side horizontal bars
- Sorted by actual goals scored (descending)
- Immediately shows which teams are clinical vs fortunate

### Chart 2 — xG Overperformance (Diverging Bar)
- `goals - xG` per team, sorted low to high
- Green = scoring more than expected (clinical), Red = scoring less (wasteful)
- Notable: Crystal Palace -15.9, Man City +5.4, Tottenham +5.4

### Chart 3 — Shot Conversion Rate
- `goals / totalShots * 100` per team, sorted
- Bar chart with league average line
- Separates efficient finishers from volume shooters

### Chart 4 — Big Chances Created vs Missed (Grouped Bar)
- Two bars per team: `bigChancesCreated` (teal) and `bigChancesMissed` (red)
- Sorted by big chances created (descending)
- Shows which teams generate most quality chances AND which squander them most

### Chart 5 — Pass Accuracy
- Re-computed: `accuratePasses / totalPasses * 100`
- Horizontal bar chart sorted low to high
- League average dashed line

### Chart 6 — Progressive Passing (Final Third)
- `accurateFinalThirdPasses` summed per team, sorted
- Shows how effectively each team advances into dangerous areas
- Horizontal bar chart with average line

### Chart 7 — Composite Team Ranking
- Weighted score from 4 min-max normalised (0–1) metrics:

| Metric | Weight | Direction |
|--------|--------|-----------|
| xG overperformance (goals − xG) | 30% | Higher = better |
| Big chances created | 25% | Higher = better |
| Pass accuracy (re-computed) | 25% | Higher = better |
| Accurate final-third passes | 20% | Higher = better |

---

## Notebook

`notebooks/team_analysis.ipynb` — generated via nbformat with:
- Intro markdown cell (project context, 20 teams, GW31)
- Paired markdown + code cells per chart section (same pattern as goalkeeper notebook)
- Composite ranking table displayed as DataFrame at the end

---

## README_team_analysis.md Structure

```
# Premier League Team Performance Analysis 2025–26
[intro paragraph]

## Charts
[all 7 charts embedded as images]

## Top 5 — Composite Ranking (GW31)
[table filled in after running the script]

## Methodology
[composite weights table]

## Data Source
[same blurb as goalkeeper README]

## How to Run
pip install -r requirements.txt
python team_analysis.py

## Project Structure
[tree showing team-specific files]
```

---

## Spec Self-Review

- **Placeholders:** None — all chart formulas, weights, and file paths are fully specified.
- **Consistency:** `charts/team/` used consistently across script, notebook, and README references.
- **Scope:** 7 charts covering the two chosen focus areas + composite. No scope creep.
- **Ambiguity:** Pass accuracy explicitly re-computed from raw totals (not averaged %) to avoid the Simpson's paradox trap.
