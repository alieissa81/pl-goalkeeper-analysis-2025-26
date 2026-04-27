# Premier League Goalkeeper Analysis 2025–26

Complete statistical analysis of all Premier League goalkeepers with **900+ minutes played**, through Gameday 31 of the 2025–26 season.

## Charts

| File | Description |
|------|-------------|
| `01_save_percentage` | Overall save % ranked, with league average line |
| `02_goals_prevented` | Goals saved above/below xG expectation (diverging bar) |
| `03_inside_outside_save_pct` | Save % split by shot location — inside vs outside box |
| `04_clean_sheet_pct` | Clean sheet rate per GK |
| `05_error_rate_per90` | Errors leading to goal or shot per 90 minutes |
| `06_high_claims_per90` | Aerial dominance — high claims per 90 |
| `07_composite_ranking` | Weighted composite score (see Methodology) |
| `08_scatter_save_vs_prevented` | Save % vs goals prevented scatter, coloured by rating |

All charts are saved to the `charts/` folder.

## Top 5 — Composite Ranking (GW31)

| Rank | Goalkeeper | Team | Score |
|------|-----------|------|-------|
| 1 | Jordan Pickford | Everton | 0.864 |
| 2 | Dean Henderson | Crystal Palace | 0.861 |
| 3 | Gianluigi Donnarumma | Manchester City | 0.834 |
| 4 | Emiliano Martínez | Aston Villa | 0.749 |
| 5 | Robert Sánchez | Chelsea | 0.748 |

## Methodology

The composite score combines 5 min-max normalised (0–1) metrics:

| Metric | Weight | Direction |
|--------|--------|-----------|
| Save % | 30% | Higher = better |
| Goals prevented per 90 (xG-based) | 30% | Higher = better |
| Clean sheet % | 20% | Higher = better |
| Error rate per 90 | 10% | Lower = better (inverted) |
| Match rating | 10% | Higher = better |

## Data Source

`data/premier_league_stats_gw31.csv` — full player stats export for all 517 PL players through GW31 of 2025–26. Sourced from Sofascore.

**Qualifying GKs:** 23 goalkeepers with 900+ minutes played. Backups with fewer than 10 full games are excluded to avoid small-sample distortions.

## How to Run

```bash
pip install -r requirements.txt
python goalkeeper_analysis.py
```

Charts are saved to `charts/`. The Jupyter notebook at `notebooks/goalkeeper_analysis.ipynb` mirrors the script with narrative markdown explanations for each section.

## Project Structure

```
pl-goalkeeper-analysis-2025-26/
├── README.md
├── requirements.txt
├── goalkeeper_analysis.py
├── data/
│   └── premier_league_stats_gw31.csv
├── charts/
│   ├── 01_save_percentage.png
│   ├── 02_goals_prevented.png
│   ├── 03_inside_outside_save_pct.png
│   ├── 04_clean_sheet_pct.png
│   ├── 05_error_rate_per90.png
│   ├── 06_high_claims_per90.png
│   ├── 07_composite_ranking.png
│   └── 08_scatter_save_vs_prevented.png
└── notebooks/
    └── goalkeeper_analysis.ipynb
```
