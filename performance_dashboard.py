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

#Application Layout
app.layout = html.Div(children = [
    #Title of Dashboard
    html.H1('US Domestice Airline Flights Performance', style = {'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),
    #Creating Outer Division
    html.Div([
        html.Div(
            [html.H2('Report Type:', style = {'margin-right':'2em'}),
            ]
        ),
        #Dropdown Creation for Selecting Report Type
        dcc.Dropdown(id = 'input-type', 
            options = [{'label': 'Yearly Airline Performance Report', 'value': 'OPT1'},
            {'label': 'Yearly Airline Delay Report', 'value': 'OPT2'}],
            placeholder = 'Select a report type',
            style = {'width': '80%', 'padding':'3px', 'font-size':'20px', 'textAlign':'center'},
            style = {'display':'flex'}), 
    #Add Next Division
    html.Div([
        html.Div([
        html.H2('Choose Year:', style = {'margin-right':'2em'})]), 
        #Dropdown for Year
        dcc.Dropdown(id = 'input-year', 
            #Update dropdown with values from list comprehension
            options = [{'label': i, 'value': i} for i in year_list], 
            placeholder = 'Select a year', 
            sytle = {'width': '80%', 'padding': '3px', 'font-size': '20px', 'textAlign': 'center'}),],
            syle = {'display':'flex'}),
        ]),
    #Add Computed graphs
    html.Div([ ], id = 'plot1'),
    html.Div([
        html.Div([ ], id = 'plot2'), 
        html.Div([ ], id = 'plot3')],
        style = {'display':'flex'}),
    html.Div([
        html.Div([ ], id = 'plot4'), 
        html.Div([ ], id = 'plot5')],
        style = {'display': 'flex'})
    #Add Next Division
])


#Callback function 
@app.callback(
    [Output('plot1', 'children'), 
    Output('plot2', 'children'),
    Output('plot3', 'children'),
    Output('plot4', 'children'),
    Output('plot5', 'children'),
    ],
    [Input('input-type', 'value'),
    Input('input-year', 'value')],
    [State("plot1", 'children'), State("plot2", 'children'),
    State("plot3", 'children'), State("plot4", 'children'),
    State("plot5", 'children'),]
    )

#Computation to callback funcation and return graph
def get_graph(chart, year, children1, children2, c3, c4, c5):
    #Select Data
    df = flight_data[flight_data['year']== int(year)]

    if chart == 'OPT1':
        #Compute required information for creating graph from data
        bar_data, line_data, div_data, map_data, tree_data = compute_data_choice_1(df)

        #Nuber of Flights under different cancelleation categories
        bar_fig = px.bar(bar_data, x = 'Month', y = 'Flights', color = 'CancellationCode', title = 'Monthly Flight Cancellation')

        #Average Flight time by reporting Airline

        #Percentage of diverted airport landings per reporting airline
        map_fig = px.choropleth(map_data, 
            locations = 'OriginState', 
            color = 'Flights', 
            hover_data = ['OriginState', 'Flights'],
            locationmode = 'USA-states',
            color_continuous_scale = 'GnBu',
            range_color = [0, map_data['Flights'].max()])
        map_fig.update_layout(
            title_text = 'Number of flights from origin staate',
            geo_scope = 'usa'
        )

        #Number of Flights flying to each state from reporting airline

        return[ dcc.Graph(figure = tree_fig),
           dcc.Graph(figure = pie_fig),
           dcc.Graph(figure = map_fig),
           dcc.Graph(figure = bar_fig), 
           dcc.Graph(figure = line_fig),]

    else: 
        #Information for creating graph from the data
        avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_data_choice_2(df)
        #Line plot for carrier delays
        carrier_fig = px.line(avg_car, x = 'Month', y = 'CarrierDelay', color = 'Reporting_Airline', title = 'Average Carrier Delay Time(Minutes) by Airline')
        weather_fig = px.line(avg_weather, x = 'Month', y = 'WeatherDelay', color = 'Reporting_Airline', title = 'Average Weather Delay Time(Minutes) by Airline')
        nas_fig = px.line(avg_NAS, x = 'Month', y = 'NASDelay', color = 'Reporting_Airline', title = 'Average NAS Delay Time(Minutes) by Airline')
        sec_fig = px.line(avg_sec, x = 'Month', y = 'SecurityDelay', color = 'Reporting_Airline', title = 'Average Security Delay Time(Minutes) by Airline')
        late_fig = px.line(avg_late, x = 'Month', y = 'LateAircraftDelay', color = 'Reporting_Airline', title = 'Average Late Aircraft Delay Time(Minutes) by Airlne')

        return[dcc.Graph(figure = carrier_fig),
           dcc.Graph(figure = weather_fig),
           dcc.Graph(figure = nas_fig),
           dcc.Graph(figure = sec_fig), 
           dcc.Graph(figure = late_fig),]


#Run the app
if __name__ == '__main__':
    app.run_server()