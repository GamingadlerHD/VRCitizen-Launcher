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
    
    def browse_file(self, extensions=None):
        """Open file browser dialog"""
        try:
            # Note: extensions parameter is kept for API compatibility but not currently used
            # due to webview file filter compatibility issues
            result = webview.windows[0].create_file_dialog(
                webview.OPEN_DIALOG,
                directory=os.path.expanduser('~')
            )
            if result and len(result) > 0:
                file_path = result[0]
                log(f"Selected file: {file_path}")
                return file_path
            return None
        except Exception as e:
            error(f"Failed to browse file: {e}")
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
    
    def list_theme_files(self):
        """Get list of all theme JSON files in the themes directory"""
        try:
            themes_dir = os.path.join(os.path.dirname(__file__), 'web_ui', 'themes')
            if not os.path.exists(themes_dir):
                log("Themes directory not found")
                return []
            
            theme_files = []
            for filename in os.listdir(themes_dir):
                if filename.endswith('.json'):
                    theme_files.append(filename)
            
            log(f"Found {len(theme_files)} theme files: {theme_files}")
            return theme_files
        except Exception as e:
            error(f"Failed to list theme files: {e}")
            return []
    
    def get_saved_theme(self):
        """Get the saved theme from config"""
        try:
            config = get_config()
            return config.get('theme', 'default')
        except Exception as e:
            error(f"Failed to get saved theme: {e}")
            return 'default'
    
    def save_theme(self, theme_id):
        """Save the current theme to config"""
        try:
            add_or_change_value_in_config('theme', theme_id)
            log(f"Saved theme: {theme_id}")
            return True
        except Exception as e:
            error(f"Failed to save theme: {e}")
            return False
    
    def get_theme_customization(self, theme_id):
        """Get theme customization data"""
        try:
            config = get_config()
            custom_key = f'theme_{theme_id}_custom'
            return config.get(custom_key, {})
        except Exception as e:
            error(f"Failed to get theme customization: {e}")
            return {}
    
    def save_theme_customization(self, theme_id, customization_data):
        """Save theme customization data"""
        try:
            custom_key = f'theme_{theme_id}_custom'
            add_or_change_value_in_config(custom_key, customization_data)
            log(f"Saved theme customization for {theme_id}")
            return True
        except Exception as e:
            error(f"Failed to save theme customization: {e}")
            return False
    
    def get_theme_selector_seen(self):
        """Check if theme selector has been seen"""
        try:
            config = get_config()
            return config.get('theme_selector_seen', False)
        except Exception as e:
            error(f"Failed to get theme selector seen status: {e}")
            return False
    
    def set_theme_selector_seen(self, seen=True):
        """Set theme selector seen status"""
        try:
            add_or_change_value_in_config('theme_selector_seen', seen)
            log(f"Set theme selector seen: {seen}")
            return True
        except Exception as e:
            error(f"Failed to set theme selector seen: {e}")
            return False

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
