
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
        # Use a parser that preserves comments and whitespace as much as possible
        parser = etree.XMLParser(remove_blank_text=False, remove_comments=False, strip_cdata=False)
        tree = etree.parse(filepath, parser)
        root = tree.getroot()

        # Default namespace from the document, if it exists
        ns = {'kgpz': root.nsmap.get(None)} if root.nsmap.get(None) else {}

        # Group stueck elements by (when, nr, von)
        stueck_groups = defaultdict(list)

        # XPath to find all beitrag elements
        beitraege = root.xpath('//beitrag')

        for beitrag in beitraege:
            stueck = beitrag.find('stueck')
            if stueck is not None:
                when = stueck.get('when')
                nr = stueck.get('nr')
                von = stueck.get('von')
                bis = stueck.get('bis')

                # Ambiguity arises for single-page entries.
                # A multi-page entry is one where `bis` is present and `bis` != `von`.
                is_multi_page = bis is not None and bis != von

                if von and not is_multi_page:
                    key = (when, nr, von)
                    stueck_groups[key].append(stueck)

        # Add order attribute where there is ambiguity
        modified = False
        for key, stuecks in stueck_groups.items():
            if len(stuecks) > 1:
                modified = True
                for i, stueck in enumerate(stuecks):
                    stueck.set('order', str(i + 1))

        # Write back to the file only if changes were made
        if modified:
            # Get the original XML declaration details
            xml_declaration = tree.docinfo.xml_version
            encoding = tree.docinfo.encoding

            tree.write(filepath,
                       encoding=encoding,
                       xml_declaration=True,
                       pretty_print=False)
            print(f"Updated order attributes in: {filepath}")
        else:
            print(f"No changes needed for: {filepath}")

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
