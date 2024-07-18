import os

def main():
    if not os.path.exists('schema_validation_errors.txt'):
        print("Keine Schema-Validierungsergebnisse gefunden.")
        return

    current_file = None
    with open('schema_validation_errors.txt', 'r') as f:
        for line in f:
            if line.startswith("Validierungsfehler in ") or line.startswith("XML-Syntaxfehler in "):
                current_file = line.split("in ", 1)[1].strip()[:-1]
            elif line.strip().startswith("Zeile"):
                parts = line.strip().split(", ")
                line_num = parts[0].split(" ")[1]
                col_num = parts[1].split(" ")[1]
                message = ": ".join(parts[2:])
                print(f"::error file={current_file},line={line_num},col={col_num}::{message}")
            else:
                print(f"::error file={current_file}::{line.strip()}")

if __name__ == "__main__":
    main()
