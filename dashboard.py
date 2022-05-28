import streamlit as st
import requests
import pandas as pd
import yfinance as yf

tickers = ["TSLA","BTC-USD","VTI","ETH-USD","NFLX", "FB","METV","ESPO"]
pull = yf.download("TSLA VTI BTC-USD ETH-USD NFLX FB METV ESPO", start = "2021-05-01", end = "2080-1-1",interval = "1d", group_by = 'tickers').fillna(method="ffill")
sheet = []
for ti in tickers:
    row = []
    t = pull[ti]
    current = round(t.iloc[-1]["Close"],2)
    od = round(100*((t.iloc[-1]["Close"])/(t.iloc[-2]["Close"])-1),2)
    om = round(100*((t.iloc[-1]["Close"])/(t.iloc[-31]["Close"])-1),2)
    oy = round(100*((t.iloc[-1]["Close"])/(t.iloc[-366]["Close"])-1),2)
    row.append(ti)
    row.append(current)
    row.append(od)
    row.append(om)
    row.append(oy)
    sheet.append(row)
sheet = pd.DataFrame(sheet)
sheet.columns = ["Ticker","Price","1D +/- (%)","1M +/- (%)","1Y +/- (%)"]
sheet = sheet.sort_values(by = "1Y +/- (%)", ascending = False)
sheet.set_index("Ticker",inplace = True)
st.dataframe(sheet.style.format("{:.2f}"))

markets = [7456,7053,7057,6867,7760,7162,7204,7085]

for i in markets:
    try:
        r = requests.get("https://www.predictit.org/api/marketdata/markets/" + str(i)).json()
        name = r["shortName"]
        st.subheader(name)
        sheet = []
        for c in r["contracts"]:
            sheet.append([c["name"],int(c["lastTradePrice"]*100),int((c["lastTradePrice"]-c["lastClosePrice"])*100)])
        sheet = pd.DataFrame(sheet)
        sheet.columns = ["Name","Price","1D Change"]
        sheet.set_index("Name", inplace=True)
        st.write(sheet)
    except:
        st.write(i)