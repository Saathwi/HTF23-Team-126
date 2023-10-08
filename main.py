import streamlit as st
import pandas as pd

st.sidebar.header("USER INPUT")

st.header("STOCK PRICE PREDICTION")
st.write("Stock price prediction is a critical aspect of financial analysis and investment decision-making. Investors and traders rely on these predictions to make informed choices about buying, selling, or holding stocks.")
st.header("Stock Prices for the selected dates are depicted using the graphs below")
def get_input():
    start_date=st.sidebar.text_input("Start Date","2003-01-03")
    end_date = st.sidebar.text_input("End Date", "2021-08-31")
    stock_symbol=st.sidebar.text_input("Symbol", "INDUSINDBK")
    return start_date,end_date,stock_symbol



def get_company(symbol):
 
    symbol_dict={'ADANIPORTS':"Adani Ports and Special Economic Zone Ltd.",
               'AXISBANK':"Axis Bank Ltd.",
               'ASIANPAINT':"Asian Paints Ltd.",
               'BAJAJ-AUTO':"Bajaj Auto Ltd",
               'HDFC':"Housing Development Finance Corporation Ltd.",
               'HDFCBANK':"HDFC Bank Ltd.",
               'ICICIBANK':"ICICI Bank Ltd.",
               'INDUSINDBK':"IndusInd Bank Ltd.",
               'KOTAKBANK':"Kotak Mahindra Bank Ltd.",
                'TATAMOTORS':"Tata Motors Ltd.",
                'TATASTEEL':"Tata Steel Ltd."
  }
    # datafr = pd.read_csv(r"C:\Users\Suresh\OneDrive\Desktop\Clon_1\HTF23-Team-126\files\stock_metadata.csv")
    # df = pd.DataFrame({'Symbols': [datafr['Symbol']], 'Company_names': [datafr['Company Name']]})
    # #print(df)
    return symbol_dict[symbol]


symbol_dict={'ADANIPORTS':r"C:\Users\Suresh\OneDrive\Desktop\Clon_1\HTF23-Team-126\files\ADANIPORTS.csv",
               'AXISBANK':r"C:\Users\Suresh\OneDrive\Desktop\Clon_1\HTF23-Team-126\files\AXISBANK.csv",
               'ASIANPAINT':r"C:\Users\Suresh\OneDrive\Desktop\Clon_1\HTF23-Team-126\files\ASIANPAINT.csv",
               'BAJAJ-AUTO':r"C:\Users\Suresh\OneDrive\Desktop\Clon_1\HTF23-Team-126\files\BAJAJ-AUTO.csv",
               'HDFC':r"C:\Users\Suresh\OneDrive\Desktop\Clon_1\HTF23-Team-126\files\HDFC.csv",
               'HDFCBANK':r"C:\Users\Suresh\OneDrive\Desktop\Clon_1\HTF23-Team-126\files\HDFCBANK.csv",
               'ICICIBANK':r"C:\Users\Suresh\OneDrive\Desktop\Clon_1\HTF23-Team-126\files\ICICIBANK.csv",
               'INDUSINDBK':r"C:\Users\Suresh\OneDrive\Desktop\Clon_1\HTF23-Team-126\files\INDUSINDBK.csv",
               'KOTAKBANK':r"C:\Users\Suresh\OneDrive\Desktop\Clon_1\HTF23-Team-126\files\KOTAKBANK.csv",
                'TATAMOTORS':r"C:\Users\Suresh\OneDrive\Desktop\Clon_1\HTF23-Team-126\files\TATAMOTORS.csv",
                'TATASTEEL':r"C:\Users\Suresh\OneDrive\Desktop\Clon_1\HTF23-Team-126\files\TATASTEEL.csv"
}
def stock_price_prediction(stock_symbol):
    global symbol_dict
    try:
       
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
    global symbol_dict
    sym = symbol_dict[symbol]
    df = pd.read_csv(sym)
    
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
company_name = get_company(symbol)
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
