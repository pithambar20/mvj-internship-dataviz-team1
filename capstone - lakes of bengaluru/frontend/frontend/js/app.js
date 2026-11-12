/* ==============================================================================
   MAIN APP ORCHESTRATOR: LAKES OF BENGALURU
   ============================================================================== */

window.BACKEND_AVAILABLE = false;
let masterLakes = [];
let masterStats = null;
let masterStories = [];

document.addEventListener('DOMContentLoaded', async () => {
  setupNavigationTabs();
  setupFilterEventListeners();
  await loadApplicationData();
  setupDirectoryTable();
});

// ------------------------------------------------------------------------------
// 1. NAVIGATION TAB SWITCHING
// ------------------------------------------------------------------------------
function setupNavigationTabs() {
  const navLinks = document.querySelectorAll('.nav-link');
  const viewPanels = document.querySelectorAll('.view-panel');

  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const targetViewId = link.getAttribute('data-view');

      // Update Nav tab classes
      navLinks.forEach(l => l.classList.remove('active'));
      link.classList.add('active');

      // Toggle View panels
      viewPanels.forEach(panel => {
        panel.classList.remove('active');
        if (panel.id === targetViewId) {
          panel.classList.add('active');
        }
      });

      // Invalidate Leaflet map size if switching to map
      if (targetViewId === 'view-map' && window.mapInstance) {
        setTimeout(() => {
          window.mapInstance.invalidateSize();
        }, 200);
      }
    });
  });
}

// ------------------------------------------------------------------------------
// 2. DATA INGESTION & FALLBACK ARCHITECTURE
// ------------------------------------------------------------------------------
async function loadApplicationData() {
  try {
    // Attempt connecting to Flask backend API
    const resLakes = await fetch('http://localhost:5000/api/lakes');
    if (resLakes.ok) {
      const dataLakes = await resLakes.json();
      masterLakes = dataLakes.lakes;
      window.BACKEND_AVAILABLE = true;

      // Stats
      const resStats = await fetch('http://localhost:5000/api/stats');
      if (resStats.ok) masterStats = await resStats.json();

      // Stories
      const resStories = await fetch('http://localhost:5000/api/story');
      if (resStories.ok) {
        const dataStories = await resStories.json();
        masterStories = dataStories.stories;
      }
      console.log('Connected to live Flask Backend on http://localhost:5000');
    } else {
      throw new Error('Backend returned non-200');
    }
  } catch (err) {
    console.warn('Backend unavailable, using static fallback dataset.', err);
    masterLakes = window.FALLBACK_LAKES || [];
    masterStories = window.FALLBACK_STORIES || [];
    computeFallbackStats(masterLakes);
  }

  // Update Top KPIs
  updateKpiStrip(masterLakes);

  // Initialize Map, Stories & Charts
  initLakeMap(masterLakes);
  initStories(masterStories);
  initChartsGallery();
  populateDirectoryTable(masterLakes);
}

function computeFallbackStats(lakes) {
  const total = lakes.length;
  const dev = lakes.filter(l => l.status === 'Developed / Rejuvenated').length;
  const wip = lakes.filter(l => l.status === 'Work in Progress').length;
  const enc = lakes.filter(l => l.status === 'Degraded / Encroached').length;
  const totalAcres = lakes.reduce((sum, l) => sum + (l.acres || 0), 0);

  masterStats = {
    total_lakes: total,
    total_acres: Math.round(totalAcres),
    developed_count: dev,
    wip_count: wip,
    encroached_count: enc,
    rejuvenation_rate_pct: Math.round((dev / total) * 1000) / 10
  };
}

function updateKpiStrip(lakes) {
  if (!lakes || lakes.length === 0) return;

  const total = lakes.length;
  const dev = lakes.filter(l => l.status === 'Developed / Rejuvenated').length;
  const wip = lakes.filter(l => l.status === 'Work in Progress').length;
  const enc = lakes.filter(l => l.status === 'Degraded / Encroached' || l.encroachment_pct > 25).length;
  const totalAcres = lakes.reduce((sum, l) => sum + (l.acres || 0), 0);
  const devPct = ((dev / total) * 100).toFixed(1);
  const wipPct = ((wip / total) * 100).toFixed(1);
  const encPct = ((enc / total) * 100).toFixed(1);

  const elTotal = document.getElementById('kpi-total-lakes');
  const elDev = document.getElementById('kpi-rejuvenated');
  const elAcres = document.getElementById('kpi-total-acres');
  const elWip = document.getElementById('kpi-wip');
  const elEnc = document.getElementById('kpi-encroached');

  if (elTotal) elTotal.textContent = total;
  if (elDev) elDev.innerHTML = `${dev} <span style="font-size:16px; font-weight:600;">(${devPct}%)</span>`;
  if (elAcres) elAcres.innerHTML = `${Math.round(totalAcres).toLocaleString()} <span style="font-size:14px; font-weight:600;">Acres</span>`;
  if (elWip) elWip.innerHTML = `${wip} <span style="font-size:16px; font-weight:600;">(${wipPct}%)</span>`;
  if (elEnc) elEnc.innerHTML = `${enc} <span style="font-size:16px; font-weight:600;">(${encPct}%)</span>`;

  const badgeCount = document.getElementById('tab-count-lakes');
  if (badgeCount) badgeCount.textContent = total;
}

