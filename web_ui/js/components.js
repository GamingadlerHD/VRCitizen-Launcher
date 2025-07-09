// Component System for Star Citizen VR Launcher

const Components = {
  // Component loader for loading HTML files
  async loadComponent(path, containerId) {
    try {
      const html = await Utils.loadHTML(path);
      if (html) {
        const container = document.getElementById(containerId);
        if (container) {
          container.innerHTML = html;

          // Apply translations to the newly loaded component
          if (window.App && window.App.translationManager) {
            window.App.translationManager.applyTranslations();
          }

          return true;
        }
      }
      return false;
    } catch (error) {
      console.error("Failed to load component:", error);
      return false;
    }
  },

  // Switch toggle functionality
  toggleSwitch(switchElement) {
    switchElement.classList.toggle("active");

    const setting = switchElement.getAttribute("data-setting");
    const isActive = switchElement.classList.contains("active");
    switchElement.style.backgroundColor = "";

    if (setting) {
      console.log("Setting changed:", setting, isActive);
    }
  },

  // Slider value update
  updateSliderValue(sliderId, displayId) {
    const slider = document.getElementById(sliderId);
    const display = document.getElementById(displayId);
    if (slider && display) {
      display.textContent = slider.value;
    }
  },

  // Apply settings to UI elements
  applySettingsToUI(settings) {
    const fieldMapping = {
      scPath: "sc-path",
      vorpxPath: "vorpx-path",
      launcherPath: "launcher-path",
      width: "width",
      height: "height",
      fov: "fov",
    };

    // Apply text inputs
    Object.entries(fieldMapping).forEach(([settingKey, elementId]) => {
      if (settings[settingKey] !== undefined) {
        const element = document.getElementById(elementId);
        if (element) {
          element.value = settings[settingKey];
          console.log(`Set ${elementId} = ${settings[settingKey]}`);
        }
      }
    });

    // Apply dropdowns
    const dropdownMapping = {
      selectedTemplate: "template-select",
      "template-select_val": "template-select",
      selectedPreset: "preset-select",
      "preset-select_val": "preset-select",
      headtrackingSource: "headtracking-source",
      "headtracking-source_val": "headtracking-source",
    };

    Object.entries(dropdownMapping).forEach(([settingKey, elementId]) => {
      if (settings[settingKey] !== undefined) {
        const element = document.getElementById(elementId);
        if (element) {
          element.value = settings[settingKey];
          console.log(`Set dropdown ${elementId} = ${settings[settingKey]}`);
        }
      }
    });

    // Apply switches (boolean settings)
    Object.entries(settings).forEach(([key, value]) => {
      // Remove _val suffix if present for switch lookup
      const switchKey = key.endsWith("_val") ? key.slice(0, -4) : key;
      const switchElement = document.querySelector(
        `[data-setting="${switchKey}"]`
      );

      if (switchElement && typeof value === "boolean") {
        // Remove any inline styles that might override CSS
        switchElement.style.backgroundColor = "";

        if (value) {
          switchElement.classList.add("active");
        } else {
          switchElement.classList.remove("active");
        }
        console.log(`Set switch ${switchKey} = ${value}`);
      }
    });

    // Apply sliders
    const sliderMapping = {
      "gforce-boost": "gforce-boost",
      "gforce-bob": "gforce-bob",
      "shake-scale": "shake-scale",
      "max-zoom": "max-zoom",
      chromatic: "chromatic",
    };

    Object.entries(sliderMapping).forEach(([settingKey, sliderId]) => {
      if (settings[settingKey] !== undefined) {
        const slider = document.getElementById(sliderId);
        if (slider) {
          slider.value = settings[settingKey];
          this.updateSliderValue(sliderId, sliderId + "-value");
          console.log(`Set slider ${sliderId} = ${settings[settingKey]}`);
        }
      }
    });
  },

  // Collect all settings from UI
  collectAllSettings() {
    const settings = {
      scPath: document.getElementById("sc-path")?.value || "",
      vorpxPath: document.getElementById("vorpx-path")?.value || "",
      launcherPath: document.getElementById("launcher-path")?.value || "",
      selectedTemplate: document.getElementById("template-select")?.value || "",
      selectedPreset: document.getElementById("preset-select")?.value || "",
      width: document.getElementById("width")?.value || "",
      height: document.getElementById("height")?.value || "",
      fov: document.getElementById("fov")?.value || "",
      headtrackingSource:
        document.getElementById("headtracking-source")?.value || "TrackIR",
    };

    // Collect boolean settings from switches
    const switches = document.querySelectorAll(".switch[data-setting]");
    switches.forEach((switchEl) => {
      const setting = switchEl.getAttribute("data-setting");
      if (setting) {
        settings[setting] = switchEl.classList.contains("active");
      }
    });

    // Collect slider values
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
        settings[sliderId] = parseInt(slider.value) || 0;
      }
    });

    return settings;
  },

  // Reset all form elements
  resetAllForms() {
    // Reset text inputs
    const inputs = [
      "sc-path",
      "vorpx-path",
      "launcher-path",
      "width",
      "height",
      "fov",
    ];
    inputs.forEach((id) => {
      const element = document.getElementById(id);
      if (element) {
        element.value = "";
      }
    });

    // Reset dropdowns
    const selects = ["template-select", "preset-select", "headtracking-source"];
    selects.forEach((id) => {
      const element = document.getElementById(id);
      if (element) {
        element.selectedIndex = 0;
      }
    });

    // Reset all switches
    const switches = document.querySelectorAll(".switch[data-setting]");
    switches.forEach((switchEl) => {
      switchEl.classList.remove("active");
      // Remove inline styles to let CSS handle theming
      switchEl.style.backgroundColor = "";
    });

    // Reset sliders
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
        this.updateSliderValue(sliderId, sliderId + "-value");
      }
    });
  },
};
