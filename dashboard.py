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
standings = pd.read_html("https://www.baseball-reference.com/leagues/majors/2022-standings.shtml")
for i in [standings[1]]:
    i.set_index("Tm",inplace = True)
    i["W-L%"] = i["W-L%"]*100
    st.dataframe(i.style.format({"W-L%":"{:.1f}"}))
s = pd.read_html("https://www.baseball-reference.com/leagues/majors/2022-playoff-odds.shtml")
s = s[1].droplevel(0,axis = 1)
s = s[s["Tm"] == "Kansas City Royals"].iloc[0]
col1, col2 = st.columns(2)
col1.metric("xWins (90% interval)",value = float(s["W"][2]),delta = str(int(s["Worst"][0:2])) + " | " + str(int(s["Best"][0:2])),delta_color = "off")
col2.metric("Playoff Odds (7D +/-)",value = (s["Post"]),delta = (s["7 Days"]))
s = pd.read_html("https://www.baseball-reference.com/leagues/majors/2022.shtml")[0]
r = s[s["Tm"]=="Kansas City Royals"].iloc[0]
l = s[s["Tm"]=="League Average"].iloc[0]
col1.metric("RS/G",r["R/G"],delta = round(float(r["R/G"]) - float(l["R/G"]),2))
col1.metric("H Age",r["BatAge"],delta = round(float(r["BatAge"]) - float(l["BatAge"]),2),delta_color = "inverse")
col1.metric("AVG",r["BA"],delta = round(float(r["BA"]) - float(l["BA"]),3))
col1.metric("OBP",r["OBP"],delta = round(float(r["OBP"]) - float(l["OBP"]),3))
col1.metric("SLG",r["SLG"],delta = round(float(r["SLG"]) - float(l["SLG"]),3))
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
r = s[s["Tm"]=="Kansas City Royals"].iloc[0]
l = s[s["Tm"]=="League Average"].iloc[0]
col2.metric("RA/G",r["RA/G"],delta = round(float(r["RA/G"]) - float(l["RA/G"]),2),delta_color="inverse")
col2.metric("P Age",r["PAge"],delta = round(float(r["PAge"]) - float(l["PAge"]),2),delta_color="inverse")
col2.metric("K/9",r["SO9"],delta = round(float(r["SO9"]) - float(l["SO9"]),2))
col2.metric("BB/9",r["BB9"],delta = round(float(r["BB9"]) - float(l["BB9"]),2),delta_color="inverse")
col2.metric("HR/9",r["HR9"],delta = round(float(r["HR9"]) - float(l["HR9"]),2),delta_color="inverse")


#POLITICS
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