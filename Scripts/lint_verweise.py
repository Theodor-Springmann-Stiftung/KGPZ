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
        print(f"Error parsing {filepath}: {e}")
        return None

def get_all_ids(root, tag):
    return set(elem.get('id') for elem in root.xpath(f'.//kgpz:{tag}', namespaces=NAMESPACE))

def check_references(beitrag_root, reference_data, filepath):
    errors = []
    relative_path = os.path.relpath(filepath, REPO_ROOT)
    for ref_type, ref_tag in [('akteur', 'akteur'), ('kategorie', 'kategorie'), 
                              ('ort', 'ort'), ('werk', 'werk')]:
        for ref in beitrag_root.xpath(f'//kgpz:{ref_tag}', namespaces=NAMESPACE):
            ref_id = ref.get('ref')
            if ref_id not in reference_data[ref_type]:
                line_number = ref.sourceline
                errors.append(f"{relative_path}, Line {line_number}: INVALID REFERENCE ({ref_type}:{ref_id})")
    return errors

def main():
    reference_data = {
        'akteur': get_all_ids(parse_xml_file(os.path.join(XML_DIR, 'akteure.xml')), 'akteur'),
        'kategorie': get_all_ids(parse_xml_file(os.path.join(XML_DIR, 'kategorien.xml')), 'kategorie'),
        'ort': get_all_ids(parse_xml_file(os.path.join(XML_DIR, 'orte.xml')), 'ort'),
        'werk': get_all_ids(parse_xml_file(os.path.join(XML_DIR, 'werke.xml')), 'werk'),
    }

    all_errors = []

    beitraege_dir = os.path.join(XML_DIR, 'beitraege')
    for filename in os.listdir(beitraege_dir):
        if filename.endswith('-beitraege.xml'):
            filepath = os.path.join(beitraege_dir, filename)
            beitrag_root = parse_xml_file(filepath)
            if beitrag_root is not None:
                errors = check_references(beitrag_root, reference_data, filepath)
                all_errors.extend(errors)

    all_errors.sort()

    if all_errors:
        print("Linter found the following errors:")
        for error in all_errors:
            print(error)
        exit(1)  # Exit with error code if there are any errors
    else:
        print("No errors found.")

if __name__ == "__main__":
    main()
