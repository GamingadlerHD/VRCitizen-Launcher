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
                attr.set('value', value)
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
        update_xml(root, key, value)

    tree.write(file_path, encoding="utf-8", xml_declaration=False)