import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(layout="wide")

@st.cache
def load_data():
    df = pd.read_csv('data/appstore_games.csv')
    df['Original Release Date'] = pd.to_datetime(df['Original Release Date'], format = '%d/%m/%Y')
    df['Current Version Release Date'] = pd.to_datetime(df['Current Version Release Date'], format = '%d/%m/%Y')
    return df

df = load_data()

def get_release():
    original_release=df[['Original Release Date','Current Version Release Date','Name']]
    original_release[['Original Release Date','Current Version Release Date']]=original_release[['Original Release Date','Current Version Release Date']].apply(pd.to_datetime)
    original_release['Release_Year']=pd.DatetimeIndex(original_release['Original Release Date']).year
    original_release['Current_Version_Year']=pd.DatetimeIndex(original_release['Current Version Release Date']).year
    return original_release

st.title("Evaluation of Every Mobile strategy game on appstore")
st.sidebar.image('images/icon_appstore.png', width=200)

def home():
    pass

def page1():
    pass

def page2():
    x = st.slider('Choose the number of rows of display: ', min_value=10, max_value=df.shape[0])
    st.write(df.head(x))

def page3():
    st.subheader('dataset summary')
    st.write(df.describe())
    st.subheader("Dimensions of Dataset")
    st.write(f"Rows: {df.shape[0]}")
    st.write(f"Columns: {df.shape[1]}")
    st.subheader('Scatter matrix')
    st.plotly_chart(px.scatter_matrix(df,dimensions=['Average User Rating','User Rating Count', 'Size']))

def page4():
    st.subheader("Average User Rating")
    st.plotly_chart(px.histogram(df, 'Average User Rating'))
    fig, ax = plt.subplots(1,1, figsize=(12, 7), dpi=72)
    sns.regplot(data=df, x='Price', y='Average User Rating', ax=ax)
    st.subheader("Price and Rating")
    st.pyplot(fig)
    st.subheader("Average User Rating Over the years")
    temp_df1 = df.groupby(df['Original Release Date'].dt.year).mean().reset_index()
    trace1 = go.Scatter(
                        x=temp_df1['Original Release Date'], 
                        y=temp_df1['Average User Rating'], 
                        name="Original Release", 
                        marker=dict(color = '#FFB3F7',
                                 line=dict(color='#000000',width=1)))
    temp_df2 = df.groupby(df['Current Version Release Date'].dt.year).mean().reset_index()
    trace2 = go.Scatter(
                        x=temp_df2['Current Version Release Date'], 
                        y=temp_df2['Average User Rating'], 
                        name="Last Version", 
                        marker=dict(color = '#47E0FF',
                                 line=dict(color='#000000',width=1)))
    layout = go.Layout(hovermode='closest', 
                       title = 'Average User Rating over the years', 
                       xaxis = dict(title = 'Year'), 
                       yaxis = dict(title = 'Average User Rating'), 
                       template= "plotly_dark")
    fig = go.Figure(data = [trace1, trace2], layout=layout)
    st.plotly_chart(fig)

# def page5():

def page6():
    age_stats=df.groupby('Age Rating').agg({'Price':'mean','Average User Rating':'mean','User Rating Count':'mean','Name':'count'}).reset_index(drop=False)
    age_stats=age_stats.rename(columns={'Name':'Count'})
    st.plotly_chart(px.pie(age_stats, 'Age Rating', 'Count'))

def page7():
    top10_count=df[df['User Rating Count']>9000][['Name','Average User Rating','User Rating Count']].sort_values(by='User Rating Count',ascending=False).reset_index(drop=True).head(10)
    fig=px.bar(top10_count,x='Name',y='User Rating Count',title='Top Ten User Rating Count',hover_data=['Average User Rating'],labels={'pop':'Average User Rating'},color='Average User Rating')
    st.plotly_chart(fig)

def page8():
    temp = list(df.Languages.dropna())
    temp = [i.split(', ') for i in temp]
    langs = []
    for i in temp:
        langs += i
    lang_dict = {}
    for i in set(langs):
        lang_dict[i] = langs.count(i)
    st.plotly_chart(px.bar(x=lang_dict.keys(), y=lang_dict.values()))
    st.write("Most of the apps are available in English")

def page9():
    st.plotly_chart(px.scatter(df, 'Average User Rating', 'Size'))
    st.plotly_chart(px.scatter(df, 'Original Release Date', 'Size'))
    st.write("App size have increased over the years")

def page10():
    st.subheader("Primary Genre")
    st.plotly_chart(px.histogram(df, 'Primary Genre'))
    temp = list(df.Genres.dropna())
    temp = [i.split(', ') for i in temp]
    genres = []
    for i in temp:
        genres += i
    genre_dict = {}
    for i in set(genres):
        genre_dict[i] = genres.count(i)
    st.plotly_chart(px.bar(x=genre_dict.keys(), y=genre_dict.values()))
    st.write("Most of the apps have Genre 'Strategy', Strategy is the most popular Genre")

def page11():
    data = get_release()
    fig = px.histogram(data,x='Release_Year',title='No. Of Games Released Per Year')
    st.plotly_chart(fig)

def page12():
    data = get_release()
    fig = px.histogram(data,x='Current_Version_Year',title='Latest Version Games by Year')
    st.plotly_chart(fig)

def page13():
    pass

options = {
            'Introduction': home,
            'About': page1,
            'View Raw Data': page2,
            'Analysis': page3,
            'Analysis - User Rating': page4,
            # 'Analysis - Analysis Average Rating': page5,
            'Analysis - age': page6,
            'Analysis - In-App purchases': page7,
            'Analysis - languages': page8,
            'Analysis - size': page9,
            'Analysis - genres': page10,
            'Analysis - original release dates': page11,
            'Analysis - current release dates': page12,
            'Conclusion': page13,
        }

menu = st.sidebar.radio("Select an Option", options)
st.header(menu)
options[menu]()
