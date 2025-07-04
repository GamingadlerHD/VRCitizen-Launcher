// Simple Translation system that leverages Python backend

class TranslationManager {
  constructor() {
    this.currentLanguage = "en";
    this.translations = {};
  }

  async init() {
    // Initialize with English as default
    // The actual saved language will be applied by App.changeLanguage() after full initialization
    this.currentLanguage = "en";
    this.translations = {};
    console.log("Translation manager initialized with default English");
  }

  async setLanguage(languageCode) {
    try {
      console.log(`Setting language to ${languageCode}`);

      if (API.isAvailable()) {
        // Use Python backend for translations
        const result = await API.getTranslations(languageCode);
        console.log("Translation API result:", result);

        if (result.success && result.data) {
          this.translations = result.data;
          this.currentLanguage = languageCode;

          console.log(
            "Loaded translations:",
            Object.keys(this.translations).length,
            "keys"
          );

          // Save language preference to both localStorage and backend config
          localStorage.setItem("sc-vr-language", languageCode);

          // Update backend language (this also saves to config)
          await API.changeLanguage(languageCode);

          // Apply translations to UI
          this.applyTranslations();

          // Update language selector
          this.updateLanguageSelector();

          console.log(`Language changed to ${languageCode}`);
          return true;
        } else {
          console.error("Failed to load translations:", result.error);
          // Apply translations anyway to use fallbacks
          this.applyTranslations();
          return false;
        }
      } else {
        console.log("API not available - language change skipped");
        // Apply translations anyway to use fallbacks
        this.applyTranslations();
        return false;
      }
    } catch (error) {
      console.error(`Failed to set language to ${languageCode}:`, error);
      // Apply translations anyway to use fallbacks
      this.applyTranslations();
      return false;
    }
  }

  applyTranslations() {
    // Translate elements with data-i18n attributes
    const elements = document.querySelectorAll("[data-i18n]");
    elements.forEach((element) => {
      const key = element.getAttribute("data-i18n");

      // Store original text as fallback if not already stored
      if (!element.hasAttribute("data-original-text")) {
        if (
          element.tagName.toLowerCase() === "input" &&
          element.type === "submit"
        ) {
          element.setAttribute("data-original-text", element.value);
        } else if (
          element.tagName.toLowerCase() === "input" &&
          element.hasAttribute("placeholder")
        ) {
          element.setAttribute("data-original-text", element.placeholder);
        } else {
          element.setAttribute(
            "data-original-text",
            element.textContent.trim()
          );
        }
      }

      // Get fallback text
      const fallback = element.getAttribute("data-original-text");
      const translation = this.get(key, fallback);

      if (
        element.tagName.toLowerCase() === "input" &&
        element.type === "submit"
      ) {
        element.value = translation;
      } else if (
        element.tagName.toLowerCase() === "input" &&
        element.hasAttribute("placeholder")
      ) {
        element.placeholder = translation;
      } else {
        element.textContent = translation;
      }
    });

    // Translate elements with data-i18n-title for tooltips
    const titleElements = document.querySelectorAll("[data-i18n-title]");
    titleElements.forEach((element) => {
      const key = element.getAttribute("data-i18n-title");

      // Store original title as fallback if not already stored
      if (!element.hasAttribute("data-original-title")) {
        element.setAttribute("data-original-title", element.title);
      }

      const fallback = element.getAttribute("data-original-title");
      const translation = this.get(key, fallback);
      element.title = translation;
    });

    // Dispatch translation changed event
    window.dispatchEvent(
      new CustomEvent("translationsChanged", {
        detail: { language: this.currentLanguage },
      })
    );
  }

  updateLanguageSelector() {
    const languageSelect = document.getElementById("language-select");
    if (languageSelect) {
      languageSelect.value = this.currentLanguage;
    }
  }

  get(key, fallback = null) {
    // Get translation from loaded translations (Python backend converts keys to lowercase)
    const lowerKey = key.toLowerCase();
    if (this.translations[lowerKey]) {
      return this.translations[lowerKey];
    }

    // Fall back to provided fallback or the key itself
    return fallback || key;
  }

  getCurrentLanguage() {
    return this.currentLanguage;
  }

  getAvailableLanguages() {
    return [
      { code: "en", name: "English", nativeName: "English" },
      { code: "de", name: "German", nativeName: "Deutsch" },
      { code: "it", name: "Italian", nativeName: "Italiano" },
      { code: "es", name: "Spanish", nativeName: "Español" },
      { code: "ru", name: "Russian", nativeName: "русский" },
      { code: "fr", name: "French", nativeName: "français" },
    ];
  }

  // Utility method to translate and set text content of an element
  translateElement(elementId, translationKey, fallback = null) {
    const element = document.getElementById(elementId);
    if (element) {
      const translation = this.get(translationKey, fallback);
      element.textContent = translation;
    }
  }
}

// Export for use in other modules
window.TranslationManager = TranslationManager;
