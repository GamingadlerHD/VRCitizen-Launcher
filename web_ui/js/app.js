const App = {
  // Application state
  currentPage: "home",
  currentLanguage: "en",
  templates: [],
  presets: [],
  themeManager: null,
  translationManager: null,
  async init() {
    console.log("Star Citizen VR Launcher initialized (Component version)");

    try {
      this.translationManager = new TranslationManager();
      await this.translationManager.init();

      this.themeManager = new ThemeManager();

      const shouldShowThemeSelector = await this.shouldShowThemeSelector();

      let userSelectedTheme = false;
      if (shouldShowThemeSelector) {
        // Show theme selector and wait for user choice
        await this.themeManager.showThemeSelector();
        userSelectedTheme = true;
      } else {
        // Apply saved theme
        await this.themeManager.applyTheme(await this.themeManager.getCurrentTheme());
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

          if (savedLanguage && savedLanguage !== "en") {
            await this.changeLanguage(savedLanguage);
          }
        } catch (error) {
          console.error("Failed to apply startup language:", error);
        }
      }, 100);

      Utils.debugLog("Application initialized successfully");
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
  async shouldShowThemeSelector() {
    try {
      // Show theme selector if user hasn't seen it before
      if (window.API && window.API.getThemeSelectorSeen) {
        const hasSeenThemeSelector = await window.API.getThemeSelectorSeen();
        
        if (!hasSeenThemeSelector) {
          await window.API.setThemeSelectorSeen(true);
          return true;
        }
      }

      return false;
    } catch (error) {
      console.error("Failed to check theme selector status:", error);
      return false;
    }
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
      const settings = await API.getSettings();

      if (settings && Object.keys(settings).length > 0) {
        // Apply theme from settings only if user didn't just select a theme
        if (settings.theme && this.themeManager && !userSelectedTheme) {
          await this.themeManager.applyTheme(settings.theme);
        }

        Utils.debugLog("Initial settings loaded successfully");
      }
    } catch (error) {
      console.error("Failed to load initial settings:", error);
      Utils.debugLog(`Failed to load initial settings: ${error.message}`);
    }
  },

  // Show a specific page
  async showPage(pageName) {
    try {
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
      this.templates = await API.getTemplates();
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
      const settings = await API.getSettings();

      if (settings && Object.keys(settings).length > 0) {
        Components.applySettingsToUI(settings);

        // Handle template selection which might trigger preset loading (Home page only)
        if (pageName === "Home" && settings.selectedTemplate) {
          await HomePage.onTemplateSelected(settings.selectedTemplate);
        }
      }
    } catch (error) {
      console.error(`Failed to load settings for ${pageName} page:`, error);
    }
  },
};

// Page-specific modules
const HomePage = {
  currentAspectRatio: null, // Store current aspect ratio
  isManualResolution: false, // Track if user manually edited resolution

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
    // Reset aspect ratio and manual mode when template changes
    this.currentAspectRatio = null;
    this.isManualResolution = false;

    if (!templateName) {
      document.getElementById("fov").value = "";
      document.getElementById("width").value = "";
      document.getElementById("height").value = "";
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

        // Add a "Custom" option for manual resolution
        const customOption = document.createElement("option");
        customOption.value = "custom";
        customOption.textContent = "Custom";
        presetSelect.appendChild(customOption);

        // Add preset options
        App.presets.forEach((preset) => {
          const option = document.createElement("option");
          option.value = preset.name;
          option.textContent = preset.name;
          presetSelect.appendChild(option);
        });

        // Clear resolution fields when template changes
        document.getElementById("width").value = "";
        document.getElementById("height").value = "";
      }
    } catch (error) {
      console.error("Failed to load presets:", error);
    }
  },

  onPresetSelected(presetName) {
    if (!presetName) {
      this.currentAspectRatio = null;
      this.isManualResolution = false;
      return;
    }

    // Handle "Custom" option
    if (presetName === "custom") {
      this.currentAspectRatio = null;
      this.isManualResolution = true;
      return;
    }

    const preset = App.presets.find((p) => p.name === presetName);
    if (preset && preset.width && preset.height) {
      // Set the resolution values
      document.getElementById("width").value = preset.width;
      document.getElementById("height").value = preset.height;

      // Calculate and store aspect ratio
      this.currentAspectRatio = preset.width / preset.height;
      this.isManualResolution = false;
    }
  },

  onResolutionChange(changedField) {
    const widthInput = document.getElementById("width");
    const heightInput = document.getElementById("height");

    const width = parseInt(widthInput.value) || 0;
    const height = parseInt(heightInput.value) || 0;

    // If we're in manual/custom mode, don't calculate aspect ratio
    if (this.isManualResolution) {
      return;
    }

    if (!width || !height || !this.currentAspectRatio) {
      return;
    }

    // Calculate the other dimension based on aspect ratio
    if (changedField === "width" && width > 0) {
      const calculatedHeight = Math.round(width / this.currentAspectRatio);
      if (calculatedHeight !== height) {
        heightInput.value = calculatedHeight;
      }
    } else if (changedField === "height" && height > 0) {
      const calculatedWidth = Math.round(height * this.currentAspectRatio);
      if (calculatedWidth !== width) {
        widthInput.value = calculatedWidth;
      }
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
        config.theme = await App.themeManager.getCurrentTheme();
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

  // Show theme selector modal
  async showThemeSelector() {
    try {
      if (this.themeManager) {
        await this.themeManager.showThemeSelector();
      }
    } catch (error) {
      console.error("Failed to show theme selector:", error);
      Utils.showToast(
        this.translationManager
          ? this.translationManager.get("theme_selector_error", "Failed to open theme selector")
          : "Failed to open theme selector",
        "error"
      );
    }
  },
};

const SettingsPage = {
  async init() {
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
    // Load and apply current settings every time VorpX page is loaded
    await App.loadAndApplySettings("VorpX");
  },
};

const InfoPage = {
  async init() {
    // Load and apply current settings when Info page is loaded
    await App.loadAndApplySettings("Info");
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
