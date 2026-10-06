const DEFAULT_WEIGHTS = {
  language: 32,
  distance: 18,
  age: 20,
  access: 15,
  price: 15,
};

const WEIGHT_LABELS = {
  language: "English first",
  distance: "Short trip",
  age: "Right for 15 months",
  access: "Vantaa can offer it",
  price: "Fee near the city cap",
};

const BAR_LABELS = {
  language: "English",
  distance: "Trip",
  age: "Age fit",
  access: "A place",
  price: "Fee",
};

const state = {
  data: null,
  weights: { ...DEFAULT_WEIGHTS },
  filters: {
    q: "",
    language: "all",
    sector: "all",
    city: "all",
    km: 10,
    ageOk: false,
    sortDistance: false,
  },
  selected: null,
  shortlist: loadShortlist(),
  map: null,
  cluster: null,
  markers: new Map(),
};

const $ = (id) => document.getElementById(id);

function loadShortlist() {
  try {
    return new Set(JSON.parse(localStorage.getItem("rekola-daycare-shortlist") || "[]"));
  } catch {
    return new Set();
  }
}

function saveShortlist() {
  try {
    localStorage.setItem("rekola-daycare-shortlist", JSON.stringify([...state.shortlist]));
  } catch {
    /* private mode */
  }
}

function distanceFactor(km) {
  const t = Math.min(km, 10) / 10;
  return (1 - t) ** 1.35;
}

function scored(daycare) {
  const w = state.weights;
  const parts = {
    language: w.language * daycare.languageFactor,
    distance: w.distance * distanceFactor(daycare.distanceKm),
    age: w.age * daycare.ageFactor,
    access: w.access * daycare.accessFactor,
    price: w.price * daycare.priceFactor,
  };
  const weightSum = Object.values(w).reduce((sum, n) => sum + n, 0) || 1;
  const raw = Object.values(parts).reduce((sum, n) => sum + n, 0);
  const total = (raw / weightSum) * 100;
  return { total, parts, weightSum };
}

function tripLabel(km) {
  if (km < 1.3) {
    const minutes = Math.max(8, Math.round((km / 4) * 60));
    return `About ${minutes} min on foot with a stroller`;
  }
  const minutes = Math.max(8, Math.round(km * 2.2 + 4));
  return `About ${minutes} min by car, rough local guess`;
}

function pinClass(daycare) {
  if (daycare.language === "english") return "pin-en";
  if (daycare.language === "shower") return "pin-shower";
  if (daycare.municipality !== "vantaa") return "pin-out";
  if (daycare.sector !== "municipal") return "pin-private";
  return "pin-muni";
}

function matches(daycare) {
  const f = state.filters;
  if (daycare.distanceKm > f.km + 0.001) return false;
  if (f.ageOk && (daycare.ageFit === "preschool" || daycare.ageFit === "weak")) return false;
  if (f.city !== "all" && daycare.municipality !== f.city) return false;
  if (f.sector !== "all" && daycare.sector !== f.sector) return false;
  if (f.language === "english" && daycare.language !== "english" && daycare.language !== "shower") return false;
  if (f.language === "finnish" && daycare.language !== "finnish") return false;
  if (f.language === "swedish" && daycare.language !== "swedish") return false;
  if (f.language === "other" && ["english", "shower", "finnish", "swedish"].includes(daycare.language)) return false;
  if (f.q) {
    const blob = [
      daycare.name,
      daycare.address,
      daycare.city,
      daycare.languageLabel,
      daycare.sectorLabel,
      ...(daycare.curriculum || []),
      ...(daycare.traits || []),
    ].join(" ").toLowerCase();
    if (!blob.includes(f.q)) return false;
  }
  return true;
}

function visible() {
  const rows = state.data.daycares.filter(matches).map((daycare) => ({
    daycare,
    score: scored(daycare).total,
  }));
  rows.sort((a, b) => {
    if (state.filters.sortDistance) return a.daycare.distanceKm - b.daycare.distanceKm || b.score - a.score;
    return b.score - a.score || a.daycare.distanceKm - b.daycare.distanceKm;
  });
  return rows;
}

function chip(container, value, label, group) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "chip";
  button.textContent = label;
  button.dataset.value = value;
  button.setAttribute("aria-pressed", String(state.filters[group] === value));
  button.addEventListener("click", () => {
    state.filters[group] = value;
    container.querySelectorAll(".chip").forEach((el) => {
      el.setAttribute("aria-pressed", String(el.dataset.value === value));
    });
    render();
  });
  container.appendChild(button);
}

