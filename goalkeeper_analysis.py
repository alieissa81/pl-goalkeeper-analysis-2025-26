import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import os

os.makedirs("charts", exist_ok=True)
os.makedirs("notebooks", exist_ok=True)

CSV_PATH = "data/premier_league_stats_gw31.csv"
MIN_MINUTES = 900

df = pd.read_csv(CSV_PATH, encoding="latin-1")
gks = df[df["position"] == "G"].copy()
gks = gks[gks["minutesPlayed"].astype(float) >= MIN_MINUTES].copy()

NUMERIC = [
    "saves", "goalsConceded", "goalsPrevented", "cleanSheet", "matchesStarted",
    "minutesPlayed", "penaltySave", "penaltyFaced", "errorLeadToGoal",
    "errorLeadToShot", "highClaims", "punches", "rating", "appearances",
    "savedShotsFromInsideTheBox", "savedShotsFromOutsideTheBox",
    "goalsConcededInsideTheBox", "goalsConcededOutsideTheBox",
]
for col in NUMERIC:
    gks[col] = pd.to_numeric(gks[col], errors="coerce")

gks["per90"] = gks["minutesPlayed"] / 90
gks["save_pct"] = gks["saves"] / (gks["saves"] + gks["goalsConceded"]) * 100
gks["clean_sheet_pct"] = gks["cleanSheet"] / gks["matchesStarted"] * 100
gks["inside_save_pct"] = (
    gks["savedShotsFromInsideTheBox"]
    / (gks["savedShotsFromInsideTheBox"] + gks["goalsConcededInsideTheBox"])
    * 100
)
gks["outside_save_pct"] = (
    gks["savedShotsFromOutsideTheBox"]
    / (gks["savedShotsFromOutsideTheBox"] + gks["goalsConcededOutsideTheBox"])
    * 100
)
gks["errors_per90"] = (gks["errorLeadToGoal"] + gks["errorLeadToShot"]) / gks["per90"]
gks["high_claims_per90"] = gks["highClaims"] / gks["per90"]
gks["prevented_per90"] = gks["goalsPrevented"] / gks["per90"]
gks["label"] = (
    gks["player_name"] + "\n(" + gks["team_name"].str.replace("&amp;", "&") + ")"
)

print(f"Qualifying GKs: {len(gks)}")
print(gks[["player_name", "team_name", "minutesPlayed"]].to_string(index=False))

# --- Chart 1: Save Percentage ---
fig, ax = plt.subplots(figsize=(12, 7))
data = gks.sort_values("save_pct", ascending=True)
colors = ["#2ecc71" if v >= 70 else "#e74c3c" for v in data["save_pct"]]
bars = ax.barh(data["label"], data["save_pct"], color=colors)
ax.axvline(data["save_pct"].mean(), color="navy", linestyle="--", linewidth=1.2,
           label=f"Avg: {data['save_pct'].mean():.1f}%")
ax.bar_label(bars, fmt="%.1f%%", padding=4, fontsize=8)
ax.set_xlabel("Save Percentage (%)")
ax.set_title("Save Percentage — GKs with 900+ mins (PL 2025–26, GW31)", fontweight="bold")
ax.legend()
plt.tight_layout()
plt.savefig("charts/01_save_percentage.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: charts/01_save_percentage.png")

# --- Chart 2: Goals Prevented (xG-based) ---
fig, ax = plt.subplots(figsize=(12, 7))
data = gks.dropna(subset=["goalsPrevented"]).sort_values("goalsPrevented", ascending=True)
colors = ["#2ecc71" if v >= 0 else "#e74c3c" for v in data["goalsPrevented"]]
bars = ax.barh(data["label"], data["goalsPrevented"], color=colors)
ax.axvline(0, color="black", linewidth=0.8)
ax.bar_label(bars, fmt="%.2f", padding=4, fontsize=8)
ax.set_xlabel("Goals Prevented (positive = better than expected)")
ax.set_title("Goals Prevented Above/Below xG — PL 2025–26, GW31", fontweight="bold")
plt.tight_layout()
plt.savefig("charts/02_goals_prevented.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: charts/02_goals_prevented.png")

# --- Chart 3: Inside vs Outside Box Save % ---
fig, ax = plt.subplots(figsize=(13, 7))
data = gks.dropna(subset=["inside_save_pct", "outside_save_pct"]).sort_values(
    "inside_save_pct", ascending=True
)
y = np.arange(len(data))
width = 0.38
ax.barh(y - width / 2, data["inside_save_pct"], width, label="Inside Box", color="#3498db")
ax.barh(y + width / 2, data["outside_save_pct"], width, label="Outside Box", color="#e67e22")
ax.set_yticks(y)
ax.set_yticklabels(data["label"], fontsize=8)
ax.set_xlabel("Save Percentage (%)")
ax.set_title("Save % — Inside Box vs Outside Box | PL 2025–26, GW31", fontweight="bold")
ax.legend()
plt.tight_layout()
plt.savefig("charts/03_inside_outside_save_pct.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: charts/03_inside_outside_save_pct.png")

# --- Chart 4: Clean Sheet Percentage ---
fig, ax = plt.subplots(figsize=(12, 7))
data = gks.sort_values("clean_sheet_pct", ascending=True)
colors = ["#2ecc71" if v >= 30 else "#e67e22" if v >= 20 else "#e74c3c"
          for v in data["clean_sheet_pct"]]
bars = ax.barh(data["label"], data["clean_sheet_pct"], color=colors)
ax.axvline(data["clean_sheet_pct"].mean(), color="navy", linestyle="--", linewidth=1.2,
           label=f"Avg: {data['clean_sheet_pct'].mean():.1f}%")
