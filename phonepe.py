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
    pass

elif selected == "Data Exploration":

    tab1,tab2,tab3 = st.tabs(["Aggregaed Analysis", "Map Analysis", "Top Analysis"])

    with tab1:

        method = st.radio("Select the Method",["Insurance Analysis","Transaction Analysis","User Analysis"],key = "1")

        if method == "Insurance Analysis":

            col1,col2 = st.columns(2)
            with col1:
                Years = st.slider("Select the Year",Aggre_insurance["Years"].min(),Aggre_insurance["Years"].max(),Aggre_insurance["Years"].min())
            Transaction_amount_amount_Y(Aggre_insurance,Years)

        elif method == "Transaction Analysis":
            pass

        elif method == "User Analysis":
            pass
    
    with tab2:

        method2 = st.radio("Select the Method",["Insurance Analysis","Transaction Analysis","User Analysis"],key = "2")
        if method2 == "Insurance Analysis":
            pass

        elif method2 == "Transaction Analysis":
            pass

        elif method2 == "User Analysis":
            pass

    with tab3:

        method3 = st.radio("Select the Method",["Insurance Analysis","Transaction Analysis","User Analysis"],key = "3")
        if method3 == "Insurance Analysis":
            pass

        elif method3 == "Transaction Analysis":
            pass
        
        elif method3 == "User Analysis":
            pass
    

elif selected == "Top Charts":
    
    st.subheader("Top Charts")

