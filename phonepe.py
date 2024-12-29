import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd 
import plotly.express as px
import requests
import json
from PIL import Image



#DataFrame Creation from SQL

#SQL Connection

mydb=psycopg2.connect(host="localhost",
                    user="postgres",
                    password="rihana",
                    database="phonepe_data",
                    port="5432")
cursor=mydb.cursor()


#Aggregated_Insurance_DF

cursor.execute("SELECT * FROM aggregated_insurance")
mydb.commit()
table1=cursor.fetchall()

Aggre_insurance= pd.DataFrame(table1,columns=("State", "Year", "Quarter", "Transaction_type", "Transaction_count",
                                              "Transaction_amount"))


#Aggregated_Transaction_DF

cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table2=cursor.fetchall()

Aggre_transaction= pd.DataFrame(table2,columns=("State", "Year", "Quarter", "Transaction_type", "Transaction_count",
                                              "Transaction_amount"))


#Aggregated_User_DF

cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table3=cursor.fetchall()

Aggre_user= pd.DataFrame(table3,columns=("State", "Year", "Quarter", "Brands", "Transaction_count",
                                              "Percentage"))

#Map_Insurance_DF

cursor.execute("SELECT * FROM map_insurance")
mydb.commit()
table4=cursor.fetchall()

Map_insurance= pd.DataFrame(table4,columns=("State", "Year", "Quarter", "District", "Transaction_count",
                                              "Transaction_amount"))

#Map_Transaction_DF

cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table5=cursor.fetchall()

Map_transaction= pd.DataFrame(table5,columns=("State", "Year", "Quarter", "District", "Transaction_count",
                                              "Transaction_amount"))

#Map_User_DF

cursor.execute("SELECT * FROM map_user")
mydb.commit()
table6=cursor.fetchall()

Map_user= pd.DataFrame(table6,columns=("State", "Year", "Quarter", "District", "RegisteredUser",
                                              "AppOpens"))

#Top_Insurance_DF

cursor.execute("SELECT * FROM top_insurance")
mydb.commit()
table7=cursor.fetchall()

Top_insurance= pd.DataFrame(table7,columns=("State", "Year", "Quarter", "Pincode", "Transaction_count",
                                              "Transaction_amount"))

#Top_Transaction_DF

cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table8=cursor.fetchall()

Top_transaction= pd.DataFrame(table8,columns=("State", "Year", "Quarter", "Pincode", "Transaction_count",
                                              "Transaction_amount"))

#Top_User_DF

cursor.execute("SELECT * FROM top_user")
mydb.commit()
table9=cursor.fetchall()

Top_user= pd.DataFrame(table9,columns=("State", "Year", "Quarter", "Pincode", "RegisteredUser"))

#Function to PLOT for Transaction in Year

