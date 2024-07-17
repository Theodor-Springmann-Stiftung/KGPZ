import os
from lxml import etree
from urllib.parse import urljoin

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
XML_DIR = os.path.join(REPO_ROOT, 'XML')

def validate_xml(xml_file):
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        root = tree.getroot()

        # Get the schema location
        schema_location = root.get('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation')
        if schema_location:
            namespace, xsd_path = schema_location.split()
            
            # Convert relative path to absolute
            xsd_path = os.path.normpath(os.path.join(os.path.dirname(xml_file), xsd_path))
            
            if os.path.exists(xsd_path):
                xsd_doc = etree.parse(xsd_path)
                schema = etree.XMLSchema(xsd_doc)
                
                # Validate the XML against the schema
                schema.assertValid(tree)
                print(f"Validation successful: {xml_file}")
            else:
                print(f"Schema file not found: {xsd_path} for {xml_file}")
        else:
            print(f"No schema location found in {xml_file}")
    
    except etree.DocumentInvalid as e:
        print(f"Validation error in {xml_file}:")
        for error in e.error_log:
            print(f"  Line {error.line}, Column {error.column}: {error.message}")
    except etree.XMLSyntaxError as e:
        print(f"XML syntax error in {xml_file}:")
        print(f"  Line {e.lineno}, Column {e.offset}: {e.msg}")
    except Exception as e:
        print(f"Error processing {xml_file}: {str(e)}")

def main():
    for root, dirs, files in os.walk(XML_DIR):
        for file in files:
            if file.endswith('.xml'):
                xml_file = os.path.join(root, file)
                validate_xml(xml_file)

if __name__ == "__main__":
    main()
