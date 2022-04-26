import pandas as pd 
import plotly.graph_objects as go 
import plotly.express as px 
import dash 
from dash import dcc 
from dash import html 
from dash.dependencies import Input, Output, State
from dash import no_update

#Create a dash Application
app = dash.Dash(__name__)

#Clear the layout and do not disply exception til callback gets initiated
app.config.suppress_callback_exceptions = True 

#Reading the Data
flight_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

# List of years 
year_list = [i for i in range(2005,2021, 1)]

#Computing graph data for creating yearly airline performance data
def compute_data_choice_1(df): 
    #Cancellation Category Count
    bar_data = df.groupby(['Month', 'ConcellationCode'])['Flights'].sum().reset_index()
    #Average flight time by reporting airline
    line_data = df.groupby(['Month', 'Reporting_Airline'])['AirTime'].mean().reset_index()
    #Diverted Airport Landings
    div_data = df[df['DivAirportLandings'] != 0.0]
    #Source state count 
    map_data = df.groupby(['OriginState'])['Flights'].sum().reset_index()
    #Destination state count
    tree_data = df.groupby(['DestState', 'Reporting_Airline'])['Flights'].sum().reset_index()
    return bar_data, line_data, div_data, map_data, tree_data

#Computing graph data for creating yearly airline delay report
def compute_data_choice_2(df): 
    #Compute delay average
    avg_car = df.groupby(['Month', 'ReportingAirline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month', 'ReportingAirline'])['WeatherDealy'].mean().reset_index()
    avg_NAS = df.groupby(['Month', 'ReportingAirline'])['NASDelay'].mean().reset_index()
    avg_sec = df.groupby(['Month', 'ReportingAirline'])['SecurityDelay'].mean().reset_index()
    avg_late = df.groupby(['Month', 'ReportingAirline'])['LateAircraftDelay'].mean().reset_index()
    return avg_car, avg_weather, avg_NAS, avg_sec, avg_late




