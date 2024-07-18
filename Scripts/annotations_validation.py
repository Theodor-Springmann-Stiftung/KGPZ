import sys
import re

def parse_error_message(line):
    match = re.match(r"Validierungsfehler in (.*?):\s*", line)
    if match:
        return match.group(1), None, None, None
    
    match = re.match(r"\s*Zeile (\d+), Spalte (\d+): (.*)", line)
    if match:
        return None, int(match.group(1)), int(match.group(2)), match.group(3)
    
    match = re.match(r"XML-Syntaxfehler in (.*?):\s*", line)
    if match:
        return match.group(1), None, None, None
    
    match = re.match(r"\s*Zeile (\d+), Spalte (\d+): (.*)", line)
    if match:
        return None, int(match.group(1)), int(match.group(2)), match.group(3)
    
    return None, None, None, None

def main():
    current_file = None
    for line in sys.stdin:
        file, line_num, column, message = parse_error_message(line.strip())
        
        if file:
            current_file = file
        elif line_num and column and message and current_file:
            print(f"::error file={current_file},line={line_num},col={column}::{message}")

if __name__ == "__main__":
    main()
