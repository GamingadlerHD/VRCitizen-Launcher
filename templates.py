import json
import os
from logs import error

def get_templates(folder_path='templates'):
    combined_templates = []

    try:
        # Walk through all subdirectories and files
        for root, _, files in os.walk(folder_path):
            for filename in files:
                if filename.endswith('.json'):
                    file_path = os.path.join(root, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            # Assuming each JSON has a 'templates' key with a list
                            combined_templates.extend(data.get('templates', []))
                    except (json.JSONDecodeError, UnicodeDecodeError) as e:
                        error(f"Error reading {file_path}: {e}")
                        continue
    except FileNotFoundError:
        error(f"Folder {folder_path} not found")
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
    error(f"Template '{templateName}' not found.")
    return []