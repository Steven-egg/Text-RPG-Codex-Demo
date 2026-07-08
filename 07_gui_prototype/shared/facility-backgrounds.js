const REGION_STORAGE_KEY = "elementMazeCurrentRegionId";
const REGION_IDS = new Set(["fire", "ice", "earth", "thunder", "final"]);

export function normalizeRegionId(regionId) {
  if (!regionId) {
    return null;
  }
  const value = String(regionId).trim();
  const normalized = value === "border_fire" ? "fire" : value;
  return REGION_IDS.has(normalized) ? normalized : null;
}

export function rememberCurrentRegion(modelOrRegion) {
  const regionId = normalizeRegionId(
    typeof modelOrRegion === "string" ? modelOrRegion : regionFromModel(modelOrRegion),
  );
  if (!regionId) {
    return null;
  }
  try {
    sessionStorage.setItem(REGION_STORAGE_KEY, regionId);
  } catch {
    // Session storage may be unavailable in restricted browser contexts.
  }
  return regionId;
}

export function currentFacilityRegion(model, options = {}) {
  const candidates = [
    options.regionId,
    regionFromModel(model),
    new URLSearchParams(window.location.search).get("region"),
    storedRegion(),
  ];

  for (const candidate of candidates) {
    const regionId = normalizeRegionId(candidate);
    if (regionId) {
      return regionId;
    }
  }
  return "fire";
}

export function routeWithFacilityRegion(route, modelOrRegion) {
  const regionId = currentFacilityRegion(
    typeof modelOrRegion === "string" ? null : modelOrRegion,
    { regionId: typeof modelOrRegion === "string" ? modelOrRegion : undefined },
  );
  const url = new URL(route, window.location.href);
  url.searchParams.set("region", regionId);
  return url.href;
}

export function applyFacilityBackground({ model, shell, selectedRegionId, backgrounds }) {
  const regionId = currentFacilityRegion(model, { regionId: selectedRegionId });
  const background = backgrounds[regionId] ?? backgrounds.fire;
  const values = typeof background === "string" ? { "--facility-background-image": background } : background;

  for (const [propertyName, imagePath] of Object.entries(values)) {
    document.documentElement.style.setProperty(propertyName, `url("${imagePath}")`);
  }
  document.body.dataset.region = regionId;
  if (shell) {
    shell.dataset.region = regionId;
  }
  rememberCurrentRegion(regionId);
  return regionId;
}

function regionFromModel(model) {
  if (!model) {
    return null;
  }
  return model.current_region_id ?? model.selected_region_id ?? model.region_id ?? null;
}

function storedRegion() {
  try {
    return sessionStorage.getItem(REGION_STORAGE_KEY);
  } catch {
    return null;
  }
}
