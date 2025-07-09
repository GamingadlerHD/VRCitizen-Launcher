// Utility Functions for Star Citizen VR Launcher

const Utils = {
  // Debug logging function
  debugLog(message) {
    console.log(message);
    const debugLog = document.getElementById("debug-log");
    if (debugLog) {
      const div = document.createElement("div");
      div.textContent = `${new Date().toLocaleTimeString()}: ${message}`;
      debugLog.appendChild(div);
      debugLog.scrollTop = debugLog.scrollHeight;
    }
  },

  // Toggle debug panel visibility
  toggleDebugPanel() {
    const debugPanel = document.getElementById("debug-panel");
    const toggleButton = document.getElementById("debug-toggle");
    if (debugPanel) {
      const isHidden = debugPanel.classList.contains("hidden");
      if (isHidden) {
        debugPanel.classList.remove("hidden");
        toggleButton.style.backgroundColor = "#10b981"; // Green when open
        toggleButton.title = App.translationManager
          ? App.translationManager.get(
              "hide_debug_console",
              "Hide Debug Console"
            )
          : "Hide Debug Console";
      } else {
        debugPanel.classList.add("hidden");
        toggleButton.style.backgroundColor = "#374151"; // Gray when closed
        toggleButton.title = App.translationManager
          ? App.translationManager.get(
              "show_debug_console",
              "Show Debug Console"
            )
          : "Show Debug Console";
      }
    }
  },

  // Show toast notification
  showToast(message, type = "info") {
    const container = document.getElementById("toast-container");
    const toast = document.createElement("div");
    toast.className = `toast p-4 rounded-lg border min-w-80 mb-2`;

    const typeClasses = {
      success: "bg-sc-bg-secondary border-green-500 text-green-400",
      error: "bg-sc-bg-secondary border-red-500 text-red-400",
      info: "bg-sc-bg-secondary border-sc-blue text-sc-blue-light",
      warning: "bg-sc-bg-secondary border-yellow-500 text-yellow-400",
    };

    toast.className += " " + (typeClasses[type] || typeClasses.info);

    // Get translated toast title from backend
    let title = type.charAt(0).toUpperCase() + type.slice(1);
    if (App.translationManager) {
      const toastKeys = {
        success: "toast_success",
        error: "toast_error",
        info: "toast_info",
        warning: "toast_warning",
      };
      title = App.translationManager.get(
        toastKeys[type] || "toast_info",
        title
      );
    }

    toast.innerHTML = `
            <div class="font-bold mb-1">${title}</div>
            <div>${message}</div>
        `;

    container.appendChild(toast);

    setTimeout(() => {
      toast.remove();
    }, 3000);
  },

  // Load HTML content from file
  async loadHTML(url) {
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.text();
    } catch (error) {
      console.error("Failed to load HTML:", error);
      return null;
    }
  },
};
