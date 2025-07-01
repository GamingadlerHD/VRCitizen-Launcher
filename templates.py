import json
import os
from logs import log, warn, error

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
                        error(f"ECL1201: Error reading {file_path}: {e}")
                        continue
    except FileNotFoundError:
        error(f"ECL1202: Templates folder {folder_path} not found")
        return []

    log(f"Total templates loaded: {len(combined_templates)}")
    return combined_templates

def GetTemplateByName(templateName: str):
    templates = get_templates()
    for template in templates:
        if template['name'] == templateName:
            return template
    warn(f"Template not found: {templateName}")
    return {}

def GetPresets(templateName):
    template = GetTemplateByName(templateName)
    if template:
        presets = template.get('presets', [])
        log(f"Found {len(presets)} presets for template {templateName}")
        return presets
    error(f"ECL1203: Template '{templateName}' not found for preset lookup.")
    return []