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


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters.
    """

    total_input = len(transactions)
    valid_transactions = []
    invalid_count = 0

    # Step 1: Validate transaction rules
    for tx in transactions:
        # Validation rules
        if tx["Quantity"] <= 0:
            invalid_count += 1
            continue
        if tx["UnitPrice"] <= 0:
            invalid_count += 1
            continue
        if not tx["TransactionID"].startswith("T"):
            invalid_count += 1
            continue
        if not tx["ProductID"].startswith("P"):
            invalid_count += 1
            continue
        if not tx["CustomerID"].startswith("C"):
            invalid_count += 1
            continue
        if tx["Region"] == "" or tx["CustomerID"] == "":
            invalid_count += 1
            continue

        valid_transactions.append(tx)

    # Summary counters for filters
    filtered_by_region = 0
    filtered_by_amount = 0

    # Step 2: Apply region filter (optional)
    if region is not None:
        filtered_region_list = []
        for tx in valid_transactions:
            if tx["Region"] == region:
                filtered_region_list.append(tx)
            else:
                filtered_by_region += 1
        valid_transactions = filtered_region_list

    # Step 3: Apply amount filter (optional)
    if min_amount is not None or max_amount is not None:
        filtered_amount_list = []
        for tx in valid_transactions:
            amount = tx["Quantity"] * tx["UnitPrice"]

            if min_amount is not None and amount < min_amount:
                filtered_by_amount += 1
                continue

            if max_amount is not None and amount > max_amount:
                filtered_by_amount += 1
                continue

            filtered_amount_list.append(tx)

        valid_transactions = filtered_amount_list

    # Build summary dictionary
    filter_summary = {
        "total_input": total_input,
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(valid_transactions),
    }

    return valid_transactions, invalid_count, filter_summary