// Main Application for Star Citizen VR Launcher

const App = {
  // Application state
  currentPage: "home",
  currentLanguage: "en",
  gameSettings: {},
  templates: [],
  presets: [],
  themeManager: null,
  translationManager: null, // Initialize the application
  async init() {
    console.log("Star Citizen VR Launcher initialized (Component version)");

    try {
      // Initialize translation manager FIRST to load the correct language
      this.translationManager = new TranslationManager();
      await this.translationManager.init();

      // Initialize theme manager after translations are loaded
      this.themeManager = new ThemeManager();

      // Check if this is the first time running or if user wants to change theme
      const shouldShowThemeSelector = this.shouldShowThemeSelector();

      let userSelectedTheme = false;
      if (shouldShowThemeSelector) {
        // Show theme selector and wait for user choice
        await this.themeManager.showThemeSelector();
        userSelectedTheme = true;
      } else {
        // Apply saved theme
        this.themeManager.applyTheme(this.themeManager.getCurrentTheme());
      }

      // Load navigation component
      await Components.loadComponent(
        "components/shared/navigation.html",
        "navigation-container"
      );

      // Ensure translations are applied to all loaded components
      this.translationManager.applyTranslations();

      // Initialize UI components BEFORE loading pages
      await this.initializeComponents(userSelectedTheme);

      // Load initial page (home)
      await this.showPage("home");

      // Apply translations after all components are loaded
      this.translationManager.applyTranslations();

      // Get saved language and apply it using the working method
      // Use a small delay to ensure all DOM elements are ready
      setTimeout(async () => {
        try {
          const savedLanguage = await API.getCurrentLanguage();
          console.log(
            "Startup language check - saved language:",
            savedLanguage
          );

          if (savedLanguage && savedLanguage !== "en") {
            console.log(
              "Applying non-English language at startup:",
              savedLanguage
            );
            await this.changeLanguage(savedLanguage);
          }
        } catch (error) {
          console.error("Failed to apply startup language:", error);
        }
      }, 100);

      Utils.debugLog("Application initialized successfully");
      console.log("Application initialization complete");
    } catch (error) {
      Utils.debugLog(`Failed to initialize: ${error.message}`);
      console.error("Failed to initialize application:", error);
      const message = this.translationManager
        ? this.translationManager.get("failed_initialize_app")
        : "Failed to initialize application";
      Utils.showToast(message, "error");
    }
  },

  // Check if theme selector should be shown
  shouldShowThemeSelector() {
    // Show theme selector if:
    // 1. No theme has been saved (first run)
    // 2. User explicitly wants to change theme (could be triggered by a setting)
    const hasSeenThemeSelector = localStorage.getItem(
      "sc-vr-theme-selector-seen"
    );
    const forceThemeSelector = localStorage.getItem(
      "sc-vr-force-theme-selector"
    );

    if (forceThemeSelector) {
      localStorage.removeItem("sc-vr-force-theme-selector");
      return true;
    }

    if (!hasSeenThemeSelector) {
      localStorage.setItem("sc-vr-theme-selector-seen", "true");
      return true;
    }

    return false;
  },

  // Initialize UI components
  async initializeComponents(userSelectedTheme = false) {
    // Load templates
    await this.loadTemplates();

    // Load saved settings and apply theme if needed
    await this.loadInitialSettings(userSelectedTheme);

    // Apply translations after components are loaded
    if (this.translationManager) {
      this.translationManager.applyTranslations();
    }
  },

  // Load initial settings for theme application only
  async loadInitialSettings(userSelectedTheme = false) {
    try {
      console.log("Loading initial settings...");
      const settings = await API.getSettings();

      if (settings && Object.keys(settings).length > 0) {
        console.log("Initial settings loaded:", settings);

        // Apply theme from settings only if user didn't just select a theme
        if (settings.theme && this.themeManager && !userSelectedTheme) {
          console.log("Applying saved theme:", settings.theme);
          this.themeManager.applyTheme(settings.theme);
        } else if (userSelectedTheme) {
          console.log(
            "Skipping saved theme application - user just selected a theme"
          );
        }

        Utils.debugLog("Initial settings loaded successfully");
      } else {
        console.log("No saved settings found");
      }
    } catch (error) {
      console.error("Failed to load initial settings:", error);
      Utils.debugLog(`Failed to load initial settings: ${error.message}`);
    }
  },

  // Show a specific page
  async showPage(pageName) {
    try {
      console.log(`Showing page: ${pageName}`);

      // Hide current page
      const currentPageElement = document.querySelector(
        ".page-component:not(.hidden)"
      );
      if (currentPageElement) {
        currentPageElement.classList.add("hidden");
      }

      // Load new page component
      const pageContainer = document.getElementById("page-container");
      if (pageContainer) {
        const success = await Components.loadComponent(
          `components/pages/${pageName}.html`,
          "page-container"
        );
        if (success) {
          this.currentPage = pageName;
          this.updateActiveNavButton();
          Utils.debugLog(`Loaded ${pageName} page`);

          this.translationManager.applyTranslations();

          // Initialize page-specific functionality
          await this.initializePage(pageName);
        } else {
          throw new Error(`Failed to load page: ${pageName}`);
        }
      }
    } catch (error) {
      Utils.debugLog(`Failed to show page ${pageName}: ${error.message}`);
      console.error("Failed to show page:", error);
      const message = this.translationManager
        ? this.translationManager.get(
            "failed_load_page",
            `Failed to load ${pageName} page`
          )
        : `Failed to load ${pageName} page`;
      Utils.showToast(message, "error");
    }
  },

  // Initialize page-specific functionality
  async initializePage(pageName) {
    switch (pageName) {
      case "home":
        await HomePage.init();
        break;
      case "settings":
        await SettingsPage.init();
        break;
      case "vorpx":
        await VorpXPage.init();
        break;
      case "info":
        await InfoPage.init();
        break;
    }
  },

  // Update active navigation button
  updateActiveNavButton() {
    const navButtons = document.querySelectorAll(".nav-button");
    navButtons.forEach((btn) => {
      btn.classList.remove("active", "bg-sc-blue", "text-white");
      btn.classList.add("text-sc-text-muted");
    });

    const activeButton = Array.from(navButtons).find(
      (btn) =>
        btn.textContent.toLowerCase().trim() === this.currentPage.toLowerCase()
    );
    if (activeButton) {
      activeButton.classList.add("active", "bg-sc-blue", "text-white");
      activeButton.classList.remove("text-sc-text-muted");
    }
  },

  // Change language
  async changeLanguage(language) {
    try {
      if (this.translationManager) {
        const result = await this.translationManager.setLanguage(language);
        if (result) {
          this.currentLanguage = language;
          Utils.showToast(
            this.translationManager.get(
              "language_changed_success",
              "Language changed successfully"
            ),
            "success"
          );
        } else {
          Utils.showToast(
            this.translationManager.get(
              "failed_change_language",
              "Failed to change language"
            ),
            "error"
          );
        }
      } else {
        Utils.showToast(
          this.translationManager
            ? this.translationManager.get(
                "translation_manager_not_available",
                "Translation manager not available"
              )
            : "Translation manager not available",
          "error"
        );
      }
    } catch (error) {
      console.error("Failed to change language:", error);
      Utils.showToast(
        this.translationManager
          ? this.translationManager.get(
              "failed_change_language",
              "Failed to change language"
            )
          : "Failed to change language",
        "error"
      );
    }
  },

  // Load templates
  async loadTemplates() {
    try {
      console.log("Loading templates...");
      this.templates = await API.getTemplates();
      console.log("Templates loaded:", this.templates.length);
      console.log("Template data:", this.templates);
      Utils.debugLog(`Loaded ${this.templates.length} templates`);
    } catch (error) {
      console.error("Failed to load templates:", error);
      Utils.debugLog(`Failed to load templates: ${error.message}`);
    }
  },

  // Show theme selector (for manual theme/background customization)
  async showThemeSelector() {
    if (this.themeManager) {
      await this.themeManager.showThemeSelector();
    } else {
      Utils.showToast(
        this.translationManager
          ? this.translationManager.get(
              "theme_manager_not_available",
              "Theme manager not available"
            )
          : "Theme manager not available",
        "error"
      );
    }
  },

  // Common settings loading function for all pages
  async loadAndApplySettings(pageName) {
    try {
      console.log(`Loading settings for ${pageName} page...`);
      const settings = await API.getSettings();

      if (settings && Object.keys(settings).length > 0) {
        console.log(`Applying settings to ${pageName} page:`, settings);
        Components.applySettingsToUI(settings);

        // Handle template selection which might trigger preset loading (Home page only)
        if (pageName === "Home" && settings.selectedTemplate) {
          await HomePage.onTemplateSelected(settings.selectedTemplate);
        }
      } else {
        console.log(`No settings found for ${pageName} page`);
      }
    } catch (error) {
      console.error(`Failed to load settings for ${pageName} page:`, error);
    }
  },
};