def Transaction_amount_count_Y(df,year):

    tacy= df[df["Year"] == year]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)


    col1,col2 = st.columns(2)

    with col1:
        fig_amount_1= px.bar(tacyg, x="State", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl, height=500, width=600)
        st.plotly_chart(fig_amount_1)

    with col2:
        fig_count_1= px.bar(tacyg, x="State", y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                                color_discrete_sequence=px.colors.sequential.Blackbody,height=500, width=600)
        st.plotly_chart(fig_count_1)

    col1,col2 = st.columns(2)

    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                    color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                    range_color= (tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                    hover_name= "State",title = f"{year} TRANSACTION AMOUNT",
                                    fitbounds= "locations",width =400, height= 600)
        fig_india_1.update_geos(visible =False)

        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2= px.choropleth(tacyg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                    color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                    range_color= (tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                    hover_name= "State",title = f"{year} TRANSACTION COUNT",
                                    fitbounds= "locations",width =400, height= 600)
        fig_india_2.update_geos(visible =False)

        st.plotly_chart(fig_india_2)
    return tacy

#Function to PLOT for Transaction in Year- Quarter

def Transaction_amount_count_Y_Q(df,quarter):

    tacy= df[df["Quarter"] == quarter]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2 = st.columns(2)

    with col1:

        fig_amount_2= px.bar(tacyg, x="State", y="Transaction_amount", title=f"{tacy['Year'].min()} YEAR {quarter} QUATER TRANSACTION AMOUNT",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount_2)
    
    with col2:
        fig_count_2= px.bar(tacyg, x="State", y="Transaction_count", title=f"{tacy['Year'].min()} YEAR {quarter} QUATER TRANSACTION COUNT",
                                color_discrete_sequence=px.colors.sequential.Blackbody)
        st.plotly_chart(fig_count_2)


    col1,col2 = st.columns(2)

    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_3= px.choropleth(tacyg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                    color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                    range_color= (tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                    hover_name= "State",title = f"{tacy['Year'].min()} YEAR {quarter} QUATER TRANSACTION AMOUNT",
                                    fitbounds= "locations",width =600, height= 600)
        fig_india_3.update_geos(visible =False)

        st.plotly_chart(fig_india_3)

    with col2:
        fig_india_4= px.choropleth(tacyg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                    color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                    range_color= (tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                    hover_name= "State",title = f"{tacy['Year'].min()} YEAR {quarter} QUATER TRANSACTION COUNT",
                                    fitbounds= "locations",width =600, height= 600)
        fig_india_4.update_geos(visible =False)

        st.plotly_chart(fig_india_4)

    return tacy

#Transaction Type by State wise

def Aggre_Tran_Type(df, state):

    tacy= df[df ["State"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2 = st.columns(2)

    with col1:
        fig_pie_1= px.pie(data_frame=tacyg, names="Transaction_type", values="Transaction_amount", width=600,
                        title=f"{state.upper()} TRANSACTION AMOUNT", hole=0.5)

        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2= px.pie(data_frame=tacyg, names="Transaction_type", values="Transaction_count", width=600,
                        title=f"{state.upper()} TRANSACTION COUNT", hole=0.5)

        st.plotly_chart(fig_pie_2)


#Aggregated user analysis by YEAR

def Aggre_user_plot_1(df, year):

    aguy = df[df["Year"]==year]
    aguy.reset_index(drop=True, inplace=True)

    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace=True)

    fig_bar_1 = px.bar(aguyg, x="Brands", y="Transaction_count", title= f"{year} BRANDS VS TRANSACTION COUNT", width = 950, 
                    color_discrete_sequence= px.colors.sequential.algae_r, hover_name= "Brands")
    st.plotly_chart(fig_bar_1)

    return aguy

#Aggregated User Analysis by quarter 

def Aggre_user_plot_2(df,quarter):

    aguyq = df[df["Quarter"]==quarter]
    aguyq.reset_index(drop=True, inplace=True)

    aguyqg= pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace=True)

    fig_bar_2 = px.bar(aguyqg, x="Brands", y="Transaction_count", title=f"{quarter} QUARTER BRANDS VS TRANSACTION COUNT", width = 950, 
                    color_discrete_sequence= px.colors.sequential.Aggrnyl,hover_name= "Brands")
    st.plotly_chart(fig_bar_2)

    return aguyq

#Aggregated user analysis by State

def Aggre_user_plot_3(df,state):

    auyqs= df[df["State"] == state]
    auyqs.reset_index(drop= True, inplace=True)

    fig_line_1= px.line(auyqs, x="Brands", y="Transaction_count", hover_data="Percentage", markers=True,
                        title=f"{state.upper()}-- PHONE BRANDS with TRANSACTION and their PERCENTAGE", width=1000)

    st.plotly_chart(fig_line_1)

#Function to PLOT for Transaction in Year

def Map_amount_count_Y(df,year):

    macy= df[df["Year"] == year]
    macy.reset_index(drop = True, inplace= True)

    macyg= macy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    macyg.reset_index(inplace= True)


    col1,col2 = st.columns(2)

    with col1:
        fig_amount_3= px.bar(macyg, x="State", y="Transaction_amount", title=f"{year} TRANSACTION AMOUNT",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl, height=500, width=600)
        st.plotly_chart(fig_amount_3)

    with col2:
        fig_count_3= px.bar(macyg, x="State", y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                                color_discrete_sequence=px.colors.sequential.Blackbody,height=500, width=600)
        st.plotly_chart(fig_count_3)

    col1,col2 = st.columns(2)

    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_5= px.choropleth(macyg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                    color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                    range_color= (macyg["Transaction_amount"].min(),macyg["Transaction_amount"].max()),
                                    hover_name= "State",title = f"{year} TRANSACTION AMOUNT",
                                    fitbounds= "locations",width =400, height= 600)
        fig_india_5.update_geos(visible =False)

        st.plotly_chart(fig_india_5)

    with col2:
        fig_india_6= px.choropleth(macyg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                    color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                    range_color= (macyg["Transaction_count"].min(),macyg["Transaction_count"].max()),
                                    hover_name= "State",title = f"{year} TRANSACTION COUNT",
                                    fitbounds= "locations",width =400, height= 600)
        fig_india_6.update_geos(visible =False)

        st.plotly_chart(fig_india_6)
    return macy

#Function to PLOT for Transaction in Year- Quarter

def Map_amount_count_Y_Q(df,quarter):

    tacy= df[df["Quarter"] == quarter]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("State")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2 = st.columns(2)

    with col1:

        fig_amount_4= px.bar(tacyg, x="State", y="Transaction_amount", title=f"{tacy['Year'].min()} YEAR {quarter} QUATER TRANSACTION AMOUNT",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount_4)
    
    with col2:
        fig_count_4= px.bar(tacyg, x="State", y="Transaction_count", title=f"{tacy['Year'].min()} YEAR {quarter} QUATER TRANSACTION COUNT",
                                color_discrete_sequence=px.colors.sequential.Blackbody)
        st.plotly_chart(fig_count_4)


    col1,col2 = st.columns(2)

    with col1:
        url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_7= px.choropleth(tacyg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                    color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                    range_color= (tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                    hover_name= "State",title = f"{tacy['Year'].min()} YEAR {quarter} QUATER TRANSACTION AMOUNT",
                                    fitbounds= "locations",width =600, height= 600)
        fig_india_7.update_geos(visible =False)

        st.plotly_chart(fig_india_7)

    with col2:
        fig_india_8= px.choropleth(tacyg, geojson= data1, locations= "State", featureidkey= "properties.ST_NM",
                                    color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                    range_color= (tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                    hover_name= "State",title = f"{tacy['Year'].min()} YEAR {quarter} QUATER TRANSACTION COUNT",
                                    fitbounds= "locations",width =600, height= 600)
        fig_india_8.update_geos(visible =False)

        st.plotly_chart(fig_india_8)

    return tacy


#Transaction Type by MAP District

def Map_insurance_District(df, state):

    tacy= df[df ["State"] == state]
    tacy.reset_index(drop = True, inplace= True)

    tacyg= tacy.groupby("District")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    fig_mapbar_3= px.bar(data_frame=tacyg, x="Transaction_amount", y="District", orientation="h",title=f"{state.upper()} DISTRICTS WITH TRANSACTION AMOUNT", 
                    color_discrete_sequence=px.colors.sequential.Brwnyl_r)

    st.plotly_chart(fig_mapbar_3)

    fig_mapbar_4= px.bar(data_frame=tacyg, x="Transaction_count", y="District", orientation="h",title=f"{state.upper()} DISTRICTS WITH TRANSACTION COUNT", 
                    color_discrete_sequence=px.colors.sequential.Blugrn_r)

    st.plotly_chart(fig_mapbar_4)

# MAP User analysis by YEAR

def map_user_plot_1(df,year):
    muy = df[df["Year"]== year]
    muy.reset_index(drop=True, inplace=True)

    muyg= muy.groupby("State")[["RegisteredUser","AppOpens"]].sum()
    muyg.reset_index(inplace=True)

    fig_mapline_2= px.line(muyg, x="State", y=["RegisteredUser","AppOpens"], markers=True, width=1000, height=800,
                        title=f"{year} REGISTERED USER AND APP OPENS")

    st.plotly_chart(fig_mapline_2)

    return muy

# MAP User analysis by QUARTER

def map_user_plot_2(df,quarter):
    muyq = df[df["Quarter"]== quarter]
    muyq.reset_index(drop=True, inplace=True)

    muyqg= muyq.groupby("State")[["RegisteredUser","AppOpens"]].sum()
    muyqg.reset_index(inplace=True)

    fig_mapline_3= px.line(muyqg, x="State", y=["RegisteredUser","AppOpens"], markers=True, width=1000, height=800,
                        title=f"{df['Year'].min()} YEAR {quarter} QUARTER REGISTERED USER AND APP OPENS", 
                        color_discrete_sequence= px.colors.sequential.BuPu_r)

    st.plotly_chart(fig_mapline_3)

    return muyq

# MAP USER ANALYSIS BY REGISTERED USER AND APP OPENS

def map_user_plot_3(df,state):
    muyqs = df[df["State"]== state]
    muyqs.reset_index(drop=True, inplace=True)

    fig_mapuser_bar_5= px.bar(muyqs, x="RegisteredUser", y="District", orientation= "h", title="REGISTERED USER", 
                        height= 800, color_discrete_sequence=px.colors.sequential.Rainbow_r)


    st.plotly_chart(fig_mapuser_bar_5)

# Top Insurance analysis by Pincode 

def Top_insurance_plot_1(df, state):
    tiy= df[df["State"]== state]
    tiy.reset_index(drop=True, inplace=True)

    tiyg= tiy.groupby("Pincode")[["Transaction_count","Transaction_amount"]].sum()
    tiyg.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:

        fig_bar_6= px.bar(tiy, x="Quarter", y="Transaction_amount", title="TRANSACTION AMOUNT", height= 600, 
                        hover_data="Pincode", color_discrete_sequence=px.colors.sequential.Rainbow)


        st.plotly_chart(fig_bar_6)
    with col2:

        fig_bar_7= px.bar(tiy, x="Quarter", y="Transaction_count", title="TRANSACTION COUNT", height= 600, 
                        hover_data="Pincode", color_discrete_sequence=px.colors.sequential.algae )


        st.plotly_chart(fig_bar_7)

# Top user analysis by year 

def top_user_plot_1(df, year):
    tuy= df[df["Year"]== year]
    tuy.reset_index(drop=True, inplace=True)

    tuyg= pd.DataFrame(tuy.groupby(["State", "Quarter"])["RegisteredUser"].sum())
    tuyg.reset_index(inplace=True)

    fig_bar_8 = px.bar(tuyg, x="State", y="RegisteredUser", color= "Quarter",height= 800, width= 1000,
                    hover_data="State", title=f"{year} REGISTERED USERS",
                    color_discrete_sequence= px.colors.sequential.BuPu_r)
    st.plotly_chart(fig_bar_8)

    return tuy 

# Top user analysis by pincodes

def top_user_plot_2(df, state):

    tuys= df[df["State"]== state]
    tuys.reset_index(drop=True, inplace=True)

    fig_bar_9= px.bar(tuys, x="Quarter", y="RegisteredUser", title="REGISTERED USER VS PINCODE VS QUARTER", height= 800, 
                        width =1000, hover_data="Pincode", color = "RegisteredUser",
                        color_continuous_scale = px.colors.sequential.Magenta)

    st.plotly_chart(fig_bar_9)

# TOP CHARTS 

#SQL Connection

def top_chart_insur_transaction_amount(table_name):
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="rihana",
                        database="phonepe_data",
                        port="5432")
    cursor=mydb.cursor()

    #PLOT 1

    query1= f'''SELECT state, SUM(insurance_amount) AS transaction_amount FROM {table_name} GROUP BY state
                ORDER BY transaction_amount  DESC LIMIT 10;'''

    cursor.execute(query1)
    table = cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table, columns=("States", "Transaction_Amount"))
    
    col1,col2= st.columns(2)
    with col1:
        fig_bar_10 = px.bar(df_1, x="States", y="Transaction_Amount", title=  "TOP 10 OF TRANSACTION AMOUNT", height =650,width = 600, 
                        color_discrete_sequence= px.colors.sequential.algae_r, hover_name= "States")
        st.plotly_chart(fig_bar_10)

    # PLOT 2

    query2= f'''SELECT state, SUM(insurance_amount) AS transaction_amount FROM {table_name} GROUP BY state
                ORDER BY transaction_amount LIMIT 10;'''

    cursor.execute(query2)
    table = cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table, columns=("States", "Transaction_Amount"))
   
    with col2:
        fig_bar_11 = px.bar(df_2, x="States", y="Transaction_Amount", title=  "LAST 10 OF TRANSACTION AMOUNT", height =650,width = 600, 
                        color_discrete_sequence= px.colors.sequential.algae, hover_name= "States")
        st.plotly_chart(fig_bar_11)


    # PLOT 3

    query3= f'''SELECT state, AVG(insurance_amount) AS transaction_amount FROM {table_name}
            GROUP BY state ORDER BY transaction_amount;'''

    cursor.execute(query3)
    table = cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table, columns=("States", "Transaction_Amount"))

    fig_bar_12 = px.bar(df_3, x="Transaction_Amount", y="States", title= "AVERAGE TRANSACTION AMOUNT", height =800,width = 1000, 
                    color_discrete_sequence= px.colors.sequential.BuPu_r, orientation ="h", hover_name= "States")
    st.plotly_chart(fig_bar_12)

    
# TOP CHARTS FOR TRANSACTION COUNT 

def top_chart_insur_transaction_count(table_name):
    
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="rihana",
                        database="phonepe_data",
                        port="5432")
    cursor=mydb.cursor()

    # PLOT 4

    query4= f'''SELECT state, SUM(insurance_count) AS transaction_count FROM {table_name} GROUP BY state
                ORDER BY transaction_count  DESC LIMIT 10;'''

    cursor.execute(query4)
    table = cursor.fetchall()
    mydb.commit()

    df_4= pd.DataFrame(table, columns=("States", "Transaction_Count"))

    col1, col2= st.columns(2)
    with col1:

        fig_bar_13 = px.bar(df_4, x="States", y="Transaction_Count", title=  "TOP 10 OF TRANSACTION COUNT", height =650,width = 600, 
                        color_discrete_sequence= px.colors.sequential.algae_r, hover_name= "States")
        st.plotly_chart(fig_bar_13)

    # PLOT 5

    query5= f'''SELECT state, SUM(insurance_count) AS transaction_count FROM {table_name} GROUP BY state
                ORDER BY transaction_count LIMIT 10;'''

    cursor.execute(query5)
    table = cursor.fetchall()
    mydb.commit()

    df_5= pd.DataFrame(table, columns=("States", "Transaction_Count"))

    with col2:

        fig_bar_14 = px.bar(df_5, x="States", y="Transaction_Count", title=  "LAST 10 OF TRANSACTION COUNT", height =650,width = 600, 
                        color_discrete_sequence= px.colors.sequential.algae, hover_name= "States")
        st.plotly_chart(fig_bar_14)


    # PLOT 6

    query6= f'''SELECT state, AVG(insurance_count) AS transaction_count FROM {table_name}
            GROUP BY state ORDER BY transaction_count;'''

    cursor.execute(query6)
    table = cursor.fetchall()
    mydb.commit()

    df_6= pd.DataFrame(table, columns=("States", "Transaction_Count"))

    fig_bar_15 = px.bar(df_6, x="Transaction_Count", y="States", title=  "AVERAGE TRANSACTION COUNT", height =800,width = 1000, 
                    color_discrete_sequence= px.colors.sequential.BuPu_r, orientation ="h", hover_name= "States")
    st.plotly_chart(fig_bar_15)

