import xml.etree.ElementTree as ET
from logs import log, warn, error

def update_xml(root, tag : str, value : str):
    """
    Update the XML file by setting the value of a specific tag.
    """
    try:
        # Update attributes if they are provided
        for attr in root.findall('Attr'):
            name = attr.get('name')
            
            if name == tag:
                log(f"Updating existing XML attribute '{tag}' to value: {value}")
                attr.set('value', str(value))
                return True
            
        # If the tag is not found, create a new one
        log(f"Creating new XML attribute '{tag}' with value: {value}")
        new_attr = ET.Element('Attr')
        new_attr.set('name', tag)
        new_attr.set('value', str(value))
        root.append(new_attr)
        return True
    except Exception as e:
        error(f"Error updating XML file: {e}")
        return False

def update_xml_by_dict(file_path : str, attributes : dict):
    """
    Update the XML file by setting the values of specific tags based on a dictionary.
    """
    log(f"Updating XML file: {file_path} with {len(attributes)} attributes")
    
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        updated_count = 0
        for key, value in attributes.items():
            log(f"Processing attribute '{key}' with value: {value}")
            
            # Handle special value conversions
            if isinstance(value, str):
                if value == "Faceware FOIP":
                    value = 2
                    log(f"Converted 'Faceware FOIP' to numeric value: {value}")
                elif value == "TrackIR":
                    value = 1
                    log(f"Converted 'TrackIR' to numeric value: {value}")
                elif value == "Tobi":
                    value = 3
                    log(f"Converted 'Tobi' to numeric value: {value}")
            
            if update_xml(root, key, value):
                updated_count += 1

        tree.write(file_path, encoding="utf-8", xml_declaration=False)
        log(f"XML file update completed - {updated_count} attributes processed")
        
    except Exception as e:
        error(f"Failed to update XML file {file_path}: {e}")
        raise


vr_settings : list[str]  = [
    "MotionBlur",
    "MaxAutoZoom",
    "ShakeScale",
    "VSync",
    "Width",
    "Height",
    "FOV",
    "AutoZoomOnSelectedTarget",
    "AutoZoomOnSelectedTargetStrength",
    "ChromaticAberration",
    "FilmGrain",
    "GForceBoostZoomScale",
    "GForceHeadBobScale",
    "CameraSpringMovement",
    "HeadtrackingToggle",
    "HeadtrackingSource",
    "HeadtrackingDisableDuringADS",
    "HeadtrackingDisableDuringMobiGlas",
    "HeadtrackingDisableDuringWalking",
    "HeadtrackingEnableRollFPS",
    "HeadtrackingThirdPersonCameraToggle",
    "HeadtrackingThirdPersonDisableDuringInventory",
]


def update_vr_settings_from_xml_to_xml(from_xml_path : str, to_xml_path : str):
    """
    Update the VR settings from one XML file to another.
    """
    log(f"Updating VR settings from {from_xml_path} to {to_xml_path}")
    
    try:
        # Parse the XML files
        to_tree = ET.parse(to_xml_path)
        to_root = to_tree.getroot()
        
        from_tree = ET.parse(from_xml_path)
        from_root = from_tree.getroot()
        
        # Create dictionaries for efficient lookup
        from_attributes = {attr.get('name') for attr in from_root.findall('Attr')}
        from_values = {attr.get('name'): attr.get('value') for attr in from_root.findall('Attr')}
        
        log(f"Found {len(from_attributes)} attributes in source XML")
        
        # Create a dictionary to store the VR settings attributes
        vr_attributes = {}
        removed_count = 0
        
        # Process VR settings in the target XML
        for attr in to_root.findall('Attr'):
            name = attr.get('name')
            if name in vr_settings:
                log(f"Processing VR setting: {name}")
                if name in from_attributes:
                    vr_attributes[name] = from_values[name]
                    log(f"VR setting '{name}' will be restored to: {from_values[name]}")
                else:
                    log(f"Removing VR setting '{name}' - not found in source")
                    to_root.remove(attr)
                    removed_count += 1

        # Update the VR attributes
        if vr_attributes:
            log(f"Updating {len(vr_attributes)} VR settings")
            for key, value in vr_attributes.items():
                update_xml(to_root, key, value)

        to_tree.write(to_xml_path, encoding="utf-8", xml_declaration=False)
        log(f"VR settings restoration completed - {len(vr_attributes)} updated, {removed_count} removed")
        
    except Exception as e:
        error(f"Failed to update VR settings from XML: {e}")
        raise
