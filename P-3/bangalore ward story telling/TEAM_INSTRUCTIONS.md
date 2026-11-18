# Bengaluru Ward Story — Three-member internship split

## Member responsibilities

### Member 1 — Data collection and preparation
- Download historical BBMP ward boundary GeoJSON and Census 2011 ward population CSV.
- Clean numeric columns and duplicates.
- Match ward IDs between the two sources.
- Save `shared_data/ward_population_clean.csv` and `shared_data/wards_matched.geojson`.
- Explain data sources, cleaning and join process.

### Member 2 — Plotly visualizations
- Use Member 1's two shared output files.
- Create the choropleth map, top-10 bar chart, gender grouped bar chart and gender-balance scatter plot.
- Save the charts as `charts/visualizations.html`.
- Explain chart types, hover details, and what each chart communicates.

### Member 3 — Storytelling and publishing
- Use Member 1's cleaned CSV and Member 2's HTML charts.
- Calculate and write three key messages from the data.
- Add annotations, page layout, data limitations and source links.
- Generate `index.html` in the project root.
- Publish `index.html` using GitHub Pages.

## Run order and folder layout
1. Member 1: open terminal in `Member_1_Data_Preparation` and run:
   `pip install pandas numpy requests`
   `python member1_data_preparation.py`
2. The generated `shared_data` folder is created in the project root beside the three member folders.
3. Member 2: open terminal in `Member_2_Visualizations` and run:
   `pip install pandas plotly`
   `python member2_visualizations.py`
4. Member 3: open terminal in `Member_3_Story_and_Publishing` and run:
   `pip install pandas`
   `python member3_story_html.py`
5. Final output is `index.html` in the project root.

**Important:** For Member 2 and Member 3, the `shared_data` folder must be at the project root. Keep the provided folder names unchanged because the scripts use relative paths. Run the scripts from their own member folders.

## Presentation checklist
- Member 1: show original sources, cleaned CSV, join and data-quality checks.
- Member 2: demonstrate map hover, zoom, bar chart, gender chart and scatter plot.
- Member 3: explain three evidence-based findings, limitations, HTML design and live published link.

## Data caution
This is a historical analysis using old 198-ward BBMP boundaries and Census 2011 population data. It is not a current map of the 369 GBA wards. Ward boundaries changed; do not claim these are current ward population figures.