#  TOP CHARTS FOR TRANSACTION AMOUNT 

def top_chart_trans_transaction_amount(table_name):
    
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="rihana",
                        database="phonepe_data",
                        port="5432")
    cursor=mydb.cursor()

    #PLOT 7

    query7= f'''SELECT state, SUM(transaction_amount) AS transaction_amount FROM {table_name} 
                    GROUP BY state ORDER BY transaction_amount  DESC LIMIT 10;'''

    cursor.execute(query7)
    table = cursor.fetchall()
    mydb.commit()

    df_7= pd.DataFrame(table, columns=("States", "Transaction_Amount"))

    col1,col2=st.columns(2)
    with col1:

        fig_bar_16 = px.bar(df_7, x="States", y="Transaction_Amount", title=  "TOP 10 OF TRANSACTION AMOUNT", height =650,width = 600, 
                        color_discrete_sequence= px.colors.sequential.algae_r, hover_name= "States")
        st.plotly_chart(fig_bar_16)

    # PLOT 8

    query8= f'''SELECT state, SUM(transaction_amount) AS transaction_amount FROM {table_name} GROUP BY state
                ORDER BY transaction_amount LIMIT 10;'''

    cursor.execute(query8)
    table = cursor.fetchall()
    mydb.commit()

    df_8= pd.DataFrame(table, columns=("States", "Transaction_Amount"))

    with col2:
        fig_bar_17 = px.bar(df_8, x="States", y="Transaction_Amount", title=  "LAST 10 OF TRANSACTION AMOUNT", height =650,width = 600, 
                        color_discrete_sequence= px.colors.sequential.algae, hover_name= "States")
        st.plotly_chart(fig_bar_17)


    # PLOT 9

    query9= f'''SELECT state, AVG(transaction_amount) AS transaction_amount FROM {table_name}
            GROUP BY state ORDER BY transaction_amount;'''

    cursor.execute(query9)
    table = cursor.fetchall()
    mydb.commit()

    df_9= pd.DataFrame(table, columns=("States", "Transaction_Amount"))

    fig_bar_18 = px.bar(df_9, x="Transaction_Amount", y="States", title=  "AVERAGE TRANSACTION AMOUNT", height =800,width = 1000, 
                    color_discrete_sequence= px.colors.sequential.BuPu_r, orientation ="h", hover_name= "States")
    st.plotly_chart(fig_bar_18)

