# Capstone Project Charter: Lakes of Bengaluru (Option 3)

**Academic Year:** 2026–27 | BCA (Data Science) Final Year Internship (DS5P3)  
**Track:** Data Visualisation Track  
**Mentor:** Ajay Balamurugadas | **Evaluation Rubric:** Section 14 (Capstone Deliverables)  
**Author:** Team Lakes of Bengaluru  
**Date:** 10 November 2026 (Day 25 Capstone Kickoff)  

---

## 1. Project Overview & The Civic Question

### Core Question:
> *"What is the spatial distribution, rejuvenation progress, ecological water quality, and encroachment risk across Bengaluru's 207 municipal lakes, and how do nature-based engineering interventions (constructed wetlands and STPs) measurably transform dying water bodies into thriving community urban sponges?"*

### Who It Is For:
- **BBMP Lakes Division Engineers:** Identifying priority zones requiring urgent desilting, sewage diversion, and anti-encroachment fencing.
- **Urban Planners & Citizen Lake Stewards (e.g. MAPSAS, Friends of Lakes):** Demonstrating the quantitative return-on-investment of community co-management models.
- **General Public & Commuters:** Exploring neighborhood water bodies, verifying walking trail infrastructure, and inspecting local water quality ratings.

---

## 2. Success Measures & Key Performance Indicators (KPIs)

| Success Dimension | Metric Target | Achieved in Project |
| :--- | :--- | :--- |
| **Spatial Coverage** | All 8 BBMP civic zones (> 180 lakes) | **207 lakes** mapped with exact GPS coordinates |
| **Rejuvenation Tracking** | Quantify % of lakes developed vs pending | **107 lakes (51.7%)** developed; **37 (17.9%)** in progress |
| **Water Quality Assessment**| Track Biochemical Oxygen Demand (BOD) & DO | Documented **78%–94% BOD reduction** post-restoration |
| **Technical Depth** | Multi-folder web architecture with Python visuals | Full **`frontend`**, **`backend`**, and **`UI`** architecture with **Matplotlib & Seaborn** |

---

## 3. Technology Architecture & 3-Folder Structure

```
c:\Users\admin\Documents\internship\
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
└── UI/                           <- Design System & Specification
    ├── UI_GUIDE.md               <- ColorBrewer accessibility, typography & UI principles
    ├── design_tokens.json        <- Master design tokens
    ├── style_guide.html          <- Living interactive component playground
    └── components/               <- KPI cards, filter bar, split slider, chart cards
```

---

## 4. UI / UX Wireframe Layout (Paper Sketch Translation)

```
┌────────────────────────────────────────────────────────────────────────┐
│  [💧] LAKES OF BENGALURU          [Map]  [Python Visuals]  [Before/After] [Directory]│
├────────────────────────────────────────────────────────────────────────┤
│  [207 Lakes]   [107 Rejuvenated (52%)]   [5,390 Acres]   [17 High Encroachment Risk]  │
├────────────────────────────────────────────────────────────────────────┤
│  FILTERS: [Zone: All ▼] [Status: All ▼] [Size: All ▼] [Search: ____________] [Reset] │
├────────────────────────────────────────┬───────────────────────────────┤
│                                        │  WATER BODIES DIRECTORY       │
│                                        ├───────────────────────────────┤
│        INTERACTIVE LEAFLET             │  Bellandur Lake (913 ac)      │
│        CITY LAKES MAP                  │  Jakkur Lake (160 ac)         │
│        (Colored Pins by Status)        │  Ulsoor Lake (123 ac)         │
│                                        │  Agara Lake (98 ac)           │
│        - Click pin to view stats       │  Kaikondrahalli Lake (48 ac)  │
│        - Zoom / pan into neighborhood  │  Sankey Tank (37 ac)          │
│                                        │  ... [Click to Pan & Inspect] │
└────────────────────────────────────────┴───────────────────────────────┘
```
