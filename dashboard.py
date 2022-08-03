import streamlit as st
import requests
import pandas as pd
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment

#FINANCIAL MARKETS
st.subheader("Financial")
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

#BASEBALL
st.subheader("Royals")
col1, col2, col3 = st.columns([3,1,1])
standings = pd.read_html("https://www.baseball-reference.com/leagues/majors/2022-standings.shtml")
for i in [standings[1]]:
    i.set_index("Tm",inplace = True)
    i["W-L%"] = i["W-L%"]*100
    col1.dataframe(i.style.format({"W-L%":"{:.1f}"}))
s = pd.read_html("https://www.baseball-reference.com/leagues/majors/2022-playoff-odds.shtml")
s = s[1].droplevel(0,axis = 1)
s = s[s["Tm"] == "Kansas City Royals"].iloc[0]
col2.metric("xWins (90% interval)",value = float(s["W"][2]),delta = str(int(s["Worst"][0:2])) + " | " + str(int(s["Best"][0:2])),delta_color = "off")
col3.metric("Playoff Odds (7D +/-)",value = (s["Post"]),delta = (s["7 Days"]))
s = pd.read_html("https://www.baseball-reference.com/leagues/majors/2022.shtml")[0]
r = s[(s["Tm"]=="Kansas City Royals") | (s["Tm"]=="League Average")]
r.set_index("Tm",inplace = True)
r = r[["BatAge","R/G","BA","OBP","SLG"]]
st.write(r)
response = requests.get("https://www.baseball-reference.com/leagues/majors/2022.shtml")
soup = BeautifulSoup(response.text, 'html.parser')
comments = soup.find_all(string=lambda text: isinstance(text, Comment))
tables = []
for each in comments:
    if 'table' in each:
        try:
            tables.append(pd.read_html(each)[0])
        except:
            continue
s = (tables[-3].loc[1:])
r = s[(s["Tm"]=="Kansas City Royals") | (s["Tm"]=="League Average")]
r.set_index("Tm",inplace = True)
r = r[["PAge","RA/G","SO9","BB9","HR9"]]
st.write(r)

#POLITICS
markets = [7456,7053,7057,6867,6874,6892,7204,7085,7107,7016]
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