# TOP CHARTS FOR TRANSACTION COUNT 

def top_chart_trans_transaction_count(table_name):
    
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="rihana",
                        database="phonepe_data",
                        port="5432")
    cursor=mydb.cursor()

    # PLOT 10

    query10= f'''SELECT state, SUM(transaction_count) AS transaction_count FROM {table_name} GROUP BY state
                ORDER BY transaction_count  DESC LIMIT 10;'''

    cursor.execute(query10)
    table = cursor.fetchall()
    mydb.commit()

    df_10= pd.DataFrame(table, columns=("States", "Transaction_Count"))
    col1,col2=st.columns(2)

    with col1:
        fig_bar_19 = px.bar(df_10, x="States", y="Transaction_Count", title=  "TOP 10 OF TRANSACTION COUNT", height =650,width = 600, 
                        color_discrete_sequence= px.colors.sequential.algae_r, hover_name= "States")
        st.plotly_chart(fig_bar_19)

    # PLOT 11

    query11= f'''SELECT state, SUM(transaction_count) AS transaction_count FROM {table_name} GROUP BY state
                ORDER BY transaction_count LIMIT 10;'''

    cursor.execute(query11)
    table = cursor.fetchall()
    mydb.commit()

    df_11= pd.DataFrame(table, columns=("States", "Transaction_Count"))
    
    with col2:
        fig_bar_20 = px.bar(df_11, x="States", y="Transaction_Count", title=  "LAST 10 OF TRANSACTION COUNT", height =650,width = 600, 
                        color_discrete_sequence= px.colors.sequential.algae, hover_name= "States")
        st.plotly_chart(fig_bar_20)


    # PLOT 12

    query12= f'''SELECT state, AVG(transaction_count) AS transaction_count FROM {table_name}
            GROUP BY state ORDER BY transaction_count;'''

    cursor.execute(query12)
    table = cursor.fetchall()
    mydb.commit()

    df_12= pd.DataFrame(table, columns=("States", "Transaction_Count"))

    fig_bar_21 = px.bar(df_12, x="Transaction_Count", y="States", title=  "AVERAGE TRANSACTION COUNT", height =800,width = 1000, 
                    color_discrete_sequence= px.colors.sequential.BuPu_r, orientation ="h", hover_name= "States")
    st.plotly_chart(fig_bar_21)

