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


def parse_transactions(raw_lines):
    """
    Parses raw sales data into a clean list of dictionaries.
    """

    transactions = []

    for line in raw_lines:
        parts = line.split("|")

        # Valid rows must have exactly 8 fields
        if len(parts) != 8:
            continue

        (
            transaction_id,
            date,
            product_id,
            product_name,
            quantity,
            unit_price,
            customer_id,
            region
        ) = parts

        # Remove commas from product name (replace commas with space)
        product_name = product_name.replace(",", " ")

        # Remove commas from numeric fields
        quantity = quantity.replace(",", "")
        unit_price = unit_price.replace(",", "")

        # Convert data types
        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
        except ValueError:
            # Skip rows where conversion fails
            continue

        transaction_dict = {
            "TransactionID": transaction_id,
            "Date": date,
            "ProductID": product_id,
            "ProductName": product_name,
            "Quantity": quantity,
            "UnitPrice": unit_price,
            "CustomerID": customer_id,
            "Region": region
        }

        transactions.append(transaction_dict)

    return transactions


