def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions.
    """
    total = 0.0

    for tx in transactions:
        total += tx["Quantity"] * tx["UnitPrice"]

    return total


def region_wise_sales(transactions):
    """
    Analyzes sales by region.
    """

    region_stats = {}
    overall_total_sales = 0.0

    # Step 1: Aggregate totals by region
    for tx in transactions:
        region = tx["Region"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        if region not in region_stats:
            region_stats[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_stats[region]["total_sales"] += amount
        region_stats[region]["transaction_count"] += 1

        overall_total_sales += amount

    # Step 2: Calculate percentages
    for region, stats in region_stats.items():
        if overall_total_sales > 0:
            stats["percentage"] = (stats["total_sales"] / overall_total_sales) * 100
        else:
            stats["percentage"] = 0.0

    # Step 3: Sort regions by total_sales (descending)
    sorted_regions = dict(
        sorted(region_stats.items(),
               key=lambda item: item[1]["total_sales"],
               reverse=True)
    )

    return sorted_regions


def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold.
    """

    product_stats = {}

    # Aggregate totals per product
    for tx in transactions:
        name = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        if name not in product_stats:
            product_stats[name] = {
                "total_qty": 0,
                "total_revenue": 0.0
            }

        product_stats[name]["total_qty"] += qty
        product_stats[name]["total_revenue"] += revenue

    # Convert to list of tuples (name, qty, revenue)
    product_list = [
        (
            name,
            stats["total_qty"],
            stats["total_revenue"]
        )
        for name, stats in product_stats.items()
    ]

    # Sort by total quantity (descending)
    product_list.sort(key=lambda x: x[1], reverse=True)

    # Return top n products
    return product_list[:n]


def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns.
    """

    customer_stats = {}

    # Step 1: Aggregate per customer
    for tx in transactions:
        cid = tx["CustomerID"]
        product = tx["ProductName"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        if cid not in customer_stats:
            customer_stats[cid] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products": set()
            }

        customer_stats[cid]["total_spent"] += amount
        customer_stats[cid]["purchase_count"] += 1
        customer_stats[cid]["products"].add(product)

    # Step 2: Finalize metrics and convert sets to lists
    final_output = {}

    for cid, stats in customer_stats.items():

        avg_order = (
            stats["total_spent"] / stats["purchase_count"]
            if stats["purchase_count"] > 0 else 0.0
        )

        final_output[cid] = {
            "total_spent": stats["total_spent"],
            "purchase_count": stats["purchase_count"],
            "avg_order_value": avg_order,
            "products_bought": list(stats["products"])
        }

    # Step 3: Sort by total_spent descending
    sorted_output = dict(
        sorted(final_output.items(),
               key=lambda item: item[1]["total_spent"],
               reverse=True)
    )

    return sorted_output

