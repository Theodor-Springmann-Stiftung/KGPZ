import os
from lxml import etree

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
XML_DIR = os.path.join(REPO_ROOT, 'XML')

def validate_xml(xml_file):
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(xml_file, parser)
        root = tree.getroot()

        schema_location = root.get('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation')
        if schema_location:
            namespace, xsd_path = schema_location.split()
            xsd_path = os.path.normpath(os.path.join(os.path.dirname(xml_file), xsd_path))
            
            if os.path.exists(xsd_path):
                xsd_doc = etree.parse(xsd_path)
                schema = etree.XMLSchema(xsd_doc)
                schema.assertValid(tree)
                print(f"Validation erfolgreich: {xml_file}")
            else:
                print(f"Schema-Datei nicht gefunden: {xsd_path} für {xml_file}")
                return False
        else:
            print(f"Keine Schema-Location gefunden in {xml_file}")
            return False
    
    except etree.DocumentInvalid as e:
        print(f"Validierungsfehler in {xml_file}:")
        for error in e.error_log:
            print(f"  Zeile {error.line}, Spalte {error.column}: {error.message}")
        return False
    except etree.XMLSyntaxError as e:
        print(f"XML-Syntaxfehler in {xml_file}:")
        print(f"  Zeile {e.lineno}, Spalte {e.offset}: {e.msg}")
        return False
    except Exception as e:
        print(f"Fehler bei der Verarbeitung von {xml_file}: {str(e)}")
        return False
    
    return True

def main():
    validation_failed = False
    for root, dirs, files in os.walk(XML_DIR):
        for file in files:
            if file.endswith('.xml'):
                xml_file = os.path.join(root, file)
                if not validate_xml(xml_file):
                    validation_failed = True
    
    if validation_failed:
        print("Validierung fehlgeschlagen. Bitte korrigieren Sie die oben genannten Fehler.")
        exit(1)
    else:
        print("Alle XML-Dateien wurden erfolgreich validiert.")

if __name__ == "__main__":
    main()
