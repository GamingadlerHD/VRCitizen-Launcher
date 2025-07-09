// Theme system for Star Citizen VR Launcher

class ThemeManager {
  constructor() {
    this.themes = {};
    this.themesLoaded = false;
    this.currentTheme = "default";

    // Load themes from JSON files
    this.loadThemesFromFiles().then(async () => {
      this.currentTheme = await this.loadSavedTheme();
      await this.loadThemeCustomization(this.currentTheme);
    });
  }

  // Load all theme files from the themes directory
  async loadThemesFromFiles() {
    try {
      console.log("Loading themes from JSON files...");
      let themeFiles = [];
      const loadedThemes = {};

      if (themeFiles.length === 0) {
        const potentialThemes = [
          "default.json",
          "starwars.json",
          "cyberpunk.json",
          "minimal.json",
        ];

        for (const filename of potentialThemes) {
          try {
            const response = await fetch(`themes/${filename}`);
            if (response.ok) {
              try {
                const themeId = filename.replace(".json", "");
                const themeData = await response.json();
                loadedThemes[themeId] = themeData;
              } catch (error) {
                console.warn(`Failed to load theme file ${filename}:`, error);
              }
            }
          } catch (error) {
            // Theme file doesn't exist, skip silently
          }
        }
      }

      this.themes = loadedThemes;
      this.themesLoaded = true;

      console.log(
        `Successfully loaded ${loadedCount} themes:`,
        Object.keys(this.themes)
      );
    } catch (error) {
      console.error("Failed to load themes:", error);
    }
  }

  // Wait for themes to be loaded
  async waitForThemes() {
    while (!this.themesLoaded) {
      await new Promise((resolve) => setTimeout(resolve, 50));
    }
  }

  async loadSavedTheme() {
    try {
      if (window.API && window.API.getSavedTheme) {
        const saved = await window.API.getSavedTheme();
        return saved && this.themes[saved] ? saved : "default";
      }
      return "default";
    } catch (error) {
      console.error("Failed to load saved theme:", error);
      return "default";
    }
  }

  async saveTheme(themeId) {
    try {
      if (window.API && window.API.saveTheme) {
        await window.API.saveTheme(themeId);
      }
    } catch (error) {
      console.error("Failed to save theme:", error);
    }
  }

  // Helper function to convert hex to RGB values
  hexToRgb(hex) {
    // Remove the hash if present
    hex = hex.replace("#", "");

    // Parse the hex values
    const r = parseInt(hex.slice(0, 2), 16);
    const g = parseInt(hex.slice(2, 4), 16);
    const b = parseInt(hex.slice(4, 6), 16);

    return `${r}, ${g}, ${b}`;
  }

  async applyTheme(themeId) {
    // Wait for themes to be loaded
    await this.waitForThemes();

    if (!this.themes[themeId]) {
      console.warn(`Theme ${themeId} not found, using default`);
      themeId = "default";
    }

    const theme = this.themes[themeId];
    const root = document.documentElement;

    // Show loading overlay
    this.showLoading();

    // Apply CSS variables with a slight delay for smooth transition
    setTimeout(async () => {
      Object.entries(theme.colors).forEach(([key, value]) => {
        root.style.setProperty(`--theme-${key}`, value);

        // Also set RGB values for backgrounds that need transparency
        if (
          key === "bg-primary" ||
          key === "bg-secondary" ||
          key === "bg-tertiary"
        ) {
          root.style.setProperty(`--theme-${key}-rgb`, this.hexToRgb(value));
        }
      });

      // Apply background image properties
      if (theme.background) {
        root.style.setProperty(
          `--theme-bg-image`,
          theme.background.image ? `url("${theme.background.image}")` : ""
        );
        root.style.setProperty(
          `--theme-bg-opacity`,
          theme.background.opacity || 0.3
        );
        root.style.setProperty(
          `--theme-bg-position`,
          theme.background.position || "center"
        );
        root.style.setProperty(
          `--theme-bg-size`,
          theme.background.size || "cover"
        );
        root.style.setProperty(
          `--theme-bg-repeat`,
          theme.background.repeat || "no-repeat"
        );

        // Set content transparency based on background opacity
        // When background is more visible (higher opacity), make content more transparent
        const bgOpacity = theme.background.opacity || 0.3;
        const contentOpacity = Math.max(0.5, 1 - bgOpacity * 0.8); // Inverse relationship
        const mainOpacity = Math.max(0.3, 1 - bgOpacity * 1.2); // Even more transparent for main area

        root.style.setProperty(`--theme-content-bg-opacity`, contentOpacity);
        root.style.setProperty(`--theme-main-bg-opacity`, mainOpacity);
      }

      // Update Tailwind config for the new theme
      this.updateTailwindConfig(theme);

      this.currentTheme = themeId;
      await this.saveTheme(themeId);

      // Hide loading overlay
      setTimeout(() => {
        this.hideLoading();

        // Clean up any inline switch styles that might interfere with theming
        this.cleanupSwitchStyles();

        // Dispatch theme change event
        window.dispatchEvent(
          new CustomEvent("themeChanged", {
            detail: { themeId, theme },
          })
        );
      }, 300);
    }, 100);
  }

