#!/usr/bin/env python3

import os
import glob
import re
from lxml import etree

def int_to_roman(num):
    """Convert integer to roman numeral"""
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
        ]
    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
        ]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num

def normalize_text_for_url(text):
    """Normalize text for URL usage according to specifications"""
    if not text:
        return ""

    # Take text up to first punctuation mark if present
    match = re.search(r'[.,:;!?]', text)
    if match:
        text = text[:match.start()]

    # Lowercase
    text = text.lower()

    # Replace German umlauts
    text = text.replace('ä', 'ae').replace('ü', 'ue').replace('ö', 'oe').replace('ß', 'ss')

    # Replace spaces with hyphens
    text = re.sub(r'\s+', '-', text)

    # Remove all punctuation and special characters except hyphens
    text = re.sub(r'[^\w\-]', '', text)

    # Remove multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)

    # Remove leading/trailing hyphens
    text = text.strip('-')

    return text

def get_element_info(element):
    """Get debugging info for an element including line number and XML content"""
    line_num = getattr(element, 'sourceline', 'unknown')

    # Get the XML representation of the element
    xml_content = etree.tostring(element, encoding='unicode', pretty_print=True).strip()

    return f"Line {line_num}: {xml_content}"

def generate_id_for_beitrag(beitrag, existing_ids):
    """Generate unique ID for a beitrag element"""

    # Get all stueck elements - use local-name() to ignore namespace
    stuecke = beitrag.xpath('./*[local-name()="stueck"]')

    if not stuecke:
        element_info = get_element_info(beitrag)
        return None, f"No stueck elements found in beitrag:\n{element_info}"

    base_id = ""

    # Determine base ID based on number of stueck elements
    if len(stuecke) == 1:
        stueck = stuecke[0]
        when = stueck.get('when')
        nr = stueck.get('nr')
        beilage = stueck.get('beilage')

        if not when or not nr:
            return None, f"Missing when ({when}) or nr ({nr}) in stueck"

        base_id = f"{when}-{nr}-"
        if beilage:
            base_id += "beil-"
    else:
        # Multiple stueck elements - use year from first one
        first_stueck = stuecke[0]
        when = first_stueck.get('when')
        if not when:
            return None, "Missing when attribute in first stueck"
        base_id = f"{when}-"

    # Check for akteur with ref attribute - prefer ones without kat attribute first
    akteur_no_kat = beitrag.xpath('./*[local-name()="akteur"][@ref and not(@kat)]')
    akteur_with_kat = beitrag.xpath('./*[local-name()="akteur"][@ref and @kat]')

    akteur_used_as_identifier = False

    if akteur_no_kat:
        # Include all akteur without kat (multiple authors)
        akteur_refs = [akteur.get('ref') for akteur in akteur_no_kat]
        base_id += f"{'-'.join(akteur_refs)}-"

    # Try to find additional identifier in order of priority
    additional_part = ""

    # 1. Try title
    titel = beitrag.xpath('./*[local-name()="titel"]')
    if titel and titel[0].text:
        additional_part = normalize_text_for_url(titel[0].text)

    # 2. Try incipit if no title
    if not additional_part:
        incipit = beitrag.xpath('./*[local-name()="incipit"]')
        if incipit and incipit[0].text:
            additional_part = normalize_text_for_url(incipit[0].text)

    # 3. Try kategorie ref if no title/incipit
    if not additional_part:
        kategorie = beitrag.xpath('./*[local-name()="kategorie"][@ref]')
        if kategorie:
            additional_part = kategorie[0].get('ref')

    # 4. Try werk if no title/incipit/kategorie (ignore provinienz)
    if not additional_part:
        werk = beitrag.xpath('./*[local-name()="werk"][@ref and @kat != "provinienz"]')
        if not werk:
            # If no werk with kat != provinienz, try werk without kat
            werk = beitrag.xpath('./*[local-name()="werk"][@ref and not(@kat)]')

        if werk:
            kat = werk[0].get('kat')
            ref = werk[0].get('ref')
            if kat:
                additional_part = f"{kat}-{ref}"
            else:
                additional_part = ref

    # 5. Try akteur with kat if no title/incipit/kategorie/werk
    if not additional_part and akteur_with_kat:
        akteur_ref = akteur_with_kat[0].get('ref')
        akteur_kat = akteur_with_kat[0].get('kat')
        additional_part = f"{akteur_ref}-{akteur_kat}"
        akteur_used_as_identifier = True

    # 6. Try anmerkung if all else fails
    if not additional_part:
        anmerkung = beitrag.xpath('./*[local-name()="anmerkung"]')
        if anmerkung and anmerkung[0].text:
            additional_part = normalize_text_for_url(anmerkung[0].text)

    # 7. Check for nested beitrag tag and append its ref+kat (only if no title/incipit was found)
    nested_beitrag = beitrag.xpath('./*[local-name()="beitrag"][@ref and @kat]')
    if nested_beitrag and additional_part:
        # Only append if we don't already have title/incipit
        titel = beitrag.xpath('./*[local-name()="titel"]')
        incipit = beitrag.xpath('./*[local-name()="incipit"]')

        # If we have title or incipit, don't append nested beitrag
        if not (titel and titel[0].text) and not (incipit and incipit[0].text):
            nested_ref = nested_beitrag[0].get('ref')
            nested_kat = nested_beitrag[0].get('kat')
            additional_part += f"-{nested_ref}-{nested_kat}"
    elif nested_beitrag and not additional_part:
        # Use nested beitrag as identifier if nothing else was found
        nested_ref = nested_beitrag[0].get('ref')
        nested_kat = nested_beitrag[0].get('kat')
        additional_part = f"{nested_ref}-{nested_kat}"

    if not additional_part:
        # Log failure with element info
        element_info = get_element_info(beitrag)
        return None, f"No identifier found for beitrag:\n{element_info}"

    # Construct final ID
    final_id = base_id + additional_part

    # Ensure uniqueness with roman numerals
    original_id = final_id
    counter = 2  # Start with II for first duplicate
    while final_id in existing_ids:
        final_id = f"{original_id}-{int_to_roman(counter)}"
        counter += 1

    return final_id, None

