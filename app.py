from twitter_scraping import TwitterScrapper
from twitter_scraping import twitter_object
from datetime import date
import streamlit as st
import time
import base64

# heading 
st.header("Twitter Data Scraping App")

# inputs 
keyword = st.text_input("Enter a keyword",key=1)
from_date = st.date_input("Select a start date", date.today(), key=2)
to_date = st.date_input("Select a end date", date.today(), key=3)
limit = st.number_input("enter the number of tweets", step=1, key=4) 

# creating an object
twitter_object = TwitterScrapper()

if st.button("scrape"):
    twitter_object.twitter_scrapper(keyword, from_date, to_date, limit)

if st.button("store in sql"):
    twitter_object.push_to_sql()

    # pop-up message 
    st.success("Data stored in SQL")
    time.sleep(2)

if st.button('Download CSV'):
    csv = twitter_object.dataframe()
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="data.csv">Download CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)

if st.button('Download JSON'):
    json = twitter_object.json()
    b64 = base64.b64encode(json.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="data.json">Download json File</a>'
    st.markdown(href, unsafe_allow_html=True)