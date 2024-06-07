import streamlit as st
import pandas as pd
import plotly.express as px
from bs4 import BeautifulSoup
import pandas as pd



def load_smp_demand_data():
    file_path = '2024 SMP 육지.xlsx'
    df_SMP = pd.read_excel(file_path)
    new_file_path = '전력수요예측.xlsx'
    df_Demand = pd.read_excel(new_file_path)
    
    for data in [df_SMP, df_Demand]:
        data['구분'] = pd.to_datetime(data['구분'], format='%Y%m%d')
        data['구분'] = data['구분'].dt.strftime('%Y-%m-%d')
    
    df_SMP_melted = df_SMP.melt(id_vars=['구분'], value_vars=[str(i) + 'h' for i in range(1, 25)], 
                                var_name='Time', value_name='SMP')
    df_Demand_melted = df_Demand.melt(id_vars=['구분'], value_vars=[str(i) + 'h' for i in range(1, 25)], 
                                      var_name='Time', value_name='Demand')
    
    for data in [df_SMP_melted, df_Demand_melted]:
        data['Time'] = data['Time'].str.replace('h', ':00')
    
    return df_SMP_melted, df_Demand_melted

def load_rec_data():
    rec_file_path = 'REC가격 변동.xlsx'
    df_REC = pd.read_excel(rec_file_path)
    df_REC['거래일'] = pd.to_datetime(df_REC['거래일'], format='%Y%m%d')
    df_REC['거래일'] = df_REC['거래일'].dt.strftime('%Y-%m-%d')
    return df_REC

def load_fuel_cost_data():
    fuel_cost_file_path = '연료비단가.xlsx'
    df_FuelCost = pd.read_excel(fuel_cost_file_path)
    df_FuelCost['기간'] = pd.to_datetime(df_FuelCost['기간'], format='%Y/%m')
    df_FuelCost['기간'] = df_FuelCost['기간'].dt.strftime('%Y-%m')
    return df_FuelCost

def load_power_trading_data():
    power_trading_file_path = '전력거래량.xlsx'
    df_PowerTrading = pd.read_excel(power_trading_file_path)
    df_PowerTrading['기간'] = pd.to_datetime(df_PowerTrading['기간'], format='%Y/%m')
    df_PowerTrading['기간'] = df_PowerTrading['기간'].dt.strftime('%Y-%m')
    return df_PowerTrading

def load_power_bidding_data():
    power_bidding_file_path = '전력입찰량.xlsx'
    df_PowerBidding = pd.read_excel(power_bidding_file_path)
    df_PowerBidding['기간'] = pd.to_datetime(df_PowerBidding['기간'], format='%Y/%m')
    df_PowerBidding['기간'] = df_PowerBidding['기간'].dt.strftime('%Y-%m')
    return df_PowerBidding

def load_UnitCost_data():
    file_path = '정산단가.xlsx'
    df_UnitCost = pd.read_excel(file_path)
    df_UnitCost['기간'] = pd.to_datetime(df_UnitCost['기간'], format='%Y/%m')
    df_UnitCost['기간'] = df_UnitCost['기간'].dt.strftime('%Y-%m')
    return df_UnitCost

def load_smp_count_data():
    file_path_smp_count = '연료원별SMP결정.xlsx'
    df_SMPCount = pd.read_excel(file_path_smp_count)
    df_SMPCount['기간'] = pd.to_datetime(df_SMPCount['기간'], format='%Y/%m')
    df_SMPCount['기간'] = df_SMPCount['기간'].dt.strftime('%Y-%m')
    return df_SMPCount


def load_today_data():
    file_path_today = 'today.xlsx'
    df_today = pd.read_excel(file_path_today)
    df_today['temporary'] = pd.to_datetime(df_today['temporary'], format='%Y-%m-%d %H:%M')
    return df_today
    

st.title("Electricity trading Dashboard")
view_option = st.radio(
    "Select data to view:",
    ('SMP and Demand Data', 'REC Price Trend', 'Fuel Cost Price', "Power Trading Volume", "Power Bidding Volume", "Unit Cost", "SMP Count Data", "Today's Announcement"),
    key="view_selector"
)

if view_option == 'SMP and Demand Data':
    df_SMP_melted, df_Demand_melted = load_smp_demand_data()
    
    # Date selection
    selected_date = st.date_input("Select a date", pd.to_datetime(df_SMP_melted['구분']).min(), key="date_selector")
    
    # Filter data based on the selected date
    filtered_df_SMP = df_SMP_melted[df_SMP_melted['구분'] == selected_date.strftime('%Y-%m-%d')]
    filtered_df_Demand = df_Demand_melted[df_Demand_melted['구분'] == selected_date.strftime('%Y-%m-%d')]
    
    # Plot SMP data
    st.subheader(f"SMP Data for {selected_date.strftime('%Y-%m-%d')}")
    fig_smp = px.line(filtered_df_SMP, x='Time', y='SMP', title=f'SMP Data for {selected_date.strftime("%Y-%m-%d")}')
    st.plotly_chart(fig_smp)
    
    # Plot Demand data
    st.subheader(f"Demand Data for {selected_date.strftime('%Y-%m-%d')}")
    fig_demand = px.line(filtered_df_Demand, x='Time', y='Demand', title=f'Demand Data for {selected_date.strftime("%Y-%m-%d")}')
    st.plotly_chart(fig_demand)
    
