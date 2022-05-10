# -*- coding: utf-8 -*-

import requests
import pandas as pd


#Obtaining Energy Data from EIA.gov for Natural Gas (ng), Coal, and Liquid Petroleum (lp)
api_key = 'ww07briKTAwpNMZbL9TO4REBb2t7DUZ8c3MeeI7V'

ng_parent_url = 'https://api.eia.gov/category/?api_key='+api_key+'&category_id=432'
ng_parent_response = requests.get(ng_parent_url).json()['category']['childseries']

coal_parent_url = 'https://api.eia.gov/category/?api_key='+api_key+'&category_id=429'
coal_parent_response = requests.get(coal_parent_url).json()['category']['childseries']

lp_parent_url = 'https://api.eia.gov/category/?api_key='+api_key+'&category_id=430'
lp_parent_response = requests.get(lp_parent_url).json()['category']['childseries']



#Create data frame
df = pd.DataFrame(columns = ['state_id', 'consumption'])

#Create function to make second API call
def get_state_data(series_id):
    child_url = 'https://api.eia.gov/series/?api_key='+api_key+'&series_id='+series_id
    child_response = requests.get(child_url).json()['series'][0]['data']
    
    return child_response


#Takes series_id returned by first API call and uses it to make second API call and iterate through the data for each territory returning only state ID and monthly consumption
for ng_child in ng_parent_response[1::3]:
    ng_series_id = ng_child['series_id']
    ng_child_response = get_state_data(ng_series_id)

    df = df.append({'state_id' : ng_series_id, 
                   'consumption' : ng_child_response}, 
                    ignore_index=True)
   

for coal_child in coal_parent_response[1::3]:
    coal_series_id = coal_child['series_id']
    coal_child_response = get_state_data(coal_series_id)

    df = df.append({'state_id' : coal_series_id, 
                   'consumption' : coal_child_response}, 
                    ignore_index=True)
    
    
for lp_child in lp_parent_response[1::3]: 
    lp_series_id = lp_child['series_id']
    lp_child_response = get_state_data(lp_series_id)

    df = df.append({'state_id' : lp_series_id, 
                   'consumption' : lp_child_response}, 
                    ignore_index=True)


print(df)