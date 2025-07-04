// Theme system for Star Citizen VR Launcher

class ThemeManager {
  constructor() {
    this.themes = {
      default: {
        name: "Star Citizen",
        description: "Classic Star Citizen styling",
        background: {
          image: "https://wallpapercave.com/wp/iqZETVS.jpg", // Path to background image
          opacity: 0.3, // Image opacity (0-1)
          position: "center",
          size: "cover",
          repeat: "no-repeat",
        },
        colors: {
          // Backgrounds
          "bg-primary": "#1a202c",
          "bg-secondary": "#2d3748",
          "bg-tertiary": "#4a5568",
          border: "#4a5568",

          // Text colors
          "text-primary": "#e2e8f0",
          "text-secondary": "#a0aec0",
          "text-muted": "#718096",

          // Navigation colors
          "nav-text": "#a0aec0",
          "nav-text-hover": "#ffffff",
          "nav-text-active": "#ffffff",
          "nav-bg-hover": "#4a5568",
          "nav-bg-active": "#3182ce",

          // Form elements
          "input-bg": "#4a5568",
          "input-border": "#718096",
          "input-text": "#ffffff",
          "input-placeholder": "#a0aec0",
          "input-focus-border": "#3182ce",

          // Dropdown colors
          "dropdown-bg": "#4a5568",
          "dropdown-border": "#718096",
          "dropdown-text": "#ffffff",
          "dropdown-option-hover": "#3182ce",

          // Button colors
          "btn-primary-bg": "#3182ce",
          "btn-primary-text": "#ffffff",
          "btn-primary-hover": "#2b6cb0",
          "btn-secondary-bg": "#4a5568",
          "btn-secondary-text": "#e2e8f0",
          "btn-secondary-hover": "#718096",

          // Accent colors
          accent: "#3182ce",
          "accent-light": "#63b3ed",
          "accent-dark": "#2b6cb0",

          // Status colors
          success: "#38a169",
          warning: "#d69e2e",
          error: "#e53e3e",
        },
      },
      starwars: {
        name: "Star Wars",
        description: "A galaxy far, far away...",
        background: {
          image: "https://wallpapercave.com/wp/iqZETVS.jpg", // Path to background image (could be Death Star, space scene, etc.)
          opacity: 0.2, // Lower opacity for darker theme
          position: "center",
          size: "cover",
          repeat: "no-repeat",
        },
        colors: {
          // Backgrounds
          "bg-primary": "#0a0a0a",
          "bg-secondary": "#1a1a1a",
          "bg-tertiary": "#2a2a2a",
          border: "#ffd700",

          // Text colors
          "text-primary": "#ffd700",
          "text-secondary": "#ffffff",
          "text-muted": "#cccccc",

          // Navigation colors
          "nav-text": "#cccccc",
          "nav-text-hover": "#ffd700",
          "nav-text-active": "#000000",
          "nav-bg-hover": "#2a2a2a",
          "nav-bg-active": "#ffd700",

          // Form elements
          "input-bg": "#2a2a2a",
          "input-border": "#ffd700",
          "input-text": "#ffd700",
          "input-placeholder": "#cccccc",
          "input-focus-border": "#ffed4e",

          // Dropdown colors
          "dropdown-bg": "#2a2a2a",
          "dropdown-border": "#ffd700",
          "dropdown-text": "#ffd700",
          "dropdown-option-hover": "#b8860b",

          // Button colors
          "btn-primary-bg": "#ffd700",
          "btn-primary-text": "#000000",
          "btn-primary-hover": "#b8860b",
          "btn-secondary-bg": "#2a2a2a",
          "btn-secondary-text": "#ffd700",
          "btn-secondary-hover": "#3a3a3a",

          // Accent colors
          accent: "#ffd700",
          "accent-light": "#ffed4e",
          "accent-dark": "#b8860b",

          // Status colors
          success: "#00ff00",
          warning: "#ff8c00",
          error: "#ff4444",
        },
      },
      cyberpunk: {
        name: "Cyberpunk",
        description: "Neon-lit future vibes",
        background: {
          image: "https://wallpapercave.com/wp/iqZETVS.jpg", // Path to background image (could be cyberpunk cityscape, neon, etc.)
          opacity: 0.25, // Medium opacity for neon visibility
          position: "center",
          size: "cover",
          repeat: "no-repeat",
        },
        colors: {
          // Backgrounds
          "bg-primary": "#0f0f0f",
          "bg-secondary": "#1a1a2e",
          "bg-tertiary": "#16213e",
          border: "#ff00ff",

          // Text colors
          "text-primary": "#00ffff",
          "text-secondary": "#ff00ff",
          "text-muted": "#a0a0a0",

          // Navigation colors
          "nav-text": "#a0a0a0",
          "nav-text-hover": "#00ffff",
          "nav-text-active": "#000000",
          "nav-bg-hover": "#16213e",
          "nav-bg-active": "#ff00ff",

          // Form elements
          "input-bg": "#16213e",
          "input-border": "#ff00ff",
          "input-text": "#00ffff",
          "input-placeholder": "#a0a0a0",
          "input-focus-border": "#ff66ff",

          // Dropdown colors
          "dropdown-bg": "#16213e",
          "dropdown-border": "#ff00ff",
          "dropdown-text": "#00ffff",
          "dropdown-option-hover": "#cc00cc",

          // Button colors
          "btn-primary-bg": "#ff00ff",
          "btn-primary-text": "#000000",
          "btn-primary-hover": "#cc00cc",
          "btn-secondary-bg": "#16213e",
          "btn-secondary-text": "#00ffff",
          "btn-secondary-hover": "#1a2a4e",

          // Accent colors
          accent: "#ff00ff",
          "accent-light": "#ff66ff",
          "accent-dark": "#cc00cc",

          // Status colors
          success: "#00ff00",
          warning: "#ffff00",
          error: "#ff0066",
        },
      },
      minimal: {
        name: "Minimal Dark",
        description: "Clean, minimal dark interface",
        background: {
          image: "https://wallpapercave.com/wp/iqZETVS.jpg", // Path to background image (could be subtle texture, pattern, etc.)
          opacity: 0.15, // Very low opacity for minimal design
          position: "center",
          size: "cover",
          repeat: "no-repeat",
        },
        colors: {
          // Backgrounds
          "bg-primary": "#1a1a1a",
          "bg-secondary": "#2a2a2a",
          "bg-tertiary": "#3a3a3a",
          border: "#555555",

          // Text colors
          "text-primary": "#ffffff",
          "text-secondary": "#cccccc",
          "text-muted": "#999999",

          // Navigation colors
          "nav-text": "#cccccc",
          "nav-text-hover": "#ffffff",
          "nav-text-active": "#ffffff",
          "nav-bg-hover": "#3a3a3a",
          "nav-bg-active": "#555555",

          // Form elements
          "input-bg": "#3a3a3a",
          "input-border": "#555555",
          "input-text": "#ffffff",
          "input-placeholder": "#999999",
          "input-focus-border": "#777777",

          // Dropdown colors
          "dropdown-bg": "#3a3a3a",
          "dropdown-border": "#555555",
          "dropdown-text": "#ffffff",
          "dropdown-option-hover": "#555555",

          // Button colors
          "btn-primary-bg": "#555555",
          "btn-primary-text": "#ffffff",
          "btn-primary-hover": "#666666",
          "btn-secondary-bg": "#3a3a3a",
          "btn-secondary-text": "#cccccc",
          "btn-secondary-hover": "#4a4a4a",

          // Accent colors
          accent: "#555555",
          "accent-light": "#777777",
          "accent-dark": "#333333",

          // Status colors
          success: "#4CAF50",
          warning: "#FF9800",
          error: "#F44336",
        },
      },
    };

    this.currentTheme = this.loadSavedTheme();

    // Load any saved customizations for the current theme
    this.loadThemeCustomization(this.currentTheme);
  }

