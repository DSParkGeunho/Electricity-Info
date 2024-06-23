#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


def load_smp_demand_data():
    file_path = 'data/2024 SMP 육지.xlsx'
    df_SMP = pd.read_excel(file_path)
    new_file_path = 'data/전력수요예측.xlsx'
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


# In[3]:


def load_rec_data():
    rec_file_path = 'data/REC가격 변동.xlsx'
    df_REC = pd.read_excel(rec_file_path)
    df_REC['거래일'] = pd.to_datetime(df_REC['거래일'], format='%Y%m%d')
    df_REC['거래일'] = df_REC['거래일'].dt.strftime('%Y-%m-%d')
    return df_REC


# In[4]:


def load_fuel_cost_data():
    fuel_cost_file_path = 'data/연료비단가.xlsx'
    df_FuelCost = pd.read_excel(fuel_cost_file_path)
    df_FuelCost['기간'] = pd.to_datetime(df_FuelCost['기간'], format='%Y/%m')
    df_FuelCost['기간'] = df_FuelCost['기간'].dt.strftime('%Y-%m')
    return df_FuelCost


# In[5]:


def load_power_trading_data():
    power_trading_file_path = 'data/전력거래량.xlsx'
    df_PowerTrading = pd.read_excel(power_trading_file_path)
    df_PowerTrading['기간'] = pd.to_datetime(df_PowerTrading['기간'], format='%Y/%m')
    df_PowerTrading['기간'] = df_PowerTrading['기간'].dt.strftime('%Y-%m')
    return df_PowerTrading


# In[6]:


def load_power_bidding_data():
    power_bidding_file_path = 'data/전력입찰량.xlsx'
    df_PowerBidding = pd.read_excel(power_bidding_file_path)
    df_PowerBidding['기간'] = pd.to_datetime(df_PowerBidding['기간'], format='%Y/%m')
    df_PowerBidding['기간'] = df_PowerBidding['기간'].dt.strftime('%Y-%m')
    return df_PowerBidding


# In[8]:


def load_UnitCost_data():
    file_path = 'data/정산단가.xlsx'
    df_UnitCost = pd.read_excel(file_path)
    df_UnitCost['기간'] = pd.to_datetime(df_UnitCost['기간'], format='%Y/%m')
    df_UnitCost['기간'] = df_UnitCost['기간'].dt.strftime('%Y-%m')
    return df_UnitCost


# In[9]:


def load_smp_count_data():
    file_path_smp_count = 'data/연료원별SMP결정.xlsx'
    df_SMPCount = pd.read_excel(file_path_smp_count)
    df_SMPCount['기간'] = pd.to_datetime(df_SMPCount['기간'], format='%Y/%m')
    df_SMPCount['기간'] = df_SMPCount['기간'].dt.strftime('%Y-%m')
    return df_SMPCount


# In[10]:


def load_today_data():
    file_path_today = 'data/today.xlsx'
    df_today = pd.read_excel(file_path_today)
    df_today['temporary'] = pd.to_datetime(df_today['temporary'], format='%Y-%m-%d %H:%M')
    return df_today


# In[ ]:




