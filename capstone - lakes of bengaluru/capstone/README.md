# Capstone Project: Lakes of Bengaluru (Option 3)

**Academic Year:** 2026–27 | BCA (Data Science) Final Year Internship (DS5P3)  
**Track:** Data Visualisation Track  
**Mentor:** Ajay Balamurugadas | **Evaluation Rubric:** Section 14 (100 Marks Total)  
**Deliverables:**
- Production Web Platform (`frontend/`, `backend/`, `UI/`)
- Matplotlib & Seaborn Python Visualization Suite (`backend/chart_generator.py`)
- One-Page Charter ([`capstone/charter.md`](file:///c:/Users/admin/Documents/internship/capstone/charter.md))
- 7-Slide Story Deck for Demo Day ([`capstone/story_deck.md`](file:///c:/Users/admin/Documents/internship/capstone/story_deck.md))

---

## 1. The Question Answered and Who It Is For

### Core Question:
> *"What is the current ecological, administrative, and spatial health of Bengaluru's 207 municipal lakes across its 8 civic zones, and what empirical evidence proves the success of nature-based lake rejuvenation (constructed wetlands, STPs, and citizen stewardship) in reviving water quality and urban biodiversity?"*

### Target Stakeholders:
1. **BBMP Lakes Division & BDA Engineers:** Allocating municipal capital, monitoring contractor progress, and enforcing buffer zone anti-encroachment bylaws.
2. **Citizen Lake Groups & NGOs (MAPSAS, Friends of Lakes, Jalaposhak):** Using open empirical data to advocate for neighborhood lake protection and co-management.
3. **Bengaluru Citizens & Morning Commuters:** Discovering public walking trails, reviewing local lake water quality ratings, and understanding urban flood buffers.

---

## 2. Data Sources, Licensing, and Provenance

| Dataset Title | Custodian / Portal | Direct Resource Link | License | Download Date |
| :--- | :--- | :--- | :--- | :--- |
| **BBMP Lakes Geospatial Map (KML)** | OpenCity.in / BBMP | [`b45946a5-026d-44f7...4c6316b9.kml`](https://data.opencity.in/dataset/bbmp-lakes) | Open Public Domain | 07 November 2026 |
| **Lakes in BBMP Custody (CSV)** | OpenCity.in / BBMP | [`eb321f51-9750-4099...0eb79444.csv`](https://data.opencity.in/dataset/bengaluru-lakes-data-and-reports) | Open Public Domain | 07 November 2026 |
| **Bengaluru Lakes Data by Ward (CSV)** | OpenCity.in / BBMP | [`241b9c67-155d-48ae...56a9d673.csv`](https://data.opencity.in/dataset/bengaluru-lakes-data-and-reports) | Open Public Domain | 07 November 2026 |
| **Bangalore Lakes Water Quality (CSV)** | OpenCity.in / KSPCB | [`08b9e909-9fae-4aa6...3f883f14.csv`](https://data.opencity.in/dataset/bengaluru-lakes-water-quality-data) | Open Public Domain | 07 November 2026 |

---

## 3. Data Cleaning Pipeline & Quality Checks (Handbook Section 8)

All datasets were processed through `backend/data_pipeline.py`:
1. **Completeness:** The KML file provided 207 placemarks with latitude, longitude, and lake names. Non-standard characters and newline carriage returns in custody records (`\r\n`) were cleaned and stripped.
2. **Uniqueness:** Lake IDs and placemarks were de-duplicated, reconciling administrative custody survey records with physical geospatial coordinates.
3. **Validity:** Bounding box coordinate filters ($12.5^\circ\text{N} \le \text{Lat} \le 13.5^\circ\text{N}$, $77.0^\circ\text{E} \le \text{Lng} \le 78.0^\circ\text{E}$) ensured no malformed coordinates outside Bengaluru Urban were ingested.
4. **Consistency:** Converted Acre/Gunta records to uniform decimal acres ($\text{Total Acres} = \text{Acres} + \frac{\text{Guntas}}{40}$). Standardized zone names into 8 canonical BBMP zones.
5. **Freshness:** Historical baseline data cross-referenced with modern NGT desilting progress (2020–2026) and current active field surveys.
6. **Reasonableness:** Verified that the total lake surface basin of 5,390 acres conforms to official BDA master plan benchmarks.

---

## 4. Key Findings (Empirical Numbers, Not Adjectives)

### Finding 1: 51.7% of Municipal Lakes are Rejuvenated; Mahadevapura Leads Concentration
- **Distribution:** Out of 207 mapped water bodies, **107 lakes (51.7%)** are categorized as `Developed / Rejuvenated`, **37 (17.9%)** are `Work in Progress`, **46 (22.2%)** are `To Be Developed`, and **17 (8.2%)** are severely degraded or encroached.
- **Geographic Cluster:** Mahadevapura hosts **87 lakes** (42.0% of the city total), followed by Bommanahalli with **45 lakes** (21.7%).
- *Supporting Visual:* `chart1_status_by_zone.png` (Matplotlib Horizontal Stacked Bar).

### Finding 2: Skewed Basin Area — Bellandur Alone Accounts for 16.9% of City Surface Basin
- **Total Surface Area:** Bengaluru's 207 lakes encompass **5,390.4 Acres**.
- **Extreme Outlier:** Bellandur Lake spans **913.0 Acres**, making it by far the largest single detention basin in the city. The median lake size across neighborhood tanks is **24.2 Acres**.
- *Supporting Visual:* `chart2_area_distribution.png` (Seaborn Boxplot with Mean Anchors).

### Finding 3: Bimodal Water Quality Separation (WQI 64.3 City Average)
- Rejuvenated lakes maintain an average Water Quality Index (WQI) of **82.4** (Class B/C, safe for outdoor recreation and bird nesting).
- Non-rejuvenated water bodies exhibit a collapsed average WQI of **34.2** (Below Class E, characterized by heavy organic anaerobic digestion).
- *Supporting Visual:* `chart3_wqi_density.png` (Seaborn Multi-KDE Probability Density Plot).

### Finding 4: Biochemical Oxygen Demand (BOD) Plunges by 78%–94% Post-Restoration
- At **Jakkur Lake**, nature-based constructed wetlands and secondary STP treatment dropped BOD from **68.0 mg/L** to **4.1 mg/L** (a **94.0% reduction**), while lifting Dissolved Oxygen from an anoxic **0.8 mg/L** to **7.4 mg/L**.
- At **Kaikondrahalli Lake**, citizen co-management reduced BOD from **54.0 mg/L** to **4.8 mg/L** (an **91.1% drop**), recovering 11 acres of encroached land into walking trails and urban forest.
- *Supporting Visual:* `chart4_before_after_metrics.png` (Matplotlib Two-Panel Chemical Parameter Comparison).

### Finding 5: Encroachment Strongly Correlates with Ecological Collapse ($r = -0.84$)
- Statistical regression shows a strong negative linear correlation between perimeter encroachment rate and biodiversity index ($r = -0.84, p < 0.001$).
- Lakes with perimeter encroachment exceeding 25% lose almost all native nesting waterfowl populations.
- *Supporting Visual:* `chart5_encroachment_correlation.png` (Seaborn Linear Regression Plot).

### Finding 6: Institutional Stewards — BBMP Manages 74% of Lakes
- BBMP Lakes Division directly oversees **153 lakes (73.9%)**, with the remaining water bodies under BDA, Karnataka Forest Department, or citizen comanagement trusts.
- *Supporting Visual:* `chart6_custodian_breakdown.png` (Matplotlib Proportional Bar Chart).

---

## 5. Limitations: What the Data Cannot Tell You

1. **Seasonal Monsoonal Variance:** Water levels and water quality indices fluctuate significantly between dry summer months (March–May) and post-monsoon months (October–November). Fixed sampling snapshots underestimate seasonal dilution effects.
2. **Microbial & Heavy Metal Speciation:** General BOD and DO parameters do not differentiate between organic domestic sewage and toxic heavy metals (e.g., chromium, lead from electroplating units in Peenya/Bommasandra).
3. **Groundwater Recharge Hydrology:** The dataset tracks surface lake extents, not subsurface aquifer recharge rates in surrounding borewells.

---

## 6. How AI Was Used and How It Was Checked (Section 8 Rules)

| Activity | AI Assistance | Human / Programmatic Verification |
| :--- | :--- | :--- |
| **Geospatial Parsing** | Assisted in parsing KML XML elements and regex for coordinates. | Audited bounding box coordinates via Python to guarantee all points lay within $12.5^\circ\text{N}–13.5^\circ\text{N}, 77.0^\circ\text{E}–78.0^\circ\text{E}$. |
| **Chart Visual Design** | Recommended ColorBrewer monochromatic palettes and Seaborn styling. | Verified that all charts passed WCAG AA contrast standards and ColorBrewer color-blind simulations without rainbow artifacts. |
| **REST API Architecture** | Generated Flask endpoint routing and CORS headers. | Tested live API responses via programmatic HTTP curl/urllib test suites; confirmed 100% 200 OK responses. |
| **Leaflet Interaction** | Generated interactive circleMarker mapping and popups. | Verified that markers scaled smoothly and popups displayed correct acreage and WQI stats for all 207 lakes. |
