/* ============================================
   대한민국 시군구 지도 퀴즈 - Main Application
   Optimized for interactive whiteboards (전자칠판)
   - No right-click context menu
   - Single-touch only (multi-touch ignored)
   - Large touch targets
   ============================================ */

// Removed hardcoded PROVINCES and MAP_CONFIG

// Colorful palette for individual municipalities
const REGION_COLORS = [
    '#f87171', '#f97316', '#fbbf24', '#a3e635', '#4ade80',
    '#34d399', '#2dd4bf', '#22d3ee', '#38bdf8', '#818cf8',
    '#a78bfa', '#e879f9', '#f472b6', '#fb7185', '#fdba74',
    '#fcd34d', '#bef264', '#86efac', '#6ee7b7', '#5eead4',
    '#67e8f9', '#7dd3fc', '#93c5fd', '#a5b4fc', '#c4b5fd',
    '#f0abfc', '#f9a8d4', '#fca5a5', '#fed7aa', '#d9f99d',
];

// ========== Application State ==========
const state = {
    // GeoJSON data
    municipalitiesGeo: null,
    provincesGeo: null,
    provincesMesh: null,

    // D3 objects
    projection: null,
    path: null,
    svg: null,
    zoom: null,

    // Quiz state
    currentProvince: null,
    currentRegions: [],
    selectedCapsule: null,
    matched: new Set(),
    completedProvinces: new Set(),
    isNationwideMode: false,
    isShowingInfo: false,
    startTime: null,
    timerInterval: null,

    // Drag state (single pointer tracking)
    activePointerId: null,
    dragState: {
        isDragging: false,
        startX: 0,
        startY: 0,
        capsule: null,
        code: null,
        ghostEl: null,
    },
};

// ========== Audio (Web Audio API) ==========

let audioCtx = null;

function getAudioCtx() {
    if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    return audioCtx;
}

function playCorrectSound() {
    try {
        const ctx = getAudioCtx();
        const now = ctx.currentTime;

        // Two-note ascending chime: C5 → E5
        [523.25, 659.25].forEach((freq, i) => {
            const osc = ctx.createOscillator();
            const gain = ctx.createGain();
            osc.type = 'sine';
            osc.frequency.value = freq;
            gain.gain.setValueAtTime(0.18, now + i * 0.12);
            gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.12 + 0.3);
            osc.connect(gain).connect(ctx.destination);
            osc.start(now + i * 0.12);
            osc.stop(now + i * 0.12 + 0.35);
        });
    } catch (e) { /* audio not supported */ }
}

function playIncorrectSound() {
    try {
        const ctx = getAudioCtx();
        const now = ctx.currentTime;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'square';
        osc.frequency.value = 200;
        gain.gain.setValueAtTime(0.12, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.25);
        osc.connect(gain).connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.3);
    } catch (e) { /* audio not supported */ }
}

// ========== Initialization ==========

document.addEventListener('DOMContentLoaded', init);

function init() {
    preventDefaultBehaviors();
    
    // Setup country selector listeners
    document.querySelectorAll('.country-card').forEach(card => {
        card.addEventListener('click', () => {
            document.getElementById('country-selector').classList.add('hidden');
            loadCountry(card.dataset.country);
        });
    });
    
    document.getElementById('country-change-btn').addEventListener('click', () => {
        document.getElementById('country-selector').classList.remove('hidden');
        document.getElementById('view-results-btn').classList.add('hidden');
        document.getElementById('completion-modal').classList.add('hidden');
    });
    
    setupEventListeners();
}

// ========== Touch & Right-Click Prevention ==========

function preventDefaultBehaviors() {
    // Prevent right-click context menu everywhere
    document.addEventListener('contextmenu', (e) => {
        e.preventDefault();
        e.stopPropagation();
        return false;
    }, true);

    // Prevent multi-touch: only allow the first touch point
    document.addEventListener('touchstart', (e) => {
        if (e.touches.length > 1) {
            e.preventDefault();
        }
    }, { passive: false });

    // Prevent pinch-to-zoom and other multi-touch gestures
    document.addEventListener('touchmove', (e) => {
        if (e.touches.length > 1) {
            e.preventDefault();
        }
    }, { passive: false });

    // Prevent double-tap zoom
    let lastTouchEnd = 0;
    document.addEventListener('touchend', (e) => {
        const now = Date.now();
        if (now - lastTouchEnd < 300) {
            e.preventDefault();
        }
        lastTouchEnd = now;
    }, { passive: false });

    // Prevent drag on images and links (browser default)
    document.addEventListener('dragstart', (e) => {
        if (e.target.tagName !== 'DIV') {
            e.preventDefault();
        }
    });

    // Prevent text selection on everything
    document.addEventListener('selectstart', (e) => {
        e.preventDefault();
    });
}

// ========== Data Loading ==========

