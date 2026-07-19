# Messi Heatmap — Full Career (2004–2024)

An animated heatmap tracing Lionel Messi's on-pitch positioning across his entire tracked career: Barcelona, PSG, Argentina (World Cups & Copa América), and his first season at Inter Miami (MLS).

23 real seasons/tournaments, 4 of them split into first/second halves for finer resolution, giving 27 total frames smoothly morphed together.

![Messi Heatmap preview](outputs/gif/messi_heatmap_vertical.gif)

Full quality video: [messi_heatmap_vertical.mp4](output/video/messi_heatmap_vertical.mp4)

## What's inside

```
scripts/    → the notebook that builds everything from raw event data
data/       → filtered/cleaned input data (raw events + season summary)
outputs/
  gif/      → vertical + horizontal animated heatmaps
  video/    → same, as MP4
```

## Data source

Built from **StatsBomb / Hudl's free open-data release** (https://github.com/hudl/open-data) — event-level (x, y) location data for every tracked touch across La Liga, Champions League, Copa del Rey, Ligue 1, FIFA World Cup, Copa América, and MLS.

Raw event/match files are **not included in this repo** (thousands of files, several GB, and not mine to bulk-redistribute) — only the filtered dataset of Messi's own located events (`data/messi_input_data.xlsx`) is included, alongside the script that regenerates it from a local copy of the open-data repo.

## Coverage

|Competition|Seasons|
|---|---|
|La Liga (Barcelona)|2004/05 – 2020/21|
|Ligue 1 (PSG)|2021/22, 2022/23|
|MLS (Inter Miami)|2023 (partial — first release only)|
|FIFA World Cup|2018, 2022|
|Copa América|2024|

World Cup 2026 is **not included** — StatsBomb/Hudl's open-data releases for major tournaments typically lag months behind the event itself, so no (x, y) event data exists publicly yet as of this tournament's conclusion.

## Rebuilding it yourself

1. Clone `hudl/open-data` locally (or download the specific competitions you need).
2. Point `DATA_DIR` in `scripts/messi_heatmap_full_career.ipynb` at your local copy.
3. Run the notebook cells in order — it walks through match discovery, event filtering, density-grid building, and exporting all formats.

## Attribution

Data sourced from **StatsBomb / Hudl open-data** (https://github.com/hudl/open-data), used under their free-for-research license. Please credit StatsBomb if you build on this.