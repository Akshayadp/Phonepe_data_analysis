import pandas as pd
import mysql.connector
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import requests
import json


mydb =  mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "NANANANA",
                            database = "PhonePe",
                            auth_plugin='mysql_native_password'
                            )


cursor = mydb.cursor()
cursor.execute("ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'NANANANA'")

cursor = mydb.cursor(buffered=True)

#df agg transaction

cursor.execute("SELECT * FROM agg_trans")
mydb.commit()
table1 = cursor.fetchall()

agg_trans = pd.DataFrame(table1, columns=("State", "Year", "Quater", "Transaction_type", "Transaction_count", "Transaction_amount"))
#agg_trans

#df agg user

cursor.execute("SELECT * FROM agg_user")
mydb.commit()
table2 = cursor.fetchall()

agg_user = pd.DataFrame(table2, columns=("State", "Year", "Quater", "Brands", "Transaction_count", "Percentage"))
#agg_user


#df map trans

cursor.execute("SELECT * FROM map_trans")
mydb.commit()
table3 = cursor.fetchall()

map_trans = pd.DataFrame(table3, columns=("State", "Year", "Quater", "Districts", "Transaction_count", "Transaction_amount"))
#map_trans


#df map user

cursor.execute("SELECT * FROM map_user")
mydb.commit()
table4 = cursor.fetchall()

map_user = pd.DataFrame(table4, columns=("State", "Year", "Quater", "Districts", "Registered_Users", "App_Opens"))
#map_user


#df top trans

cursor.execute("SELECT * FROM top_trans")
mydb.commit()
table5 = cursor.fetchall()

top_trans = pd.DataFrame(table5, columns=("State", "Year", "Quater", "Pincodes", "Transaction_count", "Transaction_amount"))
#top_trans


#df top user

cursor.execute("SELECT * FROM top_users")
mydb.commit()
table6 = cursor.fetchall()

top_user = pd.DataFrame(table6, columns=("State", "Year", "Quater", "Pincodes", "Registered_Users"))
#top_user

#col1, col2 = st.columns(2)

