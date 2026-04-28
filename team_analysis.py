import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs("charts/team", exist_ok=True)
os.makedirs("notebooks", exist_ok=True)

CSV_PATH = "data/premier_league_stats_gw31.csv"

df = pd.read_csv(CSV_PATH, encoding="latin-1")

NUMERIC = [
    "goals", "expectedGoals", "totalShots", "shotsOnTarget",
    "accuratePasses", "totalPasses", "accurateFinalThirdPasses",
    "bigChancesCreated", "bigChancesMissed",
]
for col in NUMERIC:
    df[col] = pd.to_numeric(df[col], errors="coerce")

teams = df.groupby("team_name")[NUMERIC].sum().reset_index()

# Re-compute derived metrics from raw totals (never average percentages)
teams["pass_accuracy"] = teams["accuratePasses"] / teams["totalPasses"] * 100
teams["xg_diff"] = teams["goals"] - teams["expectedGoals"]
teams["conversion_rate"] = teams["goals"] / teams["totalShots"] * 100

teams["team_name"] = teams["team_name"].str.replace("&amp;", "&")

print(f"Teams aggregated: {len(teams)}")
print(teams[["team_name", "goals", "expectedGoals", "xg_diff", "pass_accuracy"]]
      .sort_values("goals", ascending=False).to_string(index=False))
