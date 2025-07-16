import pandas as pd
import numpy as np
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji


def fetch_stats(selected_user,df):

#Total messages
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
#Total Words
    words=[]
    for message in df['message']:
        words.extend(message.split())
#Total Media Shared
    count = df[df['message'] == "<Media omitted>"].shape[0]
#Links Shared
    extractor = URLExtract()
    links = []

    for message in df['message']:
        for url in extractor.find_urls(message):
            if url.startswith("http://") or url.startswith("https://"):
                links.append(url)

    unique_links = list(set(links))


    return num_messages, len(words),count,len(unique_links)


def most_busy(df):
    x = df['user'].value_counts()
    y = x.head(25)
    return y

def create_wordcloud(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    wc = WordCloud( width=2500,height=1500, min_word_length=10,background_color='white')
    df_wc=wc.generate(df['message'].str.cat(sep=" "))

    return df_wc

#Most Common Words cleaner


import re
import string
from stopwords import get_stopwords
import emoji

def is_only_emoji(word):
    """Returns True if the entire word is only emojis (no letters or digits)."""
    return all(char in emoji.EMOJI_DATA for char in word.strip())

def clean_word_list(df):
    # Load Hindi and English stopwords
    hindi_stops = set(get_stopwords("hi"))
    english_stops = set(get_stopwords("en"))
    all_stops = hindi_stops.union(english_stops)

    def is_valid(word):
        word = word.strip().lower()

        # Remove if word is very short (length <= 2)
        if len(word) <= 2:
            return False

        # Remove if contains only emojis
        if is_only_emoji(word):
            return False

        # Remove if it contains only punctuation
        if all(char in string.punctuation for char in word):
            return False

        # Remove if it contains unwanted special characters
        if re.search(r'[<>&:()\[\]\/]', word):
            return False

        # Remove if it’s in stopwords
        if word in all_stops:
            return False

        return True

    df = df.copy()
    df = df.rename(columns={0: 'word', 1: 'freq'})
    df['clean_word'] = df['word'].astype(str).str.strip().str.lower()
    df = df[df['clean_word'].apply(is_valid)]
    df = df[df['freq'] > 3]  # Optional threshold

    return df.reset_index(drop=True)



def most_common_words(selected_user, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = set(f.read().split())

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'Group_Notification']
    temp = temp[~temp['message'].isin(['<Media omitted>', 'This message was deleted', 'null'])]

    words = []
    for message in temp['message']:
        for w in message.lower().split():
            if w not in stop_words:
                words.append(w)

    newa = pd.DataFrame(Counter(words).most_common(20), columns=["word", "freq"])
    return_df = clean_word_list(newa)
    x=return_df[['word', 'freq']]
    return x

def emoji_helper(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        for char in message:
            if char in emoji.EMOJI_DATA:
                emojis.append(char)

    emojiss = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emojiss.head(10)

def monthly_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()  # here the reset is to cahnge i tin to the data frame

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline
def hourly_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    messages_by_time = df.groupby('month_time').count()['message'].sort_values(ascending=False)
    message_time = messages_by_time.head(30)

    return message_time

def daily_time(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message']
    daily_timeline = daily_timeline.reset_index()

    return daily_timeline


def days_timeline(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    daily_name = df['day_name'].value_counts().reset_index()
    daily_name.columns = ['day_name', 'count']

    return daily_name

def activity_heat_map(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    activity_heat_map = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return activity_heat_map

#chnaged due to the using of  the plotly
# def activity_heat_map(selected_user, df):
#     if selected_user != "Overall":
#         df = df[df['user'] == selected_user]
#
#     # Force correct weekday order
#     day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
#     df['day_name'] = pd.Categorical(df['day_name'], categories=day_order, ordered=True)
#
#     # Create heatmap pivot
#     heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count')
#
#     return heatmap.fillna(0)
#
#
#
