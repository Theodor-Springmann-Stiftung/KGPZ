import os

def main():
    if not os.path.exists('reference_check_errors.txt'):
        print("Keine Referenzprüfungs-Ergebnisse gefunden.")
        return

    with open('reference_check_errors.txt', 'r') as f:
        for line in f:
            parts = line.strip().split(', Zeile ')
            if len(parts) == 2:
                file_path, rest = parts
                line_number, message = rest.split(': ', 1)
                print(f"::error file={file_path},line={line_number}::{message}")

if __name__ == "__main__":
    main()