async function loadCountry(countryId) {
    document.getElementById('loading-overlay').classList.remove('hidden');
    
    try {
        // Load config
        await new Promise((resolve, reject) => {
            const script = document.createElement('script');
            const cacheBuster = Date.now();
            script.src = `countries/${countryId}/config.js?v=${cacheBuster}`;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
        
        if (COUNTRY_CONFIG.modes && COUNTRY_CONFIG.modes.length > 0) {
            state.currentModeId = COUNTRY_CONFIG.modes[0].id;
            applyModeConfig(state.currentModeId);
        }

        await loadCountryData();
        
    } catch (e) {
        console.error('Failed to load country', e);
        alert('국가 데이터를 불러오는데 실패했습니다.');
        document.getElementById('country-selector').classList.remove('hidden');
    } finally {
        document.getElementById('loading-overlay').classList.add('hidden');
    }
}

function applyModeConfig(modeId) {
    const mode = COUNTRY_CONFIG.modes.find(m => m.id === modeId);
    if (!mode) return;
    Object.assign(COUNTRY_CONFIG, mode);
}

async function loadCountryData() {
    document.getElementById('loading-overlay').classList.remove('hidden');
    try {
        // Clear previous state data
        state.municipalitiesGeo = null;
        state.baseGeo = null;
        state.provincesGeo = null;
        const cacheBuster = Date.now();
        const regionsRes = await fetch(COUNTRY_CONFIG.dataFiles.regions + '?v=' + cacheBuster);
        const regionsData = await regionsRes.json();
        
        if (COUNTRY_CONFIG.topoConfig && COUNTRY_CONFIG.topoConfig.regions) {
            state.municipalitiesGeo = topojson.feature(regionsData, regionsData.objects[COUNTRY_CONFIG.topoConfig.regions.objectName]);
        } else {
            state.municipalitiesGeo = regionsData;
        }

        if (COUNTRY_CONFIG.hierarchy && COUNTRY_CONFIG.hierarchy.filter) {
            state.municipalitiesGeo.features = state.municipalitiesGeo.features.filter(COUNTRY_CONFIG.hierarchy.filter);
        }

        if (COUNTRY_CONFIG.dataFiles.baseRegions) {
            const baseRes = await fetch(COUNTRY_CONFIG.dataFiles.baseRegions + '?v=' + cacheBuster);
            const baseData = await baseRes.json();
            if (COUNTRY_CONFIG.topoConfig && COUNTRY_CONFIG.topoConfig.baseRegions) {
                state.baseGeo = topojson.feature(baseData, baseData.objects[COUNTRY_CONFIG.topoConfig.baseRegions.objectName]);
            } else {
                state.baseGeo = baseData;
            }
        }
        
        if (COUNTRY_CONFIG.hierarchy.hasProvinces && COUNTRY_CONFIG.dataFiles.provinces) {
            const provRes = await fetch(COUNTRY_CONFIG.dataFiles.provinces);
            const provData = await provRes.json();
            
            if (COUNTRY_CONFIG.topoConfig && COUNTRY_CONFIG.topoConfig.provinces) {
                state.provincesGeo = topojson.feature(provData, provData.objects[COUNTRY_CONFIG.topoConfig.provinces.objectName]);
                state.provincesMesh = topojson.mesh(provData, provData.objects[COUNTRY_CONFIG.topoConfig.provinces.objectName], (a, b) => a !== b);
                state.provincesOuterMesh = topojson.mesh(provData, provData.objects[COUNTRY_CONFIG.topoConfig.provinces.objectName], (a, b) => a === b);
            } else {
                state.provincesGeo = provData;
                state.provincesMesh = null;
                state.provincesOuterMesh = null;
            }
        } else {
            state.provincesGeo = null;
            state.provincesMesh = null;
            state.provincesOuterMesh = null;
        }
        
        // Load descriptions
        if (COUNTRY_CONFIG.dataFiles.descriptions) {
            await new Promise((resolve) => {
                const script = document.createElement('script');
                const cacheBuster = Date.now();
                script.src = COUNTRY_CONFIG.dataFiles.descriptions + '?v=' + cacheBuster;
                script.onload = resolve;
                script.onerror = resolve; // Continue even if missing
                document.head.appendChild(script);
            });
        }
        
        // Setup UI
        document.getElementById('sidebar-title').textContent = COUNTRY_CONFIG.labels.sidebarTitle;
        document.getElementById('current-province-name').textContent = '선택하세요';
        
        setupSVG();
        renderFullMap();
        renderProvinceButtons();
        
        // Reset state
        state.matched = new Set();
        state.selectedCapsule = null;
        state.isNationwideMode = false;
        state.currentProvince = null;
        clearTimer();
        document.getElementById('capsules-container').innerHTML = '';
        document.getElementById('capsules-instruction').classList.add('hidden');
        document.getElementById('score-text').textContent = '0 / 0';
        document.getElementById('timer-text').textContent = '00:00';
        
        // Ensure UI elements are reset
        document.getElementById('country-selector').classList.add('hidden');
        document.getElementById('completion-modal').classList.add('hidden');
        document.getElementById('view-results-btn').classList.add('hidden');
        
        // Open sidebar on large screens
        if (window.innerWidth > 900 && (COUNTRY_CONFIG.hierarchy.hasProvinces || COUNTRY_CONFIG.modes)) {
            document.getElementById('province-sidebar').classList.add('open');
        }
        
    } catch (e) {
        console.error('Failed to load country data', e);
        alert('모드 데이터를 불러오는데 실패했습니다.');
    } finally {
        document.getElementById('loading-overlay').classList.add('hidden');
    }
}

// ========== SVG Setup ==========

function setupSVG() {
    const { width, height } = COUNTRY_CONFIG.mapConfig;
    const minZoom = 0.8, maxZoom = 40;

    // Reset previous SVG contents
    d3.select('#map-svg').selectAll('g#map-group > g > *').remove();

    if (COUNTRY_CONFIG.projection === 'mercator') {
        state.projection = d3.geoMercator()
            .fitSize([width * 0.92, height * 0.95], state.baseGeo || state.municipalitiesGeo)
            .translate([width / 2, height / 2 + 10]);
    } else if (COUNTRY_CONFIG.projection === 'albersUsa') {
        state.projection = d3.geoAlbersUsa()
            .fitSize([width * 0.92, height * 0.95], state.baseGeo || state.municipalitiesGeo)
            .translate([width / 2, height / 2 + 10]);
    } else if (COUNTRY_CONFIG.projection === 'identity') {
        state.projection = d3.geoIdentity()
            .reflectY(false)
            .fitSize([width * 0.92, height * 0.95], state.baseGeo || state.municipalitiesGeo);
    } else {
        // Pre-projected (like us-atlas) without scaling
        state.projection = null;
    }

    if (state.projection) {
        state.path = d3.geoPath().projection(state.projection);
    } else {
        state.path = d3.geoPath();
    }

    state.svg = d3.select('#map-svg')
        .attr('viewBox', `0 0 ${width} ${height}`)
        .attr('preserveAspectRatio', 'xMidYMid meet');

    // Remove old zoom listener before creating new one
    state.svg.on('.zoom', null);

    // D3 zoom - interactive: single-touch pan, wheel zoom
    // Blocks multi-touch (pinch) and right-click
    state.zoom = d3.zoom()
        .scaleExtent([minZoom, maxZoom])
        .filter((event) => {
            // Block right-click
            if (event.button && event.button !== 0) return false;
            // Block multi-touch (pinch zoom)
            if (event.touches && event.touches.length > 1) return false;
            // Block double-click zoom (to avoid accidental zoom)
            if (event.type === 'dblclick') return false;
            // Allow everything else: mouse drag, single-touch drag, wheel
            return true;
        })
        .on('start', () => {
            document.getElementById('map-svg').classList.add('panning');
        })
        .on('zoom', (event) => {
            d3.select('#map-group').attr('transform', event.transform);
            // Keep labels at fixed display-pixel size
            const k = event.transform.k;
            document.querySelectorAll('.map-label').forEach(el => {
                el.style.fontSize = ((+el.dataset.displaySize || 9) / k) + 'px';
            });
        })
        .on('end', () => {
            document.getElementById('map-svg').classList.remove('panning');
        });

    state.svg.call(state.zoom);

    // Only disable double-click zoom
    state.svg.on('dblclick.zoom', null);
}

// ========== Helpers ==========

function isMapPath(el) {
    return el && (
        el.classList.contains('municipality-path') ||
        el.classList.contains('province-fill-path')
    );
}

// ========== Map Rendering ==========

function renderFullMap() {
    const muniLayer = d3.select('#municipalities-layer');
    const provFillLayer = d3.select('#provinces-fill-layer');
    const provLayer = d3.select('#provinces-layer');

    // Clear layers
    muniLayer.selectAll('*').remove();
    provFillLayer.selectAll('*').remove();
    provLayer.selectAll('*').remove();

    const nameField = COUNTRY_CONFIG.hierarchy.regionNameField;
    const codeField = COUNTRY_CONFIG.hierarchy.regionCodeField;

    // Draw base regions if available
    if (state.baseGeo) {
        muniLayer.selectAll('path.base-path')
            .data(state.baseGeo.features)
            .enter()
            .append('path')
            .attr('class', 'base-path')
            .attr('d', state.path)
            .style('fill', 'rgba(40, 50, 70, 0.35)')
            .style('stroke', 'rgba(148, 163, 184, 0.12)')
            .style('stroke-width', '0.5px');
    }

    // Draw municipality boundaries (Polygons)
    const polys = state.municipalitiesGeo.features.filter(f => f.geometry.type !== 'Point');
    if (polys.length > 0) {
        muniLayer.selectAll('path.municipality-path')
            .data(polys)
            .enter()
            .append('path')
            .attr('class', 'municipality-path')
            .attr('d', state.path)
            .attr('data-code', d => d.properties[codeField])
            .attr('data-name', d => d.properties[nameField]);
    }

    // Draw municipality points (Points)
    const points = state.municipalitiesGeo.features.filter(f => f.geometry.type === 'Point');
    if (points.length > 0) {
        muniLayer.selectAll('circle.municipality-path')
            .data(points)
            .enter()
            .append('circle')
            .attr('class', 'municipality-path point-marker')
            .attr('cx', d => {
                const p = state.projection(d.geometry.coordinates);
                return p ? p[0] : 0;
            })
            .attr('cy', d => {
                const p = state.projection(d.geometry.coordinates);
                return p ? p[1] : 0;
            })
            .style('display', d => state.projection(d.geometry.coordinates) ? null : 'none')
            .attr('r', 6)
            .attr('data-code', d => d.properties[codeField])
            .attr('data-name', d => d.properties[nameField]);
    }

    if (COUNTRY_CONFIG.hierarchy.hasProvinces && state.provincesGeo) {
        // Draw individual province fill polygons (for 전국 quiz, hidden by default)
        provFillLayer.selectAll('path')
            .data(state.provincesGeo.features)
            .enter()
            .append('path')
            .attr('class', 'province-fill-path')
            .attr('d', state.path)
            .attr('data-code', d => d.properties[codeField])
            .attr('data-name', d => d.properties[nameField]);

        d3.select('#provinces-fill-layer').style('display', 'none');

        if (state.provincesMesh) {
            // Draw province internal boundaries (solid, thicker)
            provLayer.append('path')
                .datum(state.provincesMesh)
                .attr('class', 'province-mesh')
                .attr('d', state.path);
        }
        if (state.provincesOuterMesh) {
            // Draw outer boundary
            provLayer.append('path')
                .datum(state.provincesOuterMesh)
                .attr('class', 'province-mesh')
                .attr('d', state.path)
                .style('stroke-width', '2px');
        }
    }
}

// ========== Province & Mode Sidebar ==========

function switchMode(modeId) {
    state.currentModeId = modeId;
    applyModeConfig(modeId);
    loadCountryData(); // Reloads data and updates UI
}

function renderProvinceButtons() {
    const list = document.getElementById('province-list');
    list.innerHTML = '';
    
    // 1. Render Game Modes if available
    if (COUNTRY_CONFIG.modes && COUNTRY_CONFIG.modes.length > 0) {
        COUNTRY_CONFIG.modes.forEach(mode => {
            const btn = document.createElement('button');
            btn.className = 'province-btn mode-btn';
            if (state.currentModeId === mode.id) btn.classList.add('active');
            
            btn.innerHTML = `
                <span class="province-color" style="background: #4b5563"></span>
                <span class="province-name">${mode.label}</span>
            `;
            
            btn.addEventListener('pointerdown', (e) => e.preventDefault());
            btn.addEventListener('click', () => {
                if (state.currentModeId !== mode.id) {
                    switchMode(mode.id);
                }
            });
            list.appendChild(btn);
        });
        
        // Divider
        if (COUNTRY_CONFIG.hierarchy.hasProvinces) {
            const divider = document.createElement('div');
            divider.className = 'sidebar-divider';
            list.appendChild(divider);
        }
    }

    // 2. Render Provinces if available
    if (COUNTRY_CONFIG.hierarchy.hasProvinces && COUNTRY_CONFIG.provinces) {
        // Add "전국" button at the top
        const allBtn = document.createElement('button');
        allBtn.className = 'province-btn nationwide-btn';
        allBtn.dataset.code = 'ALL';
        allBtn.innerHTML = `
            <span class="province-color"></span>
            <span class="province-name">${COUNTRY_CONFIG.emoji} ${COUNTRY_CONFIG.labels.nationwideLabel}</span>
            <span class="province-count" id="prov-count-ALL">0/${COUNTRY_CONFIG.provinces.length}</span>
        `;
        allBtn.addEventListener('pointerdown', (e) => e.preventDefault());
        allBtn.addEventListener('click', () => selectProvince('ALL'));
        list.appendChild(allBtn);

        // Divider
        const divider = document.createElement('div');
        divider.className = 'sidebar-divider';
        list.appendChild(divider);

        // Individual province buttons
        COUNTRY_CONFIG.provinces.forEach((prov) => {
            const btn = document.createElement('button');
            btn.className = 'province-btn';
            btn.dataset.code = prov.code;

            const count = state.municipalitiesGeo.features.filter(
                f => f.properties[COUNTRY_CONFIG.hierarchy.regionCodeField].startsWith(prov.code)
            ).length;

            btn.innerHTML = `
                <span class="province-color" style="background: ${prov.color}; color: ${prov.color};"></span>
                <span class="province-name">${prov.short || prov.name}</span>
                <span class="province-count" id="prov-count-${prov.code}">0/${count}</span>
            `;

            btn.addEventListener('pointerdown', (e) => e.preventDefault());
            btn.addEventListener('click', () => selectProvince(prov.code));

            list.appendChild(btn);
        });
    } else {
        // Flat hierarchy (e.g. USA, UK, Germany) - no sidebar buttons needed for sub-regions.
        // If there are modes, the mode buttons already act as the sidebar content.
        // If there are NO modes, we render a single "Start" button so the sidebar isn't empty.
        if (!COUNTRY_CONFIG.modes || COUNTRY_CONFIG.modes.length === 0) {
            const startBtn = document.createElement('button');
            startBtn.className = 'province-btn nationwide-btn active';
            startBtn.dataset.code = 'ALL';
            startBtn.innerHTML = `
                <span class="province-color"></span>
                <span class="province-name">${COUNTRY_CONFIG.emoji} ${COUNTRY_CONFIG.labels.sidebarTitle}</span>
                <span class="province-count" id="prov-count-ALL">0/${state.municipalitiesGeo.features.length}</span>
            `;
            startBtn.addEventListener('pointerdown', (e) => e.preventDefault());
            startBtn.addEventListener('click', () => selectProvince('ALL'));
            list.appendChild(startBtn);
        }
        
        // Auto-start flat quiz
        setTimeout(() => selectProvince('ALL'), 100);
    }
}

// ========== Event Listeners ==========

function setupEventListeners() {
    // Sidebar toggle
    document.getElementById('sidebar-toggle').addEventListener('click', () => {
        const sidebar = document.getElementById('province-sidebar');
        sidebar.classList.toggle('open');
    });

    document.getElementById('sidebar-close').addEventListener('click', () => {
        document.getElementById('province-sidebar').classList.remove('open');
    });

    document.getElementById('sidebar-overlay').addEventListener('click', () => {
        document.getElementById('province-sidebar').classList.remove('open');
    });

    // Completion modal
    document.getElementById('retry-btn').addEventListener('click', () => {
        document.getElementById('completion-modal').classList.add('hidden');
        selectProvince(state.currentProvince);
    });

    document.getElementById('next-province-btn').addEventListener('click', () => {
        document.getElementById('completion-modal').classList.add('hidden');
        
        if (COUNTRY_CONFIG.hierarchy.hasProvinces && COUNTRY_CONFIG.provinces) {
            if (state.currentProvince === 'ALL') {
                selectProvince(COUNTRY_CONFIG.provinces[0].code);
            } else {
                const idx = COUNTRY_CONFIG.provinces.findIndex(p => p.code === state.currentProvince);
                const nextIdx = (idx + 1) % COUNTRY_CONFIG.provinces.length;
                selectProvince(COUNTRY_CONFIG.provinces[nextIdx].code);
            }
        } else {
            // No provinces, just retry
            selectProvince('ALL');
        }
    });

    // View Results floating button
    document.getElementById('view-results-btn').addEventListener('click', () => {
        document.getElementById('view-results-btn').classList.add('hidden');
        handleCompletion();
    });

    // ===== Zoom controls =====
    document.getElementById('zoom-in-btn').addEventListener('click', (e) => {
        e.stopPropagation();
        state.svg.transition().duration(300).ease(d3.easeCubicOut)
            .call(state.zoom.scaleBy, 1.6);
    });

    document.getElementById('zoom-out-btn').addEventListener('click', (e) => {
        e.stopPropagation();
        state.svg.transition().duration(300).ease(d3.easeCubicOut)
            .call(state.zoom.scaleBy, 1 / 1.6);
    });

    document.getElementById('zoom-reset-btn').addEventListener('click', (e) => {
        e.stopPropagation();
        if (state.isNationwideMode) {
            zoomToProvince('ALL');
        } else if (state.currentProvince) {
            zoomToProvince(state.currentProvince);
        } else {
            state.svg.transition().duration(600).ease(d3.easeCubicInOut)
                .call(state.zoom.transform, d3.zoomIdentity);
        }
    });

    // Map click handler (delegated to SVG - works for both path types)
    d3.select('#map-svg').on('click', function (event) {
        const target = event.target;
        if (isMapPath(target) && target.dataset.code) {
            handleMapRegionClick(target, target.dataset.code);
        }
    });

    // Map hover handler for tooltip (delegated)
    const mapContainer = document.getElementById('map-container');
    const tooltip = document.getElementById('map-tooltip');

    d3.select('#map-svg').on('pointermove', function (event) {
        const target = event.target;
        if (isMapPath(target) &&
            target.classList.contains('quiz-region') &&
            !state.matched.has(target.dataset.code)) {
            // Highlight
            d3.selectAll('.highlight').classed('highlight', false);
            d3.select(target).classed('highlight', true);

            // Show tooltip with "?"
            if (state.selectedCapsule) {
                tooltip.textContent = '여기?';
                tooltip.classList.remove('hidden');
                const rect = mapContainer.getBoundingClientRect();
                tooltip.style.left = (event.clientX - rect.left + 16) + 'px';
                tooltip.style.top = (event.clientY - rect.top - 40) + 'px';
            }
        } else if (isMapPath(target) && target.dataset.code && state.matched.has(target.dataset.code)) {
            // Show name for matched regions
            tooltip.textContent = target.dataset.name;
            tooltip.classList.remove('hidden');
            const rect = mapContainer.getBoundingClientRect();
            tooltip.style.left = (event.clientX - rect.left + 16) + 'px';
            tooltip.style.top = (event.clientY - rect.top - 40) + 'px';
        } else {
            d3.selectAll('.highlight').classed('highlight', false);
            tooltip.classList.add('hidden');
        }
    });

    d3.select('#map-svg').on('pointerleave', function () {
        d3.selectAll('.highlight').classed('highlight', false);
        tooltip.classList.add('hidden');
    });

    // ===== Global pointer events for drag =====
    document.addEventListener('pointermove', handleGlobalPointerMove, { passive: false });
    document.addEventListener('pointerup', handleGlobalPointerUp, { passive: false });
    document.addEventListener('pointercancel', handleGlobalPointerCancel, { passive: false });
}

// ========== Province Selection ==========

function selectProvince(provinceCode) {
    if (provinceCode === 'ALL') {
        selectNationwideQuiz();
        return;
    }

    if (!COUNTRY_CONFIG.hierarchy.hasProvinces) return;
    const provInfo = COUNTRY_CONFIG.provinces.find(p => p.code === provinceCode);
    if (!provInfo) return;

    if (state.isNationwideMode) {
        state.isNationwideMode = false;
        d3.select('#municipalities-layer').style('display', null);
        d3.select('#provinces-layer').style('display', null);
        d3.select('#provinces-fill-layer').style('display', 'none');
        d3.selectAll('.province-fill-path')
            .classed('quiz-region', false)
            .classed('matched', false)
            .classed('highlight', false)
            .style('fill', null)
            .style('opacity', null);
    }

    state.currentProvince = provinceCode;
    state.matched = new Set();
    state.selectedCapsule = null;
    clearTimer();
    state.startTime = Date.now();
    startTimer();

    document.getElementById('view-results-btn').classList.add('hidden');

    const codeField = COUNTRY_CONFIG.hierarchy.regionCodeField;
    state.currentRegions = state.municipalitiesGeo.features.filter(
        f => f.properties[codeField] && f.properties[codeField].startsWith(provinceCode)
    );

    document.getElementById('current-province-name').textContent =
        `${provInfo.name} (${state.currentRegions.length} ${COUNTRY_CONFIG.labels.quizUnit})`;

    document.querySelectorAll('.province-btn:not(.mode-btn)').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.code === provinceCode);
    });

    if (window.innerWidth <= 900) {
        document.getElementById('province-sidebar').classList.remove('open');
    }

    d3.selectAll('.municipality-path')
        .classed('quiz-region', false)
        .classed('matched', false)
        .classed('highlight', false)
        .classed('drag-hover', false)
        .style('fill', null)
        .style('opacity', null)
        .style('animation', null);

    d3.select('#labels-layer').selectAll('*').remove();

    state.svg.classed('quiz-active', true);

    state.currentRegions.forEach(region => {
        d3.select(`[data-code="${region.properties[codeField]}"]`)
            .classed('quiz-region', true);
    });

    zoomToProvince(provinceCode);
    generateCapsules();
    updateProgress();
    document.getElementById('capsules-instruction').classList.remove('hidden');
}

