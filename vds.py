<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Interactive Disease Spread Map</title>
<!-- Leaflet CSS -->
<link
  rel="stylesheet"
  href="https://unpkg.com/leaflet/dist/leaflet.css"
/>
<!-- Google Fonts: Inter -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet" />
<!-- Material Icons -->
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" />
<style>
  :root {
    --color-bg: #f9fafb;
    --color-text-primary: #111827;
    --color-text-secondary: #4b5563;
    --color-accent: #2563eb;
    --color-error: #ef4444;
    --color-success: #10b981;
    --color-muted: #6b7280;
    --font-family: 'Inter', sans-serif;

    /* Circle colors - covid */
    --covid-high: #b22222;   /* Firebrick */
    --covid-mid: #ff6347;    /* Tomato */
    --covid-low: #ffa07a;    /* Light Salmon */

    /* Circle colors - tbc */
    --tbc-high: #00008b;     /* Dark Blue */
    --tbc-mid: #1e90ff;      /* Dodger Blue */
    --tbc-low: #87cefa;      /* Light Sky Blue */

    /* Circle colors - ispa */
    --ispa-high: #006400;    /* Dark Green */
    --ispa-mid: #228b22;     /* Forest Green */
    --ispa-low: #7cfc00;     /* Lawn Green */

    /* Legend box shadow */
    --shadow: 0 6px 12px rgba(0,0,0,0.1);
  }

  * {
    box-sizing: border-box;
  }

  body {
    margin: 0;
    font-family: var(--font-family);
    background: var(--color-bg);
    color: var(--color-text-primary);
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }

  header {
    background: white;
    box-shadow: var(--shadow);
    padding: 16px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 1000;
  }

  header h1 {
    font-weight: 700;
    font-size: 1.5rem;
    color: var(--color-accent);
    margin: 0;
  }

  .disease-selector {
    font-size: 1rem;
    font-weight: 600;
    color: var(--color-text-primary);
    padding: 8px 12px;
    border-radius: 8px;
    border: 1.5px solid var(--color-accent);
    cursor: pointer;
    min-width: 160px;
    outline-offset: 2px;
  }
  .disease-selector:focus {
    outline: 3px solid var(--color-accent);
  }

  #map {
    flex-grow: 1;
    height: 80vh;
    min-height: 500px;
    margin: 24px;
    border-radius: 16px;
    box-shadow: var(--shadow);
  }

  /* Popup content styling */
  .popup-content {
    font-family: var(--font-family);
    width: 260px;
    color: var(--color-text-secondary);
  }
  .popup-content h4 {
    margin: 0 0 8px 0;
    font-weight: 700;
    color: var(--color-accent);
  }
  .popup-content strong {
    display: inline-block;
    width: 90px;
  }
  .popup-content hr {
    border: none;
    border-top: 1px solid #d1d5db;
    margin: 8px 0;
  }

  /* Legend styling */
  .legend {
    position: fixed;
    bottom: 50px;
    left: 50px;
    width: 200px;
    background: white;
    border-radius: 12px;
    border: 2px solid #d1d5db;
    box-shadow: var(--shadow);
    font-family: var(--font-family);
    padding: 12px 16px;
    font-size: 14px;
    color: var(--color-text-secondary);
    z-index: 9999;
    user-select: none;
  }

  .legend b {
    display: block;
    margin-bottom: 8px;
    font-weight: 700;
    color: var(--color-text-primary);
  }

  .legend-item {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
  }

  .legend-color {
    width: 20px;
    height: 20px;
    border-radius: 6px;
    margin-right: 11px;
    opacity: 0.85;
    flex-shrink: 0;
  }

  /* Tooltip fix for small screens */
  @media (max-width: 640px) {
    #map {
      margin: 12px;
      height: 70vh;
      min-height: 400px;
    }
    .legend {
      width: 160px;
      font-size: 12px;
      bottom: 20px;
      left: 20px;
      padding: 10px 12px;
    }
  }
</style>
</head>
<body>
<header>
  <h1>Disease Spread Map</h1>
  <select aria-label="Choose Disease" id="diseaseSelect" class="disease-selector">
    <option value="COVID-19" selected>COVID-19</option>
    <option value="TBC">TBC</option>
    <option value="ISPA">ISPA</option>
  </select>