ax.bar_label(bars, fmt="%.1f%%", padding=4, fontsize=8)
ax.set_xlabel("Clean Sheet %")
ax.set_title("Clean Sheet Percentage — GKs with 900+ mins | PL 2025–26, GW31",
             fontweight="bold")
ax.legend()
plt.tight_layout()
plt.savefig("charts/04_clean_sheet_pct.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: charts/04_clean_sheet_pct.png")

# --- Chart 5: Error Rate per 90 mins ---
fig, ax = plt.subplots(figsize=(12, 7))
data = gks.sort_values("errors_per90", ascending=False)
colors = ["#e74c3c" if v > 0.1 else "#e67e22" if v > 0.05 else "#2ecc71"
          for v in data["errors_per90"]]
bars = ax.barh(data["label"], data["errors_per90"], color=colors)
ax.bar_label(bars, fmt="%.3f", padding=4, fontsize=8)
ax.set_xlabel("Errors (leading to goal or shot) per 90 mins")
ax.set_title("GK Error Rate per 90 mins — Lower is Better | PL 2025–26, GW31",
             fontweight="bold")
plt.tight_layout()
plt.savefig("charts/05_error_rate_per90.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: charts/05_error_rate_per90.png")

# --- Chart 6: High Claims per 90 mins ---
fig, ax = plt.subplots(figsize=(12, 7))
data = gks.sort_values("high_claims_per90", ascending=True)
bars = ax.barh(data["label"], data["high_claims_per90"], color="#9b59b6")
ax.axvline(data["high_claims_per90"].mean(), color="navy", linestyle="--", linewidth=1.2,
           label=f"Avg: {data['high_claims_per90'].mean():.2f}")
ax.bar_label(bars, fmt="%.2f", padding=4, fontsize=8)
ax.set_xlabel("High Claims per 90 mins")
ax.set_title("Aerial Dominance — High Claims per 90 | PL 2025–26, GW31",
             fontweight="bold")
ax.legend()
plt.tight_layout()
plt.savefig("charts/06_high_claims_per90.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: charts/06_high_claims_per90.png")

# --- Chart 7: Composite Ranking ---
rank_df = gks.dropna(subset=["save_pct", "prevented_per90", "clean_sheet_pct",
                              "errors_per90", "rating"]).copy()

def norm(series, invert=False):
    mn, mx = series.min(), series.max()
    if mx == mn:
        return pd.Series([0.5] * len(series), index=series.index)
    normalized = (series - mn) / (mx - mn)
    return 1 - normalized if invert else normalized

rank_df["score"] = (
    norm(rank_df["save_pct"])          * 0.30
    + norm(rank_df["prevented_per90"]) * 0.30
    + norm(rank_df["clean_sheet_pct"]) * 0.20
    + norm(rank_df["errors_per90"], invert=True) * 0.10
    + norm(rank_df["rating"])          * 0.10
)

rank_df = rank_df.sort_values("score", ascending=True)

fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(rank_df["label"], rank_df["score"], color="#2980b9")
ax.bar_label(bars, fmt="%.3f", padding=4, fontsize=8)
ax.set_xlabel("Composite Score (0–1)")
ax.set_title(
    "Composite GK Ranking (Save% 30% | xG-prevented 30% | CS% 20% | Errors 10% | Rating 10%)\n"
    "PL 2025–26, GW31",
    fontweight="bold",
)
plt.tight_layout()
plt.savefig("charts/07_composite_ranking.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: charts/07_composite_ranking.png")

print("\n=== TOP GK COMPOSITE RANKING ===")
top = rank_df[["player_name", "team_name", "save_pct", "goalsPrevented",
               "clean_sheet_pct", "errors_per90", "rating", "score"]
              ].sort_values("score", ascending=False)
top.columns = ["Player", "Team", "Save%", "Prevented", "CS%", "Err/90", "Rating", "Score"]
top["Score"] = top["Score"].round(3)
print(top.to_string(index=False))

# --- Chart 8: Scatter — Save% vs Goals Prevented ---
scatter_df = gks.dropna(subset=["save_pct", "goalsPrevented"])
fig, ax = plt.subplots(figsize=(11, 8))
bubble_sizes = scatter_df["appearances"] * 12
sc = ax.scatter(
    scatter_df["save_pct"],
    scatter_df["goalsPrevented"],
    s=bubble_sizes,
    alpha=0.7,
    c=scatter_df["rating"],
    cmap="RdYlGn",
    edgecolors="black",
    linewidths=0.5,
)
for _, row in scatter_df.iterrows():
    ax.annotate(
        row["player_name"].split()[-1],
        (row["save_pct"], row["goalsPrevented"]),
        textcoords="offset points",
        xytext=(6, 4),
        fontsize=7.5,
    )
ax.axhline(0, color="gray", linestyle="--", linewidth=0.8)
ax.axvline(scatter_df["save_pct"].mean(), color="gray", linestyle="--", linewidth=0.8)
plt.colorbar(sc, ax=ax, label="Match Rating")
ax.set_xlabel("Save Percentage (%)")
ax.set_ylabel("Goals Prevented (xG-based)")
ax.set_title(
    "Save % vs Goals Prevented — bubble size = appearances, colour = rating\n"
    "Top-right quadrant = elite performance | PL 2025–26, GW31",
    fontweight="bold",
)
plt.tight_layout()
plt.savefig("charts/08_scatter_save_vs_prevented.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: charts/08_scatter_save_vs_prevented.png")
