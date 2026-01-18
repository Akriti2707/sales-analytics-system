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


def generate_sales_report(
    transactions,
    enriched_transactions,
    output_file="output/sales_report.txt"
):
    """
    Generates a comprehensive formatted sales report.
    Includes all 8 required sections in the correct order.
    """

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    report = []

    # -----------------------------------------------------------
    # 1. HEADER
    # -----------------------------------------------------------
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_records = len(transactions)

    report.append("==============================================")
    report.append("             SALES ANALYTICS REPORT           ")
    report.append("==============================================")
    report.append(f"Generated: {now}")
    report.append(f"Records Processed: {total_records}")
    report.append("==============================================\n")

    # -----------------------------------------------------------
    # 2. OVERALL SUMMARY
    # -----------------------------------------------------------
    total_revenue = calculate_total_revenue(transactions)
    avg_order_value = total_revenue / total_records if total_records else 0

    dates = sorted([t["Date"] for t in transactions])
    date_range = f"{dates[0]} to {dates[-1]}"

    report.append("OVERALL SUMMARY")
    report.append("----------------------------------------------")
    report.append(f"Total Revenue: ₹{total_revenue:,.2f}")
    report.append(f"Total Transactions: {total_records}")
    report.append(f"Average Order Value: ₹{avg_order_value:,.2f}")
    report.append(f"Date Range: {date_range}\n")

    # -----------------------------------------------------------
    # 3. REGION-WISE PERFORMANCE
    # -----------------------------------------------------------
    region_stats = region_wise_sales(transactions)

    report.append("REGION-WISE PERFORMANCE")
    report.append("----------------------------------------------")
    report.append(f"{'Region':10} {'Sales':15} {'% of Total':15} {'Transactions'}")

    for region, stats in region_stats.items():
        report.append(
            f"{region:10} "
            f"₹{stats['total_sales']:,.0f}   "
            f"{stats['percentage']:.2f}%        "
            f"{stats['transaction_count']}"
        )
    report.append("")

    # -----------------------------------------------------------
    # 4. TOP 5 PRODUCTS
    # -----------------------------------------------------------
    top_products = top_selling_products(transactions, n=5)

    report.append("TOP 5 PRODUCTS")
    report.append("----------------------------------------------")
    report.append(f"{'Rank':5} {'Product':20} {'Qty Sold':10} {'Revenue'}")

    rank = 1
    for name, qty, revenue in top_products:
        report.append(
            f"{rank:<5} {name:20} {qty:<10} ₹{revenue:,.0f}"
        )
        rank += 1

    report.append("")

    # -----------------------------------------------------------
    # 5. TOP 5 CUSTOMERS
    # -----------------------------------------------------------
    customers = customer_analysis(transactions)
    sorted_customers = sorted(
        customers.items(),
        key=lambda x: x[1]["total_spent"],
        reverse=True
    )[:5]

    report.append("TOP 5 CUSTOMERS")
    report.append("----------------------------------------------")
    report.append(f"{'Rank':5} {'Customer':10} {'Total Spent':15} {'Orders'}")

    rank = 1
    for cid, stats in sorted_customers:
        report.append(
            f"{rank:<5} {cid:10} ₹{stats['total_spent']:,.0f}       {stats['purchase_count']}"
        )
        rank += 1

    report.append("")

    # -----------------------------------------------------------
    # 6. DAILY SALES TREND
    # -----------------------------------------------------------
    daily_stats = daily_sales_trend(transactions)

    report.append("DAILY SALES TREND")
    report.append("----------------------------------------------")
    report.append(f"{'Date':12} {'Revenue':12} {'Transactions':12} {'Unique Customers'}")

    for date, stats in daily_stats.items():
        report.append(
            f"{date:12} "
            f"₹{stats['revenue']:,.0f}      "
            f"{stats['transaction_count']:10}     "
            f"{stats['unique_customers']}"
        )

    report.append("")

    # -----------------------------------------------------------
    # 7. PRODUCT PERFORMANCE ANALYSIS
    # -----------------------------------------------------------
    peak_date, peak_rev, peak_count = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions, threshold=10)

    report.append("PRODUCT PERFORMANCE ANALYSIS")
    report.append("----------------------------------------------")
    report.append(f"Best Sales Day: {peak_date} (₹{peak_rev:,.0f}, {peak_count} transactions)\n")

    report.append("Low Performing Products (Qty < 10):")
    for name, qty, revenue in low_products:
        report.append(f" - {name}: Qty {qty}, Revenue ₹{revenue:,.0f}")

    report.append("")

    # -----------------------------------------------------------
    # 8. API ENRICHMENT SUMMARY
    # -----------------------------------------------------------
    total_enriched = len(enriched_transactions)
    success = sum(1 for tx in enriched_transactions if tx.get("API_Match"))
    failed = total_enriched - success
    success_pct = (success / total_enriched * 100) if total_enriched else 0
    total_unriched = 0

    report.append("API ENRICHMENT SUMMARY")
    report.append("----------------------------------------------")
    report.append(f"Total Products Enriched: {total_enriched}")
    report.append(f"Successful Matches: {success} ({success_pct:.2f}%)")

    # List products that failed API enrichment (only if any exist)
    failed_items = [tx for tx in enriched_transactions if not tx.get("API_Match")]

    if failed_items:
        report.append("Products That Could Not Be Enriched:")
        for tx in failed_items:
            report.append(f" - {tx['ProductID']} ({tx['ProductName']})")
        report.append("")  # spacing line


    # -----------------------------------------------------------
    # WRITE FILE
    # -----------------------------------------------------------
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report))

    print(f"Sales report successfully saved to: {output_file}")