function selectNationwideQuiz() {
    state.currentProvince = 'ALL';
    state.matched = new Set();
    state.selectedCapsule = null;
    state.isNationwideMode = true;
    clearTimer();
    state.startTime = Date.now();
    startTimer();

    document.getElementById('view-results-btn').classList.add('hidden');

    if (COUNTRY_CONFIG.hierarchy.hasProvinces) {
        state.currentRegions = state.provincesGeo.features;
        document.getElementById('current-province-name').textContent =
            `${COUNTRY_CONFIG.labels.nationwideLabel} (${state.currentRegions.length} ${COUNTRY_CONFIG.labels.quizUnit})`;

        d3.select('#municipalities-layer').style('display', 'none');
        d3.select('#provinces-layer').style('display', 'none');
        d3.select('#provinces-fill-layer').style('display', null);

        d3.selectAll('.province-fill-path')
            .classed('quiz-region', true)
            .classed('matched', false)
            .classed('highlight', false)
            .classed('drag-hover', false)
            .style('fill', null)
            .style('opacity', null)
            .style('animation', null);
    } else {
        // Flat hierarchy (e.g. USA, UK, Germany)
        state.currentRegions = state.municipalitiesGeo.features;
        
        if (COUNTRY_CONFIG.hierarchy.filter) {
            state.currentRegions = state.currentRegions.filter(COUNTRY_CONFIG.hierarchy.filter);
        }
        
        document.getElementById('current-province-name').textContent =
            `${COUNTRY_CONFIG.name} (${state.currentRegions.length} ${COUNTRY_CONFIG.labels.quizUnit})`;

        // First reset all paths and mark them as inactive
        d3.selectAll('.municipality-path')
            .classed('quiz-region', false)
            .classed('matched', false)
            .classed('highlight', false)
            .classed('drag-hover', false)
            .classed('inactive', true)
            .style('fill', null)
            .style('opacity', null)
            .style('animation', null);
            
        // Then activate only the current regions
        const codeField = COUNTRY_CONFIG.hierarchy.regionCodeField;
        state.currentRegions.forEach(region => {
            d3.select(`[data-code="${region.properties[codeField]}"]`)
                .classed('quiz-region', true)
                .classed('inactive', false);
        });
    }

    document.querySelectorAll('.province-btn:not(.mode-btn)').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.code === 'ALL');
    });

    if (window.innerWidth <= 900) {
        document.getElementById('province-sidebar').classList.remove('open');
    }

    d3.select('#labels-layer').selectAll('*').remove();
    state.svg.classed('quiz-active', true);
    
    zoomToProvince('ALL');
    generateCapsules();
    updateProgress();
    document.getElementById('capsules-instruction').classList.remove('hidden');
}