function setupFilters() {
  const langs = $("lang-chips");
  const sectors = $("sector-chips");
  const cities = $("city-chips");
  [
    ["all", "Any language"],
    ["english", "English"],
    ["finnish", "Finnish"],
    ["swedish", "Swedish"],
    ["other", "Other"],
  ].forEach(([value, label]) => chip(langs, value, label, "language"));
  [
    ["all", "Any provider"],
    ["municipal", "Municipal"],
    ["voucher", "Voucher"],
    ["private", "Private"],
  ].forEach(([value, label]) => chip(sectors, value, label, "sector"));
  [
    ["all", "Any city"],
    ["vantaa", "Vantaa"],
    ["helsinki", "Helsinki"],
    ["kerava", "Kerava"],
    ["tuusula", "Tuusula"],
  ].forEach(([value, label]) => chip(cities, value, label, "city"));

  $("q").addEventListener("input", (event) => {
    state.filters.q = event.target.value.trim().toLowerCase();
    render();
  });
  $("km").addEventListener("input", (event) => {
    state.filters.km = Number(event.target.value);
    $("km-label").textContent = state.filters.km.toFixed(1).replace(".0", "");
    render();
  });
  $("age-ok").addEventListener("change", (event) => {
    state.filters.ageOk = event.target.checked;
    render();
  });
  $("sort-distance").addEventListener("change", (event) => {
    state.filters.sortDistance = event.target.checked;
    render();
  });
}

function setupWeights() {
  const box = $("sliders");
  Object.entries(WEIGHT_LABELS).forEach(([key, label]) => {
    const row = document.createElement("label");
    const name = document.createElement("span");
    name.textContent = label;
    const input = document.createElement("input");
    input.type = "range";
    input.min = "0";
    input.max = "40";
    input.value = String(state.weights[key]);
    input.setAttribute("aria-label", label);
    const num = document.createElement("span");
    num.textContent = String(state.weights[key]);
    input.addEventListener("input", () => {
      state.weights[key] = Number(input.value);
      num.textContent = input.value;
      render();
    });
    row.append(name, input, num);
    box.appendChild(row);
  });
  $("reset-weights").addEventListener("click", () => {
    state.weights = { ...DEFAULT_WEIGHTS };
    box.querySelectorAll("label").forEach((row) => {
      const input = row.querySelector("input");
      const key = Object.entries(WEIGHT_LABELS).find(([, label]) => row.firstChild.textContent === label)?.[0];
      if (!key) return;
      input.value = String(DEFAULT_WEIGHTS[key]);
      row.lastChild.textContent = String(DEFAULT_WEIGHTS[key]);
    });
    render();
  });
}

function setupMap() {
  const home = state.data.home;
  state.map = L.map("map", { scrollWheelZoom: true }).setView([home.lat, home.lon], 12);
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    maxZoom: 19,
  }).addTo(state.map);
  L.circle([home.lat, home.lon], {
    radius: 10000,
    color: "#1d6b45",
    weight: 1.5,
    dashArray: "6 6",
    fillColor: "#1d6b45",
    fillOpacity: 0.05,
  }).addTo(state.map);
  const homeIcon = L.divIcon({ className: "", html: '<div class="home-pin">Home</div>', iconSize: [64, 28], iconAnchor: [32, 14] });
  L.marker([home.lat, home.lon], { icon: homeIcon, zIndexOffset: 1000, title: "Lipstikkakuja 14" }).addTo(state.map);
  state.cluster = L.markerClusterGroup({
    showCoverageOnHover: false,
    maxClusterRadius: 42,
    disableClusteringAtZoom: 15,
  });
  state.map.addLayer(state.cluster);
}

function markerIcon(daycare, on) {
  const score = Math.round(scored(daycare).total);
  return L.divIcon({
    className: "",
    html: `<div class="pin ${pinClass(daycare)} ${on ? "on" : ""}">${score}</div>`,
    iconSize: [34, 34],
    iconAnchor: [17, 17],
  });
}

function syncMarkers(rows) {
  const wanted = new Set(rows.map((row) => row.daycare.id));
  for (const [id, marker] of state.markers) {
    if (!wanted.has(id)) {
      state.cluster.removeLayer(marker);
      state.markers.delete(id);
    }
  }
  rows.forEach(({ daycare }) => {
    let marker = state.markers.get(daycare.id);
    const icon = markerIcon(daycare, daycare.id === state.selected);
    if (!marker) {
      marker = L.marker([daycare.lat, daycare.lon], { icon, title: daycare.name, keyboard: true });
      marker.on("click", () => select(daycare.id, false));
      state.cluster.addLayer(marker);
      state.markers.set(daycare.id, marker);
    } else {
      marker.setIcon(icon);
    }
  });
}

