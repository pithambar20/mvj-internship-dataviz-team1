# Project 3 Overview

This project contains several data-visualization and analysis files grouped by topic.

- `bangalore ward story telling/` — the main project. It includes data preparation scripts, cleaned ward data, chart generation, and the final HTML story about Bengaluru ward population.
- `interactive plots/` — interactive HTML plots created from Bengaluru house-price data.
- `python plots/` — Python scripts and static chart images for the same dataset.
- `BBMP chloropleth/` — ward-level geographic visualization using BBMP public goods data.
- `tableau/` — Tableau-related files and source data.
- `learning tools/` — notes and learning material shared by the team.

Overall, this project shows the full workflow from raw data to cleaned datasets, visualizations, and presentation outputs.







## (1) Learning tools

The `learning tools/` folder contains short notes written by team members while learning data visualization tools and app-building workflows. These files focus on practical beginner-level learning rather than final project outputs.

- `nithin_tools_learned.md` — notes on Plotly and Streamlit, including how interactive charts work and how a Python script can become a simple web app.
- `pithambar_tools_learned.md` — a beginner-friendly explanation of Plotly and Streamlit, with examples of creating charts and small dashboard-style apps.
- `vimal tools learned.md` — summary notes on Plotly and Streamlit, with examples of creating scatter plots and using Streamlit to display them in a browser.

These files show the team’s early exploration of data visualization libraries and how they can be used together to build interactive dashboards in Python.








## (2) Python plots

The `python plots/` folder contains static visualizations built from the Bengaluru house-price dataset. Each member was assigned a specific type of chart.

- `Pithambar` — created the violin plot for Bengaluru house data using `violin_plot.py` and saved `bengaluru_violin_plot.png`.

![Bengaluru violin plot](./python%20plots/bengaluru_violin_plot.png)

- `Vimal` — created heatmap and box plot visualizations using `heatmap.py` and `boxplot.py`, generating the heatmap PNG files and a box plot output.

![Bengaluru box plot](./python%20plots/bengaluru_box_plot.png)

- `Nithin` — created the histogram for house-price distribution with `histogram.py`, saved as `house_price_histogram.png`.

![House price histogram](./python%20plots/house_price_histogram.png)

The folder also includes the source dataset `Bengaluru_House_Data.xlsx` and the generated plot images used for basic exploratory data analysis.








## (3) Interactive plots

The `interactive plots/` folder contains browser-based Plotly visualizations exported as HTML files. These are the interactive versions of the earlier static exploratory charts.

- `Pithambar` — created the interactive heatmap in `interactive_heatmap.py` and exported it as `bengaluru_interactive_heatmap.html`.
- `Vimal` — created the interactive histogram and box plot in Python and exported them as `interactive_house_price_histogram.html` and `interactive_house_price_boxplot.html`.
- `Nithin` — created the interactive violin plot in `interactive_violin_plot.py` and exported it as `bengaluru_interactive_violin_plot.html`.

The folder also includes an animated time-chart, `animated_house_price_time_chart.html`, created from the same dataset. These files can be opened directly in a browser to explore the data interactively.









## (4) Choropleth

The `BBMP chloropleth/` folder contains BBMP ward-wise public goods data and an interactive choropleth map.

- `Vimal` — collected the ward-wise public goods data and created the GeoJSON boundary file.
- `Pithambar` — created the choropleth map using the public goods data and ward boundaries.
- `Nithin` — exported the map as `BBMP_Public_Goods_Choropleth.html`.

The folder includes the source data in CSV and Excel formats, the `BBMP-wards.geojson` map boundaries, and `chloropleth.py` to generate the interactive map.








## (5) Bengaluru ward story

The `bangalore ward story telling/` folder contains the data-preparation, visualization, and publishing workflow for a historical Bengaluru ward population story.

- `Nithin` — prepared the ward population data and matched it with ward boundaries.
- `Pithambar` — created Python visualizations, including an interactive map and population charts.
- `Vimal` — assembled the data story and published the final HTML page.

The folder includes the member scripts, source and cleaned data, generated charts, and final `index.html` story.