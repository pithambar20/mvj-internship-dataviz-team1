/* ==============================================================================
   MAP CONTROLLER: 100% FREE KEYLESS BENGALURU LAKES VISUALISATION
   Zero API Keys Required — Powered by OpenStreetMap (OSM) & Local Leaflet
   ============================================================================== */

let mapInstance = null;
let markersLayer = null;
let currentMarkers = [];
let allLakesData = [];

function initLakeMap(lakes) {
  allLakesData = lakes;
  
  const mapContainer = document.getElementById('lake-map');
  if (!mapContainer) return;
  
  // Center of Bengaluru Urban (Vidhana Soudha / MG Road coordinates)
  const bengaluruCenter = [12.9716, 77.5946];
  
  if (!mapInstance) {
    mapInstance = L.map('lake-map', {
      center: bengaluruCenter,
      zoom: 11,
      minZoom: 9,
      maxZoom: 18,
      zoomControl: true
    });

    // 100% Free, Keyless OpenStreetMap Tile Layer (No API Key or Token Needed)
    const osmLayer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors (100% Keyless & Free)'
    });

    // Secondary Keyless Fallback (Humanitarian OSM)
    const hotLayer = L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; OpenStreetMap contributors, Tiles style by Humanitarian OSM'
    });

    // Light CartoDB Keyless Layer
    const lightLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
      maxZoom: 19,
      subdomains: 'abcd',
      attribution: '&copy; OpenStreetMap &copy; CARTO'
    });

    // Add primary layer
    osmLayer.addTo(mapInstance);

    // Layer control to switch keyless styles
    const baseMaps = {
      "Standard OpenStreetMap (No Key)": osmLayer,
      "Humanitarian OSM (No Key)": hotLayer,
      "Clean Voyager (No Key)": lightLayer
    };
    L.control.layers(baseMaps, null, { position: 'topright' }).addTo(mapInstance);

    // Marker Layer Group
    markersLayer = L.layerGroup().addTo(mapInstance);

    // Add Keyless Status Banner directly onto the Map UI
    addKeylessBadge(mapInstance);
  }

  renderLakeMarkers(allLakesData);
  renderSidebarLakeList(allLakesData);
}

function addKeylessBadge(map) {
  const badgeControl = L.control({ position: 'bottomleft' });
  badgeControl.onAdd = function() {
    const div = L.DomUtil.create('div', 'keyless-map-badge');
    div.innerHTML = `
      <div style="background:rgba(27,79,114,0.92); color:#FFFFFF; padding:5px 12px; border-radius:20px; font-size:11px; font-weight:600; box-shadow:0 2px 6px rgba(0,0,0,0.25); display:flex; align-items:center; gap:6px; backdrop-filter:blur(4px);">
        <span style="color:#2ECC71; font-size:12px;">&#x2714;</span> 
        <span>100% Free OpenStreetMap &bull; <strong>No API Key Required</strong></span>
      </div>
    `;
    return div;
  };
  badgeControl.addTo(map);
}

function getStatusColor(status) {
  switch (status) {
    case 'Developed / Rejuvenated': return '#1B4F72'; // Navy
    case 'Work in Progress': return '#2980B9';        // Cyan/Blue
    case 'To Be Developed': return '#F39C12';         // Amber
    case 'Degraded / Encroached': return '#C0392B';   // Red
    default: return '#7F8C8D';
  }
}

function getStatusBadgeClass(status) {
  switch (status) {
    case 'Developed / Rejuvenated': return 'badge-developed';
    case 'Work in Progress': return 'badge-wip';
    case 'To Be Developed': return 'badge-tbd';
    case 'Degraded / Encroached': return 'badge-encroached';
    default: return '';
  }
}