elif view_option == 'REC Price Trend':
    df_REC = load_rec_data()
    
    # Plot REC price trend
    st.subheader("REC Price Trend")
    
    columns_to_plot = {
        '육지 거래량(REC)': 'Land Transaction Volume (REC)',
        '육지 평균가(원)': 'Land Average Price (KRW)',
        '육지 최고가(원)': 'Land Highest Price (KRW)',
        '육지 최저가(원)': 'Lowest price on land (KRW)',
        '제주 거래량(REC)': 'Jeju Transaction Volume (REC)',
        '제주 평균가(원)': 'Jeju Average Price (KRW)',
        '제주 최고가(원)': 'Jeju Highest Price (KRW)',
        '제주 최저가(원)': 'Jeju Lowest Price (KRW)',
        '종가(원)': 'Close Price (KRW)'
    }
    
    for column, title in columns_to_plot.items():
        st.subheader(title)
        fig = px.line(df_REC, x='거래일', y=column, title=title)
        st.plotly_chart(fig)
elif view_option == 'Fuel Cost Price':
    df_FuelCost = load_fuel_cost_data()
    
    # Plot fuel cost price trend
    st.subheader("Fuel Cost Price Trend KRW/KWh")
    
    columns_to_plot = {
        '원자력': 'Nuclear Power',
        '유연탄': 'Bituminous Coal',
        '무연탄': 'Anthracite',
        '유류': 'Oil',
        'LNG': 'LNG'
    }
    
    for column, title in columns_to_plot.items():
        st.subheader(title)
        fig = px.line(df_FuelCost, x='기간', y=column, title=title)
        st.plotly_chart(fig)
elif view_option == "Power Trading Volume":
    df_PowerTrading = load_power_trading_data()
    
    # Plot power trading volume data
    st.subheader("Power Trading Volume")
    
    columns_to_plot = [
        '원자력', '유연탄', '무연탄', '석탄 합계', '유류', 'LNG', '양수', '연료전지', 
        '석탄가스화', '태양', '풍력', '수력', '해양', '바이오', '폐기물', '신재생합계', 
        '기타', '전력시장 합계', 'PPA 합계', '전력시장+PPA 합계'
    ]
    
    for column in columns_to_plot:
        st.subheader(column)
        fig = px.line(df_PowerTrading, x='기간', y=column, title=column)
        st.plotly_chart(fig)

elif view_option == "Power Bidding Volume":
    df_PowerBidding = load_power_bidding_data()
    
    # Plot power bidding volume data
    st.subheader("Power Bidding Volume")
    
    columns_to_plot = [
        '원자력', '유연탄', '무연탄', '석탄 합계', '유류', 'LNG', '양수', '연료전지', 
        '석탄가스화', '태양', '풍력', '수력', '해양', '바이오', '폐기물', '신재생합계', 
        '기타', '합계'
    ]
    
    for column in columns_to_plot:
        st.subheader(column)
        fig = px.line(df_PowerBidding, x='기간', y=column, title=column)
        st.plotly_chart(fig)

elif view_option == "Unit Cost":
    df_UnitCost = load_UnitCost_data()
    
    # Plot new data
    st.subheader("Unit Cost")
    
    columns_to_plot = {
        '원자력': 'Nuclear Power',
        '유연탄': 'Bituminous Coal',
        '무연탄': 'Anthracite',
        '석탄합계': 'Total Coal',
        '유류': 'Oil',
        'LNG': 'LNG',
        '양수': 'Pumped Storage',
        '연료전지': 'Fuel Cell',
        '석탄가스화': 'Coal Gasification',
        '태양': 'Solar',
        '풍력': 'Wind',
        '수력': 'Hydro',
        '해양': 'Marine',
        '바이오': 'Bio',
        '폐기물': 'Waste',
        '신재생합계': 'Total Renewable',
        '기타': 'Others',
        '합계': 'Total'
    }
    
    for column, title in columns_to_plot.items():
        st.subheader(title)
        fig = px.line(df_UnitCost, x='기간', y=column, title=title)
        st.plotly_chart(fig)
elif view_option == "SMP Count Data":
    df_SMPCount = load_smp_count_data()
    
    # Plot SMP Count data
    st.subheader("SMP Count Data")
    
    columns_to_plot = {
        'LNG': 'LNG',
        '유류': 'Oil',
        '무연탄': 'Anthracite',
        '유연탄': 'Bituminous Coal',
        '원자력': 'Nuclear Power',
        '총계': 'Total'
    }
    
    for column, title in columns_to_plot.items():
        st.subheader(title)
        fig = px.line(df_SMPCount, x='기간', y=column, title=title)
        st.plotly_chart(fig)

else:
    df_Announcement = load_today_data()
    
    # Plot today's announcement data
    st.subheader("Today's Announcement")
    
    columns_to_plot = {
        'supply capacity': 'supply_capacity',
        'current load': 'current_load',
        'supply reserve capacity': 'supply_reserve_capacity',
        'supply reserve rate': 'supply_reserve_rate'
    }
    
    for column, title in columns_to_plot.items():
        st.subheader(title)
        fig = px.line(df_Announcement, x='temporary', y=column, title=title)
        st.plotly_chart(fig)