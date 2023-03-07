# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
app = Dash(__name__)
year_list = [i for i in range(2010, 2010, 1)]


df= pd.read_csv('crime.csv')
df = df.rename(columns={
    'Unit Name':'unit_name',
    'Speedy Trial':'speed_trial',
    'Woman & Child Repression': 'women_and_child_repression',
    'Police Assault': 'police_assault',
    'Other Cases': 'other_cases',
    'Arms Act': 'arms_act',
    'Total Cases':'total_cases'
})

def compute_data1(df):

    data_groupby_unit = df.groupby(['unit_name', 'Year']).total_cases.mean()
    data_groupby_unit = data_groupby_unit.to_frame()
    data_groupby_unit = data_groupby_unit.reset_index()


    return  data_groupby_unit


def compute_data2(df):
    data_groupby_year = df.groupby(['Year', 'unit_name']).total_cases.mean()
    data_groupby_year = data_groupby_year.to_frame()
    data_groupby_year.reset_index(inplace=True)
    return  data_groupby_year


def compute_data3(df):
    i = 0
    df_unit_cols = ['crimes', 'no_of_crimes']
    df_unit = pd.DataFrame(columns=df_unit_cols)

    for label in df.columns[2:-1]:
        df_unit.loc[i] = [label, df[label].sum()]
        i += 1

    return  df_unit

app.layout= html.Div(children=
                     [html.H1(children='Crimes in Bangladesh (2010-2019)', style={'textAlign':'centre',
                                                                                 'color':'#503D36',
                                                                                 'font-size': 24
                                                                                 }),
                      html.Div([
                          #A division for first dropdown menue
                          html.Div([
                              html.H2("Select a Report Type", style={'margin-right': '2em'}),
                              dcc.Dropdown(
                                  id = 'input-type',
                                  options=[
                                      {'label':'Average Total Number of cases in each unit', 'value':'Opt-1'},
                                      {'label':'Average Total Number of cases in each year', 'value':'Opt-2'},
                                      {'label': 'Ratio of the crimes', 'value': 'Opt-3'}

                                  ],
                                  placeholder='Select a report type',
                                  style={'width':'80%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'},
                                ),
                          ],style={'display':'flex'}
                          ),


                      ]),
                      html.Div([ ], id='plot1')


                      ])

@app.callback( [Output(component_id='plot1', component_property='children')

                ],
               [Input(component_id='input-type', component_property='value')
                ],

               [State("plot1", 'children')
               ])
def get_graph(chart, children):
    if chart == 'Opt-1':
        unit_data= compute_data1(df)
        unit_fig= px.bar(unit_data,  x='unit_name', y="total_cases", title="Average Number of Cases in each unit ",color='Year')
        return [dcc.Graph(figure= unit_fig)]

    elif chart == 'Opt-2':
        year_data = compute_data2(df)
        year_fig= px.bar(year_data, x='Year', y="total_cases", title="Average Number of Cases in each year ", color='unit_name')
        return [dcc.Graph(figure=year_fig)]


    else:
        crime_data = compute_data3(df)
        crime_fig = px.pie(crime_data, values='no_of_crimes', names='crimes', hole=.3)
        return [dcc.Graph(figure=crime_fig)]


if __name__ == '__main__':
    app.run_server(debug=True)
