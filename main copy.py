import streamlit as st
import yfinance as finance

import pandas as pd
from PIL import Image
st.sidebar.header("USER INPUT")

st.header("Stock market")
def get_input():
    start_date=st.sidebar.text_input("Start Date","2020-01-03")
    end_date = st.sidebar.text_input("End Date", "2020-08-04")
    stock_symbol=st.sidebar.text_input("Symbol", "INDUSINDBK")
    return start_date,end_date,stock_symbol

def get_comapany(symbol):
    if symbol=="INDUSINDBK":
        return 'INDUSIND BANK'
    elif symbol == "ICICIBANK":
        return 'ICICI '
    else:
        'None'

def stock_price_prediction(stock_symbol):
    try:
        # Fetch historical stock data
        symbol_dict={'ADANIPORTS':r"C:\Users\Suresh\OneDrive\Desktop\Now\ADANIPORTS.csv",
               'AXISBANK':r"C:\Users\Suresh\OneDrive\Desktop\Now\AXISBANK.csv",
               'ASIANPAINT':r"C:\Users\Suresh\OneDrive\Desktop\Now\ASIANPAINT.csv",
               'BAJAJ-AUTO':r"C:\Users\Suresh\OneDrive\Desktop\Now\BAJAJ-AUTO.csv",
               'HDFC':r"C:\Users\Suresh\OneDrive\Desktop\Now\HDFC.csv",
               'HDFCBANK':r"C:\Users\Suresh\OneDrive\Desktop\Now\HDFCBANK.csv",
               'ICICIBANK':r"C:\Users\Suresh\OneDrive\Desktop\Stock Price Prediction\HTF23-Team-126\files\ICICIBANK.csv",
               'INDUSINDBK':r"C:\Users\Suresh\OneDrive\Desktop\Stock Price Prediction\HTF23-Team-126\files\INDUSINDBK.csv",
               'KOTAKBANK':"",
                     'TATAMOTORS':"/content/TATAMOTORS.csv",
                     'TATASTEEL':"/content/TATASTEEL.csv"
  }
        df = pd.read_csv(symbol_dict[stock_symbol.upper()])
        stock_data = df[['Open','High','Low','Last','Prev Close']]
        print(stock_data)

        # Calculate moving averages (you can modify the window size)
        window_size = 10  # Adjust this value as needed
        stock_data['SMA'] = stock_data['Last'].rolling(window=window_size).mean()
        stock_data['EMA'] = stock_data['Last'].ewm(span=window_size, adjust=False).mean()

        # Get the last available stock price
        last_price = stock_data['Last'].iloc[-1]

        # Get the last available moving averages
        last_sma = stock_data['SMA'].iloc[-1]
        last_ema = stock_data['EMA'].iloc[-1]

        # Perform a basic prediction (you can customize this)
        prediction = "Hold"  # Default prediction
        if last_price > last_sma and last_price > last_ema:
            prediction = "Buy"
        elif last_price < last_sma and last_price < last_ema:
            prediction = "Sell"

        return {
            "last_price": last_price,
            "last_sma": last_sma,
            "last_ema": last_ema,
            "prediction": prediction,
        }

    except Exception as e:
        return {"error": str(e)}

def get_date(symbol,start,end):
    if symbol.upper() =='INDUSINDBK':
        df=pd.read_csv(r"C:\Users\Suresh\OneDrive\Desktop\Stock Price Prediction\HTF23-Team-126\files\INDUSINDBK.csv")
    if symbol.upper() == 'ICICIBANK':
        df=pd.read_csv(r"C:\Users\Suresh\OneDrive\Desktop\Stock Price Prediction\ICICIBANK.csv")

    start=pd.to_datetime(start)
    end=pd.to_datetime(end)
    start_row=0
    end_row=0
    for i in range(0, len(df)):
        if start<=pd.to_datetime(df['Date'][i]):
            start_row = i
            break
    for j in range(0, len(df)):
        if end>=pd.to_datetime(df['Date'][len(df)-1-j]):
            end_row = len(df) -1 -j
            break
    df = df.set_index(pd.DatetimeIndex(df['Date'].values))

    return df.iloc[start_row:end_row+1,:]

start, end, symbol = get_input()
df = get_date(symbol, start, end)
company_name = get_comapany(symbol.upper())
st.subheader(company_name+"Close Price\n")
st.line_chart(df['Close'])

st.subheader(company_name+"Volume\n")
st.line_chart(df['Volume'])


st.subheader("Data Statistics")
st.write(df.describe())

#st_input = st.text_input("Enter a stock symbol :")
#stock_symbol = input("Enter a stock symbol: ")
result = stock_price_prediction(symbol.upper())

st.subheader("Prediction (SMA):")
st.write(result["last_sma"])

st.subheader("Prediction (EMA):")
st.write(result["last_ema"])
    
st.subheader("Buy/Sell/Keep")
st.write(result["prediction"])

