import xml.etree.ElementTree as ET

def update_xml(root, tag : str, value : str):
    """
    Update the XML file by setting the value of a specific tag.
    """
    try:
        # Update attributes if they are provided
        for attr in root.findall('Attr'):
            name = attr.get('name')
            
            if name == tag:
                attr.set('value', str(value))
                return True
            
        # If the tag is not found, create a new one
        new_attr = ET.Element('Attr')
        new_attr.set('name', tag)
        new_attr.set('value', str(value))
        root.append(new_attr)
        return True
    except Exception as e:
        print(f"Error updating XML file: {e}")
        return False

def update_xml_by_dict(file_path : str, attributes : dict):
    """
    Update the XML file by setting the values of specific tags based on a dictionary.
    """
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    for key, value in attributes.items():
        print(f"Updating {key} to {value}")
        if isinstance(value, bool):
            value = int(value)
        elif isinstance(value, str):
            if value == "Faceware FOIP":
                value = 2
            elif value == "TrackIR":
                value = 1
            elif value == "Tobi":
                value = 3
        update_xml(root, key, value)

    tree.write(file_path, encoding="utf-8", xml_declaration=False)


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
    # Parse the XML file
    tree = ET.parse(to_xml_path)
    root = tree.getroot()
    
    # Create a dictionary to store the attributes
    attributes = {}
    
    # Iterate through the XML elements and add them to the dictionary
    from_tree = ET.parse(from_xml_path)
    from_root = from_tree.getroot()
    from_attributes = {attr.get('name') for attr in from_root.findall('Attr')}
    from_values = {attr.get('name'): attr.get('value') for attr in from_root.findall('Attr')}

    for attr in root.findall('Attr'):
        name = attr.get('name')
        if name in vr_settings:
            print(f"Updating {name}")
            if name in from_attributes:
                attributes[name] = from_values[name]
            else:
                root.remove(attr)

    tree.write(to_xml_path, encoding="utf-8", xml_declaration=False)

    
    # Update the XML file with the new values
    update_xml_by_dict(to_xml_path, attributes)
