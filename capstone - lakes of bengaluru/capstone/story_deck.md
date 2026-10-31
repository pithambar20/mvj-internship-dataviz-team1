# Demo Day Presentation Deck: Lakes of Bengaluru

**Format:** 7-Slide Story Deck (7 Minutes Presentation + 3 Minutes Q&A)  
**Track:** Data Visualisation Track (DS5P3) | **Date:** 17 November 2026 (Demo Day)  
**Presented To:** MVJ Degree College Faculty & Industry Mentors  

---

## Slide 1: The Civic Question & Context (1 Min)
- **Title:** Lakes of Bengaluru: Mapping and Reviving an Urban Sponge
- **Context:** Bengaluru has evolved from a historic cascade of 1,000+ interconnected earthen tanks (keres) into a dense IT metropolis where remaining water bodies face rapid siltation, sewage influx, and encroachment.
- **The Core Question:** What is the spatial distribution, rejuvenation progress, and water quality across Bengaluru’s 207 municipal lakes, and what empirical evidence proves the success of nature-based restoration?
- **Audience:** BBMP Lakes Division, citizen lake trusts, and urban residents.

---

## Slide 2: Data Provenance & Cleaning Pipeline (1 Min)
- **Sources:** OpenCity.in & BBMP Open Data (Geospatial KML Placemarks, BBMP Custody Census, Ward-wise Assets, KSPCB Water Quality Reports).
- **Size:** 207 geospatial lake records, spanning 5,390.4 total acres across 8 civic zones.
- **Data Quality Fixes:**
  - Standardized messy zone names into 8 canonical BBMP zones.
  - Reconciled KML coordinate placemarks with administrative survey records.
  - Calculated standardized decimal acreage from disparate Acres/Guntas columns.

---

## Slide 3: Web Platform Architecture (1 Min)
- **3-Folder Modular Engineering:**
  - **`frontend/`:** Modern responsive client with interactive Leaflet city map, multi-criteria filter bar, before/after split sliders, and live data directory.
  - **`backend/`:** Python Flask REST API serving dynamic lake queries, summary KPIs, and Python data visualization pipelines.
  - **`UI/`:** Complete design system, ColorBrewer-certified tokens, WCAG AA accessibility specs, and reusable component templates.

---

## Slide 4: Live Demo (2 Min)
- **Feature 1: Interactive City Lake Map:**
  - Filter 207 lakes in real time by Zone (e.g. Mahadevapura), Status (Rejuvenated), Size, and Name.
  - Proportional circle markers and rich interactive popups with WQI, Dissolved Oxygen, and walking trails.
- **Feature 2: Interactive Before/After Story Slider:**
  - Wipe between degraded silt beds and restored constructed wetland parks (Jakkur, Kaikondrahalli, Agara, Bellandur).
- **Feature 3: Dynamic Data Explorer:**
  - Real-time tabular search, sorting, and one-click CSV export.

---

## Slide 5: Empirical Insights (Numbers, Not Adjectives) (1 Min)
- **Insight 1:** **51.7% Rejuvenation Progress:** 107 of 207 lakes are fully developed and fenced; Mahadevapura hosts 87 lakes (42% of city total).
- **Insight 2:** **Bellandur Outlier:** At **913.0 Acres**, Bellandur alone accounts for 16.9% of the total city surface basin (median lake size is 24.2 acres).
- **Insight 3:** **BOD Collapse by 94%:** Nature-based constructed wetlands at Jakkur Lake reduced Biochemical Oxygen Demand from **68 mg/L to 4.1 mg/L**, while Dissolved Oxygen surged from **0.8 mg/L to 7.4 mg/L**.

---

## Slide 6: Visualizations Suite (Matplotlib & Seaborn) (0.5 Min)
- 6 publication-grade Python visual graphics generated with pre-attentive design:
  - Stacked horizontal status distribution by zone.
  - Surface area distribution boxplot with mean anchors.
  - Multi-distribution KDE showing bimodal water quality separation.
  - Two-panel chemical transformation comparisons (DO vs BOD).
  - Encroachment vs biodiversity regression scatter plot ($r = -0.84$).
  - Institutional custodian breakdown.

---

## Slide 7: Recommendations & AI Governance (0.5 Min)
- **Civic Recommendation:** Mandate Jakkur-style constructed wetlands upstream of all inlet channels; prioritize anti-encroachment fencing in high-risk zones where biodiversity loss is severe.
- **AI Accountability:**
  - Used AI to draft regex parsers and explore Seaborn visualization parameters.
  - Every single coordinate, acreage calculation, and chemical ratio was independently verified and cross-checked with official BBMP records.
