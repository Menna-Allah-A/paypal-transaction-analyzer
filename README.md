# PayPal Transaction Analyzer 💰

A powerful Streamlit-based web application that transforms raw PayPal transaction CSV exports into actionable financial insights with interactive visualizations and comprehensive Excel reports.

## 🚀 Features

### 📊 Transaction Analysis
- Upload PayPal CSV files for instant analysis
- Filter transactions by name, amount, and date ranges
- Identify high-value transactions
- Detect potential double transactions
- Search transactions by payment notes

### 📈 Visual Analytics
- Interactive histograms of transaction amounts
- Box & whisker plots by month
- Monthly transaction sum and count trends
- Filter by payment status, method, source, and country
- Customizable date ranges

### 📑 Comprehensive Reports
Download detailed Excel reports with multiple sheets:
- `Clean_Data`: Processed and cleaned transactions
- `Calculations`: Key metrics and KPIs
- `Names`: Customer-wise transaction summaries
- `Transaction_type`: Breakdown by payment type
- `Countries`: Geographic distribution
- `Payment_Notes`: Flagged transactions by keywords
- `High_Ticket`: Large transactions
- `Name_checker`: Name-specific searches
- `Double_Transactions`: Potential duplicate transactions

### 📊 Key Metrics Calculated
- Total transaction sum and counts
- Mean, median, and max transaction values
- Charge, refund, and chargeback totals
- Refund and chargeback rates (lifetime, 90-day, 180-day)
- Unique customer counts
- Average transactions per customer

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/paypal-transaction-analyzer.git
cd paypal-transaction-analyzer
```

2. Install required packages:
```bash
pip install streamlit pandas numpy altair xlsxwriter openpyxl matplotlib
```

3. Run the application:
```bash
streamlit run hello.py
```

## 🎯 How to Use

1. **Start** with the welcome page for an overview
2. **Navigate** to the Transactions page to upload your PayPal CSV
3. **Analyze** with filters and view metrics
4. **Download** the complete Excel report
5. **Visualize** data in the Graphs page with interactive charts

### CSV Format Requirements
Your PayPal export should include columns like:
- Total
- Type (Charge/Refund/Chargeback)
- Customer_Name
- Transaction_Notes
- Day (Date)
- Country
- Source
- Transaction_Type
- Success
- Transaction_ID
- Auth_code

## 📊 Sample Use Cases

- **E-commerce sellers**: Track sales, refunds, and customer behavior
- **Freelancers**: Monitor payments and identify high-value clients
- **Small businesses**: Analyze payment trends and geographic distribution
- **Financial analysts**: Generate regular transaction reports
