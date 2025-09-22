
import os
from lxml import etree
from collections import defaultdict
import sys

def process_xml_file(filepath):
    """
    Processes a single XML file to add 'order' attributes to <stueck> elements where necessary.

    Args:
        filepath (str): The path to the XML file.
    """
    try:
        # Use lxml to parse and find nodes, but not for writing.
        parser = etree.XMLParser(remove_blank_text=False, remove_comments=False, strip_cdata=False)
        tree = etree.parse(filepath, parser)
        root = tree.getroot()

        ns = {'kgpz': 'https://www.koenigsberger-zeitungen.de'}
        stueck_groups = defaultdict(list)
        beitraege = root.xpath('//kgpz:beitrag', namespaces=ns)

        for beitrag in beitraege:
            stueck = beitrag.find('kgpz:stueck', namespaces=ns)
            if stueck is not None:
                when, nr, von, bis = stueck.get('when'), stueck.get('nr'), stueck.get('von'), stueck.get('bis')
                is_multi_page = bis is not None and bis != von
                if von and not is_multi_page:
                    stueck_groups[(when, nr, von)].append(stueck)

        stuecks_to_modify_groups = [s for s in stueck_groups.values() if len(s) > 1]

        if not stuecks_to_modify_groups:
            print(f"No ambiguous order found in: {filepath}")
            return

        print(f"Found ambiguous stuecke in {filepath}. The following groups will be updated:")
        for group in stuecks_to_modify_groups:
            print("--- Group to be ordered ---")
            for stueck in group:
                print(etree.tostring(stueck, pretty_print=True, encoding='unicode').strip())

        # Read the file content for surgical modification
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Apply changes to the lines list
        for group in stuecks_to_modify_groups:
            for i, stueck in enumerate(group):
                order = i + 1
                lineno = stueck.sourceline - 1
                line = lines[lineno]

                # Find insertion point (before '/>' or '>')
                insertion_point = line.rfind('/>')
                if insertion_point == -1:
                    insertion_point = line.rfind('>')
                
                if insertion_point != -1:
                    lines[lineno] = line[:insertion_point] + f' order="{order}"' + line[insertion_point:]
                else:
                    print(f"Warning: Could not find closing tag on line {lineno + 1} in {filepath}. Skipping.", file=sys.stderr)

        # Write the modified lines back to the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        print(f"Finished updating order attributes in: {filepath}\n")

    except etree.XMLSyntaxError as e:
        print(f"Error parsing {filepath}: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred with {filepath}: {e}", file=sys.stderr)



def main():
    """
    Main function to find and process all relevant XML files.
    """
    # The script is in scripts/orderfix, so we go up two levels
    # to the project root, then into XML/beitraege.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    beitraege_dir = os.path.abspath(os.path.join(script_dir, '../../XML/beitraege'))

    if not os.path.isdir(beitraege_dir):
        print(f"Error: Directory not found at {beitraege_dir}", file=sys.stderr)
        return

    print(f"Scanning for XML files in: {beitraege_dir}")
    for filename in os.listdir(beitraege_dir):
        if filename.endswith('.xml'):
            filepath = os.path.join(beitraege_dir, filename)
            process_xml_file(filepath)
    print("Processing complete.")

if __name__ == "__main__":
    main()
