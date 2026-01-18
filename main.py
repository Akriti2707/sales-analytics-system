import sys
from utils.file_handler import *
from utils.api_handler import *


def main():
    print("========================================")
    print("        SALES ANALYTICS SYSTEM")
    print("========================================\n")

    try:
        # -----------------------------------------------------------
        # [1/10] READ SALES DATA
        # -----------------------------------------------------------
        print("[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_lines)} raw lines\n")

        # -----------------------------------------------------------
        # [2/10] PARSE TRANSACTIONS
        # -----------------------------------------------------------
        print("[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records\n")

        # -----------------------------------------------------------
        # [3/10] SHOW FILTER OPTIONS
        # -----------------------------------------------------------
        print("[3/10] Filter Options Available:")

        # Determine available regions
        all_regions = sorted({tx["Region"] for tx in transactions})
        print("Regions:", ", ".join(all_regions))

        # Determine amount range
        amounts = [tx["Quantity"] * tx["UnitPrice"] for tx in transactions]
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}\n")

        # User chooses to filter or not
        choice = input("Do you want to filter data? (y/n): ").strip().lower()
        region_filter = None
        min_amt, max_amt = None, None

        if choice == "y":
            print("\n--- APPLY FILTERS ---")

            region_choice = input("Enter region to filter (or press Enter to skip): ").strip()
            if region_choice in all_regions:
                region_filter = region_choice

            try:
                min_amt = input("Minimum amount (or press Enter to skip): ").strip()
                min_amt = float(min_amt) if min_amt else None

                max_amt = input("Maximum amount (or press Enter to skip): ").strip()
                max_amt = float(max_amt) if max_amt else None
            except:
                print("Invalid amount entered. Filters ignored.\n")
                min_amt, max_amt = None, None
        print()

        # -----------------------------------------------------------
        # [4/10] VALIDATE + FILTER
        # -----------------------------------------------------------
        print("[4/10] Validating transactions...")
        valid_tx, invalid_count, filter_summary = validate_and_filter(
            transactions,
            region=region_filter,
            min_amount=min_amt,
            max_amount=max_amt
        )

        print(f"✓ Valid: {len(valid_tx)} | Invalid: {invalid_count}\n")

        # -----------------------------------------------------------
        # [5/10] ANALYZE SALES DATA
        # -----------------------------------------------------------
        print("[5/10] Analyzing sales data...")
        # These computations are used inside report generator
        _ = calculate_total_revenue(valid_tx)
        _ = region_wise_sales(valid_tx)
        _ = top_selling_products(valid_tx)
        _ = customer_analysis(valid_tx)
        _ = daily_sales_trend(valid_tx)
        _ = find_peak_sales_day(valid_tx)
        _ = low_performing_products(valid_tx)
        print("✓ Analysis complete\n")

        # -----------------------------------------------------------
        # [6/10] FETCH API PRODUCTS
        # -----------------------------------------------------------
        print("[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products\n")

        # -----------------------------------------------------------
        # [7/10] ENRICH SALES DATA
        # -----------------------------------------------------------
        print("[7/10] Enriching sales data...")
        product_map = create_product_mapping(api_products)
        enriched = enrich_sales_data(valid_tx, product_map)
        success_count = sum(1 for tx in enriched if tx.get("API_Match"))
        total_count = len(enriched)
        success_rate = (success_count / total_count * 100) if total_count else 0
        print(f"✓ Enriched {success_count}/{total_count} transactions ({success_rate:.1f}%)\n")

        # -----------------------------------------------------------
        # [8/10] SAVE ENRICHED DATA
        # -----------------------------------------------------------
        print("[8/10] Saving enriched data...")
        save_enriched_data(enriched)
        print("✓ Saved to: data/enriched_sales_data.txt\n")

        # -----------------------------------------------------------
        # [9/10] GENERATE REPORT
        # -----------------------------------------------------------
        print("[9/10] Generating report...")
        generate_sales_report(valid_tx, enriched)
        print("✓ Report saved to: output/sales_report.txt\n")

        # -----------------------------------------------------------
        # [10/10] COMPLETE
        # -----------------------------------------------------------
        print("[10/10] Process Complete!")
        print("========================================")

    except Exception as e:
        print("\n An error occurred:")
        print(str(e))
        print("The program was unable to complete the process.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