</header>
<div id="map" role="region" aria-label="Map showing disease spread"></div>
<div id="legend" class="legend" aria-live="polite" aria-atomic="true"></div>

<!-- Leaflet JS -->
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
<script>
  // Data sets
  const dataSets = {
    "COVID-19": [
      {"lokasi":"Jakarta Selatan","lat":-6.260,"lng":106.794,"kasus":12500,"meninggal":500,"sembuh":11000,"laki":7000,"perempuan":5500},
      {"lokasi":"Jakarta Timur","lat":-6.215,"lng":106.878,"kasus":10700,"meninggal":420,"sembuh":9000,"laki":6000,"perempuan":4700},
      {"lokasi":"Jakarta Barat","lat":-6.174,"lng":106.799,"kasus":9800,"meninggal":380,"sembuh":8500,"laki":5200,"perempuan":4600},
      {"lokasi":"Jakarta Utara","lat":-6.123,"lng":106.865,"kasus":6700,"meninggal":200,"sembuh":6000,"laki":3500,"perempuan":3200},
      {"lokasi":"Jakarta Pusat","lat":-6.175,"lng":106.827,"kasus":5400,"meninggal":150,"sembuh":5000,"laki":2800,"perempuan":2600}
    ],
    "TBC": [
      {"lokasi":"Jakarta Selatan","lat":-6.260,"lng":106.794,"kasus":3000,"meninggal":100,"sembuh":2900,"laki":1800,"perempuan":1200},
      {"lokasi":"Jakarta Timur","lat":-6.215,"lng":106.878,"kasus":2500,"meninggal":80,"sembuh":2400,"laki":1500,"perempuan":1000},
      {"lokasi":"Jakarta Barat","lat":-6.174,"lng":106.799,"kasus":2000,"meninggal":60,"sembuh":1900,"laki":1200,"perempuan":800},
      {"lokasi":"Jakarta Utara","lat":-6.123,"lng":106.865,"kasus":1500,"meninggal":40,"sembuh":1400,"laki":800,"perempuan":700},
      {"lokasi":"Jakarta Pusat","lat":-6.175,"lng":106.827,"kasus":1200,"meninggal":30,"sembuh":1150,"laki":650,"perempuan":550}
    ],
    "ISPA": [
      {"lokasi":"Jakarta Selatan","lat":-6.260,"lng":106.794,"kasus":4000,"meninggal":50,"sembuh":3800,"laki":2200,"perempuan":1800},
      {"lokasi":"Jakarta Timur","lat":-6.215,"lng":106.878,"kasus":3500,"meninggal":40,"sembuh":3400,"laki":1900,"perempuan":1600},
      {"lokasi":"Jakarta Barat","lat":-6.174,"lng":106.799,"kasus":3000,"meninggal":30,"sembuh":2900,"laki":1600,"perempuan":1400},
      {"lokasi":"Jakarta Utara","lat":-6.123,"lng":106.865,"kasus":2500,"meninggal":20,"sembuh":2400,"laki":1300,"perempuan":1200},
      {"lokasi":"Jakarta Pusat","lat":-6.175,"lng":106.827,"kasus":2200,"meninggal":15,"sembuh":2100,"laki":1150,"perempuan":1050}
    ]
  };

  // Color functions matching python logic
  function colorCovid(kasus) {
    if (kasus > 11000) return getComputedStyle(document.documentElement).getPropertyValue('--covid-high').trim();
    if (kasus > 8000) return getComputedStyle(document.documentElement).getPropertyValue('--covid-mid').trim();
    return getComputedStyle(document.documentElement).getPropertyValue('--covid-low').trim();
  }
  function colorTbc(kasus) {
    if (kasus > 2500) return getComputedStyle(document.documentElement).getPropertyValue('--tbc-high').trim();
    if (kasus > 1500) return getComputedStyle(document.documentElement).getPropertyValue('--tbc-mid').trim();
    return getComputedStyle(document.documentElement).getPropertyValue('--tbc-low').trim();
  }
  function colorIspa(kasus) {
    if (kasus > 3500) return getComputedStyle(document.documentElement).getPropertyValue('--ispa-high').trim();
    if (kasus > 2500) return getComputedStyle(document.documentElement).getPropertyValue('--ispa-mid').trim();
    return getComputedStyle(document.documentElement).getPropertyValue('--ispa-low').trim();
  }

  // Initializing map
  const map = L.map('map', {zoomControl: true}).setView([-6.2088, 106.8456], 11);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution:
      '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(map);

  // Circle marker layer group
  let markersLayer = L.layerGroup().addTo(map);

  // Title marker on map
  // Implement with DivIcon at fixed coordinates
  const titleMarkerPos = [-6.38, 106.82];
  let titleMarker = L.marker(titleMarkerPos, {
    icon: L.divIcon({
      className: 'title-marker',
      html: '<div style="font-size:24pt; font-weight:700; color:#111827; font-family: var(--font-family); user-select:none;">PENYEBARAN COVID-19</div>',
      iconSize: [250, 30],
      iconAnchor: [125, 15],
    }),
    interactive: false,
  }).addTo(map);

  // Function to create popup HTML string
  function createPopupHTML(d) {
    return `
      <div class="popup-content" role="dialog" aria-label="Data for ${d.lokasi}">
        <h4>${d.lokasi}</h4>
        <div>
          <strong style="color: var(--color-error);">Kasus:</strong> ${d.kasus}<br />
          <strong style="color: var(--color-success);">Sembuh:</strong> ${d.sembuh}<br />
          <strong style="color: var(--color-muted);">Meninggal:</strong> ${d.meninggal}<br />
          <hr />
          <strong style="color: var(--color-accent);">Laki-laki:</strong> ${d.laki}<br />
          <strong style="color: #ec4899;">Perempuan:</strong> ${d.perempuan}
        </div>
      </div>`;
  }

  // Legend text for case levels
  const legendLabels = ["Rendah", "Sedang", "Tinggi"];

  // Current disease dataset and color function storage
  let currentDisease = "COVID-19";
  let currentColorFunc = colorCovid;
  let currentRadius = 12;

  // Function to update map markers and legend based on selected disease
  function updateMap(disease) {
    currentDisease = disease;
    markersLayer.clearLayers();

    let data = dataSets[disease];
    // Update title marker text and position
    let titleText = "PENYEBARAN " + disease;
    titleMarker.setIcon(L.divIcon({
      className: 'title-marker',
      html: <div style="font-size:24pt; font-weight:700; color:#111827; font-family: var(--font-family); user-select:none;">${titleText}</div>,
      iconSize: [250, 30],
      iconAnchor: [125, 15],
    }));

    // Set color function and radius based on disease
    if(disease === "COVID-19"){
      currentColorFunc = colorCovid;
      currentRadius = 12;
    } else if(disease === "TBC"){
      currentColorFunc = colorTbc;
      currentRadius = 10;
    } else {
      currentColorFunc = colorIspa;
      currentRadius = 10;
    }

    // Add markers
    data.forEach(d => {
      const circle = L.circleMarker([d.lat, d.lng], {
        radius: currentRadius,
        color: currentColorFunc(d.kasus),
        weight: 2,
        fill: true,
        fillColor: currentColorFunc(d.kasus),
        fillOpacity: 0.75,
      }).bindPopup(createPopupHTML(d))
      .bindTooltip(d.lokasi, {sticky: true});
      markersLayer.addLayer(circle);
    });

    // Update legend
    updateLegend();
  }

  function updateLegend(){
    const legendEl = document.getElementById('legend');
    let lowColor = currentColorFunc(0);
    let midColor = currentColorFunc(9999);
    let highColor = currentColorFunc(99999);

    legendEl.innerHTML = `
      <b>Legenda PENYEBARAN ${currentDisease}</b>
      <div class="legend-item"><span class="legend-color" style="background:${lowColor};"></span> ${legendLabels[0]}</div>
      <div class="legend-item"><span class="legend-color" style="background:${midColor};"></span> ${legendLabels[1]}</div>
      <div class="legend-item"><span class="legend-color" style="background:${highColor};"></span> ${legendLabels[2]}</div>`;
  }

  // Initial load
  updateMap(currentDisease);

  // Handle selection changes
  const selectEl = document.getElementById('diseaseSelect');
  selectEl.addEventListener('change', (e) => {
    updateMap(e.target.value);
  });
</script>
</body>
</html>
