# hello.py
import streamlit as st

st.set_page_config(
    page_title="PayPal Transaction Analyzer",
    page_icon="💰"
)

# Simple welcome header
st.title("💰 Welcome to PayPal Transaction Analyzer")
st.write("---")

# Simple explanation
st.write("## What is this app?")
st.write("""
This app helps you analyze your PayPal transactions easily. 
Whether you're tracking sales, refunds, or chargebacks, 
we've got you covered!
""")

# Simple instructions
st.write("## How to use:")
st.write("""
1. **Upload your PayPal CSV file** in the Transactions page
2. **View detailed breakdowns** of your transactions
3. **See beautiful charts** in the Graphs page
4. **Download Excel reports** for further analysis
""")

# Quick start guide in simple steps
st.write("## Quick Start Guide:")
col1, col2, col3 = st.columns(3)

with col1:
    st.write("📁 **Step 1**")
    st.write("Go to 'Transactions' page")
    st.write("- Upload your CSV")
    st.write("- Enter your name filter")
    st.write("- Set high ticket amount")

with col2:
    st.write("📊 **Step 2**")
    st.write("Go to 'Graphs' page")
    st.write("- Filter your data")
    st.write("- View different charts")
    st.write("- Spot trends easily")

with col3:
    st.write("📥 **Step 3**")
    st.write("Download results")
    st.write("- Get Excel reports")
    st.write("- Save filtered data")
    st.write("- Keep for records")

# File format reminder
st.write("---")
st.write("### 📌 Important Reminder:")
st.info("Make sure your file is a CSV export from PayPal with columns like: Total, Type, Customer_Name, Transaction_Notes, etc.")

# Quick tips box
with st.expander("💡 Quick Tips for Beginners"):
    st.write("""
    - **CSV File**: Your PayPal export should be in CSV format
    - **Name Search**: You can search for specific customers
    - **High Ticket**: Set this to find big transactions
    - **Filters**: Use the graphs page to filter by date, type, and more
    - **Download**: Always download your Excel report for backup
    """)

# Sidebar note
st.sidebar.success("👈 Select a page above to get started!")
st.sidebar.info("📊 **Pages:**\n- Transactions (data analysis)\n- Graphs (charts & visuals)")