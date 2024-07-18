import os
from lxml import etree

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
XML_DIR = os.path.join(REPO_ROOT, 'XML')

def validate_xml(xml_file):
    errors = []
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
                errors.append(f"Schema-Datei nicht gefunden: {xsd_path} für {xml_file}")
        else:
            errors.append(f"Keine Schema-Location gefunden in {xml_file}")
    
    except etree.DocumentInvalid as e:
        errors.append(f"Validierungsfehler in {xml_file}:")
        for error in e.error_log:
            errors.append(f"  Zeile {error.line}, Spalte {error.column}: {error.message}")
    except etree.XMLSyntaxError as e:
        errors.append(f"XML-Syntaxfehler in {xml_file}:")
        errors.append(f"  Zeile {e.lineno}, Spalte {e.offset}: {e.msg}")
    except Exception as e:
        errors.append(f"Fehler bei der Verarbeitung von {xml_file}: {str(e)}")
    
    return errors

def main():
    all_errors = []
    for root, dirs, files in os.walk(XML_DIR):
        for file in files:
            if file.endswith('.xml'):
                xml_file = os.path.join(root, file)
                errors = validate_xml(xml_file)
                all_errors.extend(errors)
    
    if all_errors:
        print("Validierung fehlgeschlagen. Bitte korrigieren Sie die folgenden Fehler:")
        with open('schema_validation_errors.txt', 'w') as f:
            for error in all_errors:
                print(error)
                f.write(f"{error}\n")
        exit(1)
    else:
        print("Alle XML-Dateien wurden erfolgreich validiert.")

if __name__ == "__main__":
    main()
