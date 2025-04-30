import xml.etree.ElementTree as ET

def update_attributes(file_path : str, width : int, height : int, fov : int):

    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Update attributes if they are provided
        for attr in root.findall('Attr'):
            name = attr.get('name')
            
            if width is not None and name == "Width":
                attr.set('value', str(width))
            elif height is not None and name == "Height":
                attr.set('value', str(height))
            elif fov is not None and name == "FOV":
                attr.set('value', str(fov))
        
        # Write the changes back to the file
        tree.write(file_path, encoding="utf-8", xml_declaration=False)
        print("XML file updated successfully!")
    except Exception as e:
        print(f"Error updating XML file: {e}")