function renderLakeMarkers(lakes) {
  if (!markersLayer) return;
  markersLayer.clearLayers();
  currentMarkers = [];

  lakes.forEach(lake => {
    if (!lake.lat || !lake.lng) return;

    const color = getStatusColor(lake.status);
    // Radius proportional to lake acres
    const radius = Math.min(Math.max(lake.acres / 8, 6.5), 18);

    const marker = L.circleMarker([lake.lat, lake.lng], {
      radius: radius,
      fillColor: color,
      color: '#FFFFFF',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.82
    });

    // Rich popup without any external services or tracking
    const popupContent = `
      <div class="lake-popup-card">
        <span class="badge ${getStatusBadgeClass(lake.status)}">${lake.status}</span>
        <h4 class="popup-title" style="margin-top:6px;">${lake.name}</h4>
        <div style="font-size:11px; color:#566573; margin-bottom:8px;">Zone: <strong>${lake.zone}</strong></div>
        
        <div class="popup-grid">
          <div class="popup-stat">
            <div class="popup-stat-label">SURFACE AREA</div>
            <div class="popup-stat-val">${lake.acres} Acres</div>
          </div>
          <div class="popup-stat">
            <div class="popup-stat-label">WATER QUALITY</div>
            <div class="popup-stat-val">${lake.wqi} / 100</div>
          </div>
          <div class="popup-stat">
            <div class="popup-stat-label">DISSOLVED O2</div>
            <div class="popup-stat-val">${lake.dissolved_oxygen_mg_l} mg/L</div>
          </div>
          <div class="popup-stat">
            <div class="popup-stat-label">ENCROACHMENT</div>
            <div class="popup-stat-val" style="color:${lake.encroachment_pct > 15 ? '#C0392B' : '#27AE60'};">
              ${lake.encroachment_pct}%
            </div>
          </div>
        </div>

        <div style="font-size:11px; margin-top:6px; color:#7F8C8D;">
          <strong>Custodian:</strong> ${lake.custodian || 'BBMP Lakes Division'}
        </div>
        <div style="font-size:11px; margin-top:3px; color:#7F8C8D;">
          <strong>Walking Trail:</strong> ${lake.has_walking_track ? '&#9989; Available' : '&#10060; None'}
        </div>
      </div>
    `;

    marker.bindPopup(popupContent);
    marker.lakeId = lake.id;
    marker.lakeData = lake;

    marker.addTo(markersLayer);
    currentMarkers.push(marker);
  });
}

function renderSidebarLakeList(lakes) {
  const container = document.getElementById('lake-list-container');
  if (!container) return;

  container.innerHTML = '';
  if (lakes.length === 0) {
    container.innerHTML = '<li style="padding:20px; text-align:center; color:#7F8C8D; font-size:13px;">No water bodies match selected filters.</li>';
    return;
  }

  // Sort: Largest lakes first
  const sorted = [...lakes].sort((a, b) => b.acres - a.acres);

  sorted.forEach(lake => {
    const li = document.createElement('li');
    li.className = 'lake-item';
    li.dataset.lakeId = lake.id;
    
    li.innerHTML = `
      <div class="lake-item-name">${lake.name}</div>
      <div class="lake-item-meta">
        <span>${lake.zone} &bull; <strong>${lake.acres} ac</strong></span>
        <span class="badge ${getStatusBadgeClass(lake.status)}" style="font-size:9.5px; padding:1px 6px;">${lake.status.split('/')[0]}</span>
      </div>
    `;

    li.addEventListener('click', () => {
      focusLakeOnMap(lake);
      document.querySelectorAll('.lake-item').forEach(el => el.classList.remove('active'));
      li.classList.add('active');
    });

    container.appendChild(li);
  });
}

function focusLakeOnMap(lake) {
  if (!mapInstance || !lake.lat || !lake.lng) return;

  mapInstance.flyTo([lake.lat, lake.lng], 14, {
    animate: true,
    duration: 1.2
  });

  const targetMarker = currentMarkers.find(m => m.lakeId === lake.id);
  if (targetMarker) {
    setTimeout(() => {
      targetMarker.openPopup();
    }, 1250);
  }
}

function filterMapData(criteria) {
  const filtered = allLakesData.filter(lake => {
    // Zone
    if (criteria.zone && criteria.zone !== 'all' && lake.zone.toLowerCase() !== criteria.zone.toLowerCase()) {
      return false;
    }
    // Status
    if (criteria.status && criteria.status !== 'all' && lake.status.toLowerCase() !== criteria.status.toLowerCase()) {
      return false;
    }
    // Size
    if (criteria.size && criteria.size !== 'all') {
      if (criteria.size === 'small' && lake.acres >= 15) return false;
      if (criteria.size === 'medium' && (lake.acres < 15 || lake.acres > 50)) return false;
      if (criteria.size === 'large' && lake.acres <= 50) return false;
    }
    // Search
    if (criteria.search) {
      const q = criteria.search.toLowerCase();
      const match = lake.name.toLowerCase().includes(q) || 
                    lake.zone.toLowerCase().includes(q) || 
                    (lake.village_survey && lake.village_survey.toLowerCase().includes(q));
      if (!match) return false;
    }
    return true;
  });

  const counterEl = document.getElementById('filtered-lake-count');
  if (counterEl) counterEl.textContent = filtered.length;

  renderLakeMarkers(filtered);
  renderSidebarLakeList(filtered);
}
