import bs4
import branca.colormap as cm
import requests
import pandas as pd 
import numpy as np
import folium
from folium.plugins import MarkerCluster,BeautifyIcon
from folium import FeatureGroup, LayerControl
import json 
from utils import process_df,get_data_from_sheets


# dictionaty mapping state names with abbreviation
st_abbrev = json.load(open("st_abbrev.json", 'r'))
# url of the data
curl = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
rurl = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
durl = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"
# read data
curr_df = process_df(curl,st_abbrev)
recovery_df = process_df(rurl,st_abbrev)
death_df = process_df(durl,st_abbrev)

# get states coordinates for heatmap
url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
us_states = f'{url}/us-states.json'
US_Unemployment_Oct2012 = f'{url}/US_Unemployment_Oct2012.csv'
geo_json_data = json.loads(requests.get(us_states).text)

# coloring function for heatmap
linear = cm.LinearColormap(
    ['orange', 'red'],
    vmin=0, vmax=max(curr_df.cases)
)
def my_color_function(feature):
    return linear(list(curr_df[curr_df["states"] ==feature['id']].cases)[0])


# define map
covid_map = folium.Map(location=[curr_df['Lat'].mean(
), curr_df['Long'].mean()], zoom_start=5, zoom_control=False, max_bounds=True)

# plot heatmap for states
states_feature = FeatureGroup(name="States Heatmap")
folium.GeoJson(geo_json_data,
               style_function=lambda feature: {
                   'fillColor': my_color_function(feature),
                   'color': 'black',
                   'weight': 2,
                   'dashArray': '5, 5'
               }
               ).add_to(states_feature)
states_feature.add_to(covid_map)

# plot cluster for each case in each state

# custom JS function for cluster
icon_create_function = '''
 function (cluster) {
 var childCount = cluster.getChildCount();
 var c = ' marker-cluster-';
 if (childCount < 0) {
   c += 'small';
 } 
 else if (childCount < 0) {
   c += 'medium';
 } 
 else {
   c += 'large';
 }

 return new L.DivIcon({ html: '<div><span>' + childCount + '</span></div>', 
  className: 'marker-cluster' + c, iconSize: new L.Point(40, 40) });
 }
'''

icon_create_function_test = '''
 function (cluster) {
 var childCount = cluster.getChildCount();
 var c = ' marker-cluster-';
 if (childCount < 0) {
   c += 'small';
 } 
 else if (childCount < 0) {
   c += 'medium';
 } 
 else {
   c += 'large1';
 }

 return new L.DivIcon({ html: '<div style="background-color:rgba(0,159,220,0.7)"><span>' + childCount + '</span></div>', 
  className: 'marker-cluster' + c, iconSize: new L.Point(40, 40) });
 }
'''
# ---------- plot confirmed cases ----------- #
confCases = FeatureGroup(name='Confirmed Cases')
# mc = MarkerCluster(icon_create_function=icon_create_function)

# idx = 0
# for row in curr_df.itertuples():
#     idx+=1
#     for _ in range(int(row.cases)):
#         mc.add_child(folium.Circle(
#             location=[row.Lat, row.Long], radius=0, color='red'))
#     if idx>=5:
#         break


# mc.add_to(confCases)
# confCases.add_to(covid_map)


for row in curr_df.itertuples():
   folium.Circle(
       location=[row.Lat, row.Long],
       popup="{0}, Cases: {1}".format(row.states,int(row.cases)),
       radius=10000*np.log(row.cases),
       color='crimson',
       fill=True,
       fill_color='crimson'
   ).add_to(confCases)

confCases.add_to(covid_map)
# read data from spreadsheet

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SAMPLE_SPREADSHEET_ID = '1QmwkYAsWf6_4LP4-vTADqn55DePslfjNSgtJ770v0vk'
SAMPLE_RANGE_NAME = 'Centers'

tloc = get_data_from_sheets(SCOPES, SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME)
tloc = tloc.drop(tloc.index[0])
tloc[["Latitute", "Longitude"]] = tloc[[
    "Latitute", "Longitude"]].apply(pd.to_numeric)
tloc = tloc[tloc['Latitute'].notnull()]

mc2 = MarkerCluster(icon_create_function=icon_create_function_test)
# plot testing center data
testing_feature = FeatureGroup(name='Testing Centers')
for row in tloc.itertuples():
    # folium.Marker((row.Latitute, row.Longitude), popup=folium.Popup('<a href="%s" target="_blank"> %s </a>' %
                                                                    # (row.URL, row._2)), icon=folium.Icon(color='lightblue', icon='medkit', prefix='fa')).add_to(testing_feature)
    folium.Marker((row.Latitute, row.Longitude), popup=folium.Popup('<a href="%s" target="_blank"> %s </a>' %
                                                                    (row.URL, row._2)), icon=BeautifyIcon(icon='medkit', icon_shape='marker', background_color="#009FDC")).add_to(mc2)
mc2.add_to(testing_feature)
testing_feature.add_to(covid_map)


# ------------- plot traffic ------- #

# testing_traffic = FeatureGroup(name='Present Traffic')

# # CO cellphone data
# codf = pd.read_csv('https://raw.githubusercontent.com/nthakor/imghost/master/denver-06-16-1100-1159.csv')
# for i, row in codf.iterrows():
#     folium.Marker(location=[row.lat1, row.lon1],
#                   icon=BeautifyIcon(icon='car')).add_to(testing_traffic)
# # MD cellphone data
# mddf1 = pd.read_csv(
#     'https://raw.githubusercontent.com/nthakor/imghost/master/md-carrol-03-17-1100-1159.csv')
# for i, row in mddf1.iterrows():
#     folium.Marker(location=[row.lat1, row.lon1],
#                   icon=BeautifyIcon(icon='car')).add_to(testing_traffic)
# mddf2 = pd.read_csv(
#     'https://raw.githubusercontent.com/nthakor/imghost/master/md-medstar-03-17-1100-1159.csv')
# for i, row in mddf2.iterrows():
#     folium.Marker(location=[row.lat1, row.lon1],
#                   icon=BeautifyIcon(icon='car')).add_to(testing_traffic)
# mddf3 = pd.read_csv(
#     'https://raw.githubusercontent.com/nthakor/imghost/master/md-umd-03-17-1100-1159.csv')
# for i, row in mddf3.iterrows():
#     folium.Marker(location=[row.lat1, row.lon1],
#                   icon=BeautifyIcon(icon='car')).add_to(testing_traffic)
# testing_traffic.add_to(covid_map)

# Layer Control
# LayerControl().add_to(covid_map)

# covid_map.save("covid_19_us.html")

# read map, title and footnote as html file

soup = bs4.BeautifulSoup(covid_map.get_root().render(), 'html.parser')
with open('map_title.html') as f:
    txt = f.read()
    title = bs4.BeautifulSoup(txt,'html.parser')
with open('map_bottom.html') as f:
    txt = f.read()
    bottom = bs4.BeautifulSoup(txt,'html.parser')
title_command = title.div
bottom_command = bottom.div
# add title and footnote into map file
soup.body.div.insert_after(title_command)
soup.body.div.insert_after(bottom_command)
# link style sheet
map_style = bs4.BeautifulSoup(
    '<link rel="stylesheet" href="mapStyle.css"/>','html.parser')
soup.head.style.insert_after(map_style)
# store map
with open("covid_19_us.html", "w") as file:
    file.write(str(soup))
