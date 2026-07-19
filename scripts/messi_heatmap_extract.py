import json
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd

# %%
SEASONS = {
    37: "2004/2005", 38: "2005/2006", 39: "2006/2007", 40: "2007/2008",
    41: "2008/2009", 21: "2009/2010", 22: "2010/2011", 23: "2011/2012",
    24: "2012/2013", 25: "2013/2014", 26: "2014/2015", 27: "2015/2016",
    2: "2016/2017", 1: "2017/2018", 4: "2018/2019", 42: "2019/2020",
    90: "2020/2021",
}

MATCHES_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/11/{}.json"
EVENTS_URL = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{}.json"

# %% [markdown]
# ## Step 1: get every Barcelona match_id for each season

# %%
def fetch_json(url, timeout=20):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.load(r)


season_matches = {}  # season_id -> {"season_name":..., "match_ids":[...]}
for sid, name in SEASONS.items():
    data = fetch_json(MATCHES_URL.format(sid))
    barca_ids = [
        m["match_id"] for m in data
        if m["home_team"]["home_team_name"] == "Barcelona"
        or m["away_team"]["away_team_name"] == "Barcelona"
    ]
    season_matches[sid] = {"season_name": name, "match_ids": barca_ids}
    print(f"{name}: {len(barca_ids)} matches")

# %% [markdown]
# ## Step 2: pull events for every match, keep only Messi's located events
#
# This is ~500 events files (~3MB each, ~1.5GB total). Runs threaded
# since it's network-bound. Takes a few minutes depending on connection.

# %%
def extract_messi_locations(match_id, season_name):
    """Return list of (season_name, x, y, event_type, minute) for one match."""
    try:
        events = fetch_json(EVENTS_URL.format(match_id))
    except Exception as e:
        print(f"  match {match_id} failed: {e}")
        return []

    rows = []
    for e in events:
        player = e.get("player", {})
        if not player or "Messi" not in player.get("name", ""):
            continue
        loc = e.get("location")
        if not loc:
            continue
        rows.append({
            "season": season_name,
            "x": loc[0],
            "y": loc[1],
            "event_type": e.get("type", {}).get("name"),
            "minute": e.get("minute"),
            "match_id": match_id,
        })
    return rows


all_rows = []
jobs = []
with ThreadPoolExecutor(max_workers=16) as pool:
    for sid, info in season_matches.items():
        for mid in info["match_ids"]:
            jobs.append(pool.submit(extract_messi_locations, mid, info["season_name"]))

    done = 0
    for fut in as_completed(jobs):
        all_rows.extend(fut.result())
        done += 1
        if done % 50 == 0:
            print(f"{done}/{len(jobs)} matches processed...")

print(f"\nTotal Messi located events: {len(all_rows)}")

# %% [markdown]
# ## Step 3: save to CSV

# %%
df = pd.DataFrame(all_rows)
df.to_csv("messi_locations_by_season.csv", index=False)
df.groupby("season").size().sort_index()

# %% [markdown]
# ## Step 4 (optional): quick heatmap sanity check for one season

# %%
import matplotlib.pyplot as plt
import numpy as np

season_to_plot = "2014/2015"
sub = df[df["season"] == season_to_plot]

plt.figure(figsize=(6, 9))
plt.hist2d(sub["x"], sub["y"], bins=30, range=[[0, 120], [0, 80]], cmap="inferno")
plt.gca().invert_yaxis()
plt.title(f"Messi heatmap — {season_to_plot}")
plt.show()

# %% [markdown]
# ## Notes for building the animated slider version
#
# - `df` has one row per Messi touch/event with pitch (x, y) for every
#   season from 2004/05 to 2020/21 - this is exactly what feeds the
#   year-by-year heatmap blob like the Instagram reel.
# - For the animation, bin each season into a 2D histogram (or KDE via
#   `scipy.stats.gaussian_kde`), normalize, then interpolate between
#   consecutive seasons' grids frame-by-frame for smooth morphing.
# - x runs 0-120 (length), y runs 0-80 (width). Flip y if you want
#   Messi's actual side of the pitch oriented like the reel.
# - Bring this CSV back to me any time and I'll build the interactive
#   widget / video / polished script around it.