  loadSavedTheme() {
    const saved = localStorage.getItem("sc-vr-theme");
    return saved && this.themes[saved] ? saved : "default";
  }

  saveTheme(themeId) {
    localStorage.setItem("sc-vr-theme", themeId);
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

  applyTheme(themeId) {
    if (!this.themes[themeId]) {
      console.warn(`Theme ${themeId} not found, using default`);
      themeId = "default";
    }

    const theme = this.themes[themeId];
    const root = document.documentElement;

    // Show loading overlay
    this.showLoading();

    // Apply CSS variables with a slight delay for smooth transition
    setTimeout(() => {
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
      this.saveTheme(themeId);

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

  getCurrentTheme() {
    return this.currentTheme;
  }

  getTheme(themeId) {
    return this.themes[themeId];
  }

  getAvailableThemes() {
    return Object.keys(this.themes).map((id) => ({
      id,
      ...this.themes[id],
    }));
  }

  showThemeSelector() {
    return new Promise((resolve) => {
      const modal = this.createThemeSelector(resolve);
      document.body.appendChild(modal);

      // Show modal with animation
      setTimeout(() => {
        modal.classList.remove("opacity-0");
        modal.classList.add("opacity-100");
      }, 10);
    });
  }

  createThemeSelector(onSelect) {
    const modal = document.createElement("div");
    modal.className =
      "fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 opacity-0 transition-opacity duration-300";

    const themes = this.getAvailableThemes();

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
  updateBackgroundImage(imagePath, opacity = null) {
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
      this.saveThemeCustomization();
    }
  }

  // Update background opacity for current theme
  updateBackgroundOpacity(opacity) {
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
      this.saveThemeCustomization();
    }
  }

  // Save theme customizations to localStorage
  saveThemeCustomization() {
    const currentTheme = this.themes[this.currentTheme];
    if (currentTheme) {
      localStorage.setItem(
        `sc-vr-theme-${this.currentTheme}-custom`,
        JSON.stringify(currentTheme)
      );
    }
  }

  // Load theme customizations from localStorage
  loadThemeCustomization(themeId) {
    const saved = localStorage.getItem(`sc-vr-theme-${themeId}-custom`);
    if (saved) {
      try {
        const customTheme = JSON.parse(saved);
        // Merge custom properties with default theme
        if (this.themes[themeId] && customTheme.background) {
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
