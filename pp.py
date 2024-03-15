import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json
import requests
import psycopg2
from PIL import Image

# Data Frame Creation

# SQL Connection

mydb = psycopg2.connect(host="localhost", user="postgres", password="password", port="5432", database="phonepe")
cursor = mydb.cursor()

# Aggregated Insurance DataFrame

cursor.execute("select * from aggregated_insurance;")
mydb.commit()
table1 = cursor.fetchall()

Aggre_insurance = pd.DataFrame(table1,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

# Aggregated Transaction DataFrame

cursor.execute("select * from aggregated_transaction;")
mydb.commit()
table2 = cursor.fetchall()

Aggre_transaction = pd.DataFrame(table2,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

# Aggregated User DataFrame

cursor.execute("select * from aggregated_user;")
mydb.commit()
table3 = cursor.fetchall()

Aggre_user = pd.DataFrame(table3,columns=("States","Years","Quarter","Brands","Transaction_count","Percentage"))

# Map Insurance DataFrame

cursor.execute("select * from map_insurance;")
mydb.commit()
table4 = cursor.fetchall()

map_insurance = pd.DataFrame(table4,columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

# Map Transaction DataFrame

cursor.execute("select * from map_transaction;")
mydb.commit()
table5 = cursor.fetchall()

map_transaction = pd.DataFrame(table5,columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

# Map User DataFrame

cursor.execute("select * from map_user;")
mydb.commit()
table6 = cursor.fetchall()

map_user = pd.DataFrame(table6,columns=("States","Years","Quarter","Districts","Registered_users","App_opens"))

# Top Insurance DataFrame

cursor.execute("select * from top_insurance;")
mydb.commit()
table7 = cursor.fetchall()

top_insurance = pd.DataFrame(table7,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))

# Top Transaction DataFrame

cursor.execute("select * from top_transaction;")
mydb.commit()
table8 = cursor.fetchall()

top_transaction = pd.DataFrame(table8,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))

# Top User DataFrame

cursor.execute("select * from top_user;")
mydb.commit()
table9 = cursor.fetchall()

top_user = pd.DataFrame(table9,columns=("States","Years","Quarter","Pincodes","RegisteredUsers"))

def Transaction_amount_amount_Y(df,year):
    tacy=df[df["Years"]==year]
    tacy.reset_index(drop=True,inplace=True)

    tacyg=tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
         fig_amount=px.bar(tacyg,x="States",y="Transaction_amount",title=f"{year} Transaction Amount",
                    color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
         st.plotly_chart(fig_amount)

    with col2:
        fig_count=px.bar(tacyg,x="States",y="Transaction_count",title=f"{year} Transaction Count",
                    color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
        st.plotly_chart(fig_count)
    
    col1,col2=st.columns(2)
    with col1:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1=px.choropleth(tacyg,geojson=data1,locations=states_name,featureidkey="properties.ST_NM",
                                color="Transaction_amount",color_continuous_scale="rainbow",
                                range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].min()),
                                hover_name="States",title=f"{year} Transaction Amount",fitbounds="locations",
                                height=600,width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2=px.choropleth(tacyg,geojson=data1,locations=states_name,featureidkey="properties.ST_NM",
                                  color="Transaction_count",color_continuous_scale="rainbow",
                                  range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].min()),
                                  hover_name="States",title=f"{year} Transaction Count",fitbounds="locations",
                                  height=600,width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

        return tacy

def Transaction_amount_amount_Y_Q(df, quater):
    tacy = df[df["Quarter"] == quater]
    tacy.reset_index(drop=True, inplace=True)

    tacyg = tacy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(tacyg, x="States", y="Transaction_amount", title=f"{tacy['Years'].min()} Year {quater} Quarter Transaction Amount",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tacyg, x="States", y="Transaction_count", title=f"{tacy['Years'].min()} Year {quater} Quarter Transaction Count",
                           color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)

    # Fetching geojson data
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    states_name = [feature["properties"]["ST_NM"] for feature in data1["features"]]
    states_name.sort()

    # Ensure locations matches the number of unique states in tacyg
    locations = tacyg["States"]

    # Plot choropleth maps
    col1, col2 = st.columns(2)
    with col1:
        fig_india_1 = px.choropleth(tacyg, geojson=data1, locations=locations, featureidkey="properties.ST_NM",
                                    color="Transaction_amount", color_continuous_scale="rainbow",
                                    range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].min()),
                                    hover_name="States",
                                    title=f"{tacy['Years'].min()} Year {quater} Quarter Transaction Amount",
                                    fitbounds="locations",
                                    height=600, width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2 = px.choropleth(tacyg, geojson=data1, locations=locations, featureidkey="properties.ST_NM",
                                    color="Transaction_count", color_continuous_scale="rainbow",
                                    range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].min()),
                                    hover_name="States",
                                    title=f"{tacy['Years'].min()} Year {quater} Quarter Transaction Count",
                                    fitbounds="locations",
                                    height=600, width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return tacy

