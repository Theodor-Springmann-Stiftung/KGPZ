# Project Overview

This project is dedicated to the digitization and analysis of the "Königsbergische Gelehrte und Politische Zeitungen" (Königsberg Scholar and Political Newspapers). It involves the structured recording of newspaper articles (`Beiträge`) in XML format, along with associated metadata such as categories, referenced works, people, and places.

The core of the project is a collection of XML files that represent the newspaper's content. These files are validated against XSD schemas to ensure data consistency. Python scripts are used for various data processing tasks, including statistical analysis and the generation of an HTML representation of the articles.

## Key Technologies

*   **XML:** The primary format for storing the newspaper data.
*   **XSD:** Used to define and validate the structure of the XML files.
*   **Python:** For scripting, analysis, and HTML generation.
*   **Docker:** For creating a reproducible environment for the project.

# XML Structure

The project's data is organized into a set of interconnected XML files, with their structure defined by XSD schemas in the `XSD/` directory.

## Core Data Files

These files are located in the `XML/` directory and define the core entities of the project:

*   **`akteure.xml`:** Contains a list of all individuals (`<akteur>`) mentioned in the newspapers. Each actor has a unique `id`, a `<name>`, and can have additional information like biographical data (`<lebensdaten>`) and a GND identifier (`<gnd>`).
*   **`kategorien.xml`:** Defines the categories (`<kategorie>`) used to classify the newspaper contributions. Each category has a unique `id` and a `<name>`.
*   **`orte.xml`:** A list of all locations (`<ort>`) mentioned. Each place has a unique `id`, a `<name>`, and a `<geonames>` identifier.
*   **`werke.xml`:** A catalog of all referenced works (`<werk>`). Each work has a unique `id`, a `<zitation>` (citation), and can contain references to authors (`<akteur>`), places (`<ort>`), and other works.

## Contributions and Newspaper Issues

*   **`XML/beitraege/`:** This directory holds the XML files containing the newspaper contributions (`<beitrag>`). Each file can contain multiple `<beitrag>` elements, and each `<beitrag>` represents a single article or entry.
*   **`XML/stuecke/`:** This directory contains XML files that describe the individual newspaper issues (`<stueck>`). The files are named by year (e.g., `1764-stuecke.xml`). Each `<stueck>` element has a number, date, and page range.

## Linking Structure

The data is highly interconnected through a system of references:

*   The `<beitrag>` elements are the central hub, linking to all other data types.
*   Each `<beitrag>` must reference at least one `<stueck>` to indicate where it was published.
*   A `<beitrag>` can be assigned to one or more `<kategorie>`s.
*   References to people (`<akteur>`), places (`<ort>`), and works (`<werk>`) are made using a `<ref>` attribute that points to the unique `id` of the corresponding element in the core data files.
*   The nature of a reference is specified with a `kat` attribute. For example, an `<akteur>` can be referenced as an `autor` (author) or `herausgeber` (editor).

## Source Files

*   **`DOCS/Transkribus-Ergebnisse 1764/`:** This directory contains the raw output from the Transkribus OCR software. These XML files contain the transcribed text of the newspaper pages and the layout information, serving as the source for the structured XML data.

## Python Scripts

The main Python scripts are located in the `Scripts/` directory.

### `stats.py`

This script calculates statistics on the usage of different categories in the XML files.

To run the script:

```bash
python3 Scripts/stats.py
```

The script uses the following environment variables:

*   `INPUT_DIR`: The directory containing the XML files to be processed (defaults to `./XML/beitraege`).
*   `OUTPUT_FILE`: The file to write the statistics to (defaults to `./stats.txt`).

### `generate_html.py`

This script generates an HTML file from the XML data.

To run the script:

```bash
python3 Scripts/generate_html.py
```

The script will read the XML files from `XML/beitraege` and write the generated HTML to `output/kgpz_beitraege.html`.
