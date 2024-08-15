import os
import re
import sys
from datetime import datetime, timedelta
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom

def get_files(directory):
    pattern = re.compile(r'(\d{4})-(\d+)(b\d?)?-(\d+)\.jpg')
    files = {}
    year = None
    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            file_year, stueck, beilage_info, page = match.groups()
            file_year = int(file_year)
            stueck = int(stueck)
            page = int(page)
            if year is None:
                year = file_year
            elif year != file_year:
                raise ValueError(f"Inconsistent years found: {year} and {file_year}")
            if stueck not in files:
                files[stueck] = {'main': [], 'beilage': []}
            if beilage_info:
                beilage_num = int(beilage_info[1:] or '1')
                files[stueck]['beilage'].append((beilage_num, page))
            else:
                files[stueck]['main'].append(page)
    return files, year

def calculate_date(year, stueck_number):
    base_date = datetime(year, 1, 1)  # Start from January 1st of the given year
    while base_date.weekday() != 4:  # Find the first Friday
        base_date += timedelta(days=1)
    days_to_add = (stueck_number - 1) * 3 + ((stueck_number - 1) // 2) * 1
    return base_date + timedelta(days=days_to_add)

def create_xml(files, year):
    root = Element('stuecke')
    root.set('xmlns', 'https://www.koenigsberger-zeitungen.de')
    root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    root.set('xsi:schemaLocation', 'https://www.koenigsberger-zeitungen.de ../../XSD/KGPZ.xsd')

    for stueck, pages in sorted(files.items()):
        stueck_elem = SubElement(root, 'stueck')
        
        nummer = SubElement(stueck_elem, 'nummer')
        nummer.text = str(stueck)
        
        date = calculate_date(year, stueck)
        datum = SubElement(stueck_elem, 'datum')
        datum.set('when', date.strftime('%Y-%m-%d'))
        
        if pages['main']:
            von = SubElement(stueck_elem, 'von')
            von.text = str(min(pages['main']))
            
            bis = SubElement(stueck_elem, 'bis')
            bis.text = str(max(pages['main']))

        if pages['beilage']:
            beilage_pages = sorted(pages['beilage'])
            current_beilage = [beilage_pages[0]]
            current_beilage_num = beilage_pages[0][0]
            
            for beilage_num, page in beilage_pages[1:]:
                if beilage_num == current_beilage_num and page == current_beilage[-1][1] + 1:
                    current_beilage.append((beilage_num, page))
                else:
                    beilage_elem = SubElement(stueck_elem, 'beilage')
                    beilage_elem.set('nummer', str(current_beilage_num))
                    beilage_von = SubElement(beilage_elem, 'von')
                    beilage_von.text = str(min(page for _, page in current_beilage))
                    beilage_bis = SubElement(beilage_elem, 'bis')
                    beilage_bis.text = str(max(page for _, page in current_beilage))
                    current_beilage = [(beilage_num, page)]
                    current_beilage_num = beilage_num
            
            # Add the last beilage
            beilage_elem = SubElement(stueck_elem, 'beilage')
            beilage_elem.set('nummer', str(current_beilage_num))
            beilage_von = SubElement(beilage_elem, 'von')
            beilage_von.text = str(min(page for _, page in current_beilage))
            beilage_bis = SubElement(beilage_elem, 'bis')
            beilage_bis.text = str(max(page for _, page in current_beilage))

    return root

def pretty_print(elem):
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)

    directory = sys.argv[1]
    files, year = get_files(directory)
    xml_root = create_xml(files, year)
    
    output_filename = f'{year}-stuecke.xml'
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(pretty_print(xml_root))

    print(f"XML file '{output_filename}' has been generated.")
