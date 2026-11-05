"""
MEMBER 1 — DATA COLLECTION & PREPARATION
Run this first. Output:
  shared_data/ward_population_clean.csv
  shared_data/wards_matched.geojson
"""
from pathlib import Path
import json, re, requests
import pandas as pd
import numpy as np

OUT = Path("../shared_data")
OUT.mkdir(exist_ok=True)
DATA = Path("raw_data")
DATA.mkdir(exist_ok=True)

GEO_URL = "https://raw.githubusercontent.com/datameet/Municipal_Spatial_Data/master/Bangalore/BBMP_oldWards.geojson"
CSV_URL = "https://raw.githubusercontent.com/suvajit/opendata/master/BBMP/data/CSV/Bangalore_Ward_Population_2011.csv"

def download(url, path):
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    path.write_bytes(r.content)

download(GEO_URL, DATA / "wards.geojson")
download(CSV_URL, DATA / "population.csv")

df = pd.read_csv(DATA / "population.csv")
df.columns = [str(c).strip().upper().replace(" ", "_") for c in df.columns]
required = ["WARD_NO", "POP_TOTAL", "POP_M", "POP_F"]
missing = [c for c in required if c not in df.columns]
if missing:
    raise ValueError(f"Missing {missing}; CSV columns are {list(df.columns)}")

for c in ["WARD_NO", "POP_TOTAL", "POP_M", "POP_F"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df = df.dropna(subset=["WARD_NO", "POP_TOTAL"]).copy()
df["WARD_NO"] = df["WARD_NO"].astype(int)
df["POP_TOTAL"] = df["POP_TOTAL"].astype(int)
df["POP_M"] = df["POP_M"].fillna(0)
df["POP_F"] = df["POP_F"].fillna(0)
df["FEMALES_PER_1000_MALES"] = np.where(df["POP_M"] > 0, df["POP_F"] / df["POP_M"] * 1000, np.nan)
df = df.drop_duplicates(subset=["WARD_NO"], keep="first")

with open(DATA / "wards.geojson", encoding="utf-8") as f:
    geo = json.load(f)

def norm(s):
    return re.sub(r"[^A-Z0-9]", "", str(s).upper())

props = [x.get("properties", {}) for x in geo.get("features", [])]
if not props:
    raise ValueError("GeoJSON has no ward features.")
keymap = {norm(k): k for k in props[0].keys()}
ward_key = next((keymap[k] for k in ["WARDNO", "WARDNUMBER", "WARDNUM", "WARD"] if k in keymap), None)
if ward_key is None:
    raise ValueError(f"Cannot find ward number field. GeoJSON fields: {list(props[0])}")

name_key = next((keymap[k] for k in ["WARDNAME", "NAME"] if k in keymap), None)
for feature in geo["features"]:
    raw = feature["properties"].get(ward_key)
    try:
        feature["properties"]["WARD_JOIN"] = int(float(str(raw).strip()))
    except (TypeError, ValueError):
        feature["properties"]["WARD_JOIN"] = None

valid = set(df["WARD_NO"])
geo["features"] = [f for f in geo["features"] if f["properties"].get("WARD_JOIN") in valid]
geo_ids = {f["properties"]["WARD_JOIN"] for f in geo["features"]}
df = df[df["WARD_NO"].isin(geo_ids)].copy()

name_map = {}
for f in geo["features"]:
    p = f["properties"]
    wid = p.get("WARD_JOIN")
    if wid is not None:
        name_map[wid] = str(p.get(name_key, f"Ward {wid}")) if name_key else f"Ward {wid}"
df["WARD_NAME"] = df["WARD_NO"].map(name_map).fillna("Ward " + df["WARD_NO"].astype(str))

if df.empty:
    raise ValueError("No matching ward numbers. Ensure both files are from the same historical ward boundary version.")

lookup = df.set_index("WARD_NO").to_dict("index")
for f in geo["features"]:
    row = lookup[f["properties"]["WARD_JOIN"]]
    f["properties"]["POP_TOTAL"] = int(row["POP_TOTAL"])
    f["properties"]["WARD_NAME_CENSUS"] = row["WARD_NAME"]

df.to_csv(OUT / "ward_population_clean.csv", index=False)
with open(OUT / "wards_matched.geojson", "w", encoding="utf-8") as f:
    json.dump(geo, f)

print("MEMBER 1 COMPLETE")
print("Matched wards:", len(df))
print("Total population:", f"{int(df.POP_TOTAL.sum()):,}")
print("Outputs saved in shared_data/")