#  TOP CHARTS FOR REGISTERED USER 

def top_chart_trans_registereduser(table_name, state):
    
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="rihana",
                        database="phonepe_data",
                        port="5432")
    cursor=mydb.cursor()

    #PLOT 13

    query13= f'''SELECT district, SUM(registereduser) as registereduser FROM {table_name} WHERE state= '{state}'
                GROUP BY district ORDER BY registereduser DESC LIMIT 10;'''

    cursor.execute(query13)
    table = cursor.fetchall()
    mydb.commit()

    df_13= pd.DataFrame(table, columns=("district", "registereduser"))

    col1,col2=st.columns(2)
    with col1:
        fig_bar_22 = px.bar(df_13, x="district", y="registereduser", title=  "TOP 10 OF REGISTERED USER", height =650,width = 600, 
                        color_discrete_sequence= px.colors.sequential.algae_r, hover_name= "district")
        st.plotly_chart(fig_bar_22)

    # PLOT 14

    query14= f'''SELECT district,SUM(registereduser) as registereduser FROM {table_name} WHERE state= '{state}'
                GROUP BY district ORDER BY registereduser LIMIT 10;'''

    cursor.execute(query14)
    table = cursor.fetchall()
    mydb.commit()

    df_14= pd.DataFrame(table, columns=("district", "registereduser"))

    with col2:
        fig_bar_23 = px.bar(df_14, x="district", y="registereduser", title= "LAST 10 OF REGISTERED USERS", height =650,width = 600, 
                        color_discrete_sequence= px.colors.sequential.algae, hover_name= "district")
        st.plotly_chart(fig_bar_23)


    # PLOT 15

    query15= f'''SELECT district, AVG(registereduser) as registereduser FROM {table_name} WHERE state= '{state}'
                GROUP BY district ORDER BY registereduser LIMIT 10;'''

    cursor.execute(query15)
    table = cursor.fetchall()
    mydb.commit()

    df_15= pd.DataFrame(table, columns=("district", "registereduser"))

    fig_bar_24 = px.bar(df_15, x="registereduser", y="district", title=  "AVERAGE OF REGISTERED USERS", height =800,width = 1000, 
                    color_discrete_sequence= px.colors.sequential.BuPu_r, orientation ="h", hover_name= "district")
    st.plotly_chart(fig_bar_24)

#  TOP CHARTS FOR APP OPENS

