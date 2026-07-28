const DEFAULT_LOCALE = "zh-Hant";
const STORAGE_KEY = "elementMazeLocale";

export async function createI18n(catalogPath) {
  const response = await fetch(catalogPath, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Locale catalog request failed: ${response.status}`);
  }
  const catalog = await response.json();
  const hasLocale = (candidate) => Object.prototype.hasOwnProperty.call(catalog, candidate);
  let locale = localStorage.getItem(STORAGE_KEY);
  if (!hasLocale(locale)) {
    locale = DEFAULT_LOCALE;
  }

  const translate = (key, values = {}) => {
    const template = catalog[locale]?.[key] ?? catalog[DEFAULT_LOCALE]?.[key];
    if (typeof template !== "string") {
      return `[missing: ${key}]`;
    }
    return template.replace(/\{([a-zA-Z0-9_]+)\}/g, (_, name) => String(values[name] ?? `{${name}}`));
  };

  return {
    get locale() {
      return locale;
    },
    setLocale(nextLocale) {
      locale = hasLocale(nextLocale) ? nextLocale : DEFAULT_LOCALE;
      localStorage.setItem(STORAGE_KEY, locale);
      return locale;
    },
    t: translate,
  };
}
