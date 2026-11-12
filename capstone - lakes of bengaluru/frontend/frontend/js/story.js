/* ==============================================================================
   BEFORE / AFTER STORY CONTROLLER: INTERACTIVE REJUVENATION COMPARISON
   ============================================================================== */

let storiesData = [];
let currentStoryIndex = 0;

function initStories(stories) {
  storiesData = stories;
  renderStoryPills();
  renderCurrentStory(storiesData[0]);
}

function renderStoryPills() {
  const container = document.getElementById('story-selector-pills');
  if (!container) return;

  container.innerHTML = '';
  storiesData.forEach((s, idx) => {
    const btn = document.createElement('button');
    btn.className = `story-pill ${idx === 0 ? 'active' : ''}`;
    btn.dataset.index = idx;
    
    // Choose icons
    const icons = ['&#129414;', '&#128101;', '&#127795;', '&#9888;'];
    btn.innerHTML = `${icons[idx % icons.length]} ${s.name.split(':')[0]}`;

    btn.addEventListener('click', () => {
      document.querySelectorAll('.story-pill').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentStoryIndex = idx;
      renderCurrentStory(storiesData[idx]);
    });

    container.appendChild(btn);
  });
}

function renderCurrentStory(story) {
  const container = document.getElementById('story-content-container');
  if (!container) return;

  // Render Story Body
  container.innerHTML = `
    <div class="story-container">
      <!-- Left Column: Interactive Visual Comparison Slider -->
      <div class="story-visual-column">
        <h3 style="font-size:14px; font-weight:700; color:var(--primary-navy); margin-bottom:10px;">
          Interactive Landscape Transformation (Drag Divider &#8596;)
        </h3>

        <div class="comparison-slider-wrapper" id="slider-wrapper">
          <!-- After Layer (Underneath - Clean Restored Wetland) -->
          <div class="comp-layer after" style="background: linear-gradient(135deg, #1B4F72 0%, #2980B9 50%, #27AE60 100%);">
            <span class="comp-tag after-tag">&#9989; AFTER RESTORATION</span>
            <div class="comp-content-box">
              <strong style="color:#D4EFDF;">Restored Condition:</strong>
              <div>${story.after.condition}</div>
              <div style="margin-top:6px; font-size:11px; color:#A9DFBF;">
                <strong>Walking Track:</strong> ${story.after.community_access}
              </div>
            </div>
          </div>

          <!-- Before Layer (Overlay Clipped - Choked Polluted Bed) -->
          <div class="comp-layer before" id="layer-before" style="background: linear-gradient(135deg, #7D6608 0%, #5D6D7E 50%, #78281F 100%); width: 50%;">
            <span class="comp-tag before-tag">&#9888; BEFORE INTERVENTION</span>
            <div class="comp-content-box">
              <strong style="color:#FADBD8;">Degraded State:</strong>
              <div>${story.before.condition}</div>
              <div style="margin-top:6px; font-size:11px; color:#EDBB99;">
                <strong>Encroachment:</strong> ${story.before.encroachment}
              </div>
            </div>
          </div>

          <!-- Interactive Drag Handle -->
          <div class="comp-slider-handle" id="slider-handle" style="left: 50%;">
            <div class="slider-circle">&#8596;</div>
          </div>
        </div>

        <!-- Metric Table -->
        <div style="margin-top: 1.5rem;">
          <h4 style="font-size:13px; font-weight:700; color:var(--primary-navy); margin-bottom:8px;">
            Empirical Water Quality & Ecological Metrics
          </h4>
          <table class="metrics-table">
            <thead>
              <tr>
                <th>Environmental Parameter</th>
                <th>Before</th>
                <th>After Rejuvenation</th>
                <th>Standard / Target</th>
              </tr>
            </thead>
            <tbody>
              ${story.metrics.map(m => `
                <tr>
                  <td><strong>${m.parameter}</strong></td>
                  <td class="text-danger">${m.before} ${m.unit}</td>
                  <td class="text-success">${m.after} ${m.unit}</td>
                  <td style="color:#7F8C8D;">${m.target}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      </div>

      <!-- Right Column: Narrative & Civic Takeaways -->
      <div class="story-info-panel">
        <span class="badge badge-developed" style="margin-bottom:8px;">Case Study &bull; Restored: ${story.year_restored}</span>
        <h2>${story.name}</h2>
        <div class="story-loc">&#128205; ${story.location} &bull; <strong>${story.extent_acres} Acres</strong></div>
        
        <p class="story-hero-text">
          ${story.hero_summary}
        </p>

        <!-- Detailed Side-by-Side Cards -->
        <div style="display:grid; grid-template-columns:1fr; gap:12px; margin-bottom:1.5rem;">
          <div style="background:#FDEDEC; border-left:4px solid #C0392B; padding:12px; border-radius:6px;">
            <div style="font-size:11px; font-weight:800; color:#C0392B;">HISTORICAL CHALLENGE</div>
            <p style="font-size:12px; color:#641E16; margin-top:4px;">
              <strong>Biodiversity:</strong> ${story.before.biodiversity}<br>
              <strong>Fecal Coliform:</strong> ${story.before.fecal_coliform}
            </p>
          </div>

          <div style="background:#D4EFDF; border-left:4px solid #27AE60; padding:12px; border-radius:6px;">
            <div style="font-size:11px; font-weight:800; color:#1E8449;">ENGINEERING & COMMUNITY TRIUMPH</div>
            <p style="font-size:12px; color:#145A32; margin-top:4px;">
              <strong>Biodiversity:</strong> ${story.after.biodiversity}<br>
              <strong>Fecal Coliform:</strong> ${story.after.fecal_coliform}
            </p>
          </div>
        </div>

        <!-- Key Takeaway Callout -->
        <div style="background:var(--accent-light); border:1px solid #AED6F1; border-radius:8px; padding:14px;">
          <div style="font-size:11.5px; font-weight:800; color:var(--primary-navy); margin-bottom:4px;">
            &#128161; KEY POLICY TAKEAWAY
          </div>
          <div style="font-size:12.5px; color:var(--text-main); line-height:1.5;">
            ${story.key_takeaway}
          </div>
        </div>
      </div>
    </div>
  `;

  setupSliderInteraction();
}

function setupSliderInteraction() {
  const wrapper = document.getElementById('slider-wrapper');
  const beforeLayer = document.getElementById('layer-before');
  const handle = document.getElementById('slider-handle');

  if (!wrapper || !beforeLayer || !handle) return;

  let isDragging = false;

  const updatePosition = (clientX) => {
    const rect = wrapper.getBoundingClientRect();
    let posX = clientX - rect.left;
    if (posX < 20) posX = 20;
    if (posX > rect.width - 20) posX = rect.width - 20;

    const percentage = (posX / rect.width) * 100;
    beforeLayer.style.width = `${percentage}%`;
    handle.style.left = `${percentage}%`;
  };

  handle.addEventListener('mousedown', () => { isDragging = true; });
  window.addEventListener('mouseup', () => { isDragging = false; });
  window.addEventListener('mousemove', (e) => {
    if (isDragging) updatePosition(e.clientX);
  });

  // Touch Support
  handle.addEventListener('touchstart', () => { isDragging = true; });
  window.addEventListener('touchend', () => { isDragging = false; });
  window.addEventListener('touchmove', (e) => {
    if (isDragging && e.touches.length > 0) {
      updatePosition(e.touches[0].clientX);
    }
  });

  // Click anywhere on slider to jump
  wrapper.addEventListener('click', (e) => {
    updatePosition(e.clientX);
  });
}