def top_chart_trans_appopens(table_name, state):
    
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="rihana",
                        database="phonepe_data",
                        port="5432")
    cursor=mydb.cursor()

    #PLOT 16

    query16= f'''SELECT district, SUM(appopens) as appopens FROM {table_name} WHERE state= '{state}'
                GROUP BY district ORDER BY appopens DESC LIMIT 10;'''

    cursor.execute(query16)
    table = cursor.fetchall()
    mydb.commit()

    df_16= pd.DataFrame(table, columns=("district", "appopens"))

    col1,col2=st.columns(2)
    with col1:

        fig_bar_25 = px.bar(df_16, x="district", y="appopens", title=  "TOP 10 OF APP OPENS", height =650,width = 600, 
                        color_discrete_sequence= px.colors.sequential.algae_r, hover_name= "district")
        st.plotly_chart(fig_bar_25)

    # PLOT 17

    query17= f'''SELECT district,SUM(appopens) as appopens FROM {table_name} WHERE state= '{state}'
                GROUP BY district ORDER BY appopens LIMIT 10;'''

    cursor.execute(query17)
    table = cursor.fetchall()
    mydb.commit()

    df_17= pd.DataFrame(table, columns=("district", "appopens"))
    with col2:
        fig_bar_26 = px.bar(df_17, x="district", y="appopens", title= "LAST 10 OF APP OPENS", height =650,width = 600, 
                        color_discrete_sequence= px.colors.sequential.algae, hover_name= "district")
        st.plotly_chart(fig_bar_26)


    # PLOT 18

    query18= f'''SELECT district, AVG(appopens) as appopens FROM {table_name} WHERE state= '{state}'
                GROUP BY district ORDER BY appopens LIMIT 10;'''

    cursor.execute(query18)
    table = cursor.fetchall()
    mydb.commit()

    df_18= pd.DataFrame(table, columns=("district", "appopens"))

    fig_bar_27 = px.bar(df_18, x="appopens", y="district", title=  "AVERAGE OF APP OPENS", height =800,width = 1000, 
                    color_discrete_sequence= px.colors.sequential.BuPu_r, orientation ="h", hover_name= "district")
    st.plotly_chart(fig_bar_27)

#  TOP CHARTS FOR TOPUSER REGISTERED USER 

def top_chart_top_registereduser(table_name):
    
    mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="rihana",
                        database="phonepe_data",
                        port="5432")
    cursor=mydb.cursor()

    #PLOT 19

    query19= f'''SELECT state, SUM(registereduser) as Registereduser FROM {table_name} GROUP BY state
                    ORDER BY registereduser DESC LIMIT 10;'''

    cursor.execute(query19)
    table = cursor.fetchall()
    mydb.commit()

    df_19= pd.DataFrame(table, columns=("district", "registereduser"))

    col1,col2=st.columns(2)
    with col1:
        fig_bar_28 = px.bar(df_19, x="district", y="registereduser", title=  "TOP 10 OF REGISTERED USER", height =650,width = 600, 
                        color_discrete_sequence= px.colors.sequential.algae_r, hover_name= "district")
        st.plotly_chart(fig_bar_28)

    # PLOT 20

    query20= f'''SELECT state, SUM(registereduser) as Registereduser FROM {table_name} GROUP BY state
                    ORDER BY registereduser LIMIT 10;'''

    cursor.execute(query20)
    table = cursor.fetchall()
    mydb.commit()

    df_20= pd.DataFrame(table, columns=("district", "registereduser"))

    with col2:
        fig_bar_29 = px.bar(df_20, x="district", y="registereduser", title= "LAST 10 OF REGISTERED USERS", height =650,width = 600, 
                        color_discrete_sequence= px.colors.sequential.algae, hover_name= "district")
        st.plotly_chart(fig_bar_29)


    # PLOT 21

    query21= f'''SELECT state, AVG(registereduser) as Registereduser FROM {table_name} GROUP BY state
                    ORDER BY registereduser DESC  LIMIT 10;'''

    cursor.execute(query21)
    table = cursor.fetchall()
    mydb.commit()

    df_21= pd.DataFrame(table, columns=("district", "registereduser"))

    fig_bar_30 = px.bar(df_21, x="registereduser", y="district", title=  "AVERAGE OF REGISTERED USERS", height =800,width = 1000, 
                    color_discrete_sequence= px.colors.sequential.BuPu_r, orientation ="h", hover_name= "district")
    st.plotly_chart(fig_bar_30)


   


























#Streamlit part

st.set_page_config(layout= "wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")


with st.sidebar:
    select= option_menu("Main Menu",["Home", "Data Exploration", "Top Charts"])

if select == "Home":
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
        st.image(Image.open(r"C:\Users\pc\Desktop\Phonepe\img1.jpg"), width =600)


    col3,col4= st.columns(2)
    
    with col3:
        st.image(Image.open(r"C:\Users\pc\Desktop\Phonepe\img2.jpg"), width =600)

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
        st.image(Image.open(r"C:\Users\pc\Desktop\Phonepe\img3.jpg"), width =600)


# DATA EXPLORATION TAB 

if select == "Data Exploration":
    tab1, tab2, tab3 = st.tabs(("Aggregated Analysis", "Map Analysis", "Top Analysis"))

    with tab1:
        method = st.radio("**Select the Analysis Method**",("Insurance Analysis", "Transaction Analysis", "User Analysis"), horizontal =True)
    
