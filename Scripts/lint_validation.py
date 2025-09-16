import os
from lxml import etree
from collections import defaultdict

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
XML_DIR = os.path.join(REPO_ROOT, 'XML')

def validate_stueck_constraints(tree):
    """Performs all custom validation checks for <stueck> elements."""
    errors = []
    root = tree.getroot()
    ns = {'kgpz': 'https://www.koenigsberger-zeitungen.de'}

    # --- Rule 1: Check for conditional 'order' attribute on single-page entries ---
    stuecke_without_bis = root.xpath('//kgpz:beitrag/kgpz:stueck[not(@bis)]', namespaces=ns)
    groups_single_page = defaultdict(list)
    for stueck in stuecke_without_bis:
        key = (stueck.get('when'), stueck.get('nr'), stueck.get('von'))
        groups_single_page[key].append(stueck)

    for key, stuecks in groups_single_page.items():
        if len(stuecks) > 1:
            for stueck in stuecks:
                if stueck.get('order') is None:
                    error_msg = (
                        f"Custom Validation Error: <stueck> on line {stueck.sourceline} is part of an ambiguous group "
                        f"(when='{key[0]}', nr='{key[1]}', von='{key[2]}') but is missing the 'order' attribute."
                    )
                    errors.append(error_msg)

    # --- Rule 2: Check for conditional 'order' on ambiguous multi-page entries ---
    stuecke_with_bis = root.xpath('//kgpz:beitrag/kgpz:stueck[@bis]', namespaces=ns)
    groups_multi_page = defaultdict(list)
    for stueck in stuecke_with_bis:
        key = (stueck.get('when'), stueck.get('nr'), stueck.get('von'), stueck.get('bis'))
        groups_multi_page[key].append(stueck)

    for key, stuecks in groups_multi_page.items():
        if len(stuecks) > 1:
            for stueck in stuecks:
                if stueck.get('order') is None:
                    error_msg = (
                        f"Custom Validation Error: <stueck> on line {stueck.sourceline} is part of an ambiguous multi-page group "
                        f"(when='{key[0]}', nr='{key[1]}', von='{key[2]}', bis='{key[3]}') but is missing the 'order' attribute."
                    )
                    errors.append(error_msg)
            
    return errors

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
                print(f"XSD Validation successful: {xml_file}")

                # Perform custom validation after XSD check
                custom_errors = validate_stueck_constraints(tree)
                if custom_errors:
                    errors.extend(custom_errors)
                else:
                    print(f"Custom Validation successful: {xml_file}")

            else:
                errors.append(f"Schema file not found: {xsd_path} for {xml_file}")
        else:
            errors.append(f"No schemaLocation found in {xml_file}")
    
    except etree.DocumentInvalid as e:
        errors.append(f"Validation error in {xml_file}:")
        for error in e.error_log:
            errors.append(f"  Line {error.line}, Column {error.column}: {error.message}")
    except etree.XMLSyntaxError as e:
        errors.append(f"XML syntax error in {xml_file}:")
        errors.append(f"  Line {e.lineno}, Column {e.offset}: {e.msg}")
    except Exception as e:
        errors.append(f"Error processing {xml_file}: {str(e)}")
    
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
        print("Validation failed. Please correct the following errors:")
        with open('schema_validation_errors.txt', 'w') as f:
            for error in all_errors:
                print(error)
                f.write(f"{error}\n")
        exit(1)
    else:
        print("All XML files were successfully validated.")

if __name__ == "__main__":
    main()

