/* ==============================================================================
   CHARTS CONTROLLER: PYTHON (MATPLOTLIB & SEABORN) DATA VISUALISATIONS
   ============================================================================== */

const CHARTS_LIST = [
  {
    id: 'status_by_zone',
    title: 'Lake Rejuvenation Status Breakdown by Civic Zone',
    module: 'Matplotlib (Horizontal Stacked Bar)',
    filename: 'chart1_status_by_zone.png',
    takeaway: 'Mahadevapura and Bommanahalli host 48% of total lakes, with highest ongoing active rejuvenation works.',
    description: 'Stacked bar visualization decomposing 207 lake records into 4 municipal statuses across all 8 Bengaluru civic zones. Uses ColorBrewer blues/earthy tones.'
  },
  {
    id: 'area_distribution',
    title: 'Distribution of Lake Surface Extent (Acres) by Zone',
    module: 'Seaborn (Boxplot with Mean Points)',
    filename: 'chart2_area_distribution.png',
    takeaway: 'Bellandur Lake (913 Acres) is Bengaluru’s massive outlier drainage sink; typical urban lakes median at 24 acres.',
    description: 'Seaborn boxplot displaying median, interquartile ranges, and red mean points. Bellandur is annotated as the primary catchment sink.'
  },
  {
    id: 'wqi_density',
    title: 'Water Quality Index (WQI) Probability Density Matrix',
    module: 'Seaborn (KDE Multi-Distribution Plot)',
    filename: 'chart3_wqi_density.png',
    takeaway: 'Clear bimodal separation: Rejuvenated lakes score 72–92 (Class B/C), while untreated water bodies stagnate under 45.',
    description: 'Kernel Density Estimation curves proving significant water quality elevation between raw urban runoff and bio-engineered lakes.'
  },
  {
    id: 'before_after_metrics',
    title: 'Chemical & Biological Impact: Before vs After Rejuvenation',
    module: 'Matplotlib (Two-Panel Aligned Horizontal Comparisons)',
    filename: 'chart4_before_after_metrics.png',
    takeaway: 'Constructed wetlands and STPs collapsed organic BOD load by 78%–94% while lifting Dissolved Oxygen up to 7.4 mg/L.',
    description: 'Aligned two-panel horizontal bar charts comparing critical CPCB parameters across Jakkur, Kaikondrahalli, Agara, and Bellandur.'
  },
  {
    id: 'encroachment_correlation',
    title: 'Perimeter Encroachment Rate vs Avian & Floral Biodiversity',
    module: 'Seaborn (Linear Regression with 95% Confidence Band)',
    filename: 'chart5_encroachment_correlation.png',
    takeaway: 'Statistically significant negative correlation (r = -0.84): lakes with >30% encroachment suffer catastrophic biodiversity collapse.',
    description: 'Seaborn regplot demonstrating the direct ecological harm of perimeter building violations on native waterfowl species.'
  },
  {
    id: 'custodian_breakdown',
    title: 'Institutional Custodianship of Bengaluru Water Bodies',
    module: 'Matplotlib (Bar Chart with Direct Proportions)',
    filename: 'chart6_custodian_breakdown.png',
    takeaway: 'BBMP Lakes Division stewards 74% of civic water bodies, transitioning toward citizen co-management models.',
    description: 'Bar chart mapping jurisdiction across BBMP, BDA, Karnataka Forest Department, and citizen community trusts.'
  }
];

function initChartsGallery() {
  renderCharts();

  // Zone filter listener
  const filterSelect = document.getElementById('chart-zone-filter');
  const refreshBtn = document.getElementById('btn-refresh-charts');

  if (refreshBtn) {
    refreshBtn.addEventListener('click', () => {
      const zone = filterSelect ? filterSelect.value : 'all';
      renderCharts(zone);
    });
  }
}

function getChartSource(chart, zone = 'all') {
  // If backend is active and zone filter is applied
  if (window.BACKEND_AVAILABLE && zone !== 'all') {
    return `http://localhost:5000/api/charts/${chart.id}?zone=${encodeURIComponent(zone)}&t=${Date.now()}`;
  }
  // Otherwise use local assets chart
  return `assets/charts/${chart.filename}`;
}

function renderCharts(zone = 'all') {
  const container = document.getElementById('charts-container');
  if (!container) return;

  container.innerHTML = '';

  CHARTS_LIST.forEach(chart => {
    const src = getChartSource(chart, zone);

    const card = document.createElement('div');
    card.className = 'chart-card';
    card.innerHTML = `
      <div class="chart-header">
        <div>
          <h3 class="chart-title">${chart.title}</h3>
          <span class="chart-engine-badge">${chart.module}</span>
        </div>
        <div class="chart-actions">
          <button class="btn-icon" title="View Fullscreen" onclick="openChartModal('${chart.id}')">&#x26F6;</button>
          <a href="${src}" download="${chart.filename}" class="btn-icon" title="Download High-Res PNG">&#x2193;</a>
        </div>
      </div>

      <div class="chart-body">
        <img src="${src}" alt="${chart.title}" class="chart-image" onclick="openChartModal('${chart.id}')" loading="lazy">
      </div>

      <div class="chart-footer">
        <div class="chart-takeaway">
          <strong>Key Finding:</strong> ${chart.takeaway}
        </div>
      </div>
    `;

    container.appendChild(card);
  });
}

function openChartModal(chartId) {
  const chart = CHARTS_LIST.find(c => c.id === chartId);
  if (!chart) return;

  const modal = document.getElementById('chart-modal');
  const title = document.getElementById('modal-title');
  const img = document.getElementById('modal-img');
  const desc = document.getElementById('modal-desc');

  if (modal && title && img && desc) {
    title.textContent = chart.title;
    img.src = `assets/charts/${chart.filename}`;
    desc.innerHTML = `<strong>Description:</strong> ${chart.description}<br><br><strong>Key Analytical Finding:</strong> ${chart.takeaway}`;
    modal.style.display = 'flex';
  }
}

function closeChartModal() {
  const modal = document.getElementById('chart-modal');
  if (modal) modal.style.display = 'none';
}

// Close modal on escape key or clicking backdrop
window.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeChartModal();
});

window.addEventListener('click', (e) => {
  const modal = document.getElementById('chart-modal');
  if (e.target === modal) closeChartModal();
});
