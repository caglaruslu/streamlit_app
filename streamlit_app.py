import streamlit as st
from pytrends.request import TrendReq

pytrends = TrendReq()
import pandas as pd
import time
import datetime
from datetime import datetime, date, time
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from parseCountries import parse
from fpdf import FPDF
import base64


def removeRestrictedCharactersAndWhiteSpaces(keywords):

    restricted_characters = ['-', ',', '\'', ')', '(', '[', ']', '{', '}', '.', '*', '?', '_', '@', '!', '$']

    preprocessed_list = []
    
    for keyword in keywords:
    
        clean_keyword = ""
        for char in keyword:
            if char not in restricted_characters:
                clean_keyword += char
        
        white_space_counter = 0
        
        for char in clean_keyword:
            if char == ' ':
                white_space_counter += 1
            else:
                break
        
        clean_keyword = clean_keyword[white_space_counter:]
        
        white_space_counter = 0
        
        for i in range(len(clean_keyword) - 1, 0, -1):
            if clean_keyword[i] == ' ':
                white_space_counter += 1
            else:
                break
        
        if white_space_counter != 0:
            clean_keyword = clean_keyword[:-white_space_counter]
        
        preprocessed_list.append(clean_keyword)
    
    return preprocessed_list
    
    

st.title("PyGtrends🐍🔥")
st.markdown('**Your UK 5 Top & Rising Google Trends Dashboard⚡**') 

# st.markdown("## ** Paste keywords **")

linesDeduped2 = []
MAX_LINES = 5
text2 = st.markdown("UK, Last 3 months trends data at your fingertips, no coding needed😎. To get started:")
text = st.text_area("Paste 1 keyword per line, and hit Get Trends to get your trends data⬇️", height=150, key=1)
#text2 = st.markdown('***Please make sure there are no extra spaces in the beginning or end of each keyword, also no apostrophes or dashes🙏**')
lines = text.split("\n")  # A list of lines
linesList = []
for x in lines:
    linesList.append(x)
linesList = list(dict.fromkeys(linesList))  # Remove dupes
linesList = list(filter(None, linesList))  # Remove empty

if len(linesList) > MAX_LINES:
    st.warning(f"⚠️ Only the first 5 keywords will be reviewed.)")
    linesList = linesList[:MAX_LINES]


country_names, country_codes = parse()
country_names, country_codes = country_names[:243], country_codes[:243]

country = st.selectbox("Your Country", country_names)
st.write(f"You selected " + country)
idx = country_names.index(country)
country_code = country_codes[idx],

st.write(f"Choose Period")

col1, col2, col3, col4 = st.beta_columns(4)

selected_timeframe = ""

year = col1.selectbox("Years from now", ["0", "5"])
month = col2.selectbox("Months from now", ["0", "1", "3"])
day = col3.selectbox("Days from now", ["0", "1", "7"])
hour = col4.selectbox("Hours from now", ["0", "1", "4"])

if year != "0":
    selected_timeframe = "today " + year + "-y"
elif month != "0":
    selected_timeframe = "today " + month + "-m"
elif day != "0":
    selected_timeframe = "now " + day + "-d"
else:
    selected_timeframe = "now " + hour + "-H"

st.write(f"You selected " + year + " year(s), " + month + " month(s), " + day + " day(s), " + hour + " hour(s) from now")


start_execution = st.button("Get Trends! 🤘")



if start_execution:

    if year == "0" and month == "0" and day == "0" and hour == "0":
        st.warning("Please choose a time period")
    else:

        if len(linesList) == 0:
        
            st.warning("Please enter at least 1 keyword.")
            
        else:
        
            linesList = removeRestrictedCharactersAndWhiteSpaces(linesList)
            
            pytrends.build_payload(linesList, timeframe=selected_timeframe, geo=country_code[0])
            related_queries = pytrends.related_queries()
            
            for i in range(len(linesList)):

                st.header("GTrends data for keyword {}: {}".format(i+1, str(linesList[i])))

                c29, c30, c31 = st.beta_columns([6, 2, 6])

                with c29:

                    st.subheader("Top Trends🏆")
                    st.write(related_queries.get(linesList[i]).get("top"))

                with c31:

                    st.subheader("Rising Trends⚡")
                    st.write(related_queries.get(linesList[i]).get("rising"))

            

            st.stop()

            # suggestions = pytrends.suggestions(keyword='dresses')
            # suggestions_df = pd.DataFrame(suggestions)
            # print(suggestions_df.drop(columns= 'mid'))