// Page-specific modules
const HomePage = {
  async init() {
    // Populate template dropdown
    const templateSelect = document.getElementById("template-select");
    if (templateSelect && App.templates.length > 0) {
      templateSelect.innerHTML = '<option value="">No Template</option>';
      App.templates.forEach((template) => {
        const option = document.createElement("option");
        option.value = template.name;
        option.textContent = template.name;
        templateSelect.appendChild(option);
      });
    }

    // Always load and apply current settings when HomePage is initialized
    await App.loadAndApplySettings("Home");
  },

  async browseFolder(inputId) {
    const path = await API.browseFolder();
    if (path) {
      document.getElementById(inputId).value = path;
      Utils.showToast(
        App.translationManager
          ? App.translationManager.get(
              "folder_selected_success",
              "Folder selected successfully"
            )
          : "Folder selected successfully",
        "success"
      );

      if (inputId === "sc-path") {
        await this.checkDXGI();
      }
    }
  },

  async browseFile(inputId, extensions) {
    const path = await API.browseFile(extensions);
    if (path) {
      document.getElementById(inputId).value = path;
      Utils.showToast(
        App.translationManager
          ? App.translationManager.get(
              "file_selected_success",
              "File selected successfully"
            )
          : "File selected successfully",
        "success"
      );
    }
  },

  async onTemplateSelected(templateName) {
    if (!templateName) {
      document.getElementById("fov").value = "";
      document.getElementById("preset-select").innerHTML =
        '<option value="">No Preset</option>';
      return;
    }

    // Set FOV from template
    const template = App.templates.find((t) => t.name === templateName);
    if (template) {
      document.getElementById("fov").value = template.fov;
    }

    // Load presets for template
    try {
      App.presets = await API.getPresets(templateName);
      const presetSelect = document.getElementById("preset-select");
      if (presetSelect) {
        presetSelect.innerHTML = '<option value="">No Preset</option>';
        App.presets.forEach((preset) => {
          const option = document.createElement("option");
          option.value = preset.name;
          option.textContent = preset.name;
          presetSelect.appendChild(option);
        });
      }
    } catch (error) {
      console.error("Failed to load presets:", error);
    }
  },

  onPresetSelected(presetName) {
    if (!presetName) return;

    const preset = App.presets.find((p) => p.name === presetName);
    if (preset) {
      document.getElementById("width").value = preset.width;
      document.getElementById("height").value = preset.height;
    }
  },

  onResolutionChange(changedField) {
    const widthInput = document.getElementById("width");
    const heightInput = document.getElementById("height");
    const presetSelect = document.getElementById("preset-select");

    if (!widthInput.value || !heightInput.value) return;

    const width = parseInt(widthInput.value);
    const height = parseInt(heightInput.value);

    // Check if current resolution matches any preset
    const matchingPreset = App.presets.find(
      (p) => p.width === width && p.height === height
    );
    if (matchingPreset) {
      presetSelect.value = matchingPreset.name;
    } else {
      presetSelect.value = "";
    }
  },

  async checkDXGI() {
    const statusElement = document.getElementById("dxgi-status");
    const scPath = document.getElementById("sc-path").value;

    // Show checking status
    statusElement.textContent = App.translationManager
      ? App.translationManager.get(
          "dxgi_status_checking",
          "DXGI status: Checking..."
        )
      : "DXGI status: Checking...";
    statusElement.className = "text-sc-text-muted text-sm";

    try {
      const result = await API.checkDXGIAvailability(scPath);
      if (result.available) {
        statusElement.textContent = App.translationManager
          ? App.translationManager.get(
              "dxgi_status_available",
              "DXGI status: Available"
            )
          : "DXGI status: Available";
        statusElement.className = "text-green-400 text-sm";
      } else {
        statusElement.textContent = App.translationManager
          ? App.translationManager.get(
              "dxgi_status_not_found",
              "DXGI status: Not found"
            )
          : "DXGI status: Not found";
        statusElement.className = "text-red-400 text-sm";
      }
    } catch (error) {
      console.error("Failed to check DXGI:", error);
      statusElement.textContent = App.translationManager
        ? App.translationManager.get(
            "dxgi_status_check_failed",
            "DXGI status: Check failed"
          )
        : "DXGI status: Check failed";
      statusElement.className = "text-red-400 text-sm";
    }
  },

  openDXGIHelp() {
    const url =
      "https://github.com/GamingadlerHD/VRCitizen-Launcher/wiki/Hook-Helper";
    API.openUrl(url);
  },

  async saveSettings() {
    try {
      const config = Components.collectAllSettings();

      // Add current theme to settings
      if (App.themeManager) {
        config.theme = App.themeManager.getCurrentTheme();
      }

      const result = await API.saveSettings(config);
      if (result) {
        Utils.showToast(
          App.translationManager
            ? App.translationManager.get(
                "settings_saved_success",
                "Settings saved successfully"
              )
            : "Settings saved successfully",
          "success"
        );
      } else {
        Utils.showToast(
          App.translationManager
            ? App.translationManager.get(
                "failed_save_settings",
                "Failed to save settings"
              )
            : "Failed to save settings",
          "error"
        );
      }
    } catch (error) {
      console.error("Failed to save settings:", error);
      Utils.showToast(
        App.translationManager
          ? App.translationManager.get(
              "failed_save_settings",
              "Failed to save settings"
            )
          : "Failed to save settings",
        "error"
      );
    }
  },

  async launchGame() {
    try {
      const config = Components.collectAllSettings();
      const result = await API.startGame(config);
      if (result.success) {
        Utils.showToast(
          App.translationManager
            ? App.translationManager.get(
                "game_launched_success",
                "Star Citizen VR launched successfully!"
              )
            : "Star Citizen VR launched successfully!",
          "success"
        );
      } else {
        Utils.showToast(
          result.error ||
            (App.translationManager
              ? App.translationManager.get(
                  "failed_launch_game",
                  "Failed to launch game"
                )
              : "Failed to launch game"),
          "error"
        );
      }
    } catch (error) {
      console.error("Failed to launch game:", error);
      Utils.showToast(
        App.translationManager
          ? App.translationManager.get(
              "failed_launch_game",
              "Failed to launch game"
            )
          : "Failed to launch game",
        "error"
      );
    }
  },

  async restoreSettings() {
    try {
      const settings = await API.getSettings();
      Components.applySettingsToUI(settings);
      Utils.showToast(
        App.translationManager
          ? App.translationManager.get(
              "settings_restored_success",
              "Settings restored"
            )
          : "Settings restored",
        "success"
      );
    } catch (error) {
      console.error("Failed to restore settings:", error);
      Utils.showToast(
        App.translationManager
          ? App.translationManager.get(
              "failed_restore_settings",
              "Failed to restore settings"
            )
          : "Failed to restore settings",
        "error"
      );
    }
  },
};

