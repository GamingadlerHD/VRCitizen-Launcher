// API Module for communicating with Python backend

const API = {
  // Check if pywebview API is available
  isAvailable() {
    return window.pywebview && window.pywebview.api;
  },

  // Get translations for a specific language
  async getTranslations(languageCode) {
    try {
      if (this.isAvailable()) {
        return await window.pywebview.api.get_translations(languageCode);
      } else {
        console.log("API not available - translations not loaded");
        return { success: false, error: "API not available" };
      }
    } catch (error) {
      console.error("Failed to get translations:", error);
      return { success: false, error: error.message };
    }
  },

  // Get current language from backend config
  async getCurrentLanguage() {
    try {
      if (this.isAvailable()) {
        return await window.pywebview.api.get_current_language();
      } else {
        console.log("API not available - using fallback language");
        return "en";
      }
    } catch (error) {
      console.error("Failed to get current language:", error);
      return "en";
    }
  },

  // Change application language
  async changeLanguage(languageCode) {
    try {
      if (this.isAvailable()) {
        return await window.pywebview.api.change_language(languageCode);
      } else {
        console.log("Language change not available in preview mode");
        return false;
      }
    } catch (error) {
      console.error("Failed to change language:", error);
      return false;
    }
  },

  // Get available templates
  async getTemplates() {
    try {
      if (this.isAvailable()) {
        const result = await window.pywebview.api.get_templates();
        return result;
      } else {
        console.log("Templates not available in preview mode");
        return [];
      }
    } catch (error) {
      console.error("Failed to get templates:", error);
      return [];
    }
  },

  // Get presets for a template
  async getPresets(templateName) {
    try {
      if (this.isAvailable()) {
        const result = await window.pywebview.api.get_presets(templateName);
        return result;
      } else {
        console.log("Presets not available in preview mode");
        return [];
      }
    } catch (error) {
      console.error("Failed to get presets:", error);
      return [];
    }
  },

  // Browse for folder
  async browseFolder() {
    try {
      if (this.isAvailable()) {
        return await window.pywebview.api.browse_folder();
      } else {
        console.log("Folder browser not available in preview mode");
        return null;
      }
    } catch (error) {
      console.error("Failed to browse folder:", error);
      return null;
    }
  },

  // Browse for file
  async browseFile(extensions) {
    try {
      if (this.isAvailable()) {
        return await window.pywebview.api.browse_file(extensions);
      } else {
        console.log("File browser not available in preview mode");
        return null;
      }
    } catch (error) {
      console.error("Failed to browse file:", error);
      return null;
    }
  },

  // Check DXGI availability
  async checkDXGIAvailability(scPath) {
    try {
      if (this.isAvailable()) {
        return await window.pywebview.api.check_dxgi_availability(scPath);
      } else {
        return { available: false, message: "Unable to check in preview mode" };
      }
    } catch (error) {
      console.error("Failed to check DXGI:", error);
      return { available: false, message: "Check failed" };
    }
  },

  // Save settings
  async saveSettings(config) {
    try {
      if (this.isAvailable()) {
        return await window.pywebview.api.save_settings(config);
      } else {
        console.log("Settings save not available in preview mode");
        return false;
      }
    } catch (error) {
      console.error("Failed to save settings:", error);
      return false;
    }
  },

  // Get current settings
  async getSettings() {
    try {
      if (this.isAvailable()) {
        return await window.pywebview.api.get_settings();
      } else {
        console.log("Settings restore not available in preview mode");
        return {};
      }
    } catch (error) {
      console.error("Failed to get settings:", error);
      return {};
    }
  },

  // Start game
  async startGame(config) {
    try {
      if (this.isAvailable()) {
        return await window.pywebview.api.start_game(config);
      } else {
        console.log("Game launch not available in preview mode");
        return { success: false, error: "API not available" };
      }
    } catch (error) {
      console.error("Failed to launch game:", error);
      return { success: false, error: error.message };
    }
  },

  // Open URL
  async openUrl(url) {
    try {
      if (this.isAvailable()) {
        await window.pywebview.api.open_url(url);
      } else {
        window.open(url, "_blank");
      }
    } catch (error) {
      console.error("Failed to open URL:", error);
    }
  },
};
