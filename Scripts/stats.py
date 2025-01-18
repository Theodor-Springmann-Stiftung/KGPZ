import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
import os

def parse_categories(file_paths):
    namespace = {'kgpz': 'https://www.koenigsberger-zeitungen.de'}
    stats = Counter()
    usage = defaultdict(set)  # Track where each category is used
    missing_kat_counts = Counter({"werk": 0, "akteur": 0, "ort": 0})  # Track missing 'kat'

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
            else:
                missing_kat_counts["werk"] += 1

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
            else:
                missing_kat_counts["akteur"] += 1

        # Count categories from <ort>
        for ort in root.findall(".//kgpz:ort", namespace):
            if 'kat' in ort.attrib:
                stats[ort.attrib['kat']] += 1
                usage[ort.attrib['kat']].add("ort")
            else:
                missing_kat_counts["ort"] += 1

        # Count categories from <issue>
        for issue in root.findall(".//kgpz:issue", namespace):
            if 'kat' in issue.attrib:
                stats[issue.attrib['kat']] += 1
                usage[issue.attrib['kat']].add("issue")

    return stats, usage, missing_kat_counts

def write_stats(stats, usage, missing_kat_counts, output_file):
    sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)

    with open(output_file, 'w') as f:
        f.write("Category Usage:\n")
        for category, count in sorted_stats:
            usages = ", ".join(sorted(usage[category]))
            f.write(f"{category}: {count} (used in: {usages})\n")

        f.write("\nMissing 'kat' Counts:\n")
        for tag, count in missing_kat_counts.items():
            f.write(f"<{tag}> missing 'kat': {count}\n")

def main():
    # Define file paths
    input_dir = os.getenv("INPUT_DIR", "./XML/beitraege")
    output_file = os.getenv("OUTPUT_FILE", "./stats.txt")

    # Get all XML files in the input directory
    file_paths = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.xml')]

    stats, usage, missing_kat_counts = parse_categories(file_paths)
    write_stats(stats, usage, missing_kat_counts, output_file)

if __name__ == "__main__":
    main()
