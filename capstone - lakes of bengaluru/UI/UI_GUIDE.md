# UI / UX Design System & Specification: Lakes of Bengaluru

**Project:** Lakes of Bengaluru — Data Visualisation Capstone  
**Track:** BCA (Data Science) Final Year Internship (DS5P3)  
**Theme:** Civic Environmental Data Visualisation & Storytelling  
**Design Tokens Reference:** [`design_tokens.json`](file:///c:/Users/admin/Documents/internship/UI/design_tokens.json)

---

## 1. Visual Design Rationale

Urban water systems in Bengaluru present complex spatial, biological, and administrative dimensions. This UI is engineered around three foundational pillars:
1. **Pre-Attentive Clarity:** Color hues are semantically tied to physical lake status (Deep Navy for Rejuvenated/Protected waters, Sky Blue for Work-in-Progress, Amber for Pending, and Crimson for Critical Encroachment).
2. **Cognitive Load Minimization:** Complex chemical metrics (BOD, COD, Dissolved Oxygen, Total Dissolved Solids) are translated into clear, human-understandable visual scales and indexed Water Quality Index (WQI) badges.
3. **Interactive Storytelling:** Before-and-after spatial and chemical comparisons allow stakeholders, civic engineers, and students to immediately grasp the transformative power of nature-based urban engineering (constructed wetlands, STPs, and citizen co-management).

---

## 2. Color Palette & Accessibility (ColorBrewer Guidelines)

| Swatch | Token Name | Hex Code | Visual Meaning / Accessibility |
| :--- | :--- | :--- | :--- |
| ![#1B4F72](https://via.placeholder.com/15/1B4F72/000000?text=+) | `--color-developed` | `#1B4F72` | Developed / Rejuvenated Lake (High Contrast, WCAG AAA compliant on white) |
| ![#2980B9](https://via.placeholder.com/15/2980B9/000000?text=+) | `--color-wip` | `#2980B9` | Active Desilting / Civil Work in Progress |
| ![#F39C12](https://via.placeholder.com/15/F39C12/000000?text=+) | `--color-tbd` | `#F39C12` | To Be Developed / Awaiting Tender Sanction |
| ![#C0392B](https://via.placeholder.com/15/C0392B/000000?text=+) | `--color-encroached` | `#C0392B` | Degraded / Encroached / Critical Biohazard Alert |
| ![#0E86D4](https://via.placeholder.com/15/0E86D4/000000?text=+) | `--color-water-accent`| `#0E86D4` | Primary Interactive Map Pins & Selection States |

All chosen palettes avoid ambiguous red-green combinations without luminance differences, ensuring full legibility for individuals with deuteranopia or protanopia.

---

## 3. Core UI Components Dictionary

### 1. Metric KPI Cards (`UI/components/kpi-card.html`)
- Display high-level aggregates: Total Lakes Tracked (207), Total Lake Area (Acres), Rejuvenation Rate (%), Encroachment Acreage.
- Include subtle trend/status subheadings and icon anchors.

### 2. Multi-Criteria Filter Bar (`UI/components/filter-bar.html`)
- **Zone Filter:** Allows single-click or dropdown isolation of 8 BBMP zones (Mahadevapura, Bommanahalli, Yelahanka, South, East, West, RR Nagar, Dasarahalli).
- **Status Filter:** Pills toggle Developed, Work-in-Progress, To Be Developed, Encroached.
- **Search Input:** Real-time fuzzy filtering by lake name or survey record.
- **Size Selector:** Small (<10 Acres), Medium (10–50 Acres), Large (>50 Acres).

### 3. Interactive City Lake Map (Leaflet.js Integration)
- High-performance vector tile rendering with custom SVG water drop markers.
- Dynamic color-coding matching lake development status.
- Rich hover/click cards showing coordinates, acreage, WQI, walking trail availability, and quick navigation to story mode.

### 4. Before / After Rejuvenation Story Slider (`UI/components/before-after-slider.html`)
- Interactive split comparison slider allowing viewers to wipe between the historical degraded condition and the revived urban lake park.
- Side-by-side empirical metric cards (Dissolved Oxygen surge, BOD reduction, avian species counts).

### 5. Python Chart Container Card (`UI/components/chart-container.html`)
- Encapsulates high-resolution Matplotlib and Seaborn graphics.
- Features one-click modal zoom, full resolution download, and key empirical takeaway callout box.