#AGGREGATED INSURANCE analysis

        if method == "Insurance Analysis":

            col1,col2= st.columns(2)

            with col1:
                years= st.slider("Select the Year(AYInsurance)", Aggre_insurance["Year"].min(),Aggre_insurance["Year"].max(),Aggre_insurance["Year"].min())
            tac_Y=Transaction_amount_count_Y(Aggre_insurance,years)

            col1,col2=st.columns(2)

            with col1:
                quarters= st.slider("Select the Quarter(AQInsurance)", tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y,quarters)

#AGGREGATED TRANSACTION analysis

        elif method == "Transaction Analysis":
        
            col1,col2= st.columns(2)

            with col1:
                years= st.slider("Select the Year(AYTransaction)", Aggre_transaction["Year"].min(),Aggre_transaction["Year"].max(),Aggre_transaction["Year"].min())
            Aggre_tran_tac_Y=Transaction_amount_count_Y(Aggre_transaction,years)


    # Selecting STATE to analyze the transaction by YEAR 

            states=st.selectbox("Select the State(AYTransaction)", Aggre_tran_tac_Y["State"].unique())
            Aggre_Tran_Type(Aggre_tran_tac_Y, states)
    
            col1,col2=st.columns(2)

            with col1:
                quarters= st.slider("Select the Quarter(AQTransaction)", Aggre_tran_tac_Y["Quarter"].min(),Aggre_tran_tac_Y["Quarter"].max(),Aggre_tran_tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q = Transaction_amount_count_Y_Q(Aggre_tran_tac_Y,quarters)

    # Selecting STATE to analyze the transaction by QUARTER

            states=st.selectbox("Select the State(AQTransaction)", Aggre_tran_tac_Y_Q["State"].unique())
            Aggre_Tran_Type(Aggre_tran_tac_Y_Q, states)

#AGGREGATED USER ANALYSIS

        elif method == "User Analysis":

            years= st.slider("Select the Year(AUser)", Aggre_user["Year"].min(),Aggre_user["Year"].max(),Aggre_user["Year"].min())
            Aggre_user_Y = Aggre_user_plot_1(Aggre_user, years)


            quarters= st.slider("Select the Year(AUser)", Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q = Aggre_user_plot_2(Aggre_user_Y,quarters)


    # Selecting STATE to analyze the transaction in PERCENTAGE

            states=st.selectbox("Select the State(AUser)", Aggre_user_Y_Q["State"].unique())
            Aggre_user_plot_3(Aggre_user_Y_Q, states)

# MAP INSURANCE ANALYSIS

    with tab2:
        method_map = st.radio("**Select the Analysis Method(MAP)**",("Map Insurance Analysis", "Map Transaction Analysis", "Map User Analysis"), horizontal =True)

        if method_map == "Map Insurance Analysis":
            col1,col2= st.columns(2)

            with col1:
                years= st.slider("Select the Year(MInsurance)", Map_insurance["Year"].min(),Map_insurance["Year"].max(),Map_insurance["Year"].min())
            Map_insurance_tac_Y=Map_amount_count_Y(Map_insurance,years)

        # Selecting STATE to analyze the District Transaction by YEAR 

            col1,col2= st.columns(2)

            with col1:
                states=st.selectbox("Select the State(MDInsurance)", Map_insurance_tac_Y["State"].unique())
            Map_insurance_District(Map_insurance_tac_Y, states)

            col1,col2=st.columns(2)

            with col1:
                quarters= st.slider("Select the Quarter(MInsurance)", Map_insurance_tac_Y["Quarter"].min(),Map_insurance_tac_Y["Quarter"].max(),Map_insurance_tac_Y["Quarter"].min())
            Map_insurance_tac_Y_Q= Map_amount_count_Y_Q(Map_insurance_tac_Y,quarters)

        # Selecting STATE to analyze the District Transaction by QUARTER
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State(MDWInsurance)", Map_insurance_tac_Y_Q["State"].unique())
            Map_insurance_District(Map_insurance_tac_Y_Q, states)


# MAP TRANSACTION ANALYSIS

        elif method_map == "Map Transaction Analysis":
            col1,col2= st.columns(2)

            with col1:
                years= st.slider("Select the Year(MYTransaction)", Map_transaction["Year"].min(),Map_transaction["Year"].max(),Map_transaction["Year"].min())
            Map_Tran_tac_Y=Map_amount_count_Y(Map_transaction,years)

        # Selecting STATE to analyze the District Wise TRANSACTION 

            col1,col2= st.columns(2)

            with col1:
                states=st.selectbox("Select the State(MYTransaction)", Map_Tran_tac_Y["State"].unique())
            Map_insurance_District(Map_Tran_tac_Y, states)

            col1,col2=st.columns(2)

            with col1:
                quarters= st.slider("Select the Quarter(MQTransaction)", Map_Tran_tac_Y["Quarter"].min(),Map_Tran_tac_Y["Quarter"].max(),Map_Tran_tac_Y["Quarter"].min())
            Map_Tran_tac_Y_Q= Map_amount_count_Y_Q(Map_Tran_tac_Y,quarters)

        # Selecting STATE to analyze the transaction by QUARTER
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State(MQTransaction)", Map_Tran_tac_Y_Q["State"].unique())
            Map_insurance_District(Map_Tran_tac_Y_Q, states)
        
#MAP USER ANALYSIS

        elif method_map == "Map User Analysis":
            col1,col2= st.columns(2)

            with col1:
                years= st.slider("Select the Year(MUser)", Map_user["Year"].min(),Map_user["Year"].max(),Map_user["Year"].min())
            Map_user_Y = map_user_plot_1(Map_user,years)

            col1,col2=st.columns(2)

            with col1:
                quarters= st.slider("Select the Quarter(MUser)", Map_user_Y["Quarter"].min(),Map_user_Y["Quarter"].max(),Map_user_Y["Quarter"].min())
            Map_user_Y_Q= map_user_plot_2(Map_user_Y,quarters)


        # Selecting STATE to analyze the Registered user and APP opens
            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State(MUserState)", Map_user_Y_Q["State"].unique())
            map_user_plot_3(Map_user_Y_Q, states)


    with tab3:
        method_top = st.radio("**Select the Analysis Method(TOP)**",("Top Insurance Analysis", "Top Transaction Analysis", "Top User Analysis"),horizontal= True)

        if method_top == "Top Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("Select the Year(TYInsurance)", Top_insurance["Year"].min(),Top_insurance["Year"].max(),Top_insurance["Year"].min())
            Top_insurance_tac_Y=Map_amount_count_Y(Top_insurance,years)

            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State(TSInsurance)", Top_insurance_tac_Y["State"].unique())
            Top_insurance_plot_1(Top_insurance_tac_Y, states)

            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Select the Quarter(TQInsurance)", Top_insurance_tac_Y["Quarter"].min(),Top_insurance_tac_Y["Quarter"].max(),Top_insurance_tac_Y["Quarter"].min())
            Top_insurance_Y_Q= Map_amount_count_Y_Q(Top_insurance_tac_Y,quarters)


        elif method_top == "Top Transaction Analysis":

            col1,col2= st.columns(2)
            with col1:
                years= st.slider("Select the Year(TYTransaction)", Top_transaction["Year"].min(),Top_transaction["Year"].max(),Top_transaction["Year"].min())
            Top_trans_tac_Y=Map_amount_count_Y(Top_transaction,years)


            col1,col2=st.columns(2)
            with col1:
                states=st.selectbox("Select the State(TSTransaction)", Top_trans_tac_Y["State"].unique())
            Top_insurance_plot_1(Top_trans_tac_Y, states)


            col1,col2=st.columns(2)
            with col1:
                quarters= st.slider("Select the Quarter(TQTransaction)", Top_trans_tac_Y["Quarter"].min(),Top_trans_tac_Y["Quarter"].max(),Top_trans_tac_Y["Quarter"].min())
            Top_trans_tac_Y_Q= Map_amount_count_Y_Q(Top_trans_tac_Y,quarters)


        elif method_top == "Top User Analysis":

            col1,col2= st.columns(2)
            with col1:
                years= st.slider("Select the Year(TYUser)", Top_user["Year"].min(),Top_user["Year"].max(),Top_user["Year"].min())
            Top_user_Y=top_user_plot_1(Top_user,years)

            col1,col2= st.columns(2)

            with col1:
                states=st.selectbox("Select the State(TSUser)", Top_user_Y["State"].unique())
            top_user_plot_2(Top_user_Y, states)

elif select == "Top Charts":
        
    question = st.selectbox("Select a Question",("1. Transaction amount and count of Aggregated Insurance",
                                                "2. Transaction amount and count of Map Insurance",
                                                "3. Transaction amount and count of Top Insurance",
                                                "4. Transaction amount and count of Aggregated Transaction",
                                                "5. Transaction amount and count of Map Transaction",
                                                "6. Transaction amount and count of Top Transaction",
                                                "7. Transaction count of Aggregated User",
                                                "8. Registered Users of Map User",
                                                "9. App Opens of Map User",
                                                "10. Registered Users of Top User" ))

    if question == "1. Transaction amount and count of Aggregated Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_insur_transaction_amount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_insur_transaction_count("aggregated_insurance")

    elif question == "2. Transaction amount and count of Map Insurance":
    
        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_transaction_amount("map_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_trans_transaction_count("map_insurance")

    elif question == "3. Transaction amount and count of Top Insurance":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_transaction_amount("top_insurance")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_trans_transaction_count("top_insurance")


    elif question == "4. Transaction amount and count of Aggregated Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_transaction_amount("aggregated_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_trans_transaction_count("aggregated_transaction")

    elif question == "5. Transaction amount and count of Map Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_transaction_amount("map_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_trans_transaction_count("map_transaction")

    elif question == "6. Transaction amount and count of Top Transaction":

        st.subheader("TRANSACTION AMOUNT")
        top_chart_trans_transaction_amount("top_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_trans_transaction_count("top_transaction")

    elif question == "7. Transaction count of Aggregated User":

        st.subheader("TRANSACTION COUNT")
        top_chart_trans_transaction_count("aggregated_user")

    elif question == "8. Registered Users of Map User":

        rstate = st.selectbox("Select the state(RU)", Map_user["State"].unique())
        st.subheader("REGISTERED USER")
        top_chart_trans_registereduser("map_user", rstate)

    elif question == "9. App Opens of Map User":

        astate = st.selectbox("Select the state(AU)", Map_user["State"].unique())
        st.subheader("APP OPENS")
        top_chart_trans_appopens("map_user", astate)

    elif question == "10. Registered Users of Top User":

        st.subheader("REGISTERED USERS")
        top_chart_top_registereduser("top_user")
        







    