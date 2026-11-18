"""
MEMBER 3 — VISUAL STORY, ANNOTATIONS & HTML PAGE
Run after Member 2. Output: ../index.html
"""
from pathlib import Path
import pandas as pd
from html import escape

DATA = Path("../shared_data/ward_population_clean.csv")
CHARTS = Path("../Member_2_Visualizations/charts/visualizations.html")
OUT = Path("..")

df = pd.read_csv(DATA)
charts = CHARTS.read_text(encoding="utf-8")
largest = df.loc[df.POP_TOTAL.idxmax()]
smallest = df.loc[df.POP_TOTAL.idxmin()]
median = df.POP_TOTAL.median()
ratio_median = df.FEMALES_PER_1000_MALES.median()
high = df.loc[df.FEMALES_PER_1000_MALES.idxmax()]
low = df.loc[df.FEMALES_PER_1000_MALES.idxmin()]

insights = [
    ("01 — Population is unevenly distributed",
     f"{largest.WARD_NAME} has the highest recorded population ({int(largest.POP_TOTAL):,}), while {smallest.WARD_NAME} has the lowest ({int(smallest.POP_TOTAL):,})."),
    ("02 — Ward populations vary",
     f"The median ward population is {int(median):,}. Use the map and top-10 ranking to compare population concentrations."),
    ("03 — Gender balance differs",
     f"The median is {ratio_median:.1f} females per 1,000 males. {high.WARD_NAME} is highest ({high.FEMALES_PER_1000_MALES:.1f}); {low.WARD_NAME} is lowest ({low.FEMALES_PER_1000_MALES:.1f}).")
]
cards = "".join(
    f'<article><h3>{escape(t)}</h3><p>{escape(p)}</p></article>' for t,p in insights
)

html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bengaluru Ward Story</title>
<style>
body{{margin:0;background:#f3f5f7;color:#1d2935;font-family:Arial,sans-serif}}
header{{padding:42px max(20px,calc((100% - 1100px)/2));background:#20394d;color:white}}
h1{{font-size:42px;margin:8px 0}} header p{{max-width:800px;line-height:1.6}}
main{{max-width:1100px;margin:28px auto;padding:0 16px}}
section,article{{background:white;border:1px solid #e0e5e9;border-radius:12px;padding:16px;margin:14px 0}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}}
article h3{{color:#a53b48;font-size:16px}} article p{{line-height:1.55}}
.note{{line-height:1.65;color:#4d5b68}} footer{{text-align:center;padding:22px;color:#667}}
</style></head><body>
<header><small>INTERNSHIP PROJECT 03 · INTERACTIVE DATA STORY</small>
<h1>Bengaluru Ward Story</h1>
<p>Exploring historical BBMP ward population patterns using Census 2011 data, interactive maps and charts.</p></header>
<main><h2>Three key messages</h2><div class="cards">{cards}</div>
<h2>Explore the data</h2>{charts}
<section class="note"><h2>Data and limitations</h2>
This project uses historical BBMP 198-ward boundaries and Census 2011 population data.
It is not a map of the current 369 Greater Bengaluru Authority wards and should not be presented as current population data.
The analysis describes population counts and gender composition; it does not measure service quality, income, infrastructure access or population growth.
<br><br>Boundary source: DataMeet Municipal Spatial Data — Bangalore.
Population source: Bengaluru Census 2011 ward-wise data, republished by OpenCity.
<br><br><a href="https://projects.datameet.org/Municipal_Spatial_Data/bangalore/">DataMeet ward boundaries</a> ·
<a href="https://data.opencity.in/dataset/bengaluru-census-2011">OpenCity Census data</a>
</section></main><footer>Built with Python, Pandas and Plotly · Internship Project</footer>
</body></html>"""
output = OUT / "index.html"
output.write_text(html, encoding="utf-8")
print(f"MEMBER 3 COMPLETE — {output.resolve()} created.")
