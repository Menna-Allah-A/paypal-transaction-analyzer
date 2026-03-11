import altair as alt
import pandas as pd 
import streamlit as st
import datetime
from datetime import date, timedelta
import matplotlib.pyplot as plt 

st.set_page_config(page_title="Charts")
st.title("Chart Marker")

PaymentStatus = st.selectbox(
    'What Payment Status Would You Like to see',
    ('All','Charge','Refund', 'Chargeback'))

PaymentMethod = st.selectbox(
    'What Payment Method Would You Like to see',
    ('All','Friends and Family','Goods and service'))

PaymentApplication = st.selectbox(
    'What Payment Application Would You Like to see',
    ('All','Phone','Tablet', 'Desktop'))

PaymentCountry = st.selectbox(
    'What Payment Country Would You Like to see',
    ('All','US','Uk', 'AU'))

today = datetime.datetime.now()
day180 = date.today() - timedelta(days=180)

StartDate = st.date_input("Start Date (Default 180 Days Prior)")
EndDate = st.date_input("End Date (Default Today)", today)

dfPreClean = st.file_uploader("select CSV File")

if dfPreClean is not None:
    dfPreClean = pd.read_csv(dfPreClean)
else:
    st.stop()    
    

dfPreClean.drop(['Transaction_ID','Auth_code'], axis=1, inplace=True)
dfPreClean2 = dfPreClean[dfPreClean['Success'] ==1]
dfPreClean2['Transaction_Notes'].fillna("N/A" , inplace = True)
dfPreClean2['Day'] = pd.to_datetime(dfPreClean2['Day'])
df =dfPreClean2.loc[:,['Total', 'Transaction_Notes','Type','Country',
                           'Source', 'Day', 'Customer_Name', 'Transaction_Type']]    
 
df['int_created_date'] = df['Day'].dt.year * 100 + df['Day'].dt.month



if PaymentStatus == 'Charge':
    df = df[df['Type'] == 'Charge']
elif PaymentStatus == 'Refund':
    df = df[df['Type'] == 'Refund']
elif PaymentStatus == 'Chargeback':
    df = df[df['Type'] == 'Chargeback']
else:
    pass

if PaymentMethod == 'Goods and Services':
    df = df[df['Transaction_Type'] == 'Goods and Services']
elif PaymentMethod == 'Friends & Family':
    df = df[df['Transaction_Type'] == 'Friends & Family']
else:
    pass

if PaymentApplication == 'Desktop':
    df = df[df['Source'] == 'Desktop']
elif PaymentApplication == 'Tablet':
    df = df[df['Source'] == 'Tablet']
elif PaymentApplication == 'Phone':
    df = df[df['Source'] == 'Phone']
else:
    pass

if PaymentCountry == 'US':
    df = df[df['Country'] == 'US']
elif PaymentCountry == 'UK':
    df = df[df['Country'] == 'UK']
elif PaymentCountry == 'AU':
    df = df[df['Country'] == 'AU']
else:
    pass


StartDate = pd.to_datetime(StartDate)
EndDate = pd.to_datetime(EndDate)

df = df[(df['Day'] >= StartDate) & (df['Day'] <= EndDate)]


chart1 = alt.Chart(df).mark_bar().encode(
    alt.X("Total:Q",bin=True),
    y='count()',
    ).properties(
        title = {
            "text": ["Count of Transactions"],
            "subtitle": [f"Payment Status: {PaymentStatus}", f"Payment Method: {PaymentMethod}", f"Payment Application: {PaymentApplication}", f"Payment Country: {PaymentCountry}",  f"Start Date: {StartDate}", f"End Date: {EndDate}",]
            },
        width = 800,
        height = 500
        )
        
    

chart2 = alt.Chart(df).mark_boxplot(extent='min-max').encode(
    x='int_created_date:O',
    y='Total:Q',
    ).properties(
        title = {
            "text": ["Box & Whisker By Month"],
            "subtitle": [f"Payment Status: {PaymentStatus}", f"Payment Method: {PaymentMethod}", f"Payment Application: {PaymentApplication}", f"Payment Country: {PaymentCountry}",  f"Start Date: {StartDate}", f"End Date: {EndDate}",]
            },
        width = 800,
        height = 500
        )
        
        
bar3 = alt.Chart(df).mark_bar().encode(
    x=alt.X('int_created_date:O', title='Date'),
    y=alt.Y('sum(Total):Q', title='Total'),
    color=alt.Color('Type:N', title='Payment Type')
)

chart3 = (bar3).properties(
    title={
        "text": ["Box Plot Mean Transaction Per Month"], 
        "subtitle": [f"Payment Status: {PaymentStatus}", f"Payment Method: {PaymentMethod}", f"Payment Application: {PaymentApplication}", f"Payment Country: {PaymentCountry}",  f"Start Date: {StartDate}", f"End Date: {EndDate}",],
    },
    width=800,
    height=500
)

bar4 = alt.Chart(df).mark_bar().encode(
    x=alt.X('int_created_date:O', title='Date'),
    y=alt.Y('count(Total):Q', title='Count'),
    color=alt.Color('Type:N', title='Payment Type')
)

chart4 = (bar4).properties(
    title={
      "text": ["Box Plot Transaction Count Per Month"], 
      "subtitle": [f"Payment Status: {PaymentStatus}", f"Payment Method: {PaymentMethod}", f"Payment Application: {PaymentApplication}", f"Payment Country: {PaymentCountry}",  f"Start Date: {StartDate}", f"End Date: {EndDate}",],
    },
    width=800,
    height=500
)

tab1, tab2, tab3, tab4 = st.tabs(["Histogram","Box and whiskers", "Box Plot Sum", "Box Plot Count"])

with tab1:
    st.altair_chart(chart1, use_container_width=True)
with tab2:
    st.altair_chart(chart2, use_container_width=True)
with tab3:
    st.altair_chart(chart3, use_container_width=True)
with tab4:
    st.altair_chart(chart4, use_container_width=True)





