function select(id, pan = true) {
  state.selected = id;
  const daycare = state.data.daycares.find((item) => item.id === id);
  if (!daycare) return;
  renderCard(daycare);
  renderList();
  syncMarkers(visible());
  if (pan) {
    state.map.setView([daycare.lat, daycare.lon], Math.max(state.map.getZoom(), 14), { animate: true });
    const marker = state.markers.get(id);
    if (marker) state.cluster.zoomToShowLayer(marker, () => marker.openPopup?.());
    document.querySelector(".map-section")?.scrollIntoView({ block: "nearest" });
  }
}

function renderCard(daycare) {
  const card = $("card");
  const result = scored(daycare);
  const bits = [
    ["Distance", `${daycare.distanceKm.toFixed(1)} km`],
    ["Trip", tripLabel(daycare.distanceKm)],
    ["Language", daycare.languageLabel],
    ["Ages", daycare.ageLabel],
    ["Provider", daycare.sectorLabel],
    ["Price", daycare.priceLabel],
    ["Hours", daycare.hours || "Not published"],
    ["Focus", (daycare.curriculum || []).filter((item) => item !== "Meals included").join(", ") || "National ECEC curriculum"],
  ];
  const bars = Object.entries(BAR_LABELS).map(([key, label]) => {
    const max = state.weights[key] || 0;
    const got = result.parts[key];
    const pct = max ? Math.round((got / max) * 100) : 0;
    return `<div class="bar"><span>${label}</span><i><b style="width:${pct}%"></b></i><span>${Math.round(got)}</span></div>`;
  }).join("");
  const tags = [
    daycare.city,
    daycare.language === "english" ? "English" : daycare.language === "shower" ? "Some English" : daycare.languageLabel.split(",")[0],
    daycare.sectorLabel.split(",")[0],
    daycare.confidence === "high" ? "City register" : "Check details",
  ];
  const links = [];
  if (daycare.website) links.push(`<a class="primary" href="${escapeAttr(daycare.website)}" target="_blank" rel="noreferrer">Daycare site</a>`);
  if (daycare.sourceUrl) links.push(`<a class="ghost" href="${escapeAttr(daycare.sourceUrl)}" target="_blank" rel="noreferrer">Source record</a>`);
  const saved = state.shortlist.has(daycare.id);
  $("card-body").innerHTML = `
    <p class="eyebrow">${escapeHtml(daycare.address || "")} ${escapeHtml(daycare.zip || "")} ${escapeHtml(daycare.city)}</p>
    <h3>${escapeHtml(daycare.name)}</h3>
    <div class="score-row">
      <div>
        <div class="score-num">${Math.round(result.total)}</div>
        <div class="score-cap">out of 100</div>
      </div>
      <p class="addr">Score for a November 2027 start at about 15 months, from Lipstikkakuja 14.</p>
    </div>
    <ul class="tags">${tags.map((tag) => `<li>${escapeHtml(tag)}</li>`).join("")}</ul>
    <p class="summary">${escapeHtml(daycare.summary)}</p>
    ${bars}
    <div class="facts-grid">${bits.map(([k, v]) => `<div><strong>${escapeHtml(k)}</strong>${escapeHtml(v)}</div>`).join("")}</div>
    <div class="split">
      <div class="pros"><h4>Pros</h4><ul>${(daycare.pros || []).map((item) => `<li>${escapeHtml(item)}</li>`).join("") || "<li>None recorded.</li>"}</ul></div>
      <div class="cons"><h4>Cons</h4><ul>${(daycare.cons || []).map((item) => `<li>${escapeHtml(item)}</li>`).join("") || "<li>None recorded.</li>"}</ul></div>
    </div>
    ${(daycare.traits || []).length ? `<p class="trait">${(daycare.traits || []).map(escapeHtml).join(" · ")}</p>` : ""}
    ${daycare.phone ? `<p><strong>Phone.</strong> ${escapeHtml(daycare.phone)}${daycare.contact ? " · " + escapeHtml(daycare.contact) : ""}</p>` : ""}
    ${daycare.email ? `<p><strong>Email.</strong> ${escapeHtml(daycare.email)}</p>` : ""}
    <div class="card-actions">
      <button type="button" class="ghost" id="save-btn">${saved ? "Remove from shortlist" : "Save to shortlist"}</button>
      ${links.join("")}
    </div>
    <p class="addr">Source: ${escapeHtml(daycare.source)}. ${daycare.confidence === "high" ? "Taken from the city service register." : "Thinner public record. Confirm groups, hours and the fee before you apply."}</p>
  `;
  $("save-btn").addEventListener("click", () => {
    if (state.shortlist.has(daycare.id)) state.shortlist.delete(daycare.id);
    else state.shortlist.add(daycare.id);
    saveShortlist();
    renderCard(daycare);
    renderShortlist();
  });
  card.hidden = false;
}

function renderShortlist() {
  const box = $("shortlist");
  const items = state.data.daycares.filter((daycare) => state.shortlist.has(daycare.id));
  box.hidden = items.length === 0;
  box.innerHTML = "";
  items
    .sort((a, b) => scored(b).total - scored(a).total)
    .forEach((daycare) => {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = `${daycare.name.replace(/, yksityinen/i, "")} · ${Math.round(scored(daycare).total)}`;
      button.addEventListener("click", () => select(daycare.id, true));
      box.appendChild(button);
    });
}

function renderList() {
  const rows = visible();
  const list = $("list");
  $("showing").textContent = `${rows.length} of ${state.data.daycares.length}`;
  list.innerHTML = "";
  if (!rows.length) {
    list.innerHTML = '<p class="empty">Nothing in the current filters. Widen the distance or clear a chip.</p>';
    return;
  }
  rows.forEach(({ daycare, score }, index) => {
    const li = document.createElement("li");
    const button = document.createElement("button");
    button.type = "button";
    button.className = "row" + (daycare.id === state.selected ? " on" : "");
    button.innerHTML = `
      <span class="rank">${index + 1}</span>
      <span class="row-score">${Math.round(score)}</span>
      <span>
        <strong>${escapeHtml(daycare.name)}</strong>
        <em>${daycare.distanceKm.toFixed(1)} km · ${escapeHtml(daycare.city)} · ${escapeHtml(daycare.languageLabel)} · ${escapeHtml(daycare.sectorLabel)}</em>
      </span>
      <span class="side">${escapeHtml(daycare.ageLabel)}</span>
    `;
    button.addEventListener("click", () => select(daycare.id, true));
    li.appendChild(button);
    list.appendChild(li);
  });
}

function renderHeader() {
  const all = state.data.daycares;
  const english = all.filter((daycare) => daycare.language === "english");
  const nearestGood = [...all]
    .filter((daycare) => daycare.ageFit === "strong" && daycare.municipality === "vantaa")
    .sort((a, b) => a.distanceKm - b.distanceKm)[0];
  $("lede").textContent =
    "He is 7 weeks old on 6 October 2026, so he was born around mid-August 2026. A November 2027 start means he will be about 15 months, ready for a toddler group. English is preferred and Finnish is a bonus. The map covers every daycare found inside 10 km of home.";
  $("facts").innerHTML = [
    `${all.length} daycares inside 10 km`,
    `${english.length} with English as a working language`,
    nearestGood ? `Closest published toddler ages: ${nearestGood.name.replace(/, yksityinen/i, "")}, ${nearestGood.distanceKm.toFixed(1)} km` : "",
    "Vantaa application due early July 2027",
    "Full-time municipal cap €335/month from August 2026",
  ].filter(Boolean).map((item) => `<li>${escapeHtml(item)}</li>`).join("");
  $("board-note").textContent =
    "Ordered by the score beside each name. Press a row, or a numbered dot on the map, to open the full card. English daycares in Vantaa rise first. A close Finnish municipal toddler group can still outrank a distant English one.";
  $("colophon").textContent =
    "Helsinki and Vantaa come from the Helsinki region Service Map. Kerava and Tuusula come from OpenStreetMap plus the cities' own pages, and those cards say when a detail still needs a phone call. Fees follow the national client-fee act as indexed on 1 August 2026 (next index 1 August 2028) and Vantaa's rule that a service-voucher family pays at most €30 a month above the municipal fee. A place in Helsinki, Kerava or Tuusula is not an entitlement for a child who lives in Vantaa.";
}

function render() {
  const rows = visible();
  syncMarkers(rows);
  renderList();
  renderShortlist();
  if (state.selected) {
    const daycare = state.data.daycares.find((item) => item.id === state.selected);
    if (daycare) renderCard(daycare);
  }
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function escapeAttr(value) {
  return escapeHtml(value).replaceAll("'", "&#39;");
}

async function main() {
  const response = await fetch("data.json");
  state.data = await response.json();
  state.weights = { ...state.data.weights };
  setupFilters();
  setupWeights();
  setupMap();
  renderHeader();
  render();
  $("card-close").addEventListener("click", () => {
    state.selected = null;
    $("card").hidden = true;
    renderList();
    syncMarkers(visible());
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") $("card-close").click();
  });
}

main().catch((error) => {
  $("lede").textContent = "The daycare data did not load. Serve this folder over http so data.json can be read.";
  console.error(error);
});