def Aggre_Tran_Transaction_type(df,state):

    tacy = df[df["States"] == state]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_pie1=px.pie(data_frame=tacyg,names="Transaction_type",values="Transaction_amount",
                        width=600,height=600,title=f"{state.upper()} Transaction Amount",hole=0.5,color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_pie1)

    with col2:
        fig_pie2=px.pie(data_frame=tacyg,names="Transaction_type",values="Transaction_count",
                        width=600,height=600,title=f"{state.upper()} Transaction Count",hole=0.5,color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_pie2)
    
def Aggre_user_plot_1(df,year):
    aguy = df[df["Years"] == year]
    aguy.reset_index(drop=True, inplace=True)

    aguyg = pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1=px.bar(aguyg,x="Brands",y="Transaction_count",title=f"{year} Brands and Transaction Count",
                     width=1000,color_discrete_sequence=px.colors.sequential.Aggrnyl,hover_name="Brands")
    st.plotly_chart(fig_bar_1)
    return aguy

#Aggregated User Analysis
def Aggre_user_plot_2(df,quarter):

    aguyq = df[df["Quarter"] == quarter]
    aguyq.reset_index(drop=True, inplace=True)
    aguyqg=pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)
    fig_bar_1=px.bar(aguyqg,x="Brands",y="Transaction_count",title=f"{quarter} Quarter Brands and Transaction Count",
                        width=1000,color_discrete_sequence=px.colors.sequential.Aggrnyl,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq

# Aggregated User Analysis 3
def Aggre_user_plot_3(df,state):
    auyqs=df[df["States"]==state]
    auyqs.reset_index(drop=True, inplace=True)

    fig_line_1=px.line(auyqs,x="Brands",y="Transaction_count",hover_data=["Percentage"],
                    title=f"{state} Brands, Transaction Count, Percentage",
                        width=1000,color_discrete_sequence=px.colors.sequential.Aggrnyl,markers=True)

    st.plotly_chart(fig_line_1)
# Map Insurance District
def Map_insur_District(df,state):

    tacy = df[df["States"] == state]
    tacy.reset_index(drop=True, inplace=True)

    tacyg=tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_bar1=px.bar(data_frame=tacyg,x="Transaction_amount",y="Districts",orientation="h",
                        title=f"{state} District and Transaction Amount",color_discrete_sequence=px.colors.sequential.Aggrnyl)
                        
        st.plotly_chart(fig_bar1)
    with col2:
        fig_bar2=px.bar(data_frame=tacyg,x="Transaction_count",y="Districts",orientation="h",
                        title=f"{state} District and Transaction Count",color_discrete_sequence=px.colors.sequential.Aggrnyl)
                        
        st.plotly_chart(fig_bar2)

        return tacy
# Map user plot 1
def map_user_plot_1(df,year):
    muy = df[df["Years"] == year]
    muy.reset_index(drop=True, inplace=True)

    muyg = muy.groupby("States")[["Registered_users","App_opens"]].sum()
    muyg.reset_index(inplace=True)

    fig_line_1=px.line(muyg,x="States",y=["Registered_users","App_opens"],
                    title=f"{year} Year Registered User and App Opens",
                        width=1000,height= 800,markers=True)
    st.plotly_chart(fig_line_1)

    return muy
# Map user plot 2
def map_user_plot_2(df,quarter):
    muyq = df[df["Quarter"] == quarter]
    muyq.reset_index(drop=True, inplace=True)

    muyqg = muyq.groupby("States")[["Registered_users","App_opens"]].sum()
    muyqg.reset_index(inplace=True)

    fig_line_1=px.line(muyqg,x="States",y=["Registered_users","App_opens"],
                    title=f"{df['Years'].min()} Year {quarter} Quarter Registered User and App Opens",
                        width=1000,height= 800,markers=True,color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muyq
# Map User Plot 3
def map_user_plot_3(df,states):
    muyqs = df[df["States"] == states]
    muyqs.reset_index(drop=True, inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_map_user_bar_1=px.bar(data_frame=muyqs,x="Registered_users",y="Districts",orientation="h",
                                title=f"{states} Registered Users",height=800,color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2: 
        fig_map_user_bar_2=px.bar(data_frame=muyqs,x="App_opens",y="Districts",orientation="h",
                                title=f"{states} App Opens",height=800,color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_2)
# Top Insurance Plot 1
def Top_insur_plot_1(df,state):
    tiy = df[df["States"] == state]
    tiy.reset_index(drop=True, inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_top_insur_bar_1=px.bar(data_frame=tiy,x="Quarter",y="Transaction_amount",hover_data="Pincodes",
                                title="Transaction Amount",height=500,color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_top_insur_bar_1)
    with col2:
        fig_top_insur_bar_2=px.bar(data_frame=tiy,x="Quarter",y="Transaction_count",hover_data="Pincodes",
                                title="Transaction Count",height=500,color_discrete_sequence=px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_insur_bar_2)   
        return tiy
# Top User Plot 1
def top_user_plot_1(df,year):
    tuy=df[df["Years"]==year]
    tuy.reset_index(drop=True, inplace=True)

    tuyg=pd.DataFrame(tuy.groupby(["States" , "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace=True)
    fig_top_plot_1=px.bar(data_frame=tuyg,x="States",y="RegisteredUsers",color="Quarter",width=1000,height=800,
                        color_discrete_sequence=px.colors.sequential.Burgyl,hover_name="States",
                        title=f"{year} Year Registered Users")
    st.plotly_chart(fig_top_plot_1)

    return tuy
# Top User Plot 2
def top_user_plot_2(df,state):
    tuys=df[df["States"] == state]
    tuys.reset_index(drop=True, inplace=True)

    fig_top_plot_2=px.bar(data_frame=tuys,x="Quarter",y="RegisteredUsers",title="Registered Users, Pincodes, Quarter",
                        width=1000,height=800,color="RegisteredUsers",hover_data="Pincodes",
                        color_continuous_scale=px.colors.sequential.Rainbow_r)                    
    st.plotly_chart(fig_top_plot_2)

# SQL Connection

def top_chart_transaction_amount(table_name):
    mydb = psycopg2.connect(host="localhost", user="postgres", password="password", port="5432", database="phonepe")
    cursor = mydb.cursor()

    # plot 1
    query1=f'''select states, sum(transaction_amount) as transaction_amount from {table_name} group by states order by transaction_amount desc limit 10; '''

    cursor.execute(query1)
    table=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table,columns=('states','transaction_amount'))
    col1, col2 = st.columns(2)
    with col1:
        fig_amount=px.bar(df_1,x="states",y="transaction_amount",title="Top 10 states with highest transaction amount",hover_name="states",
                        height=500,width=500,color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_amount)

    # plot 2
    query2=f'''select states, sum(transaction_amount) as transaction_amount from {table_name} group by states order by transaction_amount limit 10; '''

    cursor.execute(query2)
    table2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table2,columns=('states','transaction_amount'))


    with col2:
        fig_amount2=px.bar(df_2,x="states",y="transaction_amount",title="Top 10 states with lowest transaction amount",hover_name="states",
                        height=500,width=500,color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_amount2)

    #plot 3

    query3 =f'''SELECT states, AVG(transaction_amount) AS avg_transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY avg_transaction_amount;'''

    cursor.execute(query3)
    table3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table3,columns=('states','transaction_amount'))

    fig_amount3=px.bar(df_3,x="transaction_amount",y="states",title="Average Amount of transaction",hover_name="states",orientation="h",
                    height=500,width=1000)
    st.plotly_chart(fig_amount3)

def top_chart_transaction_count(table_name):
    mydb = psycopg2.connect(host="localhost", user="postgres", password="password", port="5432", database="phonepe")
    cursor = mydb.cursor()

    # plot 1
    query1=f'''select states, sum(transaction_count) as transaction_count from {table_name} group by states order by transaction_count desc limit 10; '''

    cursor.execute(query1)
    table=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table,columns=('states','transaction_count'))

    col1,col2=st.columns(2)
    with col1:

        fig_amount=px.bar(df_1,x="states",y="transaction_count",title="Top 10 states with highest transaction count",hover_name="states",
                        height=500,width=500,color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_amount)

    # plot 2
    query2=f'''select states, sum(transaction_count) as transaction_count from {table_name} group by states order by transaction_count limit 10; '''

    cursor.execute(query2)
    table2=cursor.fetchall()
    mydb.commit()

    with col2:
        df_2=pd.DataFrame(table2,columns=('states','transaction_count'))

        fig_amount2=px.bar(df_2,x="states",y="transaction_count",title="Top 10 states with lowest transaction count",hover_name="states",
                        height=500,width=500,color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_amount2)

    #plot 3

    query3 =f'''SELECT states, AVG(transaction_count) AS avg_transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY avg_transaction_count;'''

    cursor.execute(query3)
    table3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table3,columns=('states','transaction_count'))

    fig_amount3=px.bar(df_3,x="transaction_count",y="states",title="Average Amount of transaction count",hover_name="states",orientation="h",
                    height=500,width=1000)
    st.plotly_chart(fig_amount3)

# from qn 7 to 10

def top_chart_registered_user(table_name,state):
    mydb = psycopg2.connect(host="localhost", user="postgres", password="password", port="5432", database="phonepe")
    cursor = mydb.cursor()

    # plot 1
    query1= f'''select districts, sum(registeredusers) as registeredusers
                from {table_name}
                where states='{state}'
                group by districts
                order by registeredusers desc
                limit 10;'''

    cursor.execute(query1)
    table=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table,columns=('Districts','Registeredusers'))

    col1,col2=st.columns(2)

    with col1:

        fig_amount=px.bar(df_1,x="Districts",y="Registeredusers",title="Top 10 Districts with Registered users",hover_name="Districts",
                        height=500,width=500,color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_amount)

    # plot 2
    query2= f'''select districts, sum(registeredusers) as registeredusers
                from {table_name}
                where states='{state}'
                group by districts
                order by registeredusers
                limit 10;'''
    
    cursor.execute(query2)
    table2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table2,columns=('Districts','Registeredusers'))

    with col2:

        fig_amount2=px.bar(df_2,x="Districts",y="Registeredusers",title="Top 10 Districts with lowest Registered users",hover_name="Districts",
                        height=500,width=500,color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_amount2)

    #plot 3

    query3 =f'''select districts, avg(registeredusers) as registeredusers
                from {table_name}
                where states='{state}'
                group by districts
                order by registeredusers;'''

    cursor.execute(query3)
    table3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table3,columns=('Districts','Registeredusers'))

    fig_amount3=px.bar(df_3,x="Registeredusers",y="Districts",title="Average of Registered Users",hover_name="Districts",orientation="h",
                    height=500,width=500)
    st.plotly_chart(fig_amount3)

