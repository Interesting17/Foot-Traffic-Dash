# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 14:04:38 2020

@author: amrob
"""


import pandas as pd
import dash
import statistics as stc
import datetime as dt 
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from plotly import graph_objects as go
from Traffic_View_Class import Traffic_View as TV


data = pd.read_excel('FootTrafficUpdate.xlsx')
data = data.drop(columns = 'Unnamed: 0')
print(data.columns)


indexNames = data[ data['Traffic'] == 'Not Working' ].index
data.drop(indexNames , inplace=True)

image_saco = 'saco_logo.jpg'
image_17 = '17.png'


for i in range(data.shape[0]):
    if data.iloc[i,5] == 1:
        data.iloc[i,7] = 2020
        
print(data)



date = data['Date']
date = list(dict.fromkeys(date))
#print(date)
dic_date = dict()
for i in date:
    dic_date[i] = 0
    
list_dates = list(dic_date.keys())
#print(list_dates)

data_Central = data[data['Region'] == 'Central']
data_Western = data[data['Region'] == 'Western']
data_Eastern = data[data['Region'] == 'Eastern']


List_Traffic_Central = []
for i in date:
    dic_date[i] = 0
for k in dic_date:
     for i in range(data_Central.shape[0]):            
        if str(data_Central.iloc[i,3]) == str(k):            
            dic_date[k] = dic_date[k] + int(data_Central.iloc[i,1])
     List_Traffic_Central.append(dic_date[k])      

Sum_Central = 0    
for i in List_Traffic_Central:
    Sum_Central = Sum_Central + i    
#print(List_Traffic_Central)

List_Traffic_Western = []
for i in date:
    dic_date[i] = 0
for k in dic_date:
     for i in range(data_Western.shape[0]):            
        if str(data_Western.iloc[i,3]) == str(k):            
            dic_date[k] = dic_date[k] + int(data_Western.iloc[i,1])
     List_Traffic_Western.append(dic_date[k])      
    
Sum_Western = 0 
for i in List_Traffic_Western: 
     Sum_Western = Sum_Western + i    
#print(List_Traffic_Western)


List_Traffic_Eastern = []
for i in date:
    dic_date[i] = 0
for k in dic_date:
     for i in range(data_Eastern.shape[0]):            
        if str(data_Eastern.iloc[i,3]) == str(k):            
            dic_date[k] = dic_date[k] + int(data_Eastern.iloc[i,1])
     List_Traffic_Eastern.append(dic_date[k])      
    
Sum_Eastern = 0
for i in List_Traffic_Eastern:
     Sum_Eastern = Sum_Eastern + i     
#print(List_Traffic_Eastern)

List_Traffic_All = []
for i in date:
    dic_date[i] = 0
for k in dic_date:
     for i in range(data.shape[0]):            
        if str(data.iloc[i,3]) == str(k):            
            dic_date[k] = dic_date[k] + int(data.iloc[i,1])
     List_Traffic_All.append(dic_date[k])

Sum_All = 0 
for i in List_Traffic_All:
    Sum_All = Sum_All + i 


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
server = app.server

app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
       
    dbc.Row([html.Br(), html.Br(),
             dbc.Col(lg=1),
             #dbc.Col([html.Img(src=app.get_asset_url('saco_logo.png'))], lg= 1),
             dbc.Col([html.Br(), html.Br(), html.Div([html.P("SACO Foot Traffic Dashboard")], style={'textAlign': "center", 'font-size':'300%', 'font-family':'Roboto Condensed', 'font-weight': 'bold'})]),  
             #dbc.Col([html.Img(src=app.get_asset_url('17.png'))], lg= 1),
             dbc.Col(lg=1)
              ]),

    dbc.Row([
        html.Br(), html.Br(),
        dbc.Col(lg=1),
        dbc.Col([
            html.Br(),
            dbc.Label('Select a Region:'),
            dcc.Dropdown(id='Region_dropdown',
                         placeholder='Select Region',
                         value='All',
                         options= [{'label': 'Central', 'value': 'Central'},
                                  {'label': 'Western', 'value': 'Western'},
                                  {'label': 'Eastern', 'value': 'Eastern'},
                                  {'label':'All', 'value':'All'}
                                  ]),
                html.Br()], lg=3),
        
        dbc.Col([
         html.Br(),
         dbc.Label('Select a Year:'),
         dcc.Dropdown(id='year_select',value= 2019, options=[{'label': '2019', 'value': 2019},
                                          {'label': '2020', 'value': 2020}])
    
   
         ], lg = 3),
    
        
        dbc.Col([
         
         html.Br(),
         dbc.Label('Select an ISO_Week:'),
         html.Div(id='SliderContainer')

           ], lg = 4) ]),
    

    dbc.Row([
        dbc.Col([html.Div([
            dcc.Graph(id='Traffic_Line_Chart', config={'displayModeBar': False})
        ],style = {'border': '2px solid gray','border-radius':'15px', 'font-family': 'Roboto Condensed','font-size':'140%',
                                       'font-weight': 'bold',                                                                              
                                       'textAlign':'center'})], lg=8),

        dbc.Col([html.Div([
            dcc.Graph(id='top_weekdays',
                      config={'displayModeBar': False})
        ],style = {'border': '2px solid gray','border-radius':'15px','font-family': 'Roboto Condensed','font-size':'140%',
                                       'font-weight': 'bold',                                                                               
                                       'textAlign':'center'})], lg=4)

    ]),
            
              
    
     
        
    dbc.Row([
          
       dbc.Col([html.Br(), 
        html.Div([html.Br(), html.P('Average Traffic by ISO_Week across Region '),
            dcc.Graph(id='Stacked_ISO_Week_Chart', config={'displayModeBar': False})
        ],style = {'border': '2px solid gray','border-radius':'15px','font-size':'140%',
                                       #'font-family': 'Roboto Condensed',
                                       'font-weight': 'bold',                                                                              
                                       'textAlign':'center'})], lg=8),
        
       dbc.Col(
             
                     html.Div( 
                             [dbc.Col([                           
                                html.Br(),
                                html.Div(
                                    [html.P(id="Central_Traffic"), html.H2("Total Traffic in Central")],
                                    style = {"background-color":'#f2f2f2','border': '1px solid gray', 'border-radius':'15px'},                                   
                                    id="C_Traffic",
                                    className="mini_scorecard",
                                    
                                    
                                )]),
                             dbc.Col([
                                html.Br(),
                                html.Div(
                                    [html.P(id="Western_Traffic"), html.H2("Total Traffic in Western")],
                                    style = {"background-color":'#f2f2f2','border': '1px solid gray', 'border-radius':'15px'}, 
                                    id="W_Traffic",
                                    className="mini_scorecard",
                                    
                                )]),
                              dbc.Col([ 
                                html.Br(),
                                html.Div(
                                    [html.P(id="Eastern_Traffic"), html.H2("Total Traffic in Eastern")],
                                    style = {"background-color":'#f2f2f2','border': '1px solid gray','border-radius':'15px'}, 
                                    id="E_Traffic",
                                    className="mini_scorecard",
                                    
                                )])                                
                            ],

                            id="Scorecards",
                            style = {
                                       'width' : '100%',
                                       'margin-left':'0%',
                                       'font-size':'200%',
                                       #'font-family': 'Roboto Condensed',
                                       'font-weight': 'bold',                                                                              
                                       'textAlign':'center'
                                          }

                        )                                                              
                )
            ]),
                           
                              
    dbc.Row([
                       
        dbc.Col([html.Br(),
                 html.Div([html.Br(), html.Label('Percentage of Traffic in Regions'),
            dcc.Graph(id='pie_graph', config={'displayModeBar': False})
        ],style = {'border': '2px solid gray','border-radius':'15px','font-size':'140%',
                                       #'font-family': 'Roboto Condensed',
                                       'font-weight': 'bold',                                                                              
                                       'textAlign':'center'})],lg = 7),
                            
        
                              
        dbc.Col([
                 html.Div([ html.Br(), html.P("Insights:")],style={'textAlign': "left", 'font-size':'180%','font-weight': 'bold'}),
                 html.Div([                          
                           html.Br(),
                           html.P("This Dashboard shows Foot Traffic on Saco's Stores. Here are some briefs on each chart:"),
                           html.Ul(" - Line Chart shows Traffic across Regions for the last 2 months of 2019, and as we notice Traffic reaches high points in dates corresponding to Saturdays. You can filter by Region using the dropdown menu above. "),
                           html.Ul(" - This can be notices in the bar chart showing the levels of traffic among week days. Saturdays usually are hitting the highest scores. Filtering by ISO_Week is sone by the Slider above."),
                           html.Ul(" - Stacked Bar chart is to visualize the average Traffic by ISO_Weeks accross Regions. Week 44 scores approximately the highest in 3 Regions.You can filter by Year. "),
                           html.Ul(" - Scorecards on the right of the dashboard shows the total number of Traffic in each Region by ISO_Week. Filtering by ISO_Week is done by the slider above."),
                           html.Ul(" - Pie chart shows the percentage of Traffic in each Region. As the Central Region hits the highest Percentage, knowing that the percentages do not vary a lot.")
                           ], style={'textAlign': "left", 'font-size':'140%'})
                            ], lg = 5)                      
                              
        
       ])
       
            
            
    ], style={'backgroundColor': '#eeeee'}) 


        
        

@app.callback(Output('SliderContainer', 'children'),
              [Input('year_select', 'value')])
def return_container(year):
    
        df = data[data['Year'] == year]
        
        return dcc.Slider(id='ISO_Week_Slider',
                       tooltip={'always_visible': True},
                       min=min(df['ISO_Week']),
                       max=max(df['ISO_Week']),                       
                       included=False,
                       step=None,
                       value = max(df['ISO_Week']),
                       marks={week: {'label': str(week)}
                              for week in df['ISO_Week'].unique().tolist()})
    

@app.callback(Output('Traffic_Line_Chart', 'figure'),
              [Input('Region_dropdown', 'value')])



def Traffic_Line_Chart(Region):
    
    fig = go.Figure()
    list_Traffic = []
    
    
        
    if Region == 'Central':
        list_Traffic = List_Traffic_Central
    else:
        if Region == 'Western':
            list_Traffic = List_Traffic_Western
        else:
            if Region == 'Eastern':
               list_Traffic = List_Traffic_Eastern
            else:
                list_Traffic = List_Traffic_All
       
        
    fig.add_scatter(x=list_dates, y=list_Traffic, name=Region,
                        hoverlabel={'namelength': 200},
                        mode='markers+lines')
    fig.layout.template = 'none'
    #fig.layout.paper_bgcolor = '#eeeeee'
    #fig.layout.plot_bgcolor = '#eeeeee'
    fig.layout.title = ('<b>'+'Traffic of ' + Region)
    fig .layout.colorway=['#2a2a2d']
                         
                          
    return fig.to_dict()




@app.callback(Output('top_weekdays', 'figure'),
              [Input('ISO_Week_Slider', 'value')])
def plot_top_weekdays(week):
    
    
    df = data[data['ISO_Week'] == week]

    fig = go.Figure()
    fig.add_bar(x=df['Traffic'].groupby(df['Date']).sum(),
                y=df['WeekDay'],                
                orientation='h',
                marker={'color': ['rgba(214, 39, 40, 0.85)']*10 },
                                 
                )
    
    fig.layout.title = ( '<b>' +'Weekdays Traffic in Week:'+ str(week))
    

   

    return fig.to_dict()







@app.callback(
    Output("Stacked_ISO_Week_Chart", "figure"),
    [Input('year_select', 'value')]
)

def ISO_Week_Bar_figure(year):
    
   df = data[data['Year'] == year]
    
   df_C = df[df['Region'] == 'Central']
   value_C = []
   for i in df['ISO_Week'].unique():
       value = []
       for j in range(df_C.shape[0]):
           if i == df_C.iloc[j,5]:
               value.append(df_C.iloc[j,1])
               
       mean_week = stc.mean(value)
       value_C.append(mean_week)
   print(value_C)
             
   df_W = df[df['Region'] == 'Western']
   value_W = []
   for i in df['ISO_Week'].unique():
       value = []
       for j in range(df_W.shape[0]):
           if i == df_W.iloc[j,5]:
               value.append(df_W.iloc[j,1]) 
               
       mean_week = stc.mean(value)
       value_W.append(mean_week)
       
    
    
   df_E = df[df['Region'] == 'Eastern']
   value_E = []
   for i in df['ISO_Week'].unique():
       value = []
       for j in range(df_E.shape[0]):
           if i == df_E.iloc[j,5]:
               value.append(df_E.iloc[j,1])
       mean_week = stc.mean(value)
       value_E.append(mean_week)

   fig=go.Figure(
   data=[

    go.Bar(
        x=list(df['ISO_Week'].unique()),
        y= value_C,
        name='Central',
        marker=go.bar.Marker(
            color='#da202a',
        )
    ),

    go.Bar(
        x=list(df['ISO_Week'].unique()),
        y=value_W,
        name='Western',
        marker=go.bar.Marker(
            color='#2a2a2d',
        )
    ),

    go.Bar(
        x=list(df['ISO_Week'].unique()),
        y=value_E,
        name='Eastern',
        marker=go.bar.Marker(
            color='#c1c6c8',
        )
    )
   ],
    
    
    layout=go.Layout(
    #title='Average Traffic by ISO_Week across Region ',
    showlegend=True,    
    barmode='stack',
    xaxis = dict(tickvals= df['ISO_Week'].unique())
    )
    )
        
        
   return fig.to_dict()



 
@app.callback([Output("Central_Traffic", "children"),
               Output("Western_Traffic", "children"),
               Output("Eastern_Traffic", "children") ],[Input('ISO_Week_Slider', 'value')])

 
def update_text(week):
    
     df = data[data['ISO_Week'] == week ]
    
     Value_C = 0
     df_C = df[df['Region'] == 'Central']
     for i in range(df_C.shape[0]):
         Value_C = Value_C + df_C.iloc[i,1]
     
     Value_W = 0
     df_W = df[df['Region'] == 'Western']
     for i in range(df_W.shape[0]):
         Value_W = Value_W + df_W.iloc[i,1]
      
     Value_E = 0
     df_E = df[df['Region'] == 'Eastern']
     for i in range(df_E.shape[0]):
         Value_E = Value_E + df_E.iloc[i,1]

     return Value_C , Value_W , Value_E 






@app.callback(
    Output("pie_graph", "figure"),
    [Input('year_select', 'value')])

def pie_figure(year):
    
    Percent_C = Sum_Central*100/Sum_All
    Percent_W = Sum_Western*100/Sum_All
    Percent_E = Sum_Eastern*100/Sum_All
   
    Traffic_Region_pie = go.Pie(labels=["Central", "Western", "Eastern"], values=[round(Percent_C,2), round(Percent_W, 2), round(Percent_E,2)], marker=dict(colors=['#da202a', '#2a2a2d', '#c1c6c8']
                                                            , line=dict(color='#FFF', width=2)), 
                                                            domain={'x': [0.0, .7], 'y': [0.0, 1]}
                                                            , showlegend=True, name='Traffic in Regions', textinfo= 'label+value')
    layout = go.Layout(height = 700,
                   width = 800, 
                   autosize = True,
                   legend={"x": 0, "y": 0}
                                    
                   )
    fig = go.Figure(data = Traffic_Region_pie , layout = layout)
   
    return fig.to_dict()

if __name__ == '__main__':
    app.run_server()