function zoomToProvince(provinceCode) {
    const { width, height } = COUNTRY_CONFIG.mapConfig;

    // Find the bounding box of all municipalities in this province
    const provFeatures = state.currentRegions;
    if (provFeatures.length === 0) return;

    // Create a temporary collection to get bounds
    const collection = { type: 'FeatureCollection', features: provFeatures };
    const [[x0, y0], [x1, y1]] = state.path.bounds(collection);

    const dx = x1 - x0;
    const dy = y1 - y0;
    const cx = (x0 + x1) / 2;
    const cy = (y0 + y1) / 2;

    // Calculate scale to fit with padding
    const padding = 0.85;
    const maxZoom = 40;
    const scale = Math.min(
        maxZoom,
        padding / Math.max(dx / width, dy / height)
    );

    const translateX = width / 2 - scale * cx;
    const translateY = height / 2 - scale * cy;

    state.svg.transition()
        .duration(800)
        .ease(d3.easeCubicInOut)
        .call(
            state.zoom.transform,
            d3.zoomIdentity.translate(translateX, translateY).scale(scale)
        );
}

// ========== Capsule Generation ==========

function generateCapsules() {
    const container = document.getElementById('capsules-container');
    container.innerHTML = '';

    const shuffled = [...state.currentRegions];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }

    const nameField = COUNTRY_CONFIG.hierarchy.regionNameField;
    const codeField = COUNTRY_CONFIG.hierarchy.regionCodeField;

    shuffled.forEach(region => {
        const capsule = document.createElement('div');
        capsule.className = 'capsule';
        capsule.id = `capsule-${region.properties[codeField]}`;
        capsule.textContent = region.properties[nameField];
        capsule.dataset.code = region.properties[codeField];

        capsule.addEventListener('pointerdown', (e) => {
            handleCapsulePointerDown(e, capsule);
        });

        container.appendChild(capsule);
    });
}

// ========== Capsule Interaction (Single Pointer) ==========

function handleCapsulePointerDown(e, capsule) {
    // Ignore if already matched
    if (capsule.classList.contains('matched')) return;

    // Only track the FIRST pointer (single touch)
    if (state.activePointerId !== null) return;

    e.preventDefault();
    e.stopPropagation();

    state.activePointerId = e.pointerId;

    // Capture pointer to this element for reliable tracking
    capsule.setPointerCapture(e.pointerId);

    state.dragState = {
        isDragging: false,
        startX: e.clientX,
        startY: e.clientY,
        capsule: capsule,
        code: capsule.dataset.code,
        ghostEl: null,
    };
}

function handleGlobalPointerMove(e) {
    // Only handle our tracked pointer
    if (e.pointerId !== state.activePointerId) return;
    if (!state.dragState.capsule) return;

    const dx = e.clientX - state.dragState.startX;
    const dy = e.clientY - state.dragState.startY;
    const distance = Math.sqrt(dx * dx + dy * dy);

    // Start drag if moved more than 10px threshold
    if (!state.dragState.isDragging && distance > 10) {
        state.dragState.isDragging = true;
        state.dragState.capsule.classList.add('dragging');

        // Deselect any previously selected capsule
        document.querySelectorAll('.capsule.selected').forEach(c => c.classList.remove('selected'));
        state.selectedCapsule = null;

        // Create ghost element
        const ghost = document.createElement('div');
        ghost.className = 'capsule-ghost';
        ghost.textContent = state.dragState.capsule.textContent;
        document.body.appendChild(ghost);
        state.dragState.ghostEl = ghost;
    }

    if (state.dragState.isDragging && state.dragState.ghostEl) {
        // Move ghost
        state.dragState.ghostEl.style.left = e.clientX + 'px';
        state.dragState.ghostEl.style.top = e.clientY + 'px';

        // Highlight map region under cursor
        updateDragHighlight(e.clientX, e.clientY);
    }
}

function handleGlobalPointerUp(e) {
    // Only handle our tracked pointer
    if (e.pointerId !== state.activePointerId) return;

    if (state.dragState.isDragging) {
        // End drag - check drop target
        endDrag(e.clientX, e.clientY);
    } else if (state.dragState.capsule) {
        // It was a click (no significant movement)
        handleCapsuleClick(state.dragState.capsule);
    }

    // Cleanup
    cleanupDrag();
    state.activePointerId = null;
}

function handleGlobalPointerCancel(e) {
    if (e.pointerId !== state.activePointerId) return;
    cleanupDrag();
    state.activePointerId = null;
}

function cleanupDrag() {
    if (state.dragState.ghostEl) {
        state.dragState.ghostEl.remove();
    }
    if (state.dragState.capsule) {
        state.dragState.capsule.classList.remove('dragging');
    }
    d3.selectAll('.drag-hover').classed('drag-hover', false);
    state.dragState = {
        isDragging: false,
        startX: 0,
        startY: 0,
        capsule: null,
        code: null,
        ghostEl: null,
    };
}

function updateDragHighlight(clientX, clientY) {
    // Remove previous highlights
    d3.selectAll('.drag-hover').classed('drag-hover', false);

    // Temporarily hide ghost to find element underneath
    if (state.dragState.ghostEl) {
        state.dragState.ghostEl.style.display = 'none';
    }

    const elementUnder = document.elementFromPoint(clientX, clientY);

    if (state.dragState.ghostEl) {
        state.dragState.ghostEl.style.display = '';
    }

    if (elementUnder && isMapPath(elementUnder) &&
        elementUnder.classList.contains('quiz-region') &&
        !state.matched.has(elementUnder.dataset.code)) {
        d3.select(elementUnder).classed('drag-hover', true);
    }
}

function endDrag(clientX, clientY) {
    // Hide ghost to find element underneath
    if (state.dragState.ghostEl) {
        state.dragState.ghostEl.style.display = 'none';
    }

    const elementUnder = document.elementFromPoint(clientX, clientY);

    if (elementUnder && isMapPath(elementUnder) &&
        elementUnder.classList.contains('quiz-region') &&
        !state.matched.has(elementUnder.dataset.code)) {

        const regionCode = elementUnder.dataset.code;
        const capsuleCode = state.dragState.code;

        if (capsuleCode === regionCode) {
            handleCorrectMatch(capsuleCode);
        } else {
            handleIncorrectMatch(elementUnder, state.dragState.capsule);
        }
    }
}

// ========== Click-to-Match ==========

function handleCapsuleClick(capsule) {
    if (capsule.classList.contains('matched')) return;
    if (state.isShowingInfo) return;

    // Deselect previous
    document.querySelectorAll('.capsule.selected').forEach(c => c.classList.remove('selected'));

    // Select this capsule
    capsule.classList.add('selected');
    state.selectedCapsule = capsule;
}

function handleMapRegionClick(pathElement, regionCode) {
    if (!state.selectedCapsule) return;
    if (state.isShowingInfo) return;
    if (!pathElement.classList.contains('quiz-region')) return;
    if (state.matched.has(regionCode)) return;

    const capsuleCode = state.selectedCapsule.dataset.code;

    if (capsuleCode === regionCode) {
        handleCorrectMatch(capsuleCode);
    } else {
        handleIncorrectMatch(pathElement, state.selectedCapsule);
    }
}

// ========== Match Handling ==========

function handleCorrectMatch(code) {
    state.matched.add(code);

    const codeField = COUNTRY_CONFIG.hierarchy.regionCodeField;
    const nameField = COUNTRY_CONFIG.hierarchy.regionNameField;

    let fillColor;
    if (state.isNationwideMode && COUNTRY_CONFIG.hierarchy.hasProvinces) {
        const prov = COUNTRY_CONFIG.provinces.find(p => p.code === code);
        fillColor = prov ? prov.color : '#06b6d4';
    } else {
        const idx = state.currentRegions.findIndex(r => r.properties[codeField] === code);
        fillColor = REGION_COLORS[idx % REGION_COLORS.length];
    }
    
    const region = state.currentRegions.find(r => r.properties[codeField] === code);
    const regionName = region ? region.properties[nameField] : code;
    
    // For TTS, try to read the nativeName if present, otherwise just the regular name
    const nativeName = region && region.properties.nativeName ? region.properties.nativeName : regionName;

    // Update map region with smooth transition
    const pathEl = d3.select(`[data-code="${code}"]`);
    pathEl
        .classed('matched', true)
        .classed('quiz-region', false)
        .classed('highlight', false)
        .classed('drag-hover', false)
        .style('fill', fillColor + 'BB')
        .style('animation', 'regionMatchGlow 0.6s ease');

    // Add name label on map
    addMapLabel(code);

    // Play correct sound
    playCorrectSound();

    // Update capsule
    const capsule = document.getElementById(`capsule-${code}`);
    if (capsule) {
        capsule.classList.add('matched');
        capsule.classList.remove('selected', 'dragging');
        capsule.style.animation = 'successPulse 0.4s ease';
    }

    // Clear selection
    state.selectedCapsule = null;

    // Update progress
    updateProgress();

    // Show info popup + TTS
    const description = (typeof REGION_DESCRIPTIONS !== 'undefined' && REGION_DESCRIPTIONS[code])
        ? REGION_DESCRIPTIONS[code]
        : `${regionName}에 대해 알아보세요!`;

    showInfoPopup(regionName, description, fillColor, nativeName, () => {
        if (state.matched.size === state.currentRegions.length) {
            clearTimer();
            document.getElementById('view-results-btn').classList.remove('hidden');
        }
    });
}

// ========== Info Popup + TTS ==========

function showInfoPopup(name, description, color, nativeName, onDismiss) {
    state.isShowingInfo = true;

    const popup = document.getElementById('info-popup');
    document.getElementById('info-popup-name').textContent = name;
    document.getElementById('info-popup-desc').textContent = description;
    document.getElementById('info-popup-color-bar').style.background = color;

    popup.classList.remove('hidden', 'fade-out');

    const dismiss = () => dismissInfoPopup(onDismiss);
    
    // 팝업이 최소 4초는 표시되도록 보장 (TTS가 너무 빨리 끝나거나 에러가 나도 바로 사라지지 않음)
    const showTime = Date.now();
    let isDismissed = false;
    
    const safeDismiss = () => {
        if (isDismissed) return;
        isDismissed = true;
        const elapsed = Date.now() - showTime;
        const remaining = Math.max(0, 4000 - elapsed);
        setTimeout(dismiss, remaining);
    };

    // 만약 콜백이 안 불릴 경우를 대비한 넉넉한 45초 폴백 (긴 설명 대비)
    setTimeout(safeDismiss, 45000);

    const nativeLang = COUNTRY_CONFIG.ttsLang || 'ko';

    // Step 1: Read Native Name, Step 2: Read Korean Description
    const playDesc = () => {
        playGoogleTTS(description, 'ko', safeDismiss, () => {
            playBrowserTTS(description, 'ko-KR', safeDismiss);
        });
    };

    playGoogleTTS(nativeName, nativeLang, playDesc, () => {
        // Fallback to browser
        playBrowserTTS(nativeName, nativeLang === 'ko' ? 'ko-KR' : (nativeLang === 'en' ? 'en-US' : nativeLang), playDesc);
    });
}

function playGoogleTTS(text, lang, onEnd, onError) {
    try {
        let handled = false;
        const safeOnEnd = () => { if (!handled) { handled = true; onEnd(); } };
        const safeOnError = () => { if (!handled) { handled = true; onError(); } };

        const audio = new Audio();
        const encoded = encodeURIComponent(text);
        audio.src = `https://translate.google.com/translate_tts?ie=UTF-8&tl=${lang}&client=tw-ob&q=${encoded}`;
        audio.onended = safeOnEnd;
        audio.onerror = safeOnError;
        audio.play().catch(safeOnError);
    } catch (e) {
        onError();
    }
}

