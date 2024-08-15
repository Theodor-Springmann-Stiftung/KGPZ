import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path('XML')
BEITRAEGE_DIR = BASE_DIR / 'beitraege'
OUTPUT_DIR = Path('output')
NAMESPACES = {
    'kgpz': 'https://www.koenigsberger-zeitungen.de',
    'xsd': 'http://www.w3.org/2001/XMLSchema'
}

def parse_xml_file(file_path):
    return ET.parse(file_path).getroot()

def load_werke():
    werke_root = parse_xml_file(BASE_DIR / 'werke.xml')
    return {werk.attrib['id']: werk.find('kgpz:zitation', NAMESPACES).text
            for werk in werke_root.findall('.//kgpz:werk', NAMESPACES)}

def load_akteure():
    akteure_root = parse_xml_file(BASE_DIR / 'akteure.xml')
    return {akteur.attrib['id']: akteur.find('kgpz:name', NAMESPACES).text
            for akteur in akteure_root.findall('.//kgpz:akteur', NAMESPACES)}

def load_orte():
    orte_root = parse_xml_file(BASE_DIR / 'orte.xml')
    return {ort.attrib['id']: ort.find('kgpz:name', NAMESPACES).text
            for ort in orte_root.findall('.//kgpz:ort', NAMESPACES)}

def load_kategorien():
    kategorien_root = parse_xml_file(BASE_DIR / 'kategorien.xml')
    return {kategorie.attrib['id']: kategorie.find('kgpz:name', NAMESPACES).text
            for kategorie in kategorien_root.findall('.//kgpz:kategorie', NAMESPACES)}

def load_reference_types():
    schema_root = parse_xml_file(BASE_DIR.parent / 'XSD' / 'common.xsd')
    
    def get_types(element_name):
        complex_type = schema_root.find(f".//xsd:complexType[@name='{element_name}ref']", NAMESPACES)
        simple_type = complex_type.find(".//xsd:simpleType", NAMESPACES)
        return [e.attrib['value'] for e in simple_type.findall(".//xsd:enumeration", NAMESPACES)]

    def get_default(element_name):
        complex_type = schema_root.find(f".//xsd:complexType[@name='{element_name}ref']", NAMESPACES)
        attribute = complex_type.find(".//xsd:attribute[@name='kat']", NAMESPACES)
        return attribute.attrib.get('default', '')

    return {
        'werk': {'types': get_types('werk'), 'default': get_default('werk')},
        'akteur': {'types': get_types('akteur'), 'default': get_default('akteur')},
        'ort': {'types': get_types('ort'), 'default': get_default('ort')}
    }

WERKE = load_werke()
AKTEURE = load_akteure()
ORTE = load_orte()
KATEGORIEN = load_kategorien()
REFERENCE_TYPES = load_reference_types()

def process_stueck_or_beilage(element, current_year, current_issue):
    tag_name = element.tag.split('}')[-1]
    datum = element.attrib.get('datum', '')
    nr = element.attrib.get('nr', '')
    year = datum.split('-')[0]
    
    if tag_name == 'stueck':
        von = element.attrib.get('von', '')
        bis = element.attrib.get('bis', '')
        pages = f"{von}" if von == bis or not bis else f"{von}-{bis}"
        
        if year == current_year and nr == current_issue:
            return f"<p class='stueck'>{pages}</p>", (year, nr, 0)
        else:
            return f"<p class='stueck'>Ausgabe {nr} ({datum}), {pages}</p>", (year, nr, 0)
    else:
        beilage_nr = element.attrib.get('beilage', '')
        if year == current_year and nr == current_issue:
            return f"<p class='beilage'>Beilage {beilage_nr}</p>", (year, nr, 1)
        else:
            return f"<p class='beilage'>Beilage {beilage_nr} zu Ausgabe {nr} ({datum})</p>", (year, nr, 1)

def process_kategorie(element):
    kategorie_id = element.attrib.get('ref', '')
    kategorie_name = KATEGORIEN.get(kategorie_id, kategorie_id)
    return f'<span class="pill"><strong>{kategorie_name}</strong></span>'

def process_titel_or_incipit(element):
    return f'<p class="titel-incipit">{element.text}</p>'

