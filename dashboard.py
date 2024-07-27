import pandas as pd
import streamlit as st 
import numpy as np

sheet = pd.read_html("https://www.cbssports.com/olympics/news/2024-paris-olympics-medal-count-tracker-for-how-many-gold-silver-bronze-medals-usa-each-country-has-won/")
sheet = sheet[0]

sheet["SCORE"] = sheet["GOLD"]*3+sheet["SILVER"]*2+sheet["BRONZE"]
sheet["COUNTRY"] = sheet["COUNTRY"].str.split('  ', 1).str[1]
sheet = sheet[["COUNTRY","GOLD","SILVER","BRONZE","SCORE"]]

country_to_person = {
    'United States': 'Foster', 'France': 'Foster', 'Uzbekistan': 'Foster', 'Bulgaria': 'Foster', 'Spain': 'Foster', 'Poland': 'Foster',
    'Russia': 'Natalie', 'Canada': 'Natalie', 'South Korea': 'Natalie', 'Norway': 'Natalie', 'Denmark': 'Natalie', 'Turkey': 'Natalie',
    'Serbia': 'Connor', 'Georgia': 'Connor', 'Jamaica': 'Connor', 'Czech Republic': 'Connor', 'Netherlands': 'Connor', 'Japan': 'Connor',
    'Belgium': 'Sara', 'Greece': 'Sara', 'Sweden': 'Sara', 'Australia': 'Sara', 'Germany': 'Sara', 'Cuba': 'Sara',
    'China': 'Ken', 'Taiwan': 'Ken', 'Iran': 'Ken', 'Italy': 'Ken', 'Switzerland': 'Ken', 'Hungary': 'Ken',
    'Great Britain': 'Zoe', 'New Zealand': 'Zoe', 'Croatia': 'Zoe', 'Brazil': 'Zoe', 'Kenya': 'Zoe', 'Slovenia': 'Zoe'
}

# Map the COUNTRY column to person names
sheet['PERSON'] = sheet['COUNTRY'].map(country_to_person)

# Group by PERSON and sum the SCORE, GOLD, SILVER, and BRONZE columns
person_scores = sheet.groupby('PERSON').agg({'SCORE': 'sum', 'GOLD': 'sum', 'SILVER': 'sum', 'BRONZE': 'sum'}).reset_index()


# Display the result
st.write(person_scores.sort_values(by="SCORE",ascending = False))
st.write(sheet.sort_values(by="SCORE",ascending = False))