const SettingsPage = {
  async init() {
    console.log("Settings page initialized");

    // Load and apply current settings every time settings page is loaded
    await App.loadAndApplySettings("Settings");
  },

  applyStandardSettings() {
    const standardSettings = {
      motionBlur: false,
      vSync: false,
      autoZoomOnSelectedTarget: false,
      filmGrain: false,
      cameraSpringMovement: false,
      headtrackingToggle: true,
      headtrackingDisableDuringADS: false,
      headtrackingDisableDuringMobiGlas: false,
      headtrackingDisableDuringWalking: false,
      headtrackingEnableRollFPS: true,
      headtrackingThirdPersonCameraToggle: true,
      headtrackingThirdPersonDisableDuringInventory: false,
    };

    Components.applySettingsToUI(standardSettings);

    // Reset sliders to 0
    const sliders = [
      "gforce-boost",
      "gforce-bob",
      "shake-scale",
      "max-zoom",
      "chromatic",
    ];
    sliders.forEach((sliderId) => {
      const slider = document.getElementById(sliderId);
      if (slider) {
        slider.value = 0;
        Components.updateSliderValue(sliderId, sliderId + "-value");
      }
    });

    Utils.showToast(
      App.translationManager
        ? App.translationManager.get(
            "standard_vr_settings_applied",
            "Standard VR settings applied"
          )
        : "Standard VR settings applied",
      "success"
    );
  },

  resetToDefaults() {
    Components.resetAllForms();
    Utils.showToast(
      App.translationManager
        ? App.translationManager.get(
            "settings_reset_to_defaults",
            "Settings reset to defaults"
          )
        : "Settings reset to defaults",
      "success"
    );
  },
};

const VorpXPage = {
  async init() {
    console.log("VorpX page initialized");

    // Load and apply current settings every time VorpX page is loaded
    await App.loadAndApplySettings("VorpX");
  },
};

const InfoPage = {
  async init() {
    console.log("Info page initialized");
  },

  openUrl(url) {
    API.openUrl(url);
  },
};

// Initialize when page loads
document.addEventListener("DOMContentLoaded", () => {
  App.init();
});

// Expose App globally for debugging
window.App = App;
window.HomePage = HomePage;
window.SettingsPage = SettingsPage;
window.VorpXPage = VorpXPage;
window.InfoPage = InfoPage;