#qn 9
# SQL Connection

def top_chart_appopens(table_name,state):
    mydb = psycopg2.connect(host="localhost", user="postgres", password="password", port="5432", database="phonepe")
    cursor = mydb.cursor()

    # plot 1
    query1= f'''select districts, sum(appopens) as appopens
                from {table_name}
                where states='{state}'
                group by districts
                order by appopens desc
                limit 10;'''

    cursor.execute(query1)
    table=cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table,columns=('Districts','appopens'))

    col1,col2=st.columns(2)

    with col1:

        fig_amount=px.bar(df_1,x="Districts",y="appopens",title="Top 10 Districts with App Opens",hover_name="Districts",
                        height=500,width=500,color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_amount)

    # plot 2
    query2= f'''select districts, sum(appopens) as appopens
                from {table_name}
                where states='{state}'
                group by districts
                order by appopens
                limit 10;'''
    
    cursor.execute(query2)
    table2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table2,columns=('Districts','appopens'))

    with col2:
        fig_amount2=px.bar(df_2,x="Districts",y="appopens",title="Top 10 Districts with lowest App Opens",hover_name="Districts",
                        height=500,width=500,color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_amount2)

    #plot 3

    query3 =f'''select districts, avg(appopens) as appopens
                from {table_name}
                where states='{state}'
                group by districts
                order by appopens;'''

    cursor.execute(query3)
    table3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table3,columns=('Districts','appopens'))

    fig_amount3=px.bar(df_3,x="appopens",y="Districts",title="Average of App Opens",hover_name="Districts",orientation="h",
                    height=500,width=500)
    st.plotly_chart(fig_amount3)