def process_reference(element, ref_type):
    ref_id = element.attrib.get('ref', '')
    content = WERKE.get(ref_id, '') if ref_type == 'werk' else AKTEURE.get(ref_id, '') if ref_type == 'akteur' else ORTE.get(ref_id, '')
    if not content:
        content = f"{ref_type.capitalize()} nicht gefunden: {ref_id}"
    
    kat_id = element.attrib.get('kat', REFERENCE_TYPES[ref_type]['default'])
    kat_name = KATEGORIEN.get(kat_id, kat_id)
    return f'<p class="{ref_type}"><span class="pill"><strong>{kat_name}</strong></span> {content}</p>'

def process_anmerkung_or_vermerk(element):
    return f'<p class="{element.tag.split("}")[-1]}">{element.text}</p>'

def process_beitrag(beitrag, current_year, current_issue):
    content = f'<div class="beitrag" id="{beitrag.attrib.get("id", "")}">\n'
    
    stueck_infos = []
    for element in beitrag:
        tag = element.tag.split('}')[-1]
        if tag in ['stueck', 'beilage']:
            stueck_html, stueck_info = process_stueck_or_beilage(element, current_year, current_issue)
            content += stueck_html
            stueck_infos.append(stueck_info)
        elif tag == 'kategorie':
            content += process_kategorie(element)
        elif tag in ['titel', 'incipit']:
            content += process_titel_or_incipit(element)
        elif tag in ['werk', 'akteur', 'ort']:
            content += process_reference(element, tag)
        elif tag in ['anmerkung', 'vermerk']:
            content += process_anmerkung_or_vermerk(element)
    
    content += '</div>\n'
    return content, stueck_infos

def create_html_content(root):
    beitraege_by_year_issue = defaultdict(lambda: defaultdict(list))
    
    for beitrag in root.findall('.//kgpz:beitrag', NAMESPACES):
        for stueck in beitrag.findall('./kgpz:stueck', NAMESPACES) + beitrag.findall('./kgpz:beilage', NAMESPACES):
            year = stueck.attrib.get('datum', '').split('-')[0]
            issue = stueck.attrib.get('nr', '')
            content, _ = process_beitrag(beitrag, year, issue)
            beitraege_by_year_issue[year][issue].append(content)
    
    def sort_key(x):
        try:
            return (0, int(x))
        except ValueError:
            return (1, x)

    content = ""
    for year in sorted(beitraege_by_year_issue.keys()):
        content += f'<h2>Jahr {year}</h2>\n'
        for issue in sorted(beitraege_by_year_issue[year].keys(), key=sort_key):
            content += f'<h3>Ausgabe {issue}</h3>\n'
            content += ''.join(beitraege_by_year_issue[year][issue])
    
    return content

def generate_html(content):
    return f'''
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KGPZ Beiträge</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }}
        .beitrag {{ margin-bottom: 20px; border: 1px solid #ccc; padding: 10px; }}
        h2 {{ color: #333; margin-top: 30px; }}
        h3 {{ color: #666; margin-top: 20px; }}
        p {{ margin: 5px 0; }}
        .titel-incipit {{ font-size: 1.1em; font-weight: bold; margin-top: 10px; margin-bottom: 10px; }}
        .anmerkung, .vermerk {{ background-color: #f0f0f0; padding: 5px; margin-top: 10px; }}
        .werk, .akteur, .ort {{ background-color: #f9f9f9; padding: 5px; }}
        .pill {{
            display: inline-block;
            padding: 2px 8px;
            background-color: #e0e0e0;
            border-radius: 12px;
            font-size: 0.8em;
            margin-right: 5px;
        }}
        .pill strong {{ font-weight: bold; }}
        .stueck, .beilage {{ font-weight: bold; color: #444; }}
        .beilage {{ color: #666; }}
    </style>
</head>
<body>
    {content}
</body>
</html>
'''

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    all_content = ''
    
    for xml_file in sorted(BEITRAEGE_DIR.glob('*.xml')):
        root = parse_xml_file(xml_file)
        all_content += create_html_content(root)
    
    html_output = generate_html(all_content)
    
    with open(OUTPUT_DIR / 'kgpz_beitraege.html', 'w', encoding='utf-8') as f:
        f.write(html_output)

if __name__ == '__main__':
    main()
