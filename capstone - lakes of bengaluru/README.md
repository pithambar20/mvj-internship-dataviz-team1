# Lakes of Bengaluru — Capstone Project (Option 3)

**Academic Year:** 2026–27 | BCA (Data Science) Final Year Internship (DS5P3)  
**Track:** Data Visualisation Track  
**Mentor:** Ajay Balamurugadas | **Evaluation Rubric:** Section 14 (100 Marks Total)  
**Theme:** Environmental Data Visualisation & Spatial Storytelling  
**Dataset:** Bengaluru Lakes Data and Reports (OpenCity.in / BBMP)

---

## 1. Project Overview & Quick Start

This project is a full-stack data visualization platform built to analyze, map, and communicate the environmental status of **207 lakes across Bengaluru**. It features an interactive geospatial city map, publication-grade Python visualizations (`matplotlib`, `seaborn`), an interactive before-and-after lake rejuvenation split slider, and a comprehensive master data explorer.

### Running the Platform:
1. **Start the Flask Backend:**
   ```bash
   cd backend
   python app.py
   ```
   *The server runs at:* `http://localhost:5000` (serves both API and the Web Client).

2. **Open the Website in Browser:**
   - Navigate to [`http://localhost:5000`](http://localhost:5000)
   - Alternatively, open [`frontend/index.html`](file:///c:/Users/admin/Documents/internship/frontend/index.html) directly in any browser (supported via built-in data fallback).

---

## 2. Three-Folder Architecture

```
internship/
├── frontend/                     <- Modern interactive responsive web client
│   ├── index.html                <- Single Page Application with 4 views
│   ├── css/                      <- style.css & components.css
│   ├── js/                       <- Leaflet map controller, stories, charts, app orchestrator
│   └── assets/charts/            <- High-resolution cached data visuals
│
├── backend/                      <- Flask Python API & data analysis engine
│   ├── app.py                    <- RESTful API endpoints (/api/lakes, /api/stats, /api/charts)
│   ├── chart_generator.py        <- Matplotlib & Seaborn visual generation pipeline
│   ├── data_pipeline.py          <- OpenCity KML & CSV parsing, joining, and cleaning
│   └── data/                     <- lakes_master.json, before_after_stories.json
│
├── UI/                           <- Design System & Specification
│   ├── UI_GUIDE.md               <- ColorBrewer accessibility, typography & UI principles
│   ├── design_tokens.json        <- Master design tokens
│   ├── style_guide.html          <- Living interactive component playground
│   └── components/               <- KPI cards, filter bar, split slider, chart cards
│
└── capstone/                     <- Capstone deliverables documentation
    ├── charter.md                <- One-page project charter
    ├── README.md                 <- Capstone analytical report (6 mandatory sections)
    └── story_deck.md             <- 7-slide Demo Day presentation deck
```

---

## 3. Data Visualizations Generated with Python (`matplotlib` & `seaborn`)

1. **`chart1_status_by_zone.png`** (Matplotlib): Stacked horizontal bar chart showing rejuvenation breakdown across 8 civic zones.
2. **`chart2_area_distribution.png`** (Seaborn): Boxplot with mean anchors displaying lake surface extents (highlighting Bellandur's 913-acre basin).
3. **`chart3_wqi_density.png`** (Seaborn): Multi-KDE probability density showing the bimodal separation in Water Quality Index (WQI).
4. **`chart4_before_after_metrics.png`** (Matplotlib): Two-panel horizontal comparison of Dissolved Oxygen surge and Biochemical Oxygen Demand (BOD) collapse.
5. **`chart5_encroachment_correlation.png`** (Seaborn): Linear regression demonstrating perimeter encroachment vs. biodiversity collapse ($r = -0.84$).
6. **`chart6_custodian_breakdown.png`** (Matplotlib): Proportional bar chart showing BBMP, BDA, and Forest Department stewardship.
