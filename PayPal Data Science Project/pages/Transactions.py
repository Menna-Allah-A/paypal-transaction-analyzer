import streamlit as st
import pandas as pd
import numpy as np
import io
import xlsxwriter
import datetime
from datetime import date, timedelta

st.set_page_config(page_title ="Transactions")
st.title("Transaction Breakdown")
filename = st.text_input("Filename", key="filename")
firstname = st.text_input("Enter Name", key="firstname")
highticketstring = st.number_input("Enter High Ticket INTEGER ONLY", key="highticket")
uploaded_file = st.file_uploader("please Upload CSV File", type = ['csv'])


if uploaded_file is not None:
    
    highticketval = int(highticketstring)
    dfPreClean = pd.read_csv(uploaded_file)
    
    buffer = io.BytesIO()

    
    dfPreClean.drop(['Transaction_ID','Auth_code'], axis=1, inplace=True)
    dfPreClean2 = dfPreClean[dfPreClean['Success'] ==1]
    dfPreClean2['Transaction_Notes'].fillna("N/A" , inplace = True)
    dfPreClean2['Day'] = pd.to_datetime(dfPreClean2['Day'])
    df =dfPreClean2.loc[:,['Total', 'Transaction_Notes','Type','Country',
                           'Source', 'Day', 'Customer_Name', 'Transaction_Type']]
    
    
    totalsum = np.sum(df['Total'])
    total_transactions = df['Type'].count()
    mean_transactions = np.mean(df['Total'])
    median_transactions = np.median(df['Total'])
    max_transactions = np.max(df['Total'])
    
    
    ChargeOnlyTransactions = df[df['Type']=='Charge']
    RefundOnlyTransactions = df[df['Type']=='Refund']
    ChargeBackOnlyTransactions = df[df['Type']=='Chargeback']
    
    day90 =  pd.to_datetime(date.today() - timedelta(days=90))
    day180 =  pd.to_datetime(date.today() - timedelta(days=180))
    
    ChargeTotal = np.sum(ChargeOnlyTransactions['Total'])
    charge90days = np.sum(ChargeOnlyTransactions[ChargeOnlyTransactions['Day'] > day90]['Total'])
    charge180days = np.sum(ChargeOnlyTransactions[ChargeOnlyTransactions['Day'] > day180]['Total'])
    
    
    RefundTotal = np.sum(RefundOnlyTransactions['Total'])
    Refund90days = np.sum(RefundOnlyTransactions[RefundOnlyTransactions['Day'] > day90]['Total'])
    Refund180days = np.sum(RefundOnlyTransactions[RefundOnlyTransactions['Day'] > day180]['Total'])
    
    
    ChargeBackTotal = np.sum(ChargeBackOnlyTransactions['Total'])
    ChargeBack90days = np.sum(ChargeBackOnlyTransactions[ChargeBackOnlyTransactions['Day'] > day90]['Total'])
    ChargeBack180days = np.sum(ChargeBackOnlyTransactions[ChargeBackOnlyTransactions['Day'] > day180]['Total'])
    
    
    RefundRateLifeTime = (RefundTotal/ChargeTotal)
    RefundRate90Days = (Refund90days/charge90days)
    RefundRate180Days = (Refund180days/charge180days)
    
    
    ChargeBackRateLifeTime = (ChargeBackTotal/ChargeTotal)
    ChargeBackRate90Days = (ChargeBack90days/charge90days)
    ChargeBackRate180Days = (ChargeBack180days/charge180days)
    
    
    PivotTableNames = pd.pivot_table(df, index=['Customer_Name'], aggfunc={'Total':np.sum, 'Customer_Name':'count'})
    PivotTableNames = PivotTableNames.rename(columns={"Customer_Name": "count_of_total", "Total": "sum_of_total"})
    PivotTableNames = PivotTableNames.loc[:,["sum_of_total","count_of_total"]]
    
    total_unique_customers = PivotTableNames['sum_of_total'].count()
    
    
    avg_transactions_count_per_customer = np.mean(PivotTableNames['count_of_total'])
    avg_transactions_sum_per_customer = np.mean(PivotTableNames['sum_of_total'])
    
    
    PivotTableTransactionsType = pd.pivot_table(df, index=['Transaction_Type'],aggfunc={'Transaction_Type':'count','Total':np.sum})
    PivotTableTransactionsType['totalpercent'] = (PivotTableTransactionsType['Total']/totalsum).apply('{:.2%}'.format) 
    
    PivotTableTransactionsCountry = pd.pivot_table(df, index=['Country'],aggfunc={'Country':'count','Total':np.sum})
    PivotTableTransactionsCountry['totalpercent'] = (PivotTableTransactionsCountry['Total']/totalsum).apply('{:.2%}'.format) 
    
    
    NameFinal = df[df['Customer_Name'].str.contains(firstname, case=False)]
    
    
    #  | -> called pipe
    payment_note = df[df['Transaction_Notes'].isna() == False]
    
    flagged_words = 'raffle|razz|lottery'
    payment_note_final = df[df['Transaction_Notes'].str.contains(flagged_words, case=False)] 
    
    highticket = df[df['Total'] >= highticketval].copy()
    highticket = highticket.sort_values(by='Total', ascending=True)
    
    
    dup = df.copy() 
    dup['Customer_Name_next'] = dup['Customer_Name'].shift(1)
    dup['Customer_Name_prev'] = dup['Customer_Name'].shift(-1)
    
    dup['created_at_day'] = dup['Day']
    dup['created_at_day_next'] = dup['Day'].shift(1)
    dup['created_at_day_prev'] = dup['Day'].shift(-1)
    
    
    dup2 = dup.query('(created_at_day == created_at_day_prev | created_at_day == created_at_day_next) & (Customer_Name == Customer_Name_next | Customer_Name ==Customer_Name_prev)')
    
    dfcalc = pd.DataFrame({    'totalsum':[totalsum],
                               'mean_transaction':[mean_transactions],
                               'median_transaction':[median_transactions], 
                               'max_transaction':[max_transactions],
                               'total_transactions':[total_transactions],
                               'chargetotal':[ChargeTotal],
                               'charge90days':[charge90days],
                               'charge180days':[charge180days],
                               'refundtotal':[RefundTotal],
                               'refund90days':[Refund90days],
                               'refund180days':[Refund180days],
                               'refundrateliefetime':[RefundRateLifeTime],
                               'refundrate90days':[RefundRate90Days],
                               'refundrate180days':[RefundRate180Days],
                               'chargebacktotal':[ChargeBackTotal],
                               'chargeback90days':[ChargeBack90days],
                               'chargeback180days':[ChargeBack180days],
                               'chargebackrateliefetime':[ChargeBackRateLifeTime],
                               'chargebackrate90days':[ChargeBackRate90Days],
                               'chargebackrate180days':[ChargeBackRate180Days],
                               'total_unique_customer_names':[total_unique_customers],                      
                               'avg_transactions_count_per_customer_name':[avg_transactions_count_per_customer],
                               'avg_transactions_sum_per_customer_name':[avg_transactions_sum_per_customer],
                               '90 Days':[day90],
                               '180 Days':[day180],
                               })
    
    
    format_mapping = {"totalsum": '${:,.2f}',
                      "mean_transaction": '${:,.2f}',
                      "median_transaction": '${:,.2f}',
                      "max_transaction": '${:,.2f}',
                      "total_transactions": '{:,.0f}', 
                      'chargetotal': '${:,.2f}',
                      'charge90days': '${:,.2f}',
                      'charge180days': '${:,.2f}',
                      'refundtotal': '${:,.2f}',
                      'refund90days': '${:,.2f}',
                      'refund180days': '${:,.2f}',
                      'refundrateliefetime':'{:.2%}',
                      'refundrate90days':'{:.2%}',
                      'refundrate180days':'{:.2%}',
                      'chargebacktotal':'${:,.2f}',
                      'chargeback90days':'${:,.2f}',
                      'chargeback180days':'${:,.2f}',
                      'chargebackrateliefetime':'{:.2%}',
                      'chargebackrate90days':'{:.2%}',
                      'chargebackrate180days':'{:.2%}',
                      "total_unique_customer_names": '{:,.0f}',
                      "avg_transactions_count_per_customer_name": '{:,.2f}',
                      "avg_transactions_sum_per_customer_name": '${:,.2f}',                  
                        }
    
    for key, value in format_mapping.items():
        dfcalc[key] = dfcalc[key].apply(value.format)
        

    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Clean_Data')
        dfcalc.to_excel(writer, sheet_name='Calculations')
        PivotTableNames.to_excel(writer, sheet_name='Names')
        PivotTableTransactionsType.to_excel(writer, sheet_name='Transaction_type')
        PivotTableTransactionsCountry.to_excel(writer, sheet_name='Countries')
        payment_note_final.to_excel(writer, sheet_name='Payment_Notes')
        highticket.to_excel(writer, sheet_name='High_Ticket')
        NameFinal.to_excel(writer, sheet_name='Name_checker')
        dup2.to_excel(writer, sheet_name='Double_Transactions')
        
        writer.close()        


    st.download_button(
        label = 'Download Excel File',
        data = buffer,
        file_name = f"{st.session_state.filename}.xlsx",
        mime = "application/vnd.ms-excel"
        )    

else :
    st.warning("you need to upload a csv file first.")        