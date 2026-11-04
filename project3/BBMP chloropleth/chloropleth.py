# ============================================================
# BBMP WARD PUBLIC GOODS CHOROPLETH MAP
# Interactive Plotly map + HTML export
# ============================================================

# Install dependencies before running: python -m pip install pandas plotly

import json
import re
import unicodedata
from pathlib import Path

import pandas as pd
import plotly.express as px

# ------------------------------------------------------------
# 1. LOAD THE LOCAL DATA FILES
# ------------------------------------------------------------

data_dir = Path(__file__).resolve().parent
geo_file = data_dir / "BBMP-wards.geojson"
csv_file = data_dir / "BBMP Ward-wise Public Goods Data.csv"

for data_file in (geo_file, csv_file):
    if not data_file.is_file():
        raise FileNotFoundError(f"Required data file not found: {data_file}")

# ------------------------------------------------------------
# 2. READ THE FILES
# ------------------------------------------------------------

with geo_file.open("r", encoding="utf-8") as f:
    geojson = json.load(f)

df = pd.read_csv(csv_file)
df.columns = df.columns.astype(str).str.strip()

if "features" not in geojson or not geojson["features"]:
    raise ValueError("The GeoJSON file has no ward features.")

print("\nCSV columns:")
print(df.columns.tolist())

print("\nFirst five CSV rows:")
print(df.head())

print("\nGeoJSON ward properties:")
print(list(geojson["features"][0]["properties"].keys()))

print("\nNumber of GeoJSON features:", len(geojson["features"]))
print("Number of CSV rows:", len(df))

# ------------------------------------------------------------
# 3. NORMALIZE WARD NAMES FOR MATCHING
# ------------------------------------------------------------

def normalize(value):
    if pd.isna(value):
        return ""
    value = unicodedata.normalize("NFKD", str(value))
    value = value.lower().strip()
    value = re.sub(r"\bward\b", "", value)
    value = re.sub(r"[^a-z0-9]", "", value)
    return value

# Find possible ward-related columns
candidates = [
    c for c in df.columns
    if any(word in c.lower() for word in
           ["ward", "name", "number", "no."])
]

properties = list(geojson["features"][0]["properties"].keys())

if not candidates:
    raise ValueError(
        "Could not identify a ward column in the CSV. "
        "Check the printed CSV columns."
    )

# Find the best matching pair of ward fields
best_match = None

for prop in properties:
    geo_names = {
        normalize(feature["properties"].get(prop))
        for feature in geojson["features"]
    }
    geo_names.discard("")

    for col in candidates:
        csv_names = df[col].map(normalize)
        overlap = csv_names[csv_names.isin(geo_names)].nunique()

        if best_match is None or overlap > best_match[0]:
            best_match = (overlap, prop, col)

if best_match is None or best_match[0] == 0:
    raise ValueError(
        "No ward names matched. Compare the CSV columns and "
        "GeoJSON properties printed above."
    )

match_count, geo_ward_field, csv_ward_field = best_match

print("\nGeoJSON ward field:", geo_ward_field)
print("CSV ward field:", csv_ward_field)
print("Distinct matching ward names:", match_count)

# Create a matching key
df["_ward_key"] = df[csv_ward_field].map(normalize)

for feature in geojson["features"]:
    feature["properties"]["_ward_key"] = normalize(
        feature["properties"].get(geo_ward_field)
    )

# ------------------------------------------------------------
# 4. IDENTIFY NUMERIC PUBLIC-GOODS MEASURES
# ------------------------------------------------------------

exclude_columns = {
    csv_ward_field,
    "_ward_key"
}

numeric_columns = []

for col in df.columns:
    if col in exclude_columns:
        continue

    converted = pd.to_numeric(df[col], errors="coerce")

    if converted.notna().sum() > 0:
        df[col] = converted
        numeric_columns.append(col)

if not numeric_columns:
    raise ValueError(
        "No numeric facility columns were found in the CSV."
    )

print("\nAvailable numeric measures:")
for i, col in enumerate(numeric_columns, 1):
    print(f"{i}. {col}")

# ------------------------------------------------------------
# 5. SELECT THE PUBLIC GOOD TO DISPLAY
# ------------------------------------------------------------

choice = input(
    "\nEnter a measure number, or press Enter for the first measure: "
).strip()

if choice:
    index = int(choice) - 1
    if index < 0 or index >= len(numeric_columns):
        raise ValueError("Invalid measure number.")
    metric = numeric_columns[index]
else:
    metric = numeric_columns[0]

print("\nSelected measure:", metric)

# ------------------------------------------------------------
# 6. PREPARE THE WARD DATA
# ------------------------------------------------------------

# Keep only rows with a valid ward key and selected measure
df = df[df["_ward_key"] != ""].copy()
df = df.dropna(subset=[metric])

# Duplicate ward keys can create ambiguous map values.
# Stop rather than silently selecting an arbitrary record.
duplicates = df["_ward_key"].duplicated(keep=False)

if duplicates.any():
    print("\nDuplicate ward entries found:")
    print(df.loc[duplicates, [csv_ward_field, metric]].head(20))
    raise ValueError(
        "Resolve duplicate ward rows before mapping. "
        "Do not sum rows unless they represent separate facilities."
    )

# Keep only map features whose ward keys occur in the CSV
data_keys = set(df["_ward_key"])

matched_features = [
    feature for feature in geojson["features"]
    if feature["properties"]["_ward_key"] in data_keys
]

if not matched_features:
    raise ValueError("No ward features matched the CSV data.")

matched_geojson = {
    "type": "FeatureCollection",
    "features": matched_features
}

matched_keys = {
    feature["properties"]["_ward_key"]
    for feature in matched_features
}

map_df = df[df["_ward_key"].isin(matched_keys)].copy()

print("\nMatched map features:", len(matched_features))
print("Matched CSV wards:", len(map_df))
print("Unmatched CSV rows:", len(df) - len(map_df))

# ------------------------------------------------------------
# 7. CREATE THE INTERACTIVE CHOROPLETH
# ------------------------------------------------------------

fig = px.choropleth_map(
    map_df,
    geojson=matched_geojson,
    locations="_ward_key",
    featureidkey="properties._ward_key",
    color=metric,
    hover_name=csv_ward_field,
    hover_data={
        metric: True,
        "_ward_key": False
    },
    color_continuous_scale="YlGnBu",
    map_style="carto-positron",
    center={"lat": 12.9716, "lon": 77.5946},
    zoom=9,
    opacity=0.78,
    title=f"BBMP Ward-wise Distribution of {metric}"
)

fig.update_layout(
    title_x=0.5,
    margin={"r": 10, "t": 60, "l": 10, "b": 10},
    coloraxis_colorbar={
        "title": metric
    }
)

# Display map
fig.show()

# ------------------------------------------------------------
# 8. EXPORT THE INTERACTIVE MAP TO HTML
# ------------------------------------------------------------

output_file = data_dir / "BBMP_Public_Goods_Choropleth.html"

fig.write_html(
    output_file,
    include_plotlyjs=True,
    full_html=True
)

print("\nSUCCESS! Your interactive map is ready.")
print("Output file:", output_file)