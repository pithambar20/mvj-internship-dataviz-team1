"""
MEMBER 2 — INTERACTIVE PLOTLY VISUALIZATIONS
Run after Member 1. Output: charts/visualizations.html
"""
from pathlib import Path
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

DATA = Path("../shared_data")
OUT = Path("charts")
OUT.mkdir(exist_ok=True)
df = pd.read_csv(DATA / "ward_population_clean.csv")
with open(DATA / "wards_matched.geojson", encoding="utf-8") as f:
    geo = json.load(f)

map_function = px.choropleth_map if hasattr(px, "choropleth_map") else px.choropleth_mapbox
map_style = {"map_style": "carto-positron"} if hasattr(px, "choropleth_map") else {"mapbox_style": "carto-positron"}
map_fig = map_function(
    df, geojson=geo, locations="WARD_NO", featureidkey="properties.WARD_JOIN",
    color="POP_TOTAL", hover_name="WARD_NAME",
    hover_data={"WARD_NO": True, "POP_TOTAL": ":,", "POP_M": ":,", "POP_F": ":,"},
    color_continuous_scale="YlOrRd", **map_style,
    center={"lat": 12.9716, "lon": 77.5946}, zoom=9.1, opacity=.78,
    title="Bengaluru ward population — Census 2011"
)
map_fig.update_layout(height=650, margin=dict(l=5,r=5,t=55,b=5))

top = df.nlargest(10, "POP_TOTAL").sort_values("POP_TOTAL")
rank_fig = px.bar(top, x="POP_TOTAL", y="WARD_NAME", orientation="h",
                  title="Top 10 most populated wards",
                  labels={"POP_TOTAL":"Population","WARD_NAME":"Ward"})
rank_fig.update_layout(height=450)

gender_fig = go.Figure()
gender_fig.add_bar(x=df.WARD_NAME, y=df.POP_M, name="Male")
gender_fig.add_bar(x=df.WARD_NAME, y=df.POP_F, name="Female")
gender_fig.update_layout(title="Male and female population by ward", barmode="group",
                         height=480, xaxis_tickangle=-65,
                         yaxis_title="Population")

ratio_fig = px.scatter(
    df, x="POP_M", y="POP_F", size="POP_TOTAL",
    color="FEMALES_PER_1000_MALES", hover_name="WARD_NAME",
    hover_data={"POP_TOTAL":":,", "FEMALES_PER_1000_MALES":":.1f"},
    title="Gender balance across wards",
    labels={"POP_M":"Male population","POP_F":"Female population",
            "FEMALES_PER_1000_MALES":"Females per 1,000 males"}
)
ratio_fig.update_layout(height=470)

figures = [map_fig, rank_fig, gender_fig, ratio_fig]
parts = []
for i, fig in enumerate(figures):
    parts.append(fig.to_html(full_html=False, include_plotlyjs="cdn" if i == 0 else False))
(OUT / "visualizations.html").write_text("\n".join(parts), encoding="utf-8")
print("MEMBER 2 COMPLETE — charts/visualizations.html created.")