  showLoading() {
    const loadingOverlay = document.getElementById("theme-loading");
    if (loadingOverlay) {
      loadingOverlay.classList.add("active");
    }
  }

  hideLoading() {
    const loadingOverlay = document.getElementById("theme-loading");
    if (loadingOverlay) {
      loadingOverlay.classList.remove("active");
    }
  }

  updateTailwindConfig(theme) {
    // Update the Tailwind configuration dynamically
    if (window.tailwind && window.tailwind.config) {
      window.tailwind.config.theme.extend.colors = {
        // Backgrounds
        "sc-bg": theme.colors["bg-primary"],
        "sc-bg-secondary": theme.colors["bg-secondary"],
        "sc-bg-tertiary": theme.colors["bg-tertiary"],
        "sc-border": theme.colors["border"],

        // Text colors
        "sc-text": theme.colors["text-primary"],
        "sc-text-secondary": theme.colors["text-secondary"],
        "sc-text-muted": theme.colors["text-muted"],

        // Navigation colors
        "sc-nav-text": theme.colors["nav-text"],
        "sc-nav-text-hover": theme.colors["nav-text-hover"],
        "sc-nav-text-active": theme.colors["nav-text-active"],
        "sc-nav-bg-hover": theme.colors["nav-bg-hover"],
        "sc-nav-bg-active": theme.colors["nav-bg-active"],

        // Form elements
        "sc-input-bg": theme.colors["input-bg"],
        "sc-input-border": theme.colors["input-border"],
        "sc-input-text": theme.colors["input-text"],
        "sc-input-placeholder": theme.colors["input-placeholder"],
        "sc-input-focus": theme.colors["input-focus-border"],

        // Dropdown colors
        "sc-dropdown-bg": theme.colors["dropdown-bg"],
        "sc-dropdown-border": theme.colors["dropdown-border"],
        "sc-dropdown-text": theme.colors["dropdown-text"],
        "sc-dropdown-hover": theme.colors["dropdown-option-hover"],

        // Button colors
        "sc-btn-primary": theme.colors["btn-primary-bg"],
        "sc-btn-primary-text": theme.colors["btn-primary-text"],
        "sc-btn-primary-hover": theme.colors["btn-primary-hover"],
        "sc-btn-secondary": theme.colors["btn-secondary-bg"],
        "sc-btn-secondary-text": theme.colors["btn-secondary-text"],
        "sc-btn-secondary-hover": theme.colors["btn-secondary-hover"],

        // Accent colors
        "sc-blue": theme.colors["accent"],
        "sc-blue-light": theme.colors["accent-light"],
        "sc-blue-dark": theme.colors["accent-dark"],

        // Status colors
        "sc-green": theme.colors["success"],
        "sc-yellow": theme.colors["warning"],
        "sc-red": theme.colors["error"],
      };
    }
  }