# qn 10
# SQL Connection

def registered_user_top_chart(table_name):
    mydb = psycopg2.connect(host="localhost", user="postgres", password="password", port="5432", database="phonepe")
    cursor = mydb.cursor()

    # plot 1
    query1= f'''select states,sum(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers desc
                limit 10;'''

    cursor.execute(query1)
    table=cursor.fetchall()
    mydb.commit()

    col1,col2=st.columns(2)

    with col1:
        df_1=pd.DataFrame(table,columns=('states','registeredusers'))

        fig_amount=px.bar(df_1,x="states",y="registeredusers",title="Top 10 Registered Users",hover_name="states",
                        height=500,width=500,color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_amount)

    # plot 2
    query2= f'''select states,sum(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers
                limit 10;'''
    
    cursor.execute(query2)
    table2=cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table2,columns=('states','registeredusers'))

    with col2:

        fig_amount2=px.bar(df_2,x="states",y="registeredusers",title="Last 10 Registered Users",hover_name="states",
                        height=500,width=500,color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_amount2)

    #plot 3

    query3 =f'''select states,avg(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers;'''

    cursor.execute(query3)
    table3=cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table3,columns=('states','registeredusers'))

    fig_amount3=px.bar(df_3,x="registeredusers",y="states",title="Average of App Opens",hover_name="states",orientation="h",
                    height=500,width=500)
    st.plotly_chart(fig_amount3)

