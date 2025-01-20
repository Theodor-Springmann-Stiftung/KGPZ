import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
import os

def parse_beitraege(file_paths):
    namespace = {'kgpz': 'https://www.koenigsberger-zeitungen.de'}
    stats = Counter()
    usage = defaultdict(set)  # Track where each category is used
    missing_kat_counts = Counter({"werk": 0, "akteur": 0, "ort": 0, "beitr": 0})  # Track missing 'kat'
    multiple_categories = 0  # Count of beitraege with more than one category
    category_combinations = Counter()  # Track category combinations

    for file_path in file_paths:
        print(f"Processing file: {file_path}")  # Debugging: Log file being processed
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Iterate over direct children <beitrag> of <beitraege>
            for beitrag in root.findall("./kgpz:beitrag", namespace):
                print(f"Processing <beitrag> in file: {file_path}")  # Debugging: Log each <beitrag>

                # Collect categories for this beitrag
                categories = set()

                # Process <kategorie> elements within each <beitrag>
                for kategorie in beitrag.findall("kgpz:kategorie", namespace):
                    if 'ref' in kategorie.attrib:
                        stats[kategorie.attrib['ref']] += 1
                        usage[kategorie.attrib['ref']].add("kategorie")
                        if kategorie.attrib['ref'] != "provinienz":
                            categories.add(kategorie.attrib['ref'])

                # Process <werk> elements within each <beitrag>
                for werk in beitrag.findall("kgpz:werk", namespace):
                    if 'kat' in werk.attrib:
                        stats[werk.attrib['kat']] += 1
                        usage[werk.attrib['kat']].add("werk")
                        if werk.attrib['kat'] != "provinienz":
                            categories.add(werk.attrib['kat'])
                    else:
                        missing_kat_counts["werk"] += 1

                # Process <akteur> elements within each <beitrag>
                for akteur in beitrag.findall("kgpz:akteur", namespace):
                    if 'kat' in akteur.attrib:
                        stats[akteur.attrib['kat']] += 1
                        usage[akteur.attrib['kat']].add("akteur")
                        if akteur.attrib['kat'] != "provinienz":
                            categories.add(akteur.attrib['kat'])
                    else:
                        missing_kat_counts["akteur"] += 1

                # Process <ort> elements within each <beitrag>
                for ort in beitrag.findall("kgpz:ort", namespace):
                    if 'kat' in ort.attrib:
                        stats[ort.attrib['kat']] += 1
                        usage[ort.attrib['kat']].add("ort")
                        if ort.attrib['kat'] != "provinienz":
                            categories.add(ort.attrib['kat'])
                    else:
                        missing_kat_counts["ort"] += 1

                # Process <beitrag> elements within each <beitrag>
                for beitr in beitrag.findall("kgpz:beitrag", namespace):
                    if 'kat' in beitr.attrib:
                        stats[beitr.attrib['kat']] += 1
                        usage[beitr.attrib['kat']].add("beitr")
                        if beitr.attrib['kat'] != "provinienz":
                            categories.add(beitr.attrib['kat'])
                    else:
                        missing_kat_counts["beitr"] += 1

                # Check for multiple categories and track combinations
                if len(categories) > 1:
                    multiple_categories += 1
                    category_combinations[frozenset(categories)] += 1

        except ET.ParseError as e:
            print(f"Warning: Failed to parse {file_path}: {e}")  # Error handling: Skip malformed XML

    return stats, usage, missing_kat_counts, multiple_categories, category_combinations

def write_stats(stats, usage, missing_kat_counts, multiple_categories, category_combinations, output_file):
    sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)

    with open(output_file, 'w') as f:
        f.write("Category Usage:\n")
        for category, count in sorted_stats:
            usages = ", ".join(sorted(usage[category]))
            f.write(f"{category}: {count} (used in: {usages})\n")

        f.write("\nMissing 'kat' Counts:\n")
        for tag, count in missing_kat_counts.items():
            f.write(f"<{tag}> missing 'kat': {count}\n")

        f.write("\nBeitraege with Multiple Categories:\n")
        f.write(f"Total: {multiple_categories}\n")

        f.write("\nCategory Combinations (Ordered by Most Used):\n")
        sorted_combinations = sorted(category_combinations.items(), key=lambda x: x[1], reverse=True)
        for combination, count in sorted_combinations:
            combination_str = ", ".join(sorted(combination))
            f.write(f"{combination_str}: {count}\n")

def main():
    # Define file paths
    input_dir = os.getenv("INPUT_DIR", "./XML/beitraege")
    output_file = os.getenv("OUTPUT_FILE", "./stats.txt")

    # Get all XML files in the input directory
    file_paths = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.xml')]

    stats, usage, missing_kat_counts, multiple_categories, category_combinations = parse_beitraege(file_paths)
    write_stats(stats, usage, missing_kat_counts, multiple_categories, category_combinations, output_file)

if __name__ == "__main__":
    main()
