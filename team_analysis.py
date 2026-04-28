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

# --- Chart 1: Goals vs xG ---
fig, ax = plt.subplots(figsize=(13, 8))
data = teams.sort_values("goals", ascending=True)
y = np.arange(len(data))
width = 0.38
ax.barh(y - width / 2, data["goals"], width, label="Actual Goals", color="#2980b9")
ax.barh(y + width / 2, data["expectedGoals"], width, label="Expected Goals (xG)", color="#e67e22", alpha=0.8)
ax.set_yticks(y)
ax.set_yticklabels(data["team_name"], fontsize=9)
ax.set_xlabel("Goals")
ax.set_title("Goals Scored vs Expected Goals (xG) — PL 2025–26, GW31", fontweight="bold")
ax.legend()
plt.tight_layout()
plt.savefig("charts/team/01_goals_vs_xg.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: charts/team/01_goals_vs_xg.png")

# --- Chart 2: xG Overperformance ---
fig, ax = plt.subplots(figsize=(12, 8))
data = teams.sort_values("xg_diff", ascending=True)
colors = ["#2ecc71" if v >= 0 else "#e74c3c" for v in data["xg_diff"]]
bars = ax.barh(data["team_name"], data["xg_diff"], color=colors)
ax.axvline(0, color="black", linewidth=0.9)
ax.bar_label(bars, fmt="%.1f", padding=4, fontsize=8)
ax.set_xlabel("Goals − xG  (positive = scoring more than expected)")
ax.set_title("xG Overperformance — Clinical vs Wasteful | PL 2025–26, GW31", fontweight="bold")
plt.tight_layout()
plt.savefig("charts/team/02_xg_overperformance.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: charts/team/02_xg_overperformance.png")

# --- Chart 3: Shot Conversion Rate ---
fig, ax = plt.subplots(figsize=(12, 8))
data = teams.sort_values("conversion_rate", ascending=True)
colors = ["#2ecc71" if v >= data["conversion_rate"].mean() else "#e74c3c"
          for v in data["conversion_rate"]]
bars = ax.barh(data["team_name"], data["conversion_rate"], color=colors)
ax.axvline(data["conversion_rate"].mean(), color="navy", linestyle="--", linewidth=1.2,
           label=f"Avg: {data['conversion_rate'].mean():.1f}%")
ax.bar_label(bars, fmt="%.1f%%", padding=4, fontsize=8)
ax.set_xlabel("Shot Conversion Rate (Goals / Total Shots × 100)")
ax.set_title("Shot Conversion Rate — PL 2025–26, GW31", fontweight="bold")
ax.legend()
plt.tight_layout()
plt.savefig("charts/team/03_shot_conversion.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: charts/team/03_shot_conversion.png")

# --- Chart 4: Big Chances Created vs Missed ---
fig, ax = plt.subplots(figsize=(13, 8))
data = teams.sort_values("bigChancesCreated", ascending=True)
y = np.arange(len(data))
width = 0.38
ax.barh(y - width / 2, data["bigChancesCreated"], width,
        label="Big Chances Created", color="#1abc9c")
ax.barh(y + width / 2, data["bigChancesMissed"], width,
        label="Big Chances Missed", color="#e74c3c", alpha=0.85)
ax.set_yticks(y)
ax.set_yticklabels(data["team_name"], fontsize=9)
ax.set_xlabel("Count")
ax.set_title("Big Chances Created vs Missed — PL 2025–26, GW31", fontweight="bold")
ax.legend()
plt.tight_layout()
plt.savefig("charts/team/04_big_chances.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: charts/team/04_big_chances.png")

# --- Chart 5: Pass Accuracy ---
fig, ax = plt.subplots(figsize=(12, 8))
data = teams.sort_values("pass_accuracy", ascending=True)
colors = ["#2ecc71" if v >= data["pass_accuracy"].mean() else "#e74c3c"
          for v in data["pass_accuracy"]]
bars = ax.barh(data["team_name"], data["pass_accuracy"], color=colors)
ax.axvline(data["pass_accuracy"].mean(), color="navy", linestyle="--", linewidth=1.2,
           label=f"Avg: {data['pass_accuracy'].mean():.1f}%")
ax.bar_label(bars, fmt="%.1f%%", padding=4, fontsize=8)
ax.set_xlabel("Pass Accuracy % (re-computed from raw totals)")
ax.set_title("Team Pass Accuracy — PL 2025–26, GW31", fontweight="bold")
ax.legend()
ax.set_xlim(data["pass_accuracy"].min() - 2, 100)
plt.tight_layout()
plt.savefig("charts/team/05_pass_accuracy.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: charts/team/05_pass_accuracy.png")

# --- Chart 6: Progressive Passing ---
fig, ax = plt.subplots(figsize=(12, 8))
data = teams.sort_values("accurateFinalThirdPasses", ascending=True)
bars = ax.barh(data["team_name"], data["accurateFinalThirdPasses"], color="#8e44ad")
ax.axvline(data["accurateFinalThirdPasses"].mean(), color="navy", linestyle="--", linewidth=1.2,
           label=f"Avg: {data['accurateFinalThirdPasses'].mean():.0f}")
ax.bar_label(bars, fmt="%.0f", padding=4, fontsize=8)
ax.set_xlabel("Accurate Final-Third Passes")
ax.set_title("Progressive Passing — Accurate Final-Third Passes | PL 2025–26, GW31",
             fontweight="bold")
ax.legend()
plt.tight_layout()
plt.savefig("charts/team/06_progressive_passing.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: charts/team/06_progressive_passing.png")

# --- Chart 7: Composite Team Ranking ---
rank_df = teams.copy()

def norm(series, invert=False):
    mn, mx = series.min(), series.max()
    if mx == mn:
        return pd.Series([0.5] * len(series), index=series.index)
    normalized = (series - mn) / (mx - mn)
    return 1 - normalized if invert else normalized

rank_df["score"] = (
    norm(rank_df["xg_diff"])                    * 0.30
    + norm(rank_df["bigChancesCreated"])         * 0.25
    + norm(rank_df["pass_accuracy"])             * 0.25
    + norm(rank_df["accurateFinalThirdPasses"])  * 0.20
)

rank_df = rank_df.sort_values("score", ascending=True)

fig, ax = plt.subplots(figsize=(12, 8))
bars = ax.barh(rank_df["team_name"], rank_df["score"], color="#2980b9")
ax.bar_label(bars, fmt="%.3f", padding=4, fontsize=8)
ax.set_xlabel("Composite Score (0–1)")
ax.set_title(
    "Composite Team Ranking (xG diff 30% | Big chances 25% | Pass accuracy 25% | Final-third passes 20%)\n"
    "PL 2025–26, GW31",
    fontweight="bold",
)
plt.tight_layout()
plt.savefig("charts/team/07_composite_ranking.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: charts/team/07_composite_ranking.png")

print("\n=== COMPOSITE TEAM RANKING ===")
top = rank_df[["team_name", "goals", "xg_diff", "bigChancesCreated",
               "pass_accuracy", "accurateFinalThirdPasses", "score"]
              ].sort_values("score", ascending=False).copy()
top.columns = ["Team", "Goals", "xG Diff", "Big Chances", "Pass Acc%", "Final 3rd", "Score"]
top["Score"] = top["Score"].round(3)
top["Pass Acc%"] = top["Pass Acc%"].round(1)
print(top.to_string(index=False))
