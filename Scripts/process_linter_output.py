import os

def main():
    if not os.path.exists('linter_results.txt'):
        print("No linter results found.")
        return

    with open('linter_results.txt', 'r') as f:
        for line in f:
            parts = line.strip().split(':', 2)
            if len(parts) == 3:
                filename, line_number, error_message = parts
                print(f"::error file={filename},line={line_number}::{error_message}")

if __name__ == "__main__":
    main()
