import json

def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.
    """

    encodings_to_try = ("utf-8", "latin-1", "cp1252")
    lines = None

    # Try multiple encodings
    for enc in encodings_to_try:
        try:
            with open(filename, "r", encoding=enc) as f:
                lines = [line.rstrip("\n") for line in f.readlines()]
            break  # Successfully read
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []
        except UnicodeDecodeError:
            continue  # Try next encoding

    # If all encodings failed
    if lines is None:
        print(f"Error: Could not decode '{filename}' with available encodings.")
        return []

    # Remove header + empty lines
    data_lines = [line for line in lines[1:] if line.strip()]

    return data_lines