def trans_amt_count_year(df, year):

    agg_acy = df [df ["Year"] == year]
    agg_acy.reset_index(drop=True, inplace=True)

    acy_group = agg_acy.groupby("State")[["Transaction_count", "Transaction_amount"]].sum()
    acy_group.reset_index(inplace=True)

    col1, col2 = st.columns(2)
    
    with col1:
        fig_amt = px.bar(acy_group, x="State", y="Transaction_amount", title = f"{year} TRANSACTION AMOUNT", height=650, width=600)
        #fig_amt.show()
        st.plotly_chart(fig_amt)
        
    with col2:
        fig_count = px.bar(acy_group, x="State", y="Transaction_amount", title = f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
        #fig_count.show()
        st.plotly_chart(fig_count)


    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    res_data = json.loads(response.content)
    states_name = []
    for later in res_data["features"]:
        states_name.append(later["properties"]["ST_NM"])
    #states_name
    states_name.sort()

    with col1:
        fig_map1 = px.choropleth(acy_group, geojson = res_data, 
                                locations= "State", 
                                featureidkey= "properties.ST_NM", 
                                color= "Transaction_amount", 
                                color_continuous_scale="Rainbow",
                                range_color= (acy_group["Transaction_amount"].min(), acy_group["Transaction_amount"].max()),
                                hover_name= "State", title= f"{year} TRANSACTION AMOUNT",
                                fitbounds= "locations",
                                height=600, width=600)
        
        fig_map1.update_geos(visible = False)
        st.plotly_chart(fig_map1)

    with col2:
        fig_map2 = px.choropleth(acy_group, geojson = res_data, 
                                locations= "State", 
                                featureidkey= "properties.ST_NM", 
                                color= "Transaction_count", 
                                color_continuous_scale="Rainbow",
                                range_color= (acy_group["Transaction_count"].min(), acy_group["Transaction_count"].max()),
                                hover_name= "State", title= f"{year} TRANSACTION COUNT",
                                fitbounds= "locations",
                                height=600, width=600)
        
        fig_map2.update_geos(visible = False)
        st.plotly_chart(fig_map2)

    return agg_acy

def trans_amt_count_quarter(df, quarter):

    agg_acy = df [df ["Quater"] == quarter]
    agg_acy.reset_index(drop=True, inplace=True)

    acy_group = agg_acy.groupby("State")[["Transaction_count", "Transaction_amount"]].sum()
    acy_group.reset_index(inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_amt = px.bar(acy_group, x="State", y="Transaction_amount", 
                         title = f"{agg_acy['Year'].unique()} Quarter - {quarter} TRANSACTION AMOUNT", 
                         color_discrete_sequence=px.colors.sequential.Rainbow, 
                        range_color= (acy_group["Transaction_amount"].min(), acy_group["Transaction_amount"].max()),
                         height=650, width=600)
        st.plotly_chart(fig_amt)

    with col2:
        fig_count = px.bar(acy_group, x="State", y="Transaction_count", 
                           title = f"{agg_acy['Year'].unique()} Quarter - {quarter} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, 
                        range_color= (acy_group["Transaction_count"].min(), acy_group["Transaction_count"].max()), height=650, width=600)
        st.plotly_chart(fig_count)

#trans_amt_count_year(agg_trans, 2018)
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    res_data = json.loads(response.content)
    states_name = []
    for later in res_data["features"]:
        states_name.append(later["properties"]["ST_NM"])
    #states_name
    states_name.sort()

    with col1:
        fig_map1 = px.choropleth(acy_group, geojson = res_data, 
                                locations= "State", 
                                featureidkey= "properties.ST_NM", 
                                color= "Transaction_amount", 
                                color_continuous_scale="Rainbow",
                                range_color= (acy_group["Transaction_amount"].min(), acy_group["Transaction_amount"].max()),
                                hover_name= "State", title= f"{agg_acy['Year'].unique()} Quarter - {quarter} TRANSACTION AMOUNT",
                                fitbounds= "locations",
                                height=600, width=600)
        
        fig_map1.update_geos(visible = False)
        st.plotly_chart(fig_map1)

    with col2:
        fig_map2 = px.choropleth(acy_group, geojson = res_data, 
                                locations= "State", 
                                featureidkey= "properties.ST_NM", 
                                color= "Transaction_count", 
                                color_continuous_scale="Rainbow",
                                range_color= (acy_group["Transaction_count"].min(), acy_group["Transaction_count"].max()),
                                hover_name= "State", title= f"{agg_acy['Year'].unique()} Quarter - {quarter} TRANSACTION COUNT",
                                fitbounds= "locations",
                                height=600, width=600)
        
        fig_map2.update_geos(visible = False)
        st.plotly_chart(fig_map2)

    return agg_acy

    
def agg_trans_chart(df, state):

    agg_acy = df [df ["State"] == state]
    agg_acy.reset_index(drop=True, inplace=True)

    acy_group = agg_acy.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    acy_group.reset_index(inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_pie1 = px.pie(data_frame= trany, names= "Transaction_type", values= "Transaction_amount", 
                          width= 600, title=f"{state} TRANSACTION AMOUNT")
        st.plotly_chart(fig_pie1)

    with col2:
        fig_pie2 = px.pie(data_frame= trany, names= "Transaction_type", values= "Transaction_count", 
                          width= 600, title=f"{state} TRANSACTION COUNT")
        st.plotly_chart(fig_pie2)


#Agg user

def auser_plot1(df, year):
    auy = df[df ["Year"] == year]
    auy.reset_index(drop=True, inplace=True)

    auy_gup = pd.DataFrame(auy.groupby("Brands")["Transaction_count"].sum())
    auy_gup.reset_index(inplace=True)

    fig_bar1 = px.bar(auy_gup, x="Brands", y="Transaction_count", title=f"{year} - BRANDS",
                     color_discrete_sequence=px.colors.sequential.Rainbow, 
                     range_color= (auy_gup["Transaction_count"].min(), auy_gup["Transaction_count"].max()))
    st.plotly_chart(fig_bar1)

    return auy

def auser_plot2(df, quarter):
    auyq = df[df ["Quater"] == quarter]
    auyq.reset_index(drop=True, inplace=True)

    auyq_grp = pd.DataFrame(auyq.groupby("Brands")["Transaction_count"].sum())
    auyq_grp.reset_index(inplace=True)

    fig_bar2 = px.bar(auyq_grp, x="Brands", y="Transaction_count", title=f"{quarter} - QUARTER BRANDS",
                        color_discrete_sequence=px.colors.sequential.Rainbow,
                        range_color= (auyq_grp["Transaction_count"].min(), auyq_grp["Transaction_count"].max()))
    st.plotly_chart(fig_bar2)

    return auyq


def auser_plot3(df, state):
    auys = df[df ["State"] == state]
    auys.reset_index(drop=True, inplace=True)

    fig_chart1 = px.line(auys, x="Brands", y="Transaction_count", hover_data="Percentage",
                         title=f"{state} - DATA", markers=True)
    st.plotly_chart(fig_chart1)



#Map Transaction
def map_trans_chart(df, state):

    map_acy = df [df ["State"] == state]
    map_acy.reset_index(drop=True, inplace=True)

    mapcy_group = map_acy.groupby("Districts")[["Transaction_count", "Transaction_amount"]].sum()
    mapcy_group.reset_index(inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_bar = px.bar(mapcy_group, x= "Transaction_amount", y= "Districts", orientation= "h", width= 600, title=f"{state} - DISTRICTS & TRANSACTION AMOUNT",
                        color_discrete_sequence= px.colors.sequential.Rainbow,
                        range_color= (mapcy_group["Transaction_amount"].min(), mapcy_group["Transaction_amount"].max()))
        st.plotly_chart(fig_bar)

    with col2:
        fig_bar2 = px.bar(mapcy_group, x= "Transaction_count", y= "Districts", orientation= "h", width= 600, title=f"{state} - DISTRICTS & TRANSACTION COUNT",
                        color_discrete_sequence= px.colors.sequential.Rainbow,
                        range_color= (mapcy_group["Transaction_count"].min(), mapcy_group["Transaction_count"].max()))
        st.plotly_chart(fig_bar2)


#Map user

def muser_plot1(df, year):
    muy = df[df ["Year"] == year]
    muy.reset_index(drop=True, inplace=True)

    muy_gup = muy.groupby("State")[["Registered_Users", "App_Opens"]].sum()
    muy_gup.reset_index(inplace=True)

    fig_barm = px.line(muy_gup, x= "State", y= ["Registered_Users", "App_Opens"], 
                     title=f"{year} - REGISTERED USERS & APP OPENS",
                     color_discrete_sequence= px.colors.sequential.Rainbow, markers=True)
    st.plotly_chart(fig_barm)

    return muy


def muser_plot(df, quarter):
    muyq = df[df ["Quater"] == quarter]
    muyq.reset_index(drop=True, inplace=True)

    muyq_grp = pd.DataFrame(muyq.groupby("State")[["Registered_Users", "App_Opens"]].sum())
    muyq_grp.reset_index(inplace=True)

    fig_line = px.line(muyq_grp, x="State", y=["Registered_Users", "App_Opens"], title=f"QUARTER {quarter} - REGISTERED USERS & APP OPENS",
                        color_discrete_sequence=px.colors.sequential.Rainbow, markers=True)
    st.plotly_chart(fig_line)

    return muyq

def muser_plot_s(df, state):
    muys = df[df ["State"] == state]
    muys.reset_index(drop=True, inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_line = px.bar(muys, x="Registered_Users", y= "Districts", title=f"{state} - USERS REGISTERED",
                            color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig_line)

    with col2:
        fig_line2 = px.bar(muys, x="App_Opens", y= "Districts", title=f"{state} - USER APP OPENED",
                            color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_line2)


#Top trans

def top_trans_chart(df, state):

    top_acy = df [df ["State"] == state]
    top_acy.reset_index(drop=True, inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_bar = px.bar(top_acy, x= "Quater", y= "Transaction_amount", hover_data= "Pincodes", width= 600, title=f"{state} - TRANSACTION AMOUNT",
                        color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_bar)

    with col2:
        fig_bar1 = px.bar(top_acy, x= "Quater", y= "Transaction_count", hover_data= "Pincodes", width= 600, title=f"{state} - TRANSACTION COUNT",
                        color_discrete_sequence= px.colors.sequential.Agsunset)
        st.plotly_chart(fig_bar1)


#Top User

def tuser_plot1(df, year):
    tuy = df[df ["Year"] == year]
    tuy.reset_index(drop=True, inplace=True)

    tuy_gup = pd.DataFrame(tuy.groupby(["State", "Quater"])["Registered_Users"].sum())
    tuy_gup.reset_index(inplace=True)

    fig_bar = px.bar(tuy_gup, x= "State", y= "Registered_Users", color= "Quater",
                     height=700, width=1000, title=f"{year} - REGISTERED USERS",
                     color_discrete_sequence= px.colors.sequential.Blues)
    st.plotly_chart(fig_bar)

    return tuy

def tuser_plot2(df, state):
    tuys = df[df ["State"] == state]
    tuys.reset_index(drop=True, inplace=True)

    fig_bar1 = px.bar(tuys, x="Quater", y="Registered_Users", hover_data="Pincodes", title="OVERALL USER DATA",
                     color="Registered_Users", color_continuous_scale= px.colors.sequential.Greens)
    st.plotly_chart(fig_bar1)



#TOP CHART
def tc_tran_amt(table_name):

    mydb =  mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "NANANANA",
                            database = "PhonePe",
                            auth_plugin='mysql_native_password'
                            )


    cursor = mydb.cursor()
    cursor.execute("ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'NANANANA'")

    cursor = mydb.cursor(buffered=True)

    col1, col2 = st.columns(2)
    with col1:
        years = st.selectbox('**Year**',('2018','2019','2020','2021','2022','2023'))
    with col1:    
        Quarter = st.selectbox('**Quarter**',('1','2','3','4'))

    query1 = f'''select state, SUM(Transaction_amount) as Transaction_amount from {table_name} 
                where Years = {years} AND Quater = {Quarter} group by State order by Transaction_amount desc limit 10;'''
    cursor.execute(query1)
    qtable1 = cursor.fetchall()
    mydb.commit()

    column1, column2 = st.columns(2)

    df1 = pd.DataFrame(qtable1, columns=("State", "Transaction_amount"))

    with column1:
        fig_bar1 = px.pie(df1, names= "State", values= "Transaction_amount",
                            width= 500, title= "TOP 10",
                            color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_bar1)

    query2 = f'''select state, SUM(Transaction_amount) as Transaction_amount from {table_name} 
                where Years = {years} AND Quater = {Quarter} group by State order by Transaction_amount limit 10;'''
    cursor.execute(query2)
    qtable2 = cursor.fetchall()
    mydb.commit()

    df2 = pd.DataFrame(qtable2, columns=("State", "Transaction_amount"))
    with column2:
        fig_bar2 = px.pie(df2, names= "State", values= "Transaction_amount",
                            width= 500, title= "LEAST 10",
                            color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_bar2)

    query3 = f'''select state, avg(Transaction_amount) as Transaction_amount from {table_name} 
                where Years = {years} AND Quater = {Quarter} group by State order by Transaction_amount;'''
    cursor.execute(query3)
    qtable3 = cursor.fetchall()
    mydb.commit()

    df3 = pd.DataFrame(qtable3, columns=("State", "Transaction_amount"))

    fig_bar3 = px.bar(df3, x= "Transaction_amount", y= "State", orientation="h",
                        width= 1000, title= "AVERAGE TRANSACTION AMOUNT",
                        color_discrete_sequence= px.colors.sequential.Rainbow)
    st.plotly_chart(fig_bar3)



def tc_tran_count(table_name):

    mydb =  mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "NANANANA",
                            database = "PhonePe",
                            auth_plugin='mysql_native_password'
                            )


    cursor = mydb.cursor()
    cursor.execute("ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'NANANANA'")

    cursor = mydb.cursor(buffered=True)

    col1, col2 = st.columns(2)
    with col1:
        years = st.selectbox('**Year**',('2018','2019','2020','2021','2022','2023'))
    with col1:    
        Quarter = st.selectbox('**Quarter**',('1','2','3','4'))


    query1 = f'''select state, SUM(Transaction_count) as Transaction_count from {table_name} 
            where Years = {years} AND Quater = {Quarter} group by State order by Transaction_count desc limit 10;'''
    cursor.execute(query1)
    qtable1 = cursor.fetchall()
    mydb.commit()

    column1, column2 = st.columns(2)

    df1 = pd.DataFrame(qtable1, columns=("State", "Transaction_count"))

    with column1:
        fig_bar1 = px.pie(df1, names= "State", values= "Transaction_count",
                            width= 500, title= "TOP 10",
                            color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_bar1)

    query2 = f'''select state, SUM(Transaction_count) as Transaction_count from {table_name} 
            where Years = {years} AND Quater = {Quarter} group by State order by Transaction_count limit 10;'''
    cursor.execute(query2)
    qtable2 = cursor.fetchall()
    mydb.commit()

    df2 = pd.DataFrame(qtable2, columns=("State", "Transaction_count"))
    with column2:
        fig_bar2 = px.pie(df2, names="State", values= "Transaction_count",
                            width= 500, title= "LEAST 10",
                            color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_bar2)

    query3 = f'''select state, avg(Transaction_count) as Transaction_count from {table_name} 
                where Years = {years} AND Quater = {Quarter} group by State order by Transaction_count;'''
    cursor.execute(query3)
    qtable3 = cursor.fetchall()
    mydb.commit()

    df3 = pd.DataFrame(qtable3, columns=("State", "Transaction_count"))

    fig_bar3 = px.bar(df3, x= "Transaction_count", y= "State", orientation="h",
                        width= 1000, title= "AVERAGE TRANSACTION COUNT",
                        color_discrete_sequence= px.colors.sequential.Rainbow)
    st.plotly_chart(fig_bar3)


def tc_brands(table_name):

    mydb =  mysql.connector.connect(
                            host = "localhost",
                            user = "root",
                            password = "NANANANA",
                            database = "PhonePe",
                            auth_plugin='mysql_native_password'
                            )


    cursor = mydb.cursor()
    cursor.execute("ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'NANANANA'")

    cursor = mydb.cursor(buffered=True)

    col1, col2 = st.columns(2)
    with col1:
        years = st.selectbox('**Year**',('2018','2019','2020','2021','2022','2023'))
    with col1:    
        Quarter = st.selectbox('**Quarter**',('1','2','3','4'))


    query1 = f'''select Brands, SUM(Transaction_count) as Transaction_count from {table_name} 
            where Years = {years} AND Quater = {Quarter} group by Brands order by Transaction_count desc limit 10;'''
    cursor.execute(query1)
    qtable1 = cursor.fetchall()
    mydb.commit()

    column1, column2 = st.columns(2)

    df1 = pd.DataFrame(qtable1, columns=("Brands", "Transaction_count"))

    with column1:
        fig_bar1 = px.pie(df1, names= "Brands", values= "Transaction_count",
                            width= 500, title= "TOP 10",
                            color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_bar1)

    query2 = f'''select Brands, SUM(Transaction_count) as Transaction_count from {table_name} 
            where Years = {years} AND Quater = {Quarter} group by Brands order by Transaction_count limit 10;'''
    cursor.execute(query2)
    qtable2 = cursor.fetchall()
    mydb.commit()

    df2 = pd.DataFrame(qtable2, columns=("Brands", "Transaction_count"))
    with column2:
        fig_bar2 = px.pie(df2, names="Brands", values= "Transaction_count",
                            width= 500, title= "LEAST 10",
                            color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_bar2)

    query3 = f'''select Brands, avg(Transaction_count) as Transaction_count from {table_name} 
                where Years = {years} AND Quater = {Quarter} group by Brands order by Transaction_count;'''
    cursor.execute(query3)
    qtable3 = cursor.fetchall()
    mydb.commit()

    df3 = pd.DataFrame(qtable3, columns=("Brands", "Transaction_count"))

    fig_bar3 = px.bar(df3, x= "Transaction_count", y= "Brands", orientation="h",
                        width= 1000, title= "AVERAGE BRAND WISE TRANSACTION COUNT",
                        color_discrete_sequence= px.colors.sequential.Rainbow)
    st.plotly_chart(fig_bar3)




def tc_reg_user(table_name, state):

    col1, col2 = st.columns(2)
    with col1:
        years = st.selectbox('**Year**',('2018','2019','2020','2021','2022','2023'))
    with col1:    
        Quarter = st.selectbox('**Quarter**',('1','2','3','4'))

    column1, column2 = st.columns(2)

    query1 = f'''select districts, sum(registered_users) as registered_users from {table_name} 
                where State = '{state}' AND Years = {years} AND Quater = {Quarter}
                group by Districts order by Registered_Users desc limit 10'''
    cursor.execute(query1)
    qtable1 = cursor.fetchall()
    mydb.commit()

    with column1:
        df1 = pd.DataFrame(qtable1, columns=("Districts", "Registered_users"))

        fig_bar1 = px.pie(df1, names= "Districts", values= "Registered_users",
                            width= 600, title= "TOP 10",
                            color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_bar1)


    query2 = f'''select districts, sum(registered_users) as registered_users from {table_name} 
                where State = '{state}' AND Years = {years} AND Quater = {Quarter}
                group by Districts order by Registered_Users limit 10'''
    cursor.execute(query2)
    qtable2 = cursor.fetchall()
    mydb.commit()

    with column2:
        df2 = pd.DataFrame(qtable2, columns=("Districts", "Registered_users"))

        fig_bar2 = px.pie(df2, names= "Districts", values= "Registered_users",
                            width= 600, title= "LEAST 10",
                            color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_bar2)

    query3 = f'''select districts, avg(registered_users) as registered_users from {table_name} 
                where State = '{state}' AND Years = {years} AND Quater = {Quarter}
                group by Districts order by Registered_Users'''
    cursor.execute(query3)
    qtable3 = cursor.fetchall()
    mydb.commit()

    df3 = pd.DataFrame(qtable3, columns=("Districts", "Registered_users"))

    fig_bar3 = px.bar(df3, x= "Registered_users", y= "Districts", orientation="h",
                        width= 600, title= "AVERAGE REGISTERED USER",
                        color_discrete_sequence= px.colors.sequential.Rainbow)
    st.plotly_chart(fig_bar3)


def tc_app_open(table_name, state):

    col1, col2 = st.columns(2)
    with col1:
        years = st.selectbox('**Year**',('2018','2019','2020','2021','2022','2023'))
    with col1:    
        Quarter = st.selectbox('**Quarter**',('1','2','3','4'))

    column1, column2 = st.columns(2)

    query1 = f'''select districts, sum(App_Opens) as App_Opens from {table_name} 
                where State = '{state}' AND Years = {years} AND Quater = {Quarter}
                group by Districts order by App_Opens desc limit 10'''
    cursor.execute(query1)
    qtable1 = cursor.fetchall()
    mydb.commit()

    with column1:
        df1 = pd.DataFrame(qtable1, columns=("Districts", "App_Opens"))

        fig_bar1 = px.pie(df1, names= "Districts", values= "App_Opens",
                            width= 600, title= "TOP 10",
                            color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_bar1)


    query2 = f'''select districts, sum(App_Opens) as App_Opens from {table_name} 
                where State = '{state}' AND Years = {years} AND Quater = {Quarter}
                group by Districts order by App_Opens limit 10'''
    cursor.execute(query2)
    qtable2 = cursor.fetchall()
    mydb.commit()

    with column2:
        df2 = pd.DataFrame(qtable2, columns=("Districts", "App_Opens"))

        fig_bar2 = px.pie(df2, names= "Districts", values= "App_Opens",
                            width= 600, title= "LEAST 10",
                            color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_bar2)

    query3 = f'''select districts, avg(App_Opens) as App_Opens from {table_name} 
                where State = '{state}' AND Years = {years} AND Quater = {Quarter}
                group by Districts order by App_Opens'''
    cursor.execute(query3)
    qtable3 = cursor.fetchall()
    mydb.commit()

    df3 = pd.DataFrame(qtable3, columns=("Districts", "App_Opens"))

    fig_bar3 = px.bar(df3, x= "App_Opens", y= "Districts", orientation="h",
                        width= 600, title= "AVERAGE USER APP OPENS",
                        color_discrete_sequence= px.colors.sequential.Rainbow)
    st.plotly_chart(fig_bar3)


def tc_top_user(table_name):

    col1, col2 = st.columns(2)
    with col1:
        years = st.selectbox('**Year**',('2018','2019','2020','2021','2022','2023'))
    with col1:    
        Quarter = st.selectbox('**Quarter**',('1','2','3','4'))

    column1, column2 = st.columns(2)

    query1 = f'''select state, sum(registered_users) as Registered_users from {table_name} 
                where Years = {years} AND Quater = {Quarter} group by State
                order by Registered_Users desc limit 10'''
    cursor.execute(query1)
    qtable1 = cursor.fetchall()
    mydb.commit()

    with column1:
        df1 = pd.DataFrame(qtable1, columns=("State", "Registered_Users"))

        fig_bar1 = px.pie(df1, names= "State", values= "Registered_Users",
                            width= 600, title= "TOP 10",
                            color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_bar1)


    query2 = f'''select state, sum(registered_users) as Registered_users from {table_name} 
                where Years = {years} AND Quater = {Quarter} group by State
                order by Registered_Users limit 10'''
    cursor.execute(query2)
    qtable2 = cursor.fetchall()
    mydb.commit()

    with column2:
        df2 = pd.DataFrame(qtable2, columns=("State", "Registered_Users"))

        fig_bar2 = px.pie(df2, names= "State", values= "Registered_Users",
                            width= 600, title= "LEAST 10",
                            color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_bar2)

    query3 = f'''select state, avg(registered_users) as Registered_users from {table_name} 
                where Years = {years} AND Quater = {Quarter} group by State
                order by Registered_Users'''
    cursor.execute(query3)
    qtable3 = cursor.fetchall()
    mydb.commit()

    df3 = pd.DataFrame(qtable3, columns=("State", "Registered_Users"))

    fig_bar3 = px.bar(df3, x= "Registered_Users", y= "State", orientation="h",
                        width= 600, title= "AVERAGE REGISTERED USERS",
                        color_discrete_sequence= px.colors.sequential.Rainbow)
    st.plotly_chart(fig_bar3)


def tc_map_trans(table_name):

    col1, col2 = st.columns(2)
    with col1:
        years = st.selectbox('**Year**',('2018','2019','2020','2021','2022','2023'))
    with col1:    
        Quarter = st.selectbox('**Quarter**',('1','2','3','4'))

    column1, column2 = st.columns(2)

    query1 = f'''select Districts, sum(Transaction_count) as Transaction_count from {table_name} 
                where Years = {years} AND Quater = {Quarter} group by Districts
                order by Transaction_count desc limit 10'''
    cursor.execute(query1)
    qtable1 = cursor.fetchall()
    mydb.commit()

    with column1:
        df1 = pd.DataFrame(qtable1, columns=("Districts", "Transaction_count"))

        fig_bar1 = px.pie(df1, names= "Districts", values= "Transaction_count",
                            width= 600, title= "TOP 10",
                            color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_bar1)


    query2 = f'''select Districts, sum(Transaction_count) as Transaction_count from {table_name} 
                where Years = {years} AND Quater = {Quarter} group by Districts
                order by Transaction_count limit 10'''
    cursor.execute(query2)
    qtable2 = cursor.fetchall()
    mydb.commit()

    with column2:
        df2 = pd.DataFrame(qtable2, columns=("Districts", "Transaction_count"))

        fig_bar2 = px.pie(df2, names= "Districts", values= "Transaction_count",
                            width= 600, title= "LEAST 10",
                            color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_bar2)

    query3 = f'''select Districts, sum(Transaction_count) as Transaction_count from {table_name} 
                where Years = {years} AND Quater = {Quarter} group by Districts
                order by Transaction_count'''
    cursor.execute(query3)
    qtable3 = cursor.fetchall()
    mydb.commit()

    df3 = pd.DataFrame(qtable3, columns=("Districts", "Transaction_count"))

    fig_bar3 = px.bar(df3, x= "Transaction_count", y= "Districts", orientation="h",
                        width= 600, title= "DISTRICTS WISE AVERAGE TRANSACTION COUNT",
                        color_discrete_sequence= px.colors.sequential.Rainbow)
    st.plotly_chart(fig_bar3)




#Streamlit

st.set_page_config(layout="wide")
st.title("PhonePe DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    selected = option_menu("Menu", ["Home","Explore Data", "Charts"], 
                icons=["house","graph-up-arrow","bar-chart-line", "list-task"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#9a78eb"},
                        "nav-link-selected": {"background-color": "#5d78a3"}})
    
if selected == "Home":
    st.markdown("## :grey[A User-Friendly Tool Using Streamlit and Plotly]")
    st.markdown("### The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With over 45% market share, PhonePe's data is representative of the country's digital payment habits. This project aims on data analysis of user, that helps us to improve user requirements and friendly access.")
    st.image("phonepemap.jpeg")



if selected == "Explore Data":
    explore_data = st.sidebar.selectbox("**Type of data**",('SELECT','Aggregated Analysis', 'Map Analysis', 'Top Analysis'))
    if explore_data == 'Aggregated Analysis':
        agg_analysis = st.sidebar.selectbox("Select the data", ['Transaction', 'User'])

        if agg_analysis == 'Transaction':
            #col1, col2 = st.columns(2)
            
            #with col1:
            years = st.sidebar.slider("**Year**", agg_trans["Year"].min(), agg_trans["Year"].max(),agg_trans["Year"].min())            
            trany = trans_amt_count_year(agg_trans,years)

            #col1, col2 = st.columns(2)
            #with col1:
            states = st.selectbox("Select the States", trany["State"].unique())
            agg_trans_chart(trany, states)

            #col1, col2 = st.columns(2)
            #with col1:
            Quarter = st.sidebar.slider("Quarter", trany["Quater"].min(), trany["Quater"].max(),trany["Quater"].min())
            tranq = trans_amt_count_quarter(trany, Quarter)

            #col1, col2 = st.columns(2)
            #with col1:
            states = st.sidebar.selectbox("Select States", tranq["State"].unique())
            agg_trans_chart(tranq, states)
        
        
        elif agg_analysis == 'User':
            years = st.sidebar.slider("**Year**", agg_user["Year"].min(), agg_user["Year"].max(), agg_user["Year"].min())            
            auser_year = auser_plot1(agg_user, years)
                
            quaters = st.sidebar.slider("**Quarter**", auser_year["Quater"].min(), auser_year["Quater"].max(), auser_year["Quater"].min())            
            auser_qu = auser_plot2(auser_year, quaters)

            states = st.sidebar.selectbox("Select States", auser_qu["State"].unique())
            auser_plot3(auser_qu, states)



    if explore_data == 'Map Analysis':
        map_analysis = st.sidebar.selectbox("Select the data", ['Transaction', 'User'])

        if map_analysis == 'Transaction':
            years = st.sidebar.slider("**Year**", map_trans["Year"].min(), map_trans["Year"].max(), map_trans["Year"].min())            
            mapty = trans_amt_count_year(map_trans, years)

            states = st.selectbox("Select the States", mapty["State"].unique())
            map_trans_chart(mapty, states)

            Quarter = st.sidebar.slider("Quarter", mapty["Quater"].min(), mapty["Quater"].max(),mapty["Quater"].min())
            maptq = trans_amt_count_quarter(mapty, Quarter)

            states = st.selectbox("Select States", maptq["State"].unique())
            map_trans_chart(maptq, states)


        elif map_analysis == 'User':
            years = st.sidebar.slider("**Year**", map_user["Year"].min(), map_user["Year"].max(), map_user["Year"].min())            
            mapuy = muser_plot1(map_user, years)

            Quarter = st.sidebar.slider("Quarter", mapuy["Quater"].min(), mapuy["Quater"].max(),mapuy["Quater"].min())
            mapuq = muser_plot(mapuy, Quarter)

            states = st.sidebar.selectbox("Select States", mapuq["State"].unique())
            muser_plot_s(mapuq, states)


    if explore_data == 'Top Analysis':
        top_analysis = st.sidebar.selectbox("Select the data", ['Transaction', 'User'])

        if top_analysis == 'Transaction':
            years = st.sidebar.slider("**Year**", top_trans["Year"].min(), top_trans["Year"].max(), top_trans["Year"].min())            
            topty = trans_amt_count_year(top_trans, years)

            states = st.selectbox("Select the States", topty["State"].unique())
            top_trans_chart(topty, states)

            Quarter = st.sidebar.slider("Quarter", topty["Quater"].min(), topty["Quater"].max(),topty["Quater"].min())
            topuq = trans_amt_count_quarter(topty, Quarter)


        elif top_analysis == 'User':
            years = st.sidebar.slider("**Year**", top_user["Year"].min(), top_user["Year"].max(), top_user["Year"].min())            
            topuy = tuser_plot1(top_user, years)

            states = st.selectbox("Select the States", topuy["State"].unique())
            tuser_plot2(topuy, states)
            





if selected == "Charts":

    que = st.selectbox("TOP CHARTS", ["1. Transaction count analysis of Aggregated Transaction",
                        "2. Transaction amount analysis of Aggregated Transaction",
                        "3. Transaction count analysis of Aggregated Users",
                        "4. Brands wise analysis of Aggregated Users",
                        "5. Districts Wise Transaction count analysis of Map Transactions",
                        "6. Transaction count analysis of Map Transaction",
                        "7. Transaction amount analysis of Map Transaction",
                        "8. Registered Users analysis of Map users",
                        "9. App Opens analysis of users",
                        "10. Transaction count analysis of Top Transaction",
                        "11. Transaction amount analysis of Aggregated Transaction",
                        "12. Registered users analysis of Top User category"])
    
    if que == "1. Transaction count analysis of Aggregated Transaction":
        tc_tran_count("agg_trans")

    elif que == "2. Transaction amount analysis of Aggregated Transaction":
        tc_tran_amt("agg_trans")

    elif que == "3. Transaction count analysis of Aggregated Users":
        tc_tran_count("agg_user")

    elif que == "4. Brands wise analysis of Aggregated Users":
        tc_brands("agg_user")

    elif que == "5. Districts Wise Transaction count analysis of Map Transactions":
        tc_brands("agg_user")

    elif que == "6. Transaction count analysis of Map Transaction":
        tc_tran_count("map_trans")

    elif que == "7. Transaction amount analysis of Map Transaction":
        tc_tran_amt("map_trans")

    elif que == "8. Registered Users analysis of Map users":
        col1, col2 = st.columns(2)
        with col1:
            states = st.selectbox("Select State", map_user["State"].unique())
        tc_reg_user("map_user", states)

    elif que == "9. App Opens analysis of users":
        col1, col2 = st.columns(2)
        with col1:
            states = st.selectbox("Select State", map_user["State"].unique())
        tc_app_open("map_user", states)

    elif que == "10. Transaction count analysis of Top Transaction":
        tc_tran_count("top_trans")

    elif que == "11. Transaction amount analysis of Aggregated Transaction":
        tc_tran_amt("top_trans")

    elif que == "12. Registered users analysis of Top User category":
        tc_top_user("top_users")

    