def process_xml_file(file_path, existing_ids):
    """Process a single XML file and add IDs to beitrag elements"""

    print(f"Processing {file_path}...")

    # Parse with lxml preserving whitespace, comments, and line numbers
    parser = etree.XMLParser(strip_cdata=False, remove_blank_text=False, remove_comments=False)
    tree = etree.parse(file_path, parser)
    root = tree.getroot()

    # Find all beitrag elements that are direct children of beitraege and don't have an id attribute
    beitraege = root.xpath('./*[local-name()="beitrag"][not(@id)]')

    modified = False
    errors = []

    for beitrag in beitraege:
        generated_id, error = generate_id_for_beitrag(beitrag, existing_ids)

        if generated_id:
            beitrag.set('id', generated_id)
            existing_ids.add(generated_id)
            modified = True
            print(f"  Added ID: {generated_id}")
        else:
            errors.append(error)
            print(f"  ERROR: {error}")

    # Save the file if modified
    if modified:
        # Write back with original formatting preserved
        tree.write(file_path, encoding='utf-8', xml_declaration=True, pretty_print=False)
        print(f"  Updated {file_path}")

    return len(beitraege), len([e for e in errors if e]), errors

def main():
    """Main function to process all XML files"""

    # Change to project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '..', '..')
    os.chdir(project_root)

    # Find all beitraege XML files
    xml_files = glob.glob('XML/beitraege/*.xml')

    if not xml_files:
        print("No XML files found in XML/beitraege/")
        return

    # First pass: collect all existing IDs to ensure uniqueness
    existing_ids = set()

    print("Collecting existing IDs...")
    for file_path in xml_files:
        try:
            parser = etree.XMLParser(strip_cdata=False, remove_blank_text=False, remove_comments=False)
            tree = etree.parse(file_path, parser)
            root = tree.getroot()

            # Find all existing IDs from direct children of beitraege
            existing_beitraege = root.xpath('./*[local-name()="beitrag"][@id]')
            for beitrag in existing_beitraege:
                existing_ids.add(beitrag.get('id'))
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    print(f"Found {len(existing_ids)} existing IDs")

    # Second pass: generate IDs for beitraege without IDs
    total_processed = 0
    total_errors = 0
    all_errors = []

    for file_path in xml_files:
        try:
            processed, errors, error_list = process_xml_file(file_path, existing_ids)
            total_processed += processed
            total_errors += errors
            all_errors.extend(error_list)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            total_errors += 1

    print(f"\nSummary:")
    print(f"Total beitraege processed: {total_processed}")
    print(f"Total errors: {total_errors}")

    if all_errors:
        print(f"\nErrors encountered:")
        for error in all_errors:
            print(f"  - {error}")

if __name__ == "__main__":
    main()