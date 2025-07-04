# webview_gui.py
import os
import sys
import threading
import time
import webview

# Import your existing modules
from i18n import set_language, translate, load_translations_from_file
from config import add_or_change_value_in_config, load_input_config
from templates import get_templates, GetPresets
from logs import log, error
from constants import DXGI_DLL

def validate_star_citizen_path(path):
    """Simple validation for Star Citizen installation path"""
    if not path or not os.path.exists(path):
        return False
    # Look for StarCitizen.exe or other game files
    executable_names = ['StarCitizen.exe', 'StarCitizen_Launcher.exe', 'Launcher.exe']
    for exe in executable_names:
        if os.path.isfile(os.path.join(path, exe)):
            return True
    return False

def get_config():
    """Get configuration from file"""
    config = load_input_config()
    return config if config else {}

class WebViewAPI:
    """API class that bridges Python functions to JavaScript"""
    
    def __init__(self):
        pass
        
    def get_translations(self, language_code):
        """Get translations for a specific language"""
        try:
            translations = load_translations_from_file(language_code)
            return {"success": True, "data": translations}
        except Exception as e:
            error(f"Failed to load translations: {e}")
            return {"success": False, "error": str(e)}
    
    def get_current_language(self):
        """Get the current language from config"""
        try:
            config = load_input_config()
            if config and 'language' in config:
                return config['language']
            return 'en'  # Default fallback
        except Exception as e:
            error(f"Failed to get current language: {e}")
            return 'en'  # Default fallback
    
    def change_language(self, language_code):
        """Change the application language"""
        try:
            set_language(language_code)
            add_or_change_value_in_config("language", language_code)
            log(f"Language changed to: {language_code}")
            return True
        except Exception as e:
            error(f"Failed to change language: {e}")
            return False
    
    def browse_folder(self):
        """Open folder browser dialog"""
        try:
            result = webview.windows[0].create_file_dialog(
                webview.FOLDER_DIALOG,
                directory=os.path.expanduser('~')
            )
            if result and len(result) > 0:
                folder_path = result[0]
                log(f"Selected folder: {folder_path}")
                return folder_path
            return None
        except Exception as e:
            error(f"Failed to browse folder: {e}")
            return None
    
    def get_templates(self):
        """Get available VR templates"""
        try:
            templates = get_templates()
            return templates
        except Exception as e:
            error(f"Failed to get templates: {e}")
            return []
    
    def get_presets(self, template_name):
        """Get presets for a specific template"""
        try:
            presets = GetPresets(template_name)
            return presets
        except Exception as e:
            error(f"Failed to get presets: {e}")
            return []
    
    def validate_sc_path(self, path):
        """Validate Star Citizen installation path"""
        try:
            is_valid = validate_star_citizen_path(path)
            return is_valid
        except Exception as e:
            error(f"Failed to validate SC path: {e}")
            return False
    
    def check_dxgi_availability(self, sc_path):
        """Check if DXGI is available"""
        try:
            local_path = os.getcwd()
            dxgi_in_sc = os.path.isfile(os.path.join(sc_path, DXGI_DLL)) if sc_path else False
            dxgi_local = os.path.isfile(os.path.join(local_path, 'dxgi.dll'))
            
            return {
                "available": dxgi_in_sc or dxgi_local,
                "dxgi_in_sc": dxgi_in_sc,
                "dxgi_local": dxgi_local
            }
        except Exception as e:
            error(f"Failed to check DXGI: {e}")
            return {"available": False, "dxgi_in_sc": False, "dxgi_local": False}
    
    def start_game(self, config):
        """Start Star Citizen with VR configuration"""
        try:
            # Validate configuration
            if not config.get('scPath'):
                return {"success": False, "error": "Star Citizen path is required"}
            
            if not validate_star_citizen_path(config['scPath']):
                return {"success": False, "error": "Invalid Star Citizen path"}
            
            log(f"Starting game with config: {config}")
            
            # Here you would call your existing game launch logic
            # For now, we'll simulate a successful launch
            
            def launch_thread():
                try:
                    # Simulate launch process
                    time.sleep(2)
                    log("Game launched successfully (simulated)")
                except Exception as e:
                    error(f"Failed to launch game: {e}")
            
            thread = threading.Thread(target=launch_thread, daemon=True)
            thread.start()
            
            return {"success": True, "message": "Game launch initiated"}
            
        except Exception as e:
            error(f"Failed to start game: {e}")
            return {"success": False, "error": str(e)}
    
    def open_url(self, url):
        """Open URL in default browser"""
        try:
            import webbrowser
            webbrowser.open(url)
            return True
        except Exception as e:
            error(f"Failed to open URL: {e}")
            return False
    
    def save_settings(self, settings):
        """Save application settings"""
        try:
            for key, value in settings.items():
                add_or_change_value_in_config(key, value)
            log("Settings saved successfully")
            return True
        except Exception as e:
            error(f"Failed to save settings: {e}")
            return False
    
    def get_settings(self):
        """Get current application settings"""
        try:
            config = get_config()
            return config
        except Exception as e:
            error(f"Failed to get settings: {e}")
            return {}

def create_window():
    """Create the main webview window"""
    
    # Create API instance
    api = WebViewAPI()
    
    # Get the HTML file path
    html_file = os.path.join(os.path.dirname(__file__), "web_ui", "index.html")
    
    # Create the window
    window = webview.create_window(
        title=translate("title"),
        url=html_file,
        width=1200,
        height=800,
        min_size=(800, 600),
        resizable=True,
        js_api=api
    )
    
    return window

def main():
    """Main entry point for the webview application"""
    try:
        # Initialize logging
        log("Starting Star Citizen VR Launcher (WebView version)")
        
        # Create the window
        create_window()
        
        # Start the webview
        webview.start(debug=False)
        
    except Exception as e:
        error(f"Application failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
