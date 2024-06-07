import streamlit as st
import pandas as pd
import plotly.express as px
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

def load_smp_demand_data():
    file_path = '2024 SMP(5-22까지).xlsx'
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

def fetch_realtime_data():
    # Initialize the webdriver
    chrome_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service)
   
    # Open the webpage
    url = "https://epsis.kpx.or.kr/epsisnew/selectEkgeEpsMepRealChart.do?menuId=030300"
    driver.get(url)
    
    # Maximize the window
    driver.maximize_window()
    
    # Scroll to the bottom of the page to load initial data
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    
    # Initialize an empty DataFrame to store all data elements
    df = pd.DataFrame(columns=['temporary', 'supply capacity', 'current load', 'supply reserve capacity', 'supply reserve rate'])
    
    # Find the scrollbar element
    scrollbar = driver.find_element(By.CLASS_NAME, 'rMateH5__VBrowserScrollBar')
    
    scroll_count = 0
    max_scrolls = 24  # Set a maximum number of scrolls to prevent infinite loop
    
    while True:
        # Get the initial number of elements
        initial_size = len(df)

        # Get the page source and parse it
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Find elements containing the data
        elements = soup.find_all(class_=lambda c: c and c.startswith('rMateH5__DataGridItemRenderer rMateH5__DataGridColumn'))
        
        # Extract text from elements and add to a temporary list if not null
        new_elements = [element.text for element in elements if element.text.strip()]
        
        # Get the initial scrollbar position
        initial_scroll_position = driver.execute_script("return arguments[0].scrollTop;", scrollbar)
        
        # Scroll the scrollbar down a small amount
        driver.execute_script("arguments[0].scrollTop += 580;", scrollbar)
        time.sleep(2)
        
        # Get the new scrollbar position
        new_scroll_position = driver.execute_script("return arguments[0].scrollTop;", scrollbar)

        for element in new_elements:
            print(element)
        
        # Split the data into respective categories and append to the DataFrame
        if new_elements:
            num_entries = len(new_elements)
            num_iter = num_entries // 5 * 4   

            supply_capacity = []
            current_load = []
            supply_reserve_capacity = []
            supply_reserve_rate = []
            
            
            for i in range(0,num_iter,4):
                supply_capacity.append(new_elements[i])
                current_load.append(new_elements[i+1])
                supply_reserve_capacity.append(new_elements[i+2])
                supply_reserve_rate.append(new_elements[i+3])
            
            timestamps = new_elements[num_iter:num_entries]
                
            
            
            temp_df = pd.DataFrame({
                '시간': timestamps,
                '공급능력': supply_capacity,
                '현재부하': current_load,
                '공급예비력': supply_reserve_capacity,
                '공급예비율': supply_reserve_rate
            })
            
            df = pd.concat([df, temp_df], ignore_index=True)
        
        # Check if scrollbar position did not change
        if initial_scroll_position == new_scroll_position:
            break
        
        # Increment scroll counter and check if max scrolls reached
        scroll_count += 1
        if scroll_count >= max_scrolls:
            print("Reached maximum scroll limit.")
            break
    
    # Close the webdriver
    driver.quit()
    
    # Print the DataFrame
    df = df.drop_duplicates()
    df = df.sort_values(by = 'temporary')

    return df

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
    df_Announcement = fetch_realtime_data()
    
    # Plot today's announcement data
    st.subheader("Today's Announcement")
    
    columns_to_plot = {
        '공급능력': 'Supply Capacity (MW)',
        '현재부하': 'Current Load (MW)',
        '공급예비력': 'Supply Reserve Capacity (MW)',
        '공급예비율': 'Supply Reserve Rate (%)'
    }
    
    for column, title in columns_to_plot.items():
        st.subheader(title)
        fig = px.line(df_Announcement, x='temporary', y=column, title=title)
        st.plotly_chart(fig)