# Streamlit app

st.set_page_config(layout="wide")
st.title("Phonepe Pulse Data Analysis")

with st.sidebar:

    selected = option_menu(
        menu_title=None,
        options=["Home", "Data Exploration", "Top Charts"],
        icons=["house", "bar-chart", "geo"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Home":

    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.video("https://www.youtube.com/watch?v=yKvAS0p-qbQ")

    col3,col4= st.columns(2)
    
    with col3:
        st.video("https://www.youtube.com/watch?v=yKvAS0p-qbQ")

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.video("https://www.youtube.com/watch?v=yKvAS0p-qbQ")


    






elif selected == "Data Exploration":

    tab1,tab2,tab3 = st.tabs(["Aggregaed Analysis", "Map Analysis", "Top Analysis"])

    with tab1:

        method = st.radio("Select the Method",["Insurance Analysis","Transaction Analysis","User Analysis"],key = "1")

        if method == "Insurance Analysis":

            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",Aggre_insurance["Years"].min(),Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())
            tac_Y = Transaction_amount_amount_Y(Aggre_insurance,years)

            col1,col2=st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Transaction_amount_amount_Y_Q(tac_Y,quarters)



        elif method == "Transaction Analysis":

            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
            Aggre_tran_tac_Y = Transaction_amount_amount_Y(Aggre_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",Aggre_tran_tac_Y["States"].unique(),key='2')

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter",Aggre_tran_tac_Y["Quarter"].min(),Aggre_tran_tac_Y["Quarter"].max(),Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q=Transaction_amount_amount_Y_Q(Aggre_tran_tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",Aggre_tran_tac_Y["States"].unique(),key="3")

            Aggre_Tran_Transaction_type(Aggre_tran_tac_Y,states)

        elif method == "User Analysis":

            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",Aggre_user["Years"].min(),Aggre_user["Years"].max(),Aggre_user["Years"].min())
            Aggre_user_Y = Aggre_user_plot_1(Aggre_user,years)

            col1,col2=st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q=Aggre_user_plot_2(Aggre_user_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",Aggre_tran_tac_Y_Q["States"].unique(),key='4')

            Aggre_user_plot_3(Aggre_tran_tac_Y_Q,states)
    
    with tab2:

        method2 = st.radio("Select the Method",["Map Insurance","Map Transaction","Map User"],key = "5")
        if method2 == "Map Insurance":

            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",map_insurance["Years"].min(),map_insurance["Years"].max(),map_insurance["Years"].min(),key="6")
            map_insur_tac_Y = Transaction_amount_amount_Y(map_insurance,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",map_insur_tac_Y["States"].unique(),key='7')

            Map_insur_District(map_insur_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter",map_insur_tac_Y["Quarter"].min(),map_insur_tac_Y["Quarter"].max(),map_insur_tac_Y["Quarter"].min(),key="23")
            map_insur_tac_Y_Q=Transaction_amount_amount_Y_Q(map_insur_tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",map_insur_tac_Y_Q["States"].unique(),key="376")

            Map_insur_District(map_insur_tac_Y_Q,states)            

        elif method2 == "Map Transaction":
            
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",map_transaction["Years"].min(),map_transaction["Years"].max(),map_transaction["Years"].min(),key="66")
            map_tran_tac_Y = Transaction_amount_amount_Y(map_transaction,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",map_tran_tac_Y["States"].unique(),key='7')

            Map_insur_District(map_tran_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter",map_tran_tac_Y["Quarter"].min(),map_tran_tac_Y["Quarter"].max(),map_tran_tac_Y["Quarter"].min(),key="23")
            map_tran_tac_Y_Q=Transaction_amount_amount_Y_Q(map_tran_tac_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",map_tran_tac_Y_Q["States"].unique(),key="3")

            Map_insur_District(map_tran_tac_Y_Q,states)       

        elif method2 == "Map User":
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",map_user["Years"].min(),map_user["Years"].max(),map_user["Years"].min(),key="45")
            map_user_Y = map_user_plot_1(map_user,years)
            
            col1,col2=st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter",map_user_Y["Quarter"].min(),map_user_Y["Quarter"].max(),map_user_Y["Quarter"].min(),key="53")
            map_user_Y_Q=map_user_plot_2(map_user_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",map_user_Y_Q["States"].unique(),key="33")

            map_user_plot_3(map_user_Y_Q,states)

    with tab3:

        method3 = st.radio("Select the Method",["Top Insurance","Top Transaction","Top User"],key = "9")

        if method3 == "Top Insurance":

            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",top_insurance["Years"].min(),top_insurance["Years"].max(),top_insurance["Years"].min(),key="689")
            Top_insur_tac_Y = Transaction_amount_amount_Y(top_insurance,years)
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",Top_insur_tac_Y["States"].unique(),key="34")

            Top_insur_plot_1(Top_insur_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter",Top_insur_tac_Y["Quarter"].min(),Top_insur_tac_Y["Quarter"].max(),Top_insur_tac_Y["Quarter"].min(),key="24")
            Top_insur_tac_Y_Q=Transaction_amount_amount_Y_Q(Top_insur_tac_Y,quarters)


        elif method3 == "Top Transaction":
        
            col1,col2 = st.columns(2)
            with col1:
                years = st.slider("Select the Year",top_transaction["Years"].min(),top_transaction["Years"].max(),top_transaction["Years"].min(),key="123")
            Top_tran_tac_Y = Transaction_amount_amount_Y(top_transaction,years)
            
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",Top_tran_tac_Y["States"].unique(),key="345")

            Top_insur_plot_1(Top_tran_tac_Y,states)

            col1,col2=st.columns(2)
            with col1:

                quarters = st.slider("Select the Quarter",Top_tran_tac_Y["Quarter"].min(),Top_tran_tac_Y["Quarter"].max(),Top_tran_tac_Y["Quarter"].min(),key="456")
            Top_tran_tac_Y_Q=Transaction_amount_amount_Y_Q(Top_tran_tac_Y,quarters)
            
        
        elif method3 == "Top User":

            col1,col2=st.columns(2)
            with col1:
                years = st.slider("Select the Year",top_user["Years"].min(),top_user["Years"].max(),top_user["Years"].min(),key="567")
            Top_user_Y = top_user_plot_1(top_user,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State",Top_user_Y["States"].unique(),key="678")

            top_user_plot_2(Top_user_Y,states)
            

            
    

elif selected == "Top Charts":
    
    questions =st.selectbox("Select the Question",[
        "1. Transaction Amount and Count of Aggregated Insurance",
        "2. Transaction Amount and Count of Map Insurance",
        "3. Transaction Amount and Count of Top Insurance",
        "4. Transaction Amount and Count of Aggregated Transaction",
        "5. Transaction Amount and Count of Map Transaction",
        "6. Transaction Amount and Count of Top Transaction",
        "7. Transaction Count of Aggregated User",
        "8. Registered users of Map User",
        "9. App opens of Map User",
        "10. Registered users of Top User"
        ])
    
    if questions == "1. Transaction Amount and Count of Aggregated Insurance":

        st.subheader("Transaction Amount")
        top_chart_transaction_amount("aggregated_insurance")
        st.subheader("Transaction Count")
        top_chart_transaction_count("aggregated_insurance")

    elif questions == "2. Transaction Amount and Count of Map Insurance":

        st.subheader("Transaction Amount")
        top_chart_transaction_amount("map_insurance")
        st.subheader("Transaction Count")
        top_chart_transaction_count("map_insurance")

    elif questions == "3. Transaction Amount and Count of Top Insurance":

        st.subheader("Transaction Amount")
        top_chart_transaction_amount("top_insurance")
        st.subheader("Transaction Count")
        top_chart_transaction_count("top_insurance")

    elif questions == "4. Transaction Amount and Count of Aggregated Transaction":

        st.subheader("Transaction Amount")
        top_chart_transaction_amount("aggregated_transaction")
        st.subheader("Transaction Count")
        top_chart_transaction_count("aggregated_transaction")

    elif questions == "5. Transaction Amount and Count of Map Transaction":

        st.subheader("Transaction Amount")
        top_chart_transaction_amount("map_transaction")
        st.subheader("Transaction Count")
        top_chart_transaction_count("map_transaction")

    elif questions == "6. Transaction Amount and Count of Top Transaction":

        st.subheader("Transaction Amount")
        top_chart_transaction_amount("top_transaction")
        st.subheader("Transaction Count")
        top_chart_transaction_count("top_transaction")

    elif questions == "7. Transaction Count of Aggregated User":

        st.subheader("Transaction Count")
        top_chart_transaction_count("aggregated_user")

    elif questions == "8. Registered users of Map User":

        states=st.selectbox("Select the State",map_user["States"].unique())

        st.subheader("Registered users")
        top_chart_registered_user("map_user",states)
    
    elif questions == "9. App opens of Map User":

        states=st.selectbox("Select the State",map_user["States"].unique())

        st.subheader("App opens")
        top_chart_appopens("map_user",states)

    elif questions == "10. Registered users of Top User":

 #       states=st.selectbox("Select the State",top_user["States"].unique())

        st.subheader("Registered users")
        registered_user_top_chart("top_user")



