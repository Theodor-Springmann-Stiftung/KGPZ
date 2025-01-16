import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
import os

def parse_categories(file_paths):
    namespace = {'kgpz': 'https://www.koenigsberger-zeitungen.de'}
    stats = Counter()
    usage = defaultdict(set)  # Track where each category is used

    for file_path in file_paths:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Count categories from <kategorie>
        for category in root.findall(".//kgpz:kategorie", namespace):
            stats[category.get('ref')] += 1
            usage[category.get('ref')].add("kategorie")

        # Count categories from <werk>
        for werk in root.findall(".//kgpz:werk", namespace):
            if 'kat' in werk.attrib:
                stats[werk.attrib['kat']] += 1
                usage[werk.attrib['kat']].add("werk")

        # Count categories from <beitrag>
        for beitrag in root.findall(".//kgpz:beitrag", namespace):
            if 'kat' in beitrag.attrib:
                stats[beitrag.get('kat')] += 1
                usage[beitrag.get('kat')].add("beitrag")

        # Count categories from <akteur>
        for akteur in root.findall(".//kgpz:akteur", namespace):
            if 'kat' in akteur.attrib:
                stats[akteur.attrib['kat']] += 1
                usage[akteur.attrib['kat']].add("akteur")

        # Count categories from <ort>
        for ort in root.findall(".//kgpz:ort", namespace):
            if 'kat' in ort.attrib:
                stats[ort.attrib['kat']] += 1
                usage[ort.attrib['kat']].add("ort")

        # Count categories from <issue>
        for issue in root.findall(".//kgpz:issue", namespace):
            if 'kat' in issue.attrib:
                stats[issue.attrib['kat']] += 1
                usage[issue.attrib['kat']].add("issue")

    return stats, usage

def write_stats(stats, usage, output_file):
    sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)

    with open(output_file, 'w') as f:
        for category, count in sorted_stats:
            usages = ", ".join(sorted(usage[category]))
            f.write(f"{category}: {count} (used in: {usages})\n")

def main():
    # Define file paths
    input_dir = os.getenv("INPUT_DIR", "./XML/beitraege")
    output_file = os.getenv("OUTPUT_FILE", "./stats.txt")

    # Get all XML files in the input directory
    file_paths = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.xml')]

    stats, usage = parse_categories(file_paths)
    write_stats(stats, usage, output_file)

if __name__ == "__main__":
    main()