function playBrowserTTS(text, lang, onEnd) {
    try {
        window.speechSynthesis.cancel();
        
        let handled = false;
        const safeOnEnd = () => { if (!handled) { handled = true; onEnd(); } };

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = lang;
        utterance.rate = 1.0;
        utterance.pitch = 1.05;

        const voices = window.speechSynthesis.getVoices();
        const preferredVoice = voices.find(v => v.lang.startsWith(lang.split('-')[0]) && v.name.includes('Google'))
            || voices.find(v => v.lang.startsWith(lang.split('-')[0]));
        if (preferredVoice) utterance.voice = preferredVoice;

        utterance.onend = safeOnEnd;
        utterance.onerror = safeOnEnd;
        window.speechSynthesis.speak(utterance);
        
        // 크롬 브라우저의 긴 문장 끊김 방지용 타이머 (10초마다 pause/resume)
        const chromeBugFix = setInterval(() => {
            if (!window.speechSynthesis.speaking) {
                clearInterval(chromeBugFix);
            } else {
                window.speechSynthesis.pause();
                window.speechSynthesis.resume();
            }
        }, 10000);
        
    } catch (e) {
        setTimeout(onEnd, 2000);
    }
}

function dismissInfoPopup(onDismiss) {
    if (!state.isShowingInfo) return;
    state.isShowingInfo = false;

    // Stop any playing audio
    try { window.speechSynthesis.cancel(); } catch (e) {}

    const popup = document.getElementById('info-popup');
    popup.classList.add('fade-out');

    setTimeout(() => {
        popup.classList.add('hidden');
        popup.classList.remove('fade-out');
        if (onDismiss) onDismiss();
    }, 350);
}

function handleIncorrectMatch(pathElement, capsule) {
    // Shake animation on both map region and capsule
    playIncorrectSound();
    d3.select(pathElement)
        .classed('shake', true)
        .style('fill', 'rgba(239, 68, 68, 0.25)');

    if (capsule) {
        capsule.classList.add('shake', 'error-flash');
    }

    setTimeout(() => {
        d3.select(pathElement)
            .classed('shake', false)
            .style('fill', null);

        if (capsule) {
            capsule.classList.remove('shake', 'error-flash');
        }
    }, 600);
}

// ========== Map Labels ==========

function addMapLabel(code) {
    const codeField = COUNTRY_CONFIG.hierarchy.regionCodeField;
    const nameField = COUNTRY_CONFIG.hierarchy.regionNameField;
    const feature = state.currentRegions.find(r => r.properties[codeField] === code);
    if (!feature) return;

    const centroid = state.path.centroid(feature);
    if (isNaN(centroid[0]) || isNaN(centroid[1])) return;

    const labelsLayer = d3.select('#labels-layer');

    const displaySize = 20;
    const currentScale = d3.zoomTransform(state.svg.node()).k;
    const svgSize = displaySize / currentScale;

    labelsLayer.append('text')
        .attr('class', 'map-label')
        .attr('x', centroid[0])
        .attr('y', centroid[1])
        .attr('text-anchor', 'middle')
        .attr('dominant-baseline', 'central')
        .attr('data-display-size', displaySize)
        .style('font-size', svgSize + 'px')
        .text(feature.properties[nameField]);
}

// ========== Progress & Timer ==========

function updateProgress() {
    const total = state.currentRegions.length;
    const matched = state.matched.size;
    const percent = total > 0 ? Math.round((matched / total) * 100) : 0;

    document.getElementById('score-text').textContent = `${matched} / ${total}`;
    document.getElementById('progress-bar').style.width = `${percent}%`;
    document.getElementById('progress-text').textContent = `${percent}%`;

    // Update province button count
    if (state.currentProvince) {
        const countEl = document.getElementById(`prov-count-${state.currentProvince}`);
        if (countEl) countEl.textContent = `${matched}/${total}`;
    }
}

function startTimer() {
    state.timerInterval = setInterval(() => {
        if (!state.startTime) return;
        const elapsed = Math.floor((Date.now() - state.startTime) / 1000);
        const minutes = String(Math.floor(elapsed / 60)).padStart(2, '0');
        const seconds = String(elapsed % 60).padStart(2, '0');
        document.getElementById('timer-text').textContent = `${minutes}:${seconds}`;
    }, 1000);
}

function clearTimer() {
    if (state.timerInterval) {
        clearInterval(state.timerInterval);
        state.timerInterval = null;
    }
    document.getElementById('timer-text').textContent = '00:00';
}

// ========== Completion ==========

function handleCompletion() {
    clearTimer();

    const elapsed = Math.floor((Date.now() - state.startTime) / 1000);
    const minutes = Math.floor(elapsed / 60);
    const seconds = elapsed % 60;
    const total = state.currentRegions.length;

    let regionTitle = COUNTRY_CONFIG.name;
    if (COUNTRY_CONFIG.hierarchy.hasProvinces && state.currentProvince !== 'ALL') {
        const provInfo = COUNTRY_CONFIG.provinces.find(p => p.code === state.currentProvince);
        if (provInfo) regionTitle = provInfo.name;
    }

    let stars = 3;
    const avgTimePerRegion = elapsed / total;
    if (avgTimePerRegion > 15) stars = 1;
    else if (avgTimePerRegion > 8) stars = 2;

    state.completedProvinces.add(state.currentProvince);
    const btn = document.querySelector(`.province-btn[data-code="${state.currentProvince}"]`);
    if (btn) btn.classList.add('completed');

    document.getElementById('completion-message').innerHTML = `
        <strong>${regionTitle}</strong>의<br>
        ${total} ${COUNTRY_CONFIG.labels.quizUnit}를 모두 맞추셨습니다!<br>
        <span style="color: var(--accent-cyan); font-size: 22px; font-weight: 700;">
            ${minutes}분 ${seconds}초
        </span>
    `;

    const starsEl = document.getElementById('modal-stars');
    starsEl.textContent = '⭐'.repeat(stars) + '☆'.repeat(3 - stars);

    document.getElementById('completion-modal').classList.remove('hidden');
}