// ------------------------------------------------------------------------------
// 3. FILTER EVENT LISTENERS
// ------------------------------------------------------------------------------
function setupFilterEventListeners() {
  const zoneSelect = document.getElementById('filter-zone');
  const statusSelect = document.getElementById('filter-status');
  const sizeSelect = document.getElementById('filter-size');
  const searchInput = document.getElementById('filter-search');
  const resetBtn = document.getElementById('btn-reset-filters');

  function triggerFilters() {
    const criteria = {
      zone: zoneSelect ? zoneSelect.value : 'all',
      status: statusSelect ? statusSelect.value : 'all',
      size: sizeSelect ? sizeSelect.value : 'all',
      search: searchInput ? searchInput.value.trim() : ''
    };
    filterMapData(criteria);
  }

  if (zoneSelect) zoneSelect.addEventListener('change', triggerFilters);
  if (statusSelect) statusSelect.addEventListener('change', triggerFilters);
  if (sizeSelect) sizeSelect.addEventListener('change', triggerFilters);
  if (searchInput) searchInput.addEventListener('input', triggerFilters);

  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      if (zoneSelect) zoneSelect.value = 'all';
      if (statusSelect) statusSelect.value = 'all';
      if (sizeSelect) sizeSelect.value = 'all';
      if (searchInput) searchInput.value = '';
      triggerFilters();
    });
  }
}

// ------------------------------------------------------------------------------
// 4. DIRECTORY TABLE EXPLORER & CSV EXPORT
// ------------------------------------------------------------------------------
function setupDirectoryTable() {
  const exportBtn = document.getElementById('btn-export-csv');
  if (exportBtn) {
    exportBtn.addEventListener('click', () => {
      exportMasterCSV();
    });
  }
}

function populateDirectoryTable(lakes) {
  const tbody = document.getElementById('directory-table-body');
  if (!tbody) return;

  tbody.innerHTML = '';
  // Sort by size descending
  const sorted = [...lakes].sort((a, b) => b.acres - a.acres);

  sorted.forEach(lake => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${lake.name}</strong></td>
      <td>${lake.zone}</td>
      <td><strong>${lake.acres}</strong> ac</td>
      <td><span class="badge ${getStatusBadgeClass(lake.status)}">${lake.status}</span></td>
      <td><strong>${lake.wqi}</strong> / 100</td>
      <td>${lake.dissolved_oxygen_mg_l} mg/L</td>
      <td style="color:${lake.encroachment_pct > 15 ? '#C0392B' : '#27AE60'}; font-weight:600;">${lake.encroachment_pct}%</td>
      <td>${lake.has_walking_track ? '&#9989; Yes' : '&#10060; No'}</td>
      <td style="font-size:11.5px; color:#566573;">${lake.custodian || 'BBMP'}</td>
    `;
    tbody.appendChild(tr);
  });
}

function exportMasterCSV() {
  if (!masterLakes || masterLakes.length === 0) return;

  const headers = ['ID', 'Lake_Name', 'Zone', 'Latitude', 'Longitude', 'Surface_Acres', 'Status', 'WQI', 'Dissolved_Oxygen_mg_l', 'BOD_mg_l', 'Encroachment_Pct', 'Walking_Track', 'Custodian'];
  const rows = masterLakes.map(l => [
    l.id,
    `"${l.name.replace(/"/g, '""')}"`,
    `"${l.zone}"`,
    l.lat,
    l.lng,
    l.acres,
    `"${l.status}"`,
    l.wqi,
    l.dissolved_oxygen_mg_l,
    l.bod_mg_l,
    l.encroachment_pct,
    l.has_walking_track ? 'Yes' : 'No',
    `"${l.custodian || 'BBMP'}"`
  ]);

  const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
  const encodedUri = encodeURI(csvContent);
  const link = document.createElement('a');
  link.setAttribute('href', encodedUri);
  link.setAttribute('download', 'bengaluru_lakes_master_data.csv');
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
