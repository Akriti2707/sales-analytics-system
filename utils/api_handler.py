import requests
import datetime
import os
from utils.data_processor import *

def fetch_all_products():
    """
    Fetches all products from DummyJSON API.
    """

    url = "https://dummyjson.com/products?limit=100&skip=100"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # raises HTTPError for bad responses

        data = response.json()

        # Extract product list
        products = data.get("products", [])
        print(f"Successfully fetched {len(products)} products from API.")

        return products

    except Exception as e:
        print("Failed to fetch products from API.")
        print("Error:", e)
        return []


def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info.
    """

    product_map = {}

    for product in api_products:
        pid = product.get("id")

        # Extract required fields only
        info = {
            "title": product.get("title"),
            "category": product.get("category"),
            "brand": product.get("brand"),
            "rating": product.get("rating"),
            "price": product.get("price")
        }

        product_map[pid] = info

    return product_map


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information.
    """

    enriched = []

    for tx in transactions:

        # Copy original transaction (avoid modifying original)
        new_tx = tx.copy()

        # Extract numeric product ID from ProductID like 'P101'
        pid_raw = tx.get("ProductID", "")

        try:
            numeric_id = int(pid_raw[1:])

        except:
            numeric_id = None

        # Fetch API product info
        api_info = product_mapping.get(numeric_id)

        if api_info is not None:
            # Successful match
            new_tx["API_Category"] = api_info.get("category")
            new_tx["API_Brand"] = api_info.get("brand")
            new_tx["API_Rating"] = api_info.get("rating")
            new_tx["API_Match"] = True
        else:
            # No match found
            new_tx["API_Category"] = None
            new_tx["API_Brand"] = None
            new_tx["API_Rating"] = None
            new_tx["API_Match"] = False

        enriched.append(new_tx)

    return enriched


def save_enriched_data(enriched_transactions, filename="data/enriched_sales_data.txt"):
    """
    Saves enriched transactions to a pipe-delimited text file.
    """

    # Define header fields in correct order
    headers = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(filename, "w", encoding="utf-8") as f:

        # Write header row
        f.write("|".join(headers) + "\n")

        # Write each transaction row
        for tx in enriched_transactions:
            row = []
            for h in headers:
                value = tx.get(h)
                # Convert None to string "None"
                row.append(str(value) if value is not None else "None")
            f.write("|".join(row) + "\n")


