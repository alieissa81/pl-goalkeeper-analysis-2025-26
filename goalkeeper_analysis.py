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
