import pandas as pd
import mysql.connector as con
import snscrape.modules.twitter as snt
import streamlit as st


class TwitterScrapper():

    def __init__(self):
        pass

    df = pd.DataFrame()

    def twitter_scrapper(self, keyword, since_date, until_date, limit):

        date = []
        username = []
        tweets = []

        for tweet in snt.TwitterSearchScraper(keyword + f" since:{since_date} until:{until_date}").get_items():

            if len(tweets) == limit:
                break
            else:
                date.append(tweet.date)
                username.append(tweet.user.username)
                tweets.append(tweet.rawContent)

        TwitterScrapper.df["date_time"], TwitterScrapper.df["username"], TwitterScrapper.df[
            "tweet"] = date, username, tweets

        TwitterScrapper.df["date_time"] = TwitterScrapper.df["date_time"].astype(
            "str")
        TwitterScrapper.df["tweet"] = TwitterScrapper.df["tweet"].astype("str")

        st.write(TwitterScrapper.df)

    def push_to_sql(self):

        mydb = con.connect(host="localhost",
                           user="root",
                           password="Password@12",
                           database="twitter")

        data = TwitterScrapper.df

        mycursor = mydb.cursor()

        sql = "insert into tweets(date_time, user_name, tweet) VALUES(%s, %s, %s)"

        for i in range(data.shape[0]):
            values = tuple(data.loc[i].values)
            mycursor.execute(sql, values)
            mydb.commit()

    # dataframe file
    def dataframe(self):
        return TwitterScrapper.df.to_csv(index=False)

    # json file
    def json(self):
        return TwitterScrapper.df.to_json(orient="records")

twitter_object = TwitterScrapper()