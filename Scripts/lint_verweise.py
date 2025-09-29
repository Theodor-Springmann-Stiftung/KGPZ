import os
from lxml import etree

NAMESPACE = {'kgpz': 'https://www.koenigsberger-zeitungen.de'}
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
XML_DIR = os.path.join(REPO_ROOT, 'XML')

def parse_xml_file(filepath):
    try:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(filepath, parser)
        return tree.getroot()
    except etree.ParseError as e:
        print(f"Fehler beim Parsen von {filepath}: {e}")
        return None

def get_all_ids(root, tag):
    return set(elem.get('id') for elem in root.xpath(f'.//kgpz:{tag}', namespaces=NAMESPACE))

def check_references(beitrag_root, reference_data, filepath):
    errors = []
    relative_path = os.path.relpath(filepath, REPO_ROOT)
    for ref_type, ref_tag in [('akteur', 'akteur'), ('kategorie', 'kategorie'),
                              ('ort', 'ort'), ('werk', 'werk')]:
        for ref in beitrag_root.xpath(f'//kgpz:{ref_tag}', namespaces=NAMESPACE):
            # Skip elements that have an 'id' attribute (they are definitions, not references)
            if ref.get('id') is not None:
                continue

            ref_id = ref.get('ref')
            if ref_id and ref_id not in reference_data[ref_type]:
                line_number = ref.sourceline
                errors.append(f"{relative_path}, Zeile {line_number}: UNGÜLTIGER VERWEIS ({ref_type}:{ref_id})")
    return errors

def main():
    reference_data = {
        'akteur': get_all_ids(parse_xml_file(os.path.join(XML_DIR, 'akteure.xml')), 'akteur'),
        'kategorie': get_all_ids(parse_xml_file(os.path.join(XML_DIR, 'kategorien.xml')), 'kategorie'),
        'ort': get_all_ids(parse_xml_file(os.path.join(XML_DIR, 'orte.xml')), 'ort'),
        'werk': get_all_ids(parse_xml_file(os.path.join(XML_DIR, 'werke.xml')), 'werk'),
    }

    all_errors = []

    # Check all XML files in XML directory
    xml_files_to_check = []

    # Add core data files
    for filename in ['akteure.xml', 'kategorien.xml', 'orte.xml', 'werke.xml']:
        xml_files_to_check.append(os.path.join(XML_DIR, filename))

    # Add all files in beitraege/
    beitraege_dir = os.path.join(XML_DIR, 'beitraege')
    if os.path.exists(beitraege_dir):
        for filename in os.listdir(beitraege_dir):
            if filename.endswith('.xml'):
                xml_files_to_check.append(os.path.join(beitraege_dir, filename))

    # Add all files in stuecke/
    stuecke_dir = os.path.join(XML_DIR, 'stuecke')
    if os.path.exists(stuecke_dir):
        for filename in os.listdir(stuecke_dir):
            if filename.endswith('.xml'):
                xml_files_to_check.append(os.path.join(stuecke_dir, filename))

    # Check all collected files
    for filepath in xml_files_to_check:
        root = parse_xml_file(filepath)
        if root is not None:
            errors = check_references(root, reference_data, filepath)
            all_errors.extend(errors)

    all_errors.sort()

    if all_errors:
        print("Der Linter hat folgende Fehler gefunden:")
        for error in all_errors:
            print(error)
        with open('reference_check_errors.txt', 'w') as f:
            for error in all_errors:
                f.write(f"{error}\n")
        exit(1)  # Beenden mit Fehlercode, wenn Fehler gefunden wurden
    else:
        print("Keine Fehler gefunden.")

if __name__ == "__main__":
    main()