  async getCurrentTheme() {
    await this.waitForThemes();
    return this.currentTheme;
  }

  async getTheme(themeId) {
    await this.waitForThemes();
    return this.themes[themeId];
  }

  async getAvailableThemes() {
    await this.waitForThemes();
    return Object.keys(this.themes).map((id) => ({
      id,
      ...this.themes[id],
    }));
  }

  async showThemeSelector() {
    await this.waitForThemes();

    return new Promise(async (resolve) => {
      const modal = await this.createThemeSelector(resolve);
      document.body.appendChild(modal);

      // Show modal with animation
      setTimeout(() => {
        modal.classList.remove("opacity-0");
        modal.classList.add("opacity-100");
      }, 10);
    });
  }

  async createThemeSelector(onSelect) {
    const modal = document.createElement("div");
    modal.className =
      "fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 opacity-0 transition-opacity duration-300";

    const themes = await this.getAvailableThemes();

    modal.innerHTML = `
            <div class="bg-gray-900 rounded-lg p-8 max-w-2xl w-full mx-4 transform scale-95 transition-transform duration-300" id="theme-modal-content">
                <div class="text-center mb-6">
                    <h2 class="text-2xl font-bold text-white mb-2">Choose Your Theme</h2>
                    <p class="text-gray-400">Select the visual style for your launcher</p>
                </div>
                
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <!-- Theme Selection -->
                    <div>
                        <h3 class="text-lg font-semibold text-white mb-4">Theme</h3>
                        <div class="space-y-3">
                            ${themes
                              .map(
                                (theme) => `
                                <div class="theme-option relative group cursor-pointer" data-theme="${
                                  theme.id
                                }">
                                    <div class="border-2 border-gray-600 rounded-lg p-3 transition-all duration-200 group-hover:border-blue-500 ${
                                      theme.id === this.currentTheme
                                        ? "border-blue-500 bg-blue-900 bg-opacity-20"
                                        : ""
                                    }">
                                        <div class="flex items-center justify-between">
                                            <div>
                                                <h4 class="text-md font-semibold text-white">${
                                                  theme.name
                                                }</h4>
                                                <p class="text-xs text-gray-400">${
                                                  theme.description
                                                }</p>
                                            </div>
                                            <div class="theme-preview w-8 h-8 rounded border-2 flex items-center justify-center" 
                                                 style="background: linear-gradient(45deg, ${
                                                   theme.colors["bg-primary"]
                                                 }, ${
                                  theme.colors["bg-secondary"]
                                }); border-color: ${theme.colors["accent"]};">
                                                <div class="w-1 h-1 rounded-full" style="background-color: ${
                                                  theme.colors["accent"]
                                                };"></div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            `
                              )
                              .join("")}
                        </div>
                    </div>
                    
                    <!-- Background Image Settings -->
                    <div>
                        <h3 class="text-lg font-semibold text-white mb-4">Background Image</h3>
                        <div class="space-y-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-300 mb-2">Image File</label>
                                <div class="flex space-x-2">
                                    <input type="text" id="bg-image-path" placeholder="Select image file..." 
                                           class="flex-1 bg-gray-800 border border-gray-600 text-white px-3 py-2 rounded text-sm focus:outline-none focus:border-blue-500">
                                    <button id="bg-image-browse" class="px-3 py-2 bg-blue-600 text-white rounded text-sm hover:bg-blue-700">
                                        Browse
                                    </button>
                                </div>
                            </div>
                            
                            <div>
                                <label class="block text-sm font-medium text-gray-300 mb-2">
                                    Opacity: <span id="bg-opacity-value">30%</span>
                                </label>
                                <input type="range" id="bg-opacity-slider" min="0" max="100" value="30" 
                                       class="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer">
                            </div>
                            
                            <div class="text-xs text-gray-400">
                                <strong>Background Image:</strong> Fills the entire main area (excluding navigation).<br>
                                <strong>Opacity Control:</strong> Higher values make the image more visible and content panels more transparent.<br>
                                <strong>Real-time Preview:</strong> Changes apply immediately as you adjust the slider.
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="flex justify-end mt-8">
                    <div class="space-x-3">
                        <button id="theme-cancel-btn" class="px-4 py-2 bg-gray-700 text-white rounded hover:bg-gray-600 transition-colors">
                            Cancel
                        </button>
                        <button id="theme-apply-btn" class="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors">
                            Apply
                        </button>
                    </div>
                </div>
            </div>
        `;

    // Add event listeners
    let selectedTheme = this.currentTheme;
    let currentBgImage =
      this.themes[this.currentTheme]?.background?.image || "";
    let currentBgOpacity =
      (this.themes[this.currentTheme]?.background?.opacity || 0.3) * 100;

    // Initialize background controls
    const bgImageInput = modal.querySelector("#bg-image-path");
    const bgOpacitySlider = modal.querySelector("#bg-opacity-slider");
    const bgOpacityValue = modal.querySelector("#bg-opacity-value");
    const bgBrowseBtn = modal.querySelector("#bg-image-browse");

    bgImageInput.value = currentBgImage;
    bgOpacitySlider.value = currentBgOpacity;
    bgOpacityValue.textContent = Math.round(currentBgOpacity) + "%";

    // Theme selection
    modal.querySelectorAll(".theme-option").forEach((option) => {
      option.addEventListener("click", () => {
        // Remove selection from all options
        modal.querySelectorAll(".theme-option div").forEach((div) => {
          div.classList.remove(
            "border-blue-500",
            "bg-blue-900",
            "bg-opacity-20"
          );
          div.classList.add("border-gray-600");
        });

        // Add selection to clicked option
        const div = option.querySelector("div");
        div.classList.remove("border-gray-600");
        div.classList.add("border-blue-500", "bg-blue-900", "bg-opacity-20");

        selectedTheme = option.dataset.theme;

        // Update background controls for selected theme
        const themeData = this.themes[selectedTheme];
        if (themeData?.background) {
          currentBgImage = themeData.background.image || "";
          currentBgOpacity = (themeData.background.opacity || 0.3) * 100;
          bgImageInput.value = currentBgImage;
          bgOpacitySlider.value = currentBgOpacity;
          bgOpacityValue.textContent = Math.round(currentBgOpacity) + "%";
        }
      });
    });

    // Background image browse button
    bgBrowseBtn.addEventListener("click", async () => {
      try {
        // Use the API to browse for image files
        const imagePath = await API.browseFile([
          ".jpg",
          ".jpeg",
          ".png",
          ".gif",
          ".bmp",
          ".webp",
        ]);
        if (imagePath) {
          currentBgImage = imagePath;
          bgImageInput.value = imagePath;
        }
      } catch (error) {
        console.error("Failed to browse for image:", error);
      }
    });

    // Background image path input
    bgImageInput.addEventListener("input", (e) => {
      currentBgImage = e.target.value;
    });

    // Background opacity slider
    bgOpacitySlider.addEventListener("input", (e) => {
      currentBgOpacity = parseFloat(e.target.value);
      bgOpacityValue.textContent = Math.round(currentBgOpacity) + "%";

      // Apply opacity change in real-time for preview
      this.updateBackgroundOpacity(currentBgOpacity / 100);
    });

    // Cancel button
    modal.querySelector("#theme-cancel-btn").addEventListener("click", () => {
      this.closeModal(modal);
      onSelect(this.currentTheme);
    });

    // Apply button
    modal.querySelector("#theme-apply-btn").addEventListener("click", () => {
      // Apply the selected theme first
      this.applyTheme(selectedTheme);

      // Apply background image settings
      if (
        currentBgImage !== this.themes[selectedTheme]?.background?.image ||
        currentBgOpacity / 100 !==
          this.themes[selectedTheme]?.background?.opacity
      ) {
        this.updateBackgroundImage(currentBgImage, currentBgOpacity / 100);
      }

      this.closeModal(modal);
      onSelect(selectedTheme);
    });

    // Close on backdrop click
    modal.addEventListener("click", (e) => {
      if (e.target === modal) {
        this.closeModal(modal);
        onSelect(this.currentTheme);
      }
    });

    // Animate in the modal content
    setTimeout(() => {
      const content = modal.querySelector("#theme-modal-content");
      content.classList.remove("scale-95");
      content.classList.add("scale-100");
    }, 50);

    return modal;
  }

  closeModal(modal) {
    modal.classList.remove("opacity-100");
    modal.classList.add("opacity-0");
    setTimeout(() => {
      if (modal.parentNode) {
        modal.parentNode.removeChild(modal);
      }
    }, 300);
  }

  cleanupSwitchStyles() {
    // Remove any inline styles from switches that might override CSS theming
    const switches = document.querySelectorAll(".switch");
    switches.forEach((switchEl) => {
      switchEl.style.backgroundColor = "";
    });
  }

  // Update background image for current theme
  async updateBackgroundImage(imagePath, opacity = null) {
    const currentTheme = this.themes[this.currentTheme];
    if (currentTheme && currentTheme.background) {
      currentTheme.background.image = imagePath;
      if (opacity !== null) {
        currentTheme.background.opacity = opacity;
      }

      // Apply the changes immediately
      const root = document.documentElement;
      root.style.setProperty(
        `--theme-bg-image`,
        imagePath ? `url("${imagePath}")` : ""
      );
      root.style.setProperty(
        `--theme-bg-opacity`,
        currentTheme.background.opacity
      );

      // Update content transparency based on background opacity
      const bgOpacity = currentTheme.background.opacity;
      const contentOpacity = Math.max(0.5, 1 - bgOpacity * 0.8); // Inverse relationship
      const mainOpacity = Math.max(0.3, 1 - bgOpacity * 1.2); // Even more transparent for main area

      root.style.setProperty(`--theme-content-bg-opacity`, contentOpacity);
      root.style.setProperty(`--theme-main-bg-opacity`, mainOpacity);

      // Save the updated theme
      await this.saveThemeCustomization();
    }
  }

  // Update background opacity for current theme
  async updateBackgroundOpacity(opacity) {
    const currentTheme = this.themes[this.currentTheme];
    if (currentTheme && currentTheme.background) {
      currentTheme.background.opacity = opacity;

      // Apply the change immediately
      const root = document.documentElement;
      root.style.setProperty(`--theme-bg-opacity`, opacity);

      // Update content transparency based on background opacity
      // When background is more visible (higher opacity), make content more transparent
      const contentOpacity = Math.max(0.5, 1 - opacity * 0.8); // Inverse relationship
      const mainOpacity = Math.max(0.3, 1 - opacity * 1.2); // Even more transparent for main area

      root.style.setProperty(`--theme-content-bg-opacity`, contentOpacity);
      root.style.setProperty(`--theme-main-bg-opacity`, mainOpacity);

      // Save the updated theme
      await this.saveThemeCustomization();
    }
  }

  // Save theme customizations to backend
  async saveThemeCustomization() {
    const currentTheme = this.themes[this.currentTheme];
    if (currentTheme && window.API && window.API.saveThemeCustomization) {
      try {
        await window.API.saveThemeCustomization(
          this.currentTheme,
          currentTheme
        );
      } catch (error) {
        console.error("Failed to save theme customization:", error);
      }
    }
  }

  // Load theme customizations from backend
  async loadThemeCustomization(themeId) {
    if (window.API && window.API.getThemeCustomization) {
      try {
        const customTheme = await window.API.getThemeCustomization(themeId);
        // Merge custom properties with default theme
        if (this.themes[themeId] && customTheme && customTheme.background) {
          this.themes[themeId].background = {
            ...this.themes[themeId].background,
            ...customTheme.background,
          };
        }
      } catch (error) {
        console.warn(`Failed to load custom theme data for ${themeId}:`, error);
      }
    }
  }
}

// Export for use in other modules
window.ThemeManager = ThemeManager;
