#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go


# In[2]:


import json
import requests

api_1="https://api.rootnet.in/covid19-in/stats/history"
api_2="https://api.rootnet.in/covid19-in/stats/latest"
jsonData = requests.get(api_1) # (your url)
data = jsonData.json()



from pandas.io.json import json_normalize
import pandas as pd


total_number=len(data['data'])


data_df=pd.DataFrame()

for i in range(total_number):

  df=pd.json_normalize(data["data"][i]['regional'])
  day=data["data"][i]['day']
  df['day']=day

  data_df = pd.concat([data_df, df], axis=0) 


# In[3]:


data_df.head()


# In[4]:


def update_graph(value):
    dff = data_df[data_df['day']==str(value)]
    fig = px.bar(dff, x='loc', y='confirmedCasesIndian')
    return fig
newfig=update_graph('2020-03-10')
newfig.show()


# In[5]:



dff = data_df[data_df['day']==str('2020-03-10')]
figln = px.bar(dff, x='loc', y='confirmedCasesIndian')
figln.show()


# In[6]:


col_names=list(data_df.columns)


col_names.remove('loc')
col_names.remove('day')
print(col_names)


# In[7]:


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server=app.server


# In[ ]:



app.layout = dbc.Container([

    dbc.Row(
        dbc.Col(html.H1("Covid Spread In India",
                        className='text-center text-primary mb-4'),
                width=12)
    ),
    
    dbc.Row([
        
        dbc.Col([
            
            dcc.Dropdown(id='drop_day', multi=False, value='2020-03-10',
                         options=[{'label':x, 'value':x}
                                  for x in sorted(data_df['day'].unique())],
                         ),
              
        ],xs=12, sm=12, md=12, lg=5, xl=5),
        
        dbc.Col([
            
            dcc.Dropdown(id='drop_cases', multi=False, value='totalConfirmed',
                         options=[{'label':x, 'value':x}
                                  for x in col_names],
                         ),
        ],xs=12, sm=12, md=12, lg=5, xl=5)
    ]),
    
    dbc.Row([
        
        dbc.Col([
            
             dcc.Graph(id='graph', figure={}),
            
        ])
       
    ]),
    
    dbc.Row([
        
        dbc.Col([
            
            html.H3(html.Div(id='textarea-output', style={'whiteSpace': 'pre-line'}),
                        className='text-center text-primary mb-4'),
        ])
    ])
    

],fluid=True)


@app.callback(
    Output('textarea-output', component_property='children'),
    [Input('drop_day', 'value'),
    Input('drop_cases','value')]
)
def update_output(day,case):
    text= 'Bar Chart showing ',case,' across states dated ',day
    return text

@app.callback(
    Output('graph', 'figure'),
    [Input('drop_day', 'value'),
    Input('drop_cases','value')]
)
def update_graph(day,case):
    dff = data_df[data_df['day']==str(day)]
    fig = px.bar(dff, x='loc', y=case)
    return fig




if __name__=='__main__':
    app.run_server()


# In[ ]:




