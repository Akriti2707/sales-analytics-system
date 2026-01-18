# Sales Analytics System

Student Name: Akriti Sharma  
Student ID: 25071909  
Email: dr.akritis09@gmail.com  
Date: 18/01/2026

---

## Project Overview
This project implements a complete sales analytics workflow including:
- File handling and preprocessing
- Data validation, filtering, and cleaning
- Sales and product performance analysis
- API integration with DummyJSON
- Report generation
- Full main application workflow

---

## Folder Structure
```
sales-analytics-system/
│
├── main.py
├── README.md
├── requirements.txt
│
├── data/
│   ├── sales_data.txt
│   ├── enriched_sales_data.txt
│
├── output/
│   └── sales_report.txt
│
└── utils/
    ├── file_handler.py
    ├── data_processor.py
    └── api_handler.py
```

---

## How to Run

### 1. Install dependencies
```
pip install -r requirements.txt
```

### 2. Run the application
```
python main.py
```

---

## Output 
```
========================================
        SALES ANALYTICS SYSTEM
========================================

[1/10] Reading sales data...
✓ Successfully read 80 raw lines

[2/10] Parsing and cleaning data...
✓ Parsed 80 records

[3/10] Filter Options Available:
Regions: , East, North, South, West
Amount Range: ₹-8,982 - ₹818,960

Do you want to filter data? (y/n): n

[4/10] Validating transactions...
✓ Valid: 70 | Invalid: 10

[5/10] Analyzing sales data...
✓ Analysis complete

[6/10] Fetching product data from API...
Successfully fetched 94 products from API.
✓ Fetched 94 products

[7/10] Enriching sales data...
✓ Enriched 70/70 transactions (100.0%)

[8/10] Saving enriched data...
✓ Saved to: data/enriched_sales_data.txt

[9/10] Generating report...
Sales report successfully saved to: output/sales_report.txt
✓ Report saved to: output/sales_report.txt

[10/10] Process Complete!
========================================
```