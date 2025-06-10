import json
import os

def get_templates(folder_path='templates'):
    combined_templates = []
    
    try:
        # List all files in the directory
        for filename in os.listdir(folder_path):
            if filename.endswith('.json'):
                file_path = os.path.join(folder_path, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Assuming each JSON has a 'templates' key with a list
                        combined_templates.extend(data.get('templates', []))
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    print(f"Error reading {filename}: {e}")
                    continue
    except FileNotFoundError:
        print(f"Folder {folder_path} not found")
        return []
    
    return combined_templates

def GetTemplateByName(templateName: str):
    templates = get_templates()
    for template in templates:
        if template['name'] == templateName:
            return template
    return {}

def GetPresets(templateName):
    template = GetTemplateByName(templateName)
    if template:
        return template.get('presets', [])
    else:
        print(f"Template '{templateName}' not found.")
        return []