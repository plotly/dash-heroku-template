# Import required libraries
import os
from random import randint

import plotly.plotly as py
from plotly.graph_objs import *

import flask
import dash
from dash.dependencies import Input, Output, State, Event
import dash_core_components as dcc
import dash_html_components as html


# Setup the app
# Make sure not to change this file name or the variable names below,
# the template is configured to execute 'server' on 'app.py'
server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__, server=server)


# Put your Dash code here
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 12:57:02 2020

@author: arupnar.mim2013
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 18:34:50 2020

@author: arupnar.mim2013
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import dash_table
import math
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import json
from plotly.offline import plot
import plotly.express as px
from plotly.subplots import make_subplots
import sqlite3


colors=pd.read_excel(r'C:\Users\arupnar.mim2013\AnacondaProjects\Plotly colours.xlsx')

def plot_stack(df,x_axis_col,y_axis_col,stacks_col,*hovercol):
    if x_axis_col is None or stacks_col is None:
        fig=go.Figure()
    else:
        if hovercol:
            for x in hovercol:
                hover_col=x
        else:
            hover_col=stacks_col
        fig=go.Figure()
        p=df.groupby([x_axis_col])[y_axis_col].sum().reset_index().sort_values(by=y_axis_col)
        j=p[y_axis_col].sum()    
            
        fig2=go.Scatter(y=p[y_axis_col],x=p[x_axis_col],text=p[x_axis_col],hoverinfo='x+y+text',mode='markers',name='Total',showlegend=True,marker_color='blueviolet')     
        fig.add_trace(fig2)       
        if (x_axis_col==stacks_col):
            if(hover_col==stacks_col):
                a=df.groupby([x_axis_col])[y_axis_col].sum().reset_index()
            else:
                if (x_axis_col==hover_col):
                    a=df.groupby([x_axis_col])[y_axis_col].sum().reset_index()
                else:
                    a=df.groupby([x_axis_col,hover_col])[y_axis_col].sum().reset_index()
        else:
            if (hover_col==stacks_col):
                a=df.groupby([x_axis_col,stacks_col])[y_axis_col].sum().reset_index()
            else:
                a=df.groupby([x_axis_col,stacks_col,hover_col])[y_axis_col].sum().reset_index()
                
        stacks=df[stacks_col].dropna().drop_duplicates(keep='first').reset_index().sort_values(by=stacks_col).reset_index()
        for i,v in stacks[stacks_col].items():
            # print(v)
            b=a[a[stacks_col]==v]
            q=b[y_axis_col].sum()/1000000
            # i=131
            x=i-115*(math.floor(i/115))
            
            fig1=go.Bar(y=b[y_axis_col],x=b[x_axis_col],hovertext=b[hover_col],hoverinfo='x+y+text',name=v+" ("+str("{:,.2f}".format(q))+"M)",showlegend=True,marker_color=colors.loc[x,'Colour'])
            
            fig.add_trace(fig1)
        fig.update_layout(hovermode='x',barmode='relative',title='Total : '+str("{:,.2f}".format(j))+'/-')
    return fig


def plot_timeseries(df,x_axis_col,y_axis_col,legend_col,hover_col):
    if x_axis_col is None or legend_col is None:
        fig=go.Figure()
    else:
        fig=go.Figure()
        p=df[legend_col].dropna().drop_duplicates(keep='first').reset_index().sort_values(by=legend_col).reset_index()
        for i,v in p[legend_col].items():
            df1=df[df[legend_col]==v]
            x=i-115*(math.floor(i/115))
            fig2=go.Scatter(y=df1[y_axis_col],x=df1[x_axis_col],text=df1[hover_col],hoverinfo='x+y+text',mode='markers',name=v,showlegend=True,marker_color=colors.loc[x,'Colour'])     
            fig.add_trace(fig2)       
    return fig



# external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP,css']



centres=pd.read_csv(r'C:\Users\arupnar.mim2013\AnacondaProjects\centres.csv')
centres1=[{'label':i,'value':i} for i in centres['flexa_Profit Ctr']]

# app=dash.Dash(__name__,external_stylesheets=external_stylesheets,suppress_callback_exceptions = True)
       
# app.config['suppress_callback_exceptions'] = True


fig=go.Figure()

finance=html.Div([html.Div([
            html.Div(id='f-data',style={'display':'none'}),
            html.Div([
                html.Div([
                    html.Label('X-axis : ',style={'width':'100%'}),
                    dcc.Dropdown(id='f-xaxis1',
                                 options=[],
                                 value='glgroup_GL Type',#'P059-OIL STF MADHUBAN',
                                 multi=False,
                                 placeholder="X-Axis",
                                 style={'width':'100%'}),
                    html.Label('Legend : ',style={'width':'100%'}),
                    dcc.Dropdown(id='f-stacks1',
                                 options=[],
                                 value='glgroup_GL schedule',#'P059-OIL STF MADHUBAN',
                                 multi=False,
                                 placeholder="Legend",
                                 style={'width':'100%'})],
                    style={'width':'15%','display':'inline-block','vertical-align':'Top'}),
                html.Div([dcc.Graph(id='f-fig1',figure=fig)],
                         style={'width':'85%','display':'inline-block'})],
                style={'width':'100%','border':'2px blue solid'}),
            html.Div([
                html.Div([
                    html.Label('Filter field : ',style={'width':'100%'}),
                    dcc.Dropdown(id='f-filtercol1',
                                 options=[],
                                 value='glgroup_GL schedule',#'P059-OIL STF MADHUBAN',
                                 multi=False,
                                 placeholder="Filter field",
                                 clearable=False,
                                 style={'width':"100%"}),
                    html.Label('Filter values : ',style={'width':'100%'}),
                    dcc.Dropdown(id='f-filterval1',
                                 options=[],
                                 multi=True,
                                 placeholder="Filter values",
                                 value='Cost of Material Consumed',
                                 clearable=False,
                                 style={'width':'100%'})],
                    style={'width':'15%','display':'inline-block','vertical-align':'Top'}),
                html.Div([
                    html.Div([
                        html.Div([html.Label('X-axis : ')],style={'width':'5%','display':'inline-block','vertical-align':'Top'}),
                        html.Div([
                        dcc.Dropdown(id='f-xaxis2',
                                     options=[],
                                     value='glgroup_GL name',#'P059-OIL STF MADHUBAN',
                                     multi=False,
                                     placeholder="X-Axis")],
                        style={'width':'35%','display':'inline-block'}),
                    html.Div([html.Label('Legend : ')],style={'margin-left':'4%','width':'5%','display':'inline-block','vertical-align':'Top'}),
                    html.Div([
                        dcc.Dropdown(id='f-stacks2',
                                     options=[],
                                     value='glgroup_Account head Grouping',#'P059-OIL STF MADHUBAN',
                                     multi=False,
                                     placeholder="Legend")],
                        style={'width':'35%','display':'inline-block'})],
                    style={'width':'100%','margin-left':'5%'}),
                    html.Div([
                        dcc.Graph(id='f-fig2',figure=fig)],
                        style={'width':'100%'})],
                    style={'width':'85%','display':'inline-block'})],
                style={'width':'100%','margin-top':'4%','border':'2px blue solid'}),
            html.H3('All effects',style={'width':'100%','margin-top':'4%'}),
                
            html.Div([
                html.Div([
                html.Label('Filter field : ',style={'width':'100%'}),
                dcc.Dropdown(id='f-filtercol2',
                             options=[],
                             value='glgroup_GL name',#'P059-OIL STF MADHUBAN',
                             multi=False,
                             placeholder="Filter field",
                             clearable=False,
                             style={'width':"100%"}),
                html.Label('Filter values : ',style={'width':'100%'}),
                dcc.Dropdown(id='f-filterval2',
                             options=[],
                             multi=True,
                             placeholder="Filter values",
                             # value='ABC',
                             clearable=False,
                             style={'width':'100%'})],
                    style={'width':'15%','display':'inline-block','vertical-align':'Top'}),
            
                html.Div([
                    html.Div([
                        html.Div([html.Label('X-axis : ')],style={'width':'5%','display':'inline-block','vertical-align':'Top'}),
                        html.Div([
                            dcc.Dropdown(id='f-xaxis3',
                                         options=[],
                                         value='glgroup_GL name',#'P059-OIL STF MADHUBAN',
                                         multi=False,
                                         placeholder="X-Axis")],
                            style={'width':'35%','display':'inline-block'}),
                        html.Div([html.Label('Legend : ')],style={'margin-left':'4%','width':'5%','display':'inline-block','vertical-align':'Top'}),
                        html.Div([
                            dcc.Dropdown(id='f-stacks3',
                                         options=[],
                                         value='flexa_Profit Ctr',#'P059-OIL STF MADHUBAN',
                                         multi=False,
                                         placeholder="Legend")],
                            style={'width':'35%','display':'inline-block'})],
                        style={'width':'100%','margin-left':'5%'}),
                    
                    html.Div([
                        dcc.Graph(id='f-fig3',figure=fig)],
                        style={'width':'100%'})],
                    style={'width':'85%','display':'inline-block'})],
                style={'width':'100%','display':'flex','border':'2px blue solid'})],
            style={'width':'100%'})])

documents=html.Div([html.Div([
                    html.Div([
                        html.Div(id='d-data1',style={'display':'none'}),
                        html.Label('GL name : ',style={'width':'100%'}),
                        dcc.Dropdown(id='d-glname',
                                     options=[],
                                     multi=False,
                                     placeholder="GL name",
                                     style={'width':'100%'}),
                        html.Label('Legend : ',style={'width':'100%'}),
                        dcc.Dropdown(id='d-legend',
                                     options=[],
                                     multi=False,
                                     placeholder="Legend",
                                     style={'width':'100%'})],
                style={'width':'15%','display':'inline-block','vertical-align':'Top'}),
                html.Div([dcc.Graph(id='d-fig1',figure=fig)],
                         style={'width':'85%','display':'inline-block'})],
                    style={'width':'100%','display':'flex','border':'2px blue solid'}),
                dash_table.DataTable(
                    id='d-table',
                    editable=False,
                    filter_action='native',
                    sort_action='native',
                    sort_mode='multi',
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current=0,
                        page_size=100,)
                ])

search=html.Div([html.Div(id='s-data',style={'display':'none'}),
                 html.Label('flexa_key'),
                 dcc.Input(id='s-flexa_key_x',value='', type='text'),
                 dash_table.DataTable(
                    id='s-table',
                    editable=False,
                    filter_action='native',
                    sort_action='native',
                    sort_mode='multi',
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current=0,
                        page_size=100,)
                ])

material=html.Div([html.Div(id='m-data1',style={'display':'none'}),
                   html.Div(id='m-data2',style={'display':'none'}),
                   html.Div([dcc.Graph(id='m-fig1',figure=fig)],
                            style={'border':'2px blue solid'}),
                   html.Div([dcc.Dropdown(id='m-materials',
                                          multi=True,
                                          placeholder='Materialname')],
                            style={'width':'100%'}),
                   html.Div([
                        html.Div([
                        html.Label('Filter field : ',style={'width':'100%'}),
                        dcc.Dropdown(id='m-filtercol1',
                                     options=[],
                                     value='flexa_Profit Ctr',#'P059-OIL STF MADHUBAN',
                                     multi=False,
                                     placeholder="Filter field",
                                     clearable=False,
                                     style={'width':"100%"}),
                        html.Label('Filter values : ',style={'width':'100%'}),
                        dcc.Dropdown(id='m-filterval1',
                                     options=[],
                                     multi=True,
                                     placeholder="Filter values",
                                    
                                     clearable=True,
                                     style={'width':'100%'})],
                            style={'width':'15%','display':'inline-block','vertical-align':'Top'}),
                        html.Div([
                                dcc.Graph(id='m-fig2',figure=fig)],
                                style={'width':'85%','display':'inline-block'})],
                            style={'width':'100%','display':'inline-block','border':'2px blue solid'})]
                  )
                        

customer=html.Div([html.Div(id='c-data',style={'display':'none'}),
                   html.Div([
                       html.Div([
                           html.Label('Filter field : ',style={'width':'100%'}),
                           dcc.Dropdown(id='c-filtercol1',
                                         options=[],
                                         value='flexa_Profit Ctr',#'P059-OIL STF MADHUBAN',
                                         multi=False,
                                         placeholder="Filter field",
                                         clearable=False,
                                         style={'width':"100%"}),
                           html.Label('Filter values : ',style={'width':'100%'}),
                           dcc.Dropdown(id='c-filterval1',
                             options=[],
                             multi=True,
                             placeholder="Filter values",
                             # value='ABC',
                             clearable=True,
                             style={'width':'100%'})],
                           style={'width':'15%','display':'inline-block','vertical-align':'Top'}),
                       html.Div([
                           html.Div([
                               html.Div([html.Label('X-axis : ')],
                                        style={'width':'5%','display':'inline-block','vertical-align':'Top'}),
                               html.Div([
                                   dcc.Dropdown(id='c-xaxis1',
                                                options=[],
                                                value='glgroup_GL name',#'P059-OIL STF MADHUBAN',
                                                multi=False,
                                                placeholder="X-Axis")],
                                   style={'width':'35%','display':'inline-block'}),
                               html.Div([
                                   html.Label('Legend : ')],style={'margin-left':'4%','width':'6%','display':'inline-block','vertical-align':'Top'}),
                               html.Div([
                                   dcc.Dropdown(id='c-stacks1',
                                                options=[],
                                                value='Effect',#'P059-OIL STF MADHUBAN',
                                                multi=False,
                                                placeholder="Legend")],
                                   style={'width':'35%','display':'inline-block'})],
                               style={'width':'100%','margin-left':'5%'}),
                           html.Div([dcc.Graph(id='c-fig1',figure=fig)])],
                           style={'width':'85%','display':'inline-block'})],
                       style={'border':'2px blue solid'}),
                   html.Div([
                       html.Div([dcc.Graph(id='c-fig2',figure=fig)],
                                 style={'width':'100%','display':'inline-block'}),
                       # html.Div([dcc.Graph(id='c-fig3',figure=fig)],
                       #           style={'width':'50%','display':'inline-block'})
                   ],
                       style={'width':'100%','display':'inline-block','border':'2px blue solid'}
                       ),
                   dcc.Dropdown(id='c-customer',
                                     options=[],
                                     multi=True,
                                     placeholder="Customer name",
                                    
                                     clearable=True,
                                     style={'width':'100%'}),
                    html.Div([
                    html.Div(id='c-data1',style={'display':'none'}),
                       html.Div([
                           html.Label('Filter field : ',style={'width':'100%'}),
                           dcc.Dropdown(id='c-filtercol2',
                                         options=[],
                                         value='flexa_Profit Ctr',#'P059-OIL STF MADHUBAN',
                                         multi=False,
                                         placeholder="Filter field",
                                         clearable=False,
                                         style={'width':"100%"}),
                           html.Label('Filter values : ',style={'width':'100%'}),
                           dcc.Dropdown(id='c-filterval2',
                             options=[],
                             multi=True,
                             placeholder="Filter values",
                             value='Self-effects',
                             clearable=True,
                             style={'width':'100%'})],
                           style={'width':'15%','display':'inline-block','vertical-align':'Top'}),
                       html.Div([
                           html.Div([
                               html.Div([html.Label('X-axis : ')],
                                        style={'width':'5%','display':'inline-block','vertical-align':'Top'}),
                               html.Div([
                                   dcc.Dropdown(id='c-xaxis2',
                                                options=[],
                                                value='Posting date',#'P059-OIL STF MADHUBAN',
                                                multi=False,
                                                placeholder="X-Axis")],
                                   style={'width':'35%','display':'inline-block'}),
                               html.Div([
                                   html.Label('Legend : ')],style={'margin-left':'4%','width':'6%','display':'inline-block','vertical-align':'Top'}),
                               html.Div([
                                   dcc.Dropdown(id='c-stacks2',
                                                options=[],
                                                value='flexa_Profit Ctr',#'P059-OIL STF MADHUBAN',
                                                multi=False,
                                                placeholder="Legend")],
                                   style={'width':'35%','display':'inline-block'})],
                               style={'width':'100%','margin-left':'5%'}),
                           html.Div([dcc.Graph(id='c-fig4',figure=fig)])],
                           style={'width':'85%','display':'inline-block'})],
                       style={'border':'2px blue solid'}),
                    html.H3('Other effects',style={'width':'100%','margin-top':'4%'}),
                    html.Div([
                    # html.Div(id='c-data1',style={'display':'none'}),
                       html.Div([
                           html.Label('Filter field : ',style={'width':'100%'}),
                           dcc.Dropdown(id='c-filtercol3',
                                         options=[],
                                         value='flexa_Profit Ctr',#'P059-OIL STF MADHUBAN',
                                         multi=False,
                                         placeholder="Filter field",
                                         clearable=False,
                                         style={'width':"100%"}),
                           html.Label('Filter values : ',style={'width':'100%'}),
                           dcc.Dropdown(id='c-filterval3',
                             options=[],
                             multi=True,
                             placeholder="Filter values",
                             value='Other-effects',
                             clearable=True,
                             style={'width':'100%'})],
                           style={'width':'15%','display':'inline-block','vertical-align':'Top'}),
                       html.Div([
                           html.Div([
                               html.Div([html.Label('X-axis : ')],
                                        style={'width':'5%','display':'inline-block','vertical-align':'Top'}),
                               html.Div([
                                   dcc.Dropdown(id='c-xaxis3',
                                                options=[],
                                                value='Posting date',#'P059-OIL STF MADHUBAN',
                                                multi=False,
                                                placeholder="X-Axis")],
                                   style={'width':'35%','display':'inline-block'}),
                               html.Div([
                                   html.Label('Legend : ')],style={'margin-left':'4%','width':'6%','display':'inline-block','vertical-align':'Top'}),
                               html.Div([
                                   dcc.Dropdown(id='c-stacks3',
                                                options=[],
                                                value='glgroup_Account head Grouping',#'P059-OIL STF MADHUBAN',
                                                multi=False,
                                                placeholder="Legend")],
                                   style={'width':'35%','display':'inline-block'})],
                               style={'width':'100%','margin-left':'5%'}),
                           html.Div([dcc.Graph(id='c-fig5',figure=fig)])],
                           style={'width':'85%','display':'inline-block'})],
                       style={'border':'2px blue solid'})
                   ])

vendor=html.Div([html.Div(id='v-data',style={'display':'none'}),
                   html.Div([
                       html.Div([
                           html.Label('Filter field : ',style={'width':'100%'}),
                           dcc.Dropdown(id='v-filtercol1',
                                         options=[],
                                         value='flexa_Profit Ctr',#'P059-OIL STF MADHUBAN',
                                         multi=False,
                                         placeholder="Filter field",
                                         clearable=False,
                                         style={'width':"100%"}),
                           html.Label('Filter values : ',style={'width':'100%'}),
                           dcc.Dropdown(id='v-filterval1',
                             options=[],
                             multi=True,
                             placeholder="Filter values",
                             # value='ABC',
                             clearable=True,
                             style={'width':'100%'})],
                           style={'width':'15%','display':'inline-block','vertical-align':'Top'}),
                       html.Div([
                           html.Div([
                               html.Div([html.Label('X-axis : ')],
                                        style={'width':'5%','display':'inline-block','vertical-align':'Top'}),
                               html.Div([
                                   dcc.Dropdown(id='v-xaxis1',
                                                options=[],
                                                value='glgroup_GL name',#'P059-OIL STF MADHUBAN',
                                                multi=False,
                                                placeholder="X-Axis")],
                                   style={'width':'35%','display':'inline-block'}),
                               html.Div([
                                   html.Label('Legend : ')],style={'margin-left':'4%','width':'6%','display':'inline-block','vertical-align':'Top'}),
                               html.Div([
                                   dcc.Dropdown(id='v-stacks1',
                                                options=[],
                                                value='Effect',#'P059-OIL STF MADHUBAN',
                                                multi=False,
                                                placeholder="Legend")],
                                   style={'width':'35%','display':'inline-block'})],
                               style={'width':'100%','margin-left':'5%'}),
                           html.Div([dcc.Graph(id='v-fig1',figure=fig)])],
                           style={'width':'85%','display':'inline-block'})],
                       style={'border':'2px blue solid'}),
                   html.Div([
                       html.Div([dcc.Graph(id='v-fig2',figure=fig)],
                                 style={'width':'100%','display':'inline-block'}),
                       # html.Div([dcc.Graph(id='v-fig3',figure=fig)],
                       #           style={'width':'50%','display':'inline-block'})
                   ],
                       style={'width':'100%','display':'inline-block','border':'2px blue solid'}
                       ),
                   dcc.Dropdown(id='v-vendor',
                                     options=[],
                                     multi=True,
                                     placeholder="Vendor name",
                                    
                                     clearable=True,
                                     style={'width':'100%'}),
                    html.Div([
                    html.Div(id='v-data1',style={'display':'none'}),
                       html.Div([
                           html.Label('Filter field : ',style={'width':'100%'}),
                           dcc.Dropdown(id='v-filtercol2',
                                         options=[],
                                         value='flexa_Profit Ctr',#'P059-OIL STF MADHUBAN',
                                         multi=False,
                                         placeholder="Filter field",
                                         clearable=False,
                                         style={'width':"100%"}),
                           html.Label('Filter values : ',style={'width':'100%'}),
                           dcc.Dropdown(id='v-filterval2',
                             options=[],
                             multi=True,
                             placeholder="Filter values",
                             value='Self-effects',
                             clearable=True,
                             style={'width':'100%'})],
                           style={'width':'15%','display':'inline-block','vertical-align':'Top'}),
                       html.Div([
                           html.Div([
                               html.Div([html.Label('X-axis : ')],
                                        style={'width':'5%','display':'inline-block','vertical-align':'Top'}),
                               html.Div([
                                   dcc.Dropdown(id='v-xaxis2',
                                                options=[],
                                                value='Posting date',#'P059-OIL STF MADHUBAN',
                                                multi=False,
                                                placeholder="X-Axis")],
                                   style={'width':'35%','display':'inline-block'}),
                               html.Div([
                                   html.Label('Legend : ')],style={'margin-left':'4%','width':'6%','display':'inline-block','vertical-align':'Top'}),
                               html.Div([
                                   dcc.Dropdown(id='v-stacks2',
                                                options=[],
                                                value='flexa_Profit Ctr',#'P059-OIL STF MADHUBAN',
                                                multi=False,
                                                placeholder="Legend")],
                                   style={'width':'35%','display':'inline-block'})],
                               style={'width':'100%','margin-left':'5%'}),
                           html.Div([dcc.Graph(id='v-fig4',figure=fig)])],
                           style={'width':'85%','display':'inline-block'})],
                       style={'border':'2px blue solid'}),
                    html.H3('Other effects',style={'width':'100%','margin-top':'4%'}),
                    html.Div([
                    # html.Div(id='v-data1',style={'display':'none'}),
                       html.Div([
                           html.Label('Filter field : ',style={'width':'100%'}),
                           dcc.Dropdown(id='v-filtercol3',
                                         options=[],
                                         value='flexa_Profit Ctr',#'P059-OIL STF MADHUBAN',
                                         multi=False,
                                         placeholder="Filter field",
                                         clearable=False,
                                         style={'width':"100%"}),
                           html.Label('Filter values : ',style={'width':'100%'}),
                           dcc.Dropdown(id='v-filterval3',
                             options=[],
                             multi=True,
                             placeholder="Filter values",
                             value='Other-effects',
                             clearable=True,
                             style={'width':'100%'})],
                           style={'width':'15%','display':'inline-block','vertical-align':'Top'}),
                       html.Div([
                           html.Div([
                               html.Div([html.Label('X-axis : ')],
                                        style={'width':'5%','display':'inline-block','vertical-align':'Top'}),
                               html.Div([
                                   dcc.Dropdown(id='v-xaxis3',
                                                options=[],
                                                value='Posting date',#'P059-OIL STF MADHUBAN',
                                                multi=False,
                                                placeholder="X-Axis")],
                                   style={'width':'35%','display':'inline-block'}),
                               html.Div([
                                   html.Label('Legend : ')],style={'margin-left':'4%','width':'6%','display':'inline-block','vertical-align':'Top'}),
                               html.Div([
                                   dcc.Dropdown(id='v-stacks3',
                                                options=[],
                                                value='glgroup_Account head Grouping',#'P059-OIL STF MADHUBAN',
                                                multi=False,
                                                placeholder="Legend")],
                                   style={'width':'35%','display':'inline-block'})],
                               style={'width':'100%','margin-left':'5%'}),
                           html.Div([dcc.Graph(id='v-fig5',figure=fig)])],
                           style={'width':'85%','display':'inline-block'})],
                       style={'border':'2px blue solid'})
                   ])

                    
                   # html.Div(id='data3',style={'display':'none'}),
           
                
z=[finance,documents,material,customer,vendor,search]     

app.layout=html.Div([
    # dcc.Store(id='store_financials'),
    # dcc.Store(id='store_customers'),
    dcc.Dropdown(id='centres',
                 options=centres1,
                 value=[],#'P059-OIL STF MADHUBAN',
                 multi=True,
                 placeholder="Project name"),
    dcc.Tabs(id='tabs',
              # value='materialtab',
             children=[
                 dcc.Tab(label='Financials',value='financetab'),
                
                 dcc.Tab(label='Customers',value='customertab'),
                 dcc.Tab(label='Vendors',value='vendortab'),
                 dcc.Tab(label='Materials',value='materialtab'),
                 dcc.Tab(label='Documents',value='documenttab'),
                 dcc.Tab(label='Search',value='searchtab')]),
    html.Div(id='content',children=z)])

@app.callback(Output('content','children'),
              [Input('tabs','value')])
def render_content(tab):
    if tab=='financetab':
        content=finance
        return content
        
    
    elif tab=='documenttab':
        content=documents
        return content
        
    elif tab=='customertab':
        content=customer
        return content
    
    elif tab=='vendortab':
        content=vendor
        return content
        
    elif tab=='materialtab':
        content=material
        return content
    
    elif tab=='searchtab':
        content=search
        return content


        
@app.callback(Output('f-data','children'),
              [Input('centres','value')])
def update_data(value):
    
    v=[]
    if type(value)==str:
        v=[value]
    else:
        for val in value:
            v.append(val)
    if not v:
        final={'pivot1':pd.DataFrame().to_json(orient='split',date_format='iso'),'pivot2':pd.DataFrame().to_json(orient='split',date_format='iso'),'pivot3':pd.DataFrame().to_json(orient='split',date_format='iso')}
    else:
        # v=['P059-OIL STF MADHUBAN']
    #     # l = v.astype(str)
    #     # v=str(value)
    # # v1=v.replace('"','')
    # # v2=v1.replace("'","")
    #     cnx = sqlite3.connect(r'C:\Users\arupnar.mim2013\data.db')
    # # test='2017.0100000001.0'
    # # quote="'"
    #     df=pd.DataFrame()
    #     for k in v:
    #         query1="SELECT DISTINCT flexa_key_x FROM df101 WHERE [flexa_Profit Ctr] IN ({})".format(','.join(''+item+'' for item in v))
    #         df1 = pd.read_sql(query1, cnx)
    #         # df2=df1.astype(str)
    #         w=list(df1['flexa_key_x'])
    #         df4=pd.DataFrame()
    #         for i in w:
    #             # query2="SELECT * FROM df101 WHERE [flexa_key_x] = ({})".format(i)
    #             print(i)
    #             query2="SELECT * FROM df101 WHERE [flexa_key_x] = '%s'"%(str(i),)
    #             df3=pd.read_sql(query2, cnx)
    #             df4=pd.concat([df4,df3],axis=1)
        
        
    
        
        
        
        pclines2=pd.DataFrame()
        for a in v:
           pclines1=pd.read_pickle(r"C:\Users\arupnar.mim2013\AnacondaProjects\Profit Centre\{}.pkl".format(a))
           pclines2=pd.concat([pclines2,pclines1],ignore_index=True)
        pclines3=pclines2.drop_duplicates(keep='first')
        pclines3=pclines3[pclines3['bkpf_Reversal_x'].isnull()]
        pclines4=pclines3[pclines3['flexa_Profit Ctr'].isin(v)]
        pclines4['bseg_Customer'].dtype
        customerdocs0=pclines4[pclines4['bseg_Customer']!='nan']
        customerdocs=customerdocs0['flexa_key_x'].dropna().drop_duplicates(keep='first')
        vendordocs0=pclines4[pclines4['bseg_Vendor']!='nan']
        vendordocs=vendordocs0['flexa_key_x'].dropna().drop_duplicates(keep='first')
        # vendordocs=pclines4[-pclines4['bseg_Vendor'].isna()]['flexa_key_x'].dropna().drop_duplicates(keep='first')
        df9=pclines4
        df9_customer=df9[(df9['flexa_key_x'].isin(customerdocs))&(-df9['flexa_key_x'].isin(vendordocs))]
        df9_customer['Group']='Customer'
        df9_vendor=df9[(-df9['flexa_key_x'].isin(customerdocs))&(df9['flexa_key_x'].isin(vendordocs))]
        df9_vendor['Group']='Vendor'
        df9_both=df9[(df9['flexa_key_x'].isin(customerdocs))&(df9['flexa_key_x'].isin(vendordocs))]
        df9_both['Group']='Both'
        df9_none=df9[(-df9['flexa_key_x'].isin(customerdocs))&(-df9['flexa_key_x'].isin(vendordocs))]
        df9_none['Group']='None'
        df91=pd.concat([df9_customer,df9_vendor,df9_both,df9_none],ignore_index=True)
        df92=df91.fillna('blank')
        othereffects1=pd.DataFrame()
        pivot1=pd.pivot_table(df92,index=['flexa_Year','flexa_key_x','flexa_Profit Ctr','glgroup_GL Type','glgroup_GL schedule','glgroup_Account head Grouping','glgroup_GL name','Group'],values=['flexa_LC Amount'],aggfunc=np.sum).reset_index()
       
        final={'pivot1':pivot1.to_json(orient='split',date_format='iso'),'pivot2':othereffects1.to_json(orient='split',date_format='iso')}#,'pivot3':allpoints.to_json(orient='split',date_format='iso')}
    return json.dumps(final)



@app.callback(Output('f-xaxis1','options'),
              [Input('f-data','children')])#,
              # Input('centres','value')])
def update_figure(value):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
    return options


@app.callback(Output('f-stacks1','options'),
              [Input('f-data','children')])#,
              # Input('centres','value')])
def update_figure(value):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
    return options



@app.callback(Output('f-fig1','figure'),
              [Input('f-data','children'),
               Input('f-xaxis1','value'),
               Input('f-stacks1','value')])#,
              # Input('centres','value')])
def update_figure(value,xaxis,stacks):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        fig=go.Figure()
    else:
        fig=plot_stack(data,xaxis,'flexa_LC Amount',stacks)
    return fig

@app.callback(Output('f-filtercol1','options'),
              [Input('f-data','children')])#,
              # Input('centres','value')])
def update_figure(value):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
    return options

@app.callback(Output('f-filterval1','options'),
              [Input('f-data','children'),
               Input('f-filtercol1','value')])#,
              # Input('centres','value')])
def update_figure(value,value2):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty or value2 is None:
        options=[]
    else:
        data1=data[value2].dropna().drop_duplicates(keep='first').reset_index().sort_values(by=value2)
        options=[{'label':i,'value':i} for i in data1[value2]]
    return options


@app.callback(Output('f-filtercol2','options'),
              [Input('f-data','children')])#,
              # Input('centres','value')])
def update_figure(value):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
    return options

@app.callback(Output('f-filterval2','options'),
              [Input('f-data','children'),
               Input('f-filtercol2','value')])#,
              # Input('centres','value')])
def update_figure(value,value2):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty or value2 is None:
        options=[]
    else:
        data1=data[value2].dropna().drop_duplicates(keep='first').reset_index().sort_values(by=value2)
        options=[{'label':i,'value':i} for i in data1[value2]]
    return options



@app.callback(Output('f-xaxis2','options'),
              [Input('f-data','children')])#,
              # Input('centres','value')])
def update_figure(value):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
    return options


@app.callback(Output('f-stacks2','options'),
              [Input('f-data','children')])#,
              # Input('centres','value')])
def update_figure(value):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
    return options

@app.callback(Output('f-xaxis3','options'),
              [Input('f-data','children')])#,
              # Input('centres','value')])
def update_figure(value):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
    return options


@app.callback(Output('f-stacks3','options'),
              [Input('f-data','children')])#,
              # Input('centres','value')])
def update_figure(value):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
    return options


@app.callback(Output('f-fig2','figure'),
              [Input('f-data','children'),
                Input('f-xaxis2','value'),
                Input('f-stacks2','value'),
                Input('f-filtercol1','value'),
                Input('f-filterval1','value')])
def update_figure(value,xaxis,stacks,filtercol1,filterval1):#,filtercol2,filterval2,filtercol3,filterval3):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        fig=go.Figure()
    else:
        v=[]
        if type(filterval1)==str:
            v=[filterval1]
        else:
            for val in filterval1:
                v.append(val)
       
      
        data1=data[(data[filtercol1].isin(v))]#&(data[filtercol2].isin(w))]#&(data[filtercol3].isin(x))]
        if data1.empty:
            fig=go.Figure()
        else:
            fig=plot_stack(data1,xaxis,'flexa_LC Amount',stacks)
    return fig

@app.callback(Output('f-fig3','figure'),
              [Input('f-data','children'),
               Input('f-xaxis3','value'),
               Input('f-stacks3','value'),
               Input('f-filtercol2','value'),
               Input('f-filterval2','value'),
               Input('centres','value')])#,
            
def update_figure(value,xaxis,stacks,filtercol,filterval,centres):#,filtercol2,filterval2,filtercol3,filterval3):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        fig=go.Figure()
    else:
        # if filtercol1 is None or filterval1 is None:
        #     fig=go.Figure()
        # else:
        v=[]
        # for val in filterval:
        #     v.append(val)
            
        # w=[]
        if type(filterval)==str:
            v=[filterval]
        elif type(filterval)==list:
            for val in filterval:
                v.append(val)
       
        x=[]
        if type(centres)==str:
            x=[centres]
        else:
            for val in centres:
                x.append(val)
                
        # # if not v:
        #         fig=go.Figure()
        #     else:
        data1=data[data[filtercol].isin(v)]['flexa_key_x'].dropna().drop_duplicates(keep='first').reset_index()#&(data[filtercol2].isin(w))]#&(data[filtercol3].isin(x))]
        data2=data[(data['flexa_key_x'].isin(data1['flexa_key_x']))]#&(-((data[filtercol].isin(v))))]#&(data['flexa_Profit Ctr'].isin(x)))))]
        
        if data1.empty:
            fig=go.Figure()
        else:
            fig=plot_stack(data2,xaxis,'flexa_LC Amount',stacks)
    return fig
       
        
@app.callback(Output('d-data1','children'),
              [Input('centres','value')])
def update_data(value):
    
    v=[]
    if type(value)==str:
        v=[value]
    else:
        for val in value:
            v.append(val)
    if not v:
        final={'pivot1':pd.DataFrame().to_json(orient='split',date_format='iso'),'pivot2':pd.DataFrame().to_json(orient='split',date_format='iso'),'pivot3':pd.DataFrame().to_json(orient='split',date_format='iso')}
    else:
       
        pclines2=pd.DataFrame()
        for a in v:
           pclines1=pd.read_pickle(r"C:\Users\arupnar.mim2013\AnacondaProjects\Profit Centre\{}.pkl".format(a))
           pclines2=pd.concat([pclines2,pclines1],ignore_index=True)
        pclines3=pclines2.drop_duplicates(keep='first')
        pclines3=pclines3[pclines3['bkpf_Reversal_x'].isnull()]
        glnames=pclines3['glgroup_GL name'].dropna().drop_duplicates(keep='first').reset_index()
        columns=pclines3.head()
        # pclines4=pclines3[pclines3['flexa_Profit Ctr'].isin(v)]
        
        othereffects1=pd.DataFrame()
        # pivot1=pd.pivot_table(pclines4,index=['flexa_key_x','flexa_Profit Ctr','glgroup_GL Type','glgroup_GL schedule','glgroup_Account head Grouping','glgroup_GL name'],values=['flexa_LC Amount'],aggfunc=np.sum).reset_index()
       
        final={'pivot1':glnames.to_json(orient='split',date_format='iso'),'pivot2':columns.to_json(orient='split',date_format='iso')}#,'pivot3':allpoints.to_json(orient='split',date_format='iso')}
    return json.dumps(final)


@app.callback(Output('d-glname','options'),
              [Input('d-data1','children')])#,
              # Input('centres','value')])
def update_figure(value):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        data1=data
        options=[{'label':i,'value':i} for i in data1['glgroup_GL name']]
    return options
        
        
                 
@app.callback(Output('d-legend','options'),
              [Input('d-data1','children')])#,
              # Input('centres','value')])
def update_figure(value):
    b=json.loads(value)
    data=pd.read_json(b['pivot2'],orient='split')
    if data.empty:
        options=[]
    else:
        data1=data
        options=[{'label':i,'value':i} for i in data1.columns]
    return options



@app.callback(Output('d-fig1','figure'),
              [Input('centres','value'),
               Input('d-glname','value'),
               Input('d-legend','value')])#,
                # Input('filtercol1','value'),
                # Input('filterval1','value')])#,
              #   Input('filtercol2','value'),
              #   Input('filterval2','value'),
              #   Input('filtercol3','value'),
              #   Input('filterval3','value')])#,
              # # Input('centres','value')])
def update_figure(value,glname,legend):#,filtercol2,filterval2,filtercol3,filterval3):
    v=[]
    if type(value)==str:
        v=[value]
    else:
        for val in value:
            v.append(val)
    if not v:
        fig=go.Figure()
    else:
       
        pclines2=pd.DataFrame()
        for a in v:
           pclines1=pd.read_pickle(r"C:\Users\arupnar.mim2013\AnacondaProjects\Profit Centre\{}.pkl".format(a))
           pclines2=pd.concat([pclines2,pclines1],ignore_index=True)
        pclines3=pclines2.drop_duplicates(keep='first')
        pclines3=pclines3[pclines3['bkpf_Reversal_x'].isnull()]
        # pclines3=data
        data1=pclines3[pclines3['glgroup_GL name']==glname]['flexa_key_x'].dropna().drop_duplicates(keep='first').reset_index()
        data2=pclines3[pclines3['flexa_key_x'].isin(data1['flexa_key_x'])]
        data2['new']=data2['flexa_DocumentNo'].astype(str)+" // "+data2['flexa_Profit Ctr'].astype(str)+" // "+data2['bseg_Text'].astype(str)
       
        fig=plot_timeseries(data2,'flexa_Pstng Date','flexa_LC Amount',legend,'new')
    return fig

@app.callback(Output('s-table','data'),
              [Input('s-flexa_key_x','value')])
def update_table(value):
    v=str(value)
    # v1=v.replace('"','')
    # v2=v1.replace("'","")
    cnx = sqlite3.connect(r'C:\Users\arupnar.mim2013\data.db')
    # test='2017.0100000001.0'
    # quote="'"
    query="SELECT * FROM df101 WHERE [flexa_key_x] = '%s'"%(str(v),)
    # query="SELECT * FROM df101 WHERE [flexa_Profit Ctr] = 'P059-OIL STF MADHUBAN'"
    df = pd.read_sql(query, cnx)
    # print (df)
    # df1=df[df['flexa_key_x']==value]
    df1=df[['flexa_Year', 'flexa_DocumentNo', 'flexa_Itm',
       'flexa_Account','glgroup_GL name', 'flexa_Profit Ctr', 'flexa_LC Amount', 'bseg_Text',
       'bseg_ClgEntDate','bseg_Clrng doc.','flexa_Pstng Date','Vendor',
       'Customer']].astype(str)
    docs=df1.to_dict('records')
        
    return docs

@app.callback(Output('s-table','columns'),
              [Input('centres','value')])
def update_table(value):
    list=['flexa_Year', 'flexa_DocumentNo', 'flexa_Itm',
       'flexa_Account','glgroup_GL name', 'flexa_Profit Ctr', 'flexa_LC Amount', 'bseg_Text',
       'bseg_ClgEntDate','bseg_Clrng doc.','flexa_Pstng Date','Vendor',
       'Customer']
    columns=[{"name":i,"id":i,"deletable":True,"selectable":True} for i in list]
    return columns
                    

@app.callback(Output('d-table','data'),
              [Input('centres','value')])
def update_table(value):
    v=[]
    if type(value)==str:
        v=[value]
    else:
        for val in value:
            v.append(val)
    if not v:
        docs=[]
    else:
       
        pclines2=pd.DataFrame()
        for a in v:
           pclines1=pd.read_pickle(r"C:\Users\arupnar.mim2013\AnacondaProjects\Profit Centre\{}.pkl".format(a))
           pclines2=pd.concat([pclines2,pclines1],ignore_index=True)
        pclines3=pclines2.drop_duplicates(keep='first')
        pclines3=pclines3[pclines3['bkpf_Reversal_x'].isnull()]
        pclines4=pclines3[['flexa_Year', 'flexa_DocumentNo', 'flexa_Itm',
       'flexa_Account','glgroup_GL name', 'flexa_Profit Ctr', 'flexa_LC Amount', 'bseg_Text',
       'bseg_ClgEntDate','bseg_Clrng doc.','flexa_Pstng Date','Vendor',
       'Customer']]
        pclines4[['flexa_Year', 'flexa_DocumentNo', 'flexa_Itm',
       'flexa_Account','bseg_ClgEntDate','bseg_Clrng doc.']]=pclines4[['flexa_Year', 'flexa_DocumentNo', 'flexa_Itm',
       'flexa_Account','bseg_ClgEntDate','bseg_Clrng doc.']].astype(str)
        docs=pclines4.to_dict('records')
        
    return docs
    
@app.callback(Output('d-table','columns'),
              [Input('centres','value')])
def update_table(value):
    list=['flexa_Year', 'flexa_DocumentNo', 'flexa_Itm',
       'flexa_Account','glgroup_GL name', 'flexa_Profit Ctr', 'flexa_LC Amount', 'bseg_Text',
       'bseg_ClgEntDate','bseg_Clrng doc.','flexa_Pstng Date','Vendor',
       'Customer']
    columns=[{"name":i,"id":i,"deletable":True,"selectable":True} for i in list]
    return columns
                    
@app.callback(Output('m-data1','children'),
              [Input('centres','value')])
def update_data(value):
    
    v=[]
    if type(value)==str:
        v=[value]
    else:
        for val in value:
            v.append(val)
    if not v:
        final={'pivot1':pd.DataFrame().to_json(orient='split',date_format='iso'),'pivot2':pd.DataFrame().to_json(orient='split',date_format='iso'),'pivot3':pd.DataFrame().to_json(orient='split',date_format='iso')}
    else:
       pclines2=pd.DataFrame()
       materiallines=pd.read_pickle(r"C:\Users\arupnar.mim2013\AnacondaProjects\Materials\materialfile.pkl")
       materiallines2=materiallines[materiallines['flexa_Profit Ctr'].isin(v)]
       materials=materiallines2['mara_Material description'].dropna().drop_duplicates(keep='first').reset_index()
       
       columns=materiallines2.head()
       othereffects1=pd.DataFrame()
       final={'pivot1':materials.to_json(orient='split',date_format='iso'),'pivot2':columns.to_json(orient='split',date_format='iso')}#,'pivot3':allpoints.to_json(orient='split',date_format='iso')}
    return json.dumps(final)

@app.callback(Output('m-materials','options'),
              [Input('m-data1','children')])
def update_figure(value):
   b=json.loads(value)
   data=pd.read_json(b['pivot1'],orient='split')
   # v=[]
   # if type(value2)==str:
   #     v=[value2]
   # else:
   #      for val in value2:
   #          v.append(val)
   if data.empty:
       options=[]
   else:
       options=[{'label':i,'value':i} for i in data['mara_Material description']]

       # options=data
   return options


@app.callback(Output('m-data2','children'),
              [Input('m-materials','value')])
def update_data(value):
    
    v=[]
    if (value==None):
        v=[]
    elif type(value)==str:
        v=[value]
    else:
        for val in value:
            v.append(val)
    if not v:
        final={'pivot1':pd.DataFrame().to_json(orient='split',date_format='iso'),'pivot2':pd.DataFrame().to_json(orient='split',date_format='iso')}
    else:
        # pclines2=pd.DataFrame()
        materiallines=pd.read_pickle(r"C:\Users\arupnar.mim2013\AnacondaProjects\Materials\materialfile.pkl")
        materiallines2=materiallines[materiallines['mara_Material description'].isin(v)]
        columns=pd.DataFrame()
        final={'pivot1':materiallines2.to_json(orient='split',date_format='iso'),'pivot2':columns.to_json(orient='split',date_format='iso')}#,'pivot3':allpoints.to_json(orient='split',date_format='iso')}
    return json.dumps(final)
# final=json.dumps(final)

# v=['DRY M-SAND']

@app.callback(Output('m-filtercol1','options'),
              [Input('m-data1','children')])#,
              # Input('centres','value')])
def update_figure(value):
   b=json.loads(value)
   data=pd.read_json(b['pivot2'],orient='split')
   if data.empty:
        options=[]
   else:
        options=[{'label':i,'value':i} for i in data.columns]
   return options


@app.callback(Output('m-filterval1','options'),
              [Input('m-materials','value'),
               Input('m-filtercol1','value'),
               Input('m-data2','children')])#,
              # Input('centres','value')])
def update_figure(value1,value2,value3):
    if value1==None:
        options=[]
    else:
        v=[]
        if type(value1)==str:
            v=[value1]
        else:
            for val in value1:
                v.append(val)
        if not v:
            options=[]
        
        else:
            b=json.loads(value3)
            data=pd.read_json(b['pivot1'],orient='split')
            materiallines=data#s2=materiallines[materiallines['flexa_Profit Ctr'].isin(v)]
            materiallines1=materiallines#[materiallines['mara_Material description'].isin(v)]
            materiallines3=materiallines1[value2].dropna().drop_duplicates(keep='first').reset_index()
           # materiallines2['new']=materiallines2['mara_Material description'].astype(str)+" ("+materiallines2['bseg_BUn'].astype(str)+")"
           # materials=materiallines2['mara_Material description'].dropna().drop_duplicates(keep='first').reset_index()
            options=[{'label':i,'value':i} for i in materiallines3[value2]]
    return options

@app.callback(Output('m-filterval1','value'),
              [Input('m-materials','value'),
               Input('m-filtercol1','value'),
               Input('m-data2','children')])#,
              # Input('centres','value')])
def update_figure(value1,value2,value3):
    if value1==None:
        options=[]
    else:
        v=[]
        if type(value1)==str:
            v=[value1]
        else:
            for val in value1:
                v.append(val)
        if not v:
            options=[]
        
        else:
            b=json.loads(value3)
            data=pd.read_json(b['pivot1'],orient='split')
            materiallines=data
            materiallines1=materiallines[materiallines['mara_Material description'].isin(v)]
            materiallines3=materiallines1[value2].dropna().drop_duplicates(keep='first').reset_index()
            options=materiallines3[value2]
    return options



@app.callback(Output('m-fig1','figure'),
              [Input('centres','value')])
def update_data(value2):
    
    v=[]
    if type(value2)==str:
        v=[value2]
    else:
        for val in value2:
            v.append(val)
        # materiallines=data
        materiallines=pd.read_pickle(r"C:\Users\arupnar.mim2013\AnacondaProjects\Materials\materialfile.pkl")
        # a=materiallines.groupby(['glgroup_GL Type','glgroup_GL schedule'])['flexa_LC Amount'].sum()
        materiallines2=materiallines[materiallines['flexa_Profit Ctr'].isin(v)]
        materiallines3=materiallines2[materiallines2['glgroup_GL Type'].isin(['Asset','Expense'])]
        # materiallines3=materiallines2
        # materiallines3=materiallines2[materiallines2['Vendor'].isna()]
        materiallines4=materiallines3.groupby(['mara_Matl Group','mara_Material description','bseg_BUn'])['flexa_LC Amount'].sum().reset_index()
        materiallines4['All']='Material codes with positive values'
        materiallines5=materiallines4[materiallines4['flexa_LC Amount']>0]
        # materiallines1=pd.merge(materiallines,glgrouping,how='left',on=['glgroup_GL name'])
        # materiallines3.to_csv(r"C:\Users\arupnar.mim2013\AnacondaProjects\Materials\test2.csv")
        # print (materiallines5['flexa_LC Amount'].sum())
        # materiallines5['flexa_LC Amount']=materiallines5['flexa_LC Amount']*-1
        fig=px.treemap(materiallines5,path=['All','bseg_BUn','mara_Material description'],values='flexa_LC Amount')
    return fig


# materiallines1=materiallines[materiallines['glgroup_GL Type'].isin(['Asset','Expense'])]
# materiallines2=materiallines1.groupby(['mara_Material description'])['flexa_LC Amount'].sum()
    # data=materiallines2    
# filtercol='flexa_Profit Ctr'
# filterval=['P042-MSV BPCL Kochi Refin']
@app.callback(Output('m-fig2','figure'),
              [Input('m-filtercol1','value'),
               Input('m-data2','children'),#,               
               Input('m-filterval1','value')])#,
               # 
                
           #,
def update_data(filtercol,value2,filterval):#,filterval,value2):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        fig=go.Figure()
    else:
        # fig=go.Figure()
        if not filterval:
            w=[]
        else:
   
            w=[]
            if type(filterval)==str:
                w=[filterval]
            else:
                for val in filterval:
                    w.append(val)
        # v=['PLATE,SA516GR60,44MMTHK']
        # w=['P070-IOCL-BONGAIGAON']
        # filtercol='flexa_Profit Ctr'
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        materiallines=data
        materiallines2=materiallines
        materiallines3=materiallines2[materiallines2['glgroup_GL Type'].isin(['Asset','Expense'])]
        k=materiallines3['bseg_BUn'].dropna().drop_duplicates(keep='first').reset_index()
        if k.empty:
            k1='NIL'
        else:
            k1=k.loc[0,'bseg_BUn']
        materiallines4=materiallines3[materiallines3[filtercol].isin(w)]
        materiallines4=materiallines4[-materiallines4['Vendor'].isna()]
        materiallines4['Rate']=materiallines4['flexa_LC Amount']/materiallines4['bseg_Quantity']
        vendors=materiallines4.groupby(['Vendor'])['flexa_LC Amount'].sum().reset_index().sort_values(by='flexa_LC Amount',ascending=False).reset_index()
        
        
        m=pd.DataFrame()
        # n=pd.DataFrame()
        for i,v in vendors['Vendor'].items():
            data=materiallines4[materiallines4['Vendor']==v]
            data=data.reset_index()
            q=data['flexa_LC Amount'].sum()/100000
            b=str("{:,.0f}".format(q))
            fig1=go.Scatter(y=data['Rate'],x=data['flexa_Pstng Date'],text=data['mara_Material description'].astype(str)+'<br>'+data['flexa_Profit Ctr'].astype(str)+'<br>'+data['Vendor'].astype(str),hoverinfo='y+x+text',mode='markers',name=str(v)+"("+str(b)+" L)",showlegend=True,legendgroup=v)     
            for x in range(0,len(data)):
                # print(x)
                # x=0
                if (data.loc[x,'flexa_LC Amount']<0):
                    data.loc[x,'bseg_Quantity']=data.loc[x,'bseg_Quantity']*-1
            data['Rate1']=data['Rate'].astype(int).astype(str)    
            data1=data.groupby(['flexa_Pstng Date','mara_Material description','bseg_BUn','flexa_Profit Ctr','Vendor','Rate1'])['bseg_Quantity'].sum().reset_index()    
            fig2=go.Bar(y=data1['bseg_Quantity'],x=data1['flexa_Pstng Date'],text=data1['bseg_BUn'].astype(str)+" , "+data1['mara_Material description'].astype(str)+'<br>'+data1['flexa_Profit Ctr'].astype(str)+'<br>'+data1['Vendor'].astype(str)+'<br>'+"Rate : "+data1['Rate1'].astype(str)+"/-",hoverinfo='y+text',name=str(v)+"("+str(b)+" L)",showlegend=True,legendgroup=v)     
            # data2=data1.groupby(['flexa_Pstng Date'])['bseg_Quantity'].sum().reset_index()
            fig.add_trace(fig2,secondary_y=False)
            fig.add_trace(fig1,secondary_y=True)
            m=pd.concat([m,data])
            # n=pd.concat([n,data2])
        n=materiallines4.groupby(['flexa_Pstng Date'])['bseg_Quantity'].sum().reset_index()

        dates=materiallines4['flexa_Pstng Date'].reset_index().sort_values(by='flexa_Pstng Date')
        if m.empty:
            ratemin=0
            ratemax=0
        else:
            ratemin=m['Rate'].min()
            ratemax=m['Rate'].max()
        if (ratemin<0):
            ratemin=ratemin*-1
        
        minquant=n['bseg_Quantity'].min()
        if (minquant<0):
            minquant=minquant*-1
        maxquant=n['bseg_Quantity'].max()
        e=max(ratemin,ratemax)
        f=max(minquant,maxquant)
        fig.update_layout(barmode='relative',xaxis = dict(type = "category"))
        fig.update_yaxes(title_text="Rate", secondary_y=True,range=[e*-1.02,e*1.02])
        fig.update_yaxes(title_text="Quantity ("+str(k1)+")", secondary_y=False,range=[f*-1.02,f*1.02])
        fig.update_layout(xaxis=dict(categoryarray=dates['flexa_Pstng Date']))
    return fig
# plot(fig)
@app.callback(Output('c-data','children'),
              [Input('centres','value')])
def update_data(value):
    
    v=[]
    if type(value)==str:
        v=[value]
    else:
        for val in value:
            v.append(val)
    if not v:
        final={'pivot1':pd.DataFrame().to_json(orient='split',date_format='iso'),'pivot2':pd.DataFrame().to_json(orient='split',date_format='iso'),'pivot3':pd.DataFrame().to_json(orient='split',date_format='iso')}
    else:
        # v=['FD01-Textile Division']
        pclines2=pd.DataFrame()
        for a in v:
           pclines1=pd.read_pickle(r"C:\Users\arupnar.mim2013\AnacondaProjects\Profit Centre\{}.pkl".format(a))
           pclines2=pd.concat([pclines2,pclines1],ignore_index=True)
        pclines3=pclines2.drop_duplicates(keep='first')
        pclines3=pclines3[pclines3['bkpf_Reversal_x'].isnull()]
        customerdocs=pclines3[-pclines3['Customer'].isna()]['flexa_key_x'].dropna().drop_duplicates(keep='first').reset_index()
        customerlines=pclines3[pclines3['flexa_key_x'].isin(customerdocs['flexa_key_x'])]
        customerlines=customerlines[customerlines['flexa_Profit Ctr'].isin(v)]
        # customerlines['new']
        customerselfeffects=customerlines[-customerlines['Customer'].isna()]
        customerselfeffects['Effect']='Self-effects'
        customerothereffects=customerlines[customerlines['Customer'].isna()]
        customerothereffects['Effect']= 'Other-effects'
        customerdata=pd.concat([customerselfeffects,customerothereffects])
        pivot2=customerdata.groupby(['Customer'])['flexa_LC Amount'].sum().reset_index()
        customerdata1 = customerdata.fillna('blank')
        pivot1=pd.pivot_table(customerdata1,index=['Effect','Customer','flexa_Profit Ctr','glgroup_GL Type','glgroup_GL schedule','glgroup_Account head Grouping','glgroup_GL name'],values=['flexa_LC Amount'],aggfunc=np.sum,fill_value=0).reset_index()
        final={'pivot1':pivot1.to_json(orient='split',date_format='iso'),'pivot2':pivot2.to_json(orient='split',date_format='iso'),'pivot3':pd.DataFrame().to_json(orient='split',date_format='iso')}
    return json.dumps(final)
# print(pivot1.columns)
# data=pivot1    
    
@app.callback(Output('c-customer','options'),
              [Input('c-data','children')])
def update_figure(value):
   b=json.loads(value)
   data=pd.read_json(b['pivot2'],orient='split')
   # v=[]
   # if type(value2)==str:
   #     v=[value2]
   # else:
   #      for val in value2:
   #          v.append(val)
   if data.empty:
       options=[]
   else:
       options=[{'label':i,'value':i} for i in data['Customer']]

       # options=data
   return options

@app.callback(Output('c-data1','children'),
              [Input('c-customer','value')])
def update_data(value):
    
    v=[]
    if type(value)==str:
        v=[value]
    elif type(value)==list:
        for val in value:
            v.append(val)
    if not v:
        final={'pivot1':pd.DataFrame().to_json(orient='split',date_format='iso'),'pivot2':pd.DataFrame().to_json(orient='split',date_format='iso'),'pivot3':pd.DataFrame().to_json(orient='split',date_format='iso')}
    else:
        # v=['FD01-Textile Division']
        customerlines2=pd.DataFrame()
        for a in v:
           customerlines1=pd.read_pickle(r"C:\Users\arupnar.mim2013\AnacondaProjects\Customer\{}.pkl".format(a))
           customerlines2=pd.concat([customerlines2,customerlines1],ignore_index=True)
        customerlines3=customerlines2.drop_duplicates(keep='first')
        customerlines=customerlines3[customerlines3['bkpf_Reversal_x'].isnull()]
        # customerdocs=customerlines3[-customerlines3['Customer'].isna()]['flexa_key_x'].dropna().drop_duplicates(keep='first').reset_index()
        # customerlines=customerlines3[customerlines3['flexa_key_x'].isin(customerdocs['flexa_key_x'])]
        # customerlines=customerlines[customerlines['flexa_Profit Ctr'].isin(v)]
        # customerlines['new']
        customerselfeffects=customerlines[customerlines['Customer'].isin(v)]
        customerselfeffects['Effect']='Self-effects'
        customerothereffects=customerlines[-customerlines['Customer'].isin(v)]
        customerothereffects['Effect']= 'Other-effects'
        customerdata=pd.concat([customerselfeffects,customerothereffects])
        # pivot2=customerdata.groupby(['Customer'])['flexa_LC Amount'].sum().reset_index()
        customerdata1 = customerdata.fillna('blank')
        # customerdata1=customerdata1.sort_values(by='flexa_Pstng Date')
        # customerdata1['Posting date']
        pivot1=pd.pivot_table(customerdata1,index=['flexa_Pstng Date','Effect','Customer','bkpf_Reference','bkpf_HeaderText','bseg_Text','flexa_key_x','flexa_Profit Ctr','glgroup_GL Type','glgroup_GL schedule','glgroup_Account head Grouping','glgroup_GL name'],values=['flexa_LC Amount'],aggfunc=np.sum,fill_value=0).reset_index()
        pivot1=pivot1.sort_values(by='flexa_Pstng Date')
        pivot1['Posting date']=pivot1['flexa_Pstng Date'].dt.strftime('%d/%m/%Y')
        pivot1['new']=pivot1['flexa_key_x'].astype(str)+"//"+pivot1['bkpf_Reference'].astype(str)+"//"+pivot1['bkpf_HeaderText'].astype(str)+"//"+pivot1['bseg_Text'].astype(str)
        
        pivot1=pivot1.drop(columns=['flexa_Pstng Date','bkpf_Reference','bkpf_HeaderText','bseg_Text','flexa_key_x'])
        
        
        # pivot1['flexa_Pstng Date']=pivot1['flexa_Pstng Date'].astype('category')
        final={'pivot1':pivot1.to_json(orient='split',date_format='iso'),'pivot2':pd.DataFrame().to_json(orient='split',date_format='iso'),'pivot3':pd.DataFrame().to_json(orient='split',date_format='iso')}
    return json.dumps(final)
# print (customerdata.columns)
# a=plot_stack(pivot1,'flexa_Pstng Date','flexa_LC Amount','flexa_Profit Ctr')
# a.update_layout(barmode='relative',xaxis = dict(type = "category"))
# plot(a)

@app.callback(Output('c-filtercol1','options'),
              [Input('c-data','children')])
def update_data(value2):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
        
    return options

@app.callback(Output('c-filterval1','options'),
              [Input('c-data','children'),
               Input('c-filtercol1','value')])
def update_data(value2,value3):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        data1=data[value3].dropna().drop_duplicates(keep='first').reset_index()
        options=[{'label':i,'value':i} for i in data1[value3]]
        
    return options

@app.callback(Output('c-filterval1','value'),
              [Input('c-data','children'),
               Input('c-filtercol1','value')])
def update_data(value2,value3):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        data1=data[value3].dropna().drop_duplicates(keep='first').reset_index()
        options=data1[value3]
        
    return options

@app.callback(Output('c-xaxis1','options'),
              [Input('c-data','children')])
def update_data(value2):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
        
    return options

@app.callback(Output('c-stacks1','options'),
              [Input('c-data','children')])
def update_data(value2):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
        
    return options

@app.callback(Output('c-fig1','figure'),
              [Input('c-data','children'),
               Input('c-xaxis1','value'),
               Input('c-stacks1','value'),
               Input('c-filtercol1','value'),
               Input('c-filterval1','value')])
def update_figure(value,xaxis,stacks,filtercol1,filterval1):#,filtercol2,filterval2,filtercol3,filterval3):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        fig=go.Figure()
    else:
        v=[]
        if type(filterval1)==str:
            v=[filterval1]
        else:
            for val in filterval1:
                v.append(val)
       
        data1=data[(data[filtercol1].isin(v))]#&(data[filtercol2].isin(w))]#&(data[filtercol3].isin(x))]
        if data1.empty:
            fig=go.Figure()
        else:
            fig=plot_stack(data1,xaxis,'flexa_LC Amount',stacks)
    return fig


@app.callback(Output('c-fig2','figure'),
              [Input('c-data','children')])
def update_figure(value):#,filtercol2,filterval2,filtercol3,filterval3):
    # value=final
    # value=a
    b=json.loads(value)
    data=pd.read_json(b['pivot2'],orient='split')
    if data.empty:
        fig=go.Figure()
    else:
        data1=data[data['flexa_LC Amount']>0]
        data1['All']='Positive values'
        data2=data[data['flexa_LC Amount']<0]
        data2['flexa_LC Amount']=data2['flexa_LC Amount']*-1
        data2['All']='Negative values'
        data3=pd.concat([data1,data2],ignore_index=True)
        # data3['Overall']='Customers'
        fig=px.treemap(data3,path=['All','Customer'],values='flexa_LC Amount')
  
    return fig
# plot(fig)
# data=pivot2
# @app.callback(Output('c-fig3','figure'),
#               [Input('c-data','children')])
# def update_figure(value):#,filtercol2,filterval2,filtercol3,filterval3):
#     b=json.loads(value)
#     data=pd.read_json(b['pivot2'],orient='split')
#     if data.empty:
#         fig=go.Figure()
#     else:
#         data1=data[data['flexa_LC Amount']<0]
#         data1['flexa_LC Amount']=data1['flexa_LC Amount']*-1
#         data1['All']='Negative values'
#         fig=px.treemap(data1,path=['All','Customer'],values='flexa_LC Amount')
  
#     return fig

@app.callback(Output('c-filtercol2','options'),
              [Input('c-data1','children')])
def update_data(value2):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
        
    return options

@app.callback(Output('c-filterval2','options'),
              [Input('c-data1','children'),
               Input('c-filtercol2','value')])
def update_data(value2,value3):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        data1=data[value3].dropna().drop_duplicates(keep='first').reset_index()
        options=[{'label':i,'value':i} for i in data1[value3]]
        
    return options

# @app.callback(Output('c-filterval2','value'),
#               [Input('c-data1','children'),
#                Input('c-filtercol2','value')])
# def update_data(value2,value3):
#     b=json.loads(value2)
#     data=pd.read_json(b['pivot1'],orient='split')
#     if data.empty:
#         options=[]
#     else:
#         data1=data[value3].dropna().drop_duplicates(keep='first').reset_index()
#         options=data1[value3]
        
#     return options

@app.callback(Output('c-xaxis2','options'),
              [Input('c-data1','children')])
def update_data(value2):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
        
    return options

@app.callback(Output('c-stacks2','options'),
              [Input('c-data1','children')])
def update_data(value2):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
        
    return options

@app.callback(Output('c-fig4','figure'),
              [Input('c-data1','children'),
               Input('c-xaxis2','value'),
               Input('c-stacks2','value'),
               Input('c-filtercol2','value'),
               Input('c-filterval2','value')])
def update_figure(value,xaxis,stacks,filtercol1,filterval1):#,filtercol2,filterval2,filtercol3,filterval3):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        fig=go.Figure()
    else:
        v=[]
        if type(filterval1)==str:
            v=[filterval1]
        else:
            for val in filterval1:
                v.append(val)
        data=data[data['Effect']=='Self-effects']
       
        data1=data[(data[filtercol1].isin(v))]
       
        # data1['flexa_Pstng Date']=data1['flexa_Pstng Date'].astype('category')
        if data1.empty:
            fig=go.Figure()
        else:
            # data1['new']=data1['bkpf_']
            fig=plot_stack(data1,xaxis,'flexa_LC Amount',stacks,'new')
            if (xaxis=='Posting date'):
                 fig.update_layout(xaxis = dict(type = "category"))
                 fig.update_layout(xaxis=dict(categoryarray=data1['Posting date']))
                 # fig.update_layout(hoverinfo=data1['flexa_Profit Ctr'])
   
    return fig

@app.callback(Output('c-filtercol3','options'),
              [Input('c-data1','children')])
def update_data(value2):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
        
    return options

@app.callback(Output('c-filterval3','options'),
              [Input('c-data1','children'),
               Input('c-filtercol3','value')])
def update_data(value2,value3):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        data1=data[value3].dropna().drop_duplicates(keep='first').reset_index()
        options=[{'label':i,'value':i} for i in data1[value3]]
        
    return options

# @app.callback(Output('c-filterval2','value'),
#               [Input('c-data1','children'),
#                Input('c-filtercol2','value')])
# def update_data(value2,value3):
#     b=json.loads(value2)
#     data=pd.read_json(b['pivot1'],orient='split')
#     if data.empty:
#         options=[]
#     else:
#         data1=data[value3].dropna().drop_duplicates(keep='first').reset_index()
#         options=data1[value3]
        
#     return options

@app.callback(Output('c-xaxis3','options'),
              [Input('c-data1','children')])
def update_data(value2):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
        
    return options

@app.callback(Output('c-stacks3','options'),
              [Input('c-data1','children')])
def update_data(value2):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
        
    return options

@app.callback(Output('c-fig5','figure'),
              [Input('c-data1','children'),
               Input('c-xaxis3','value'),
               Input('c-stacks3','value'),
               Input('c-filtercol3','value'),
               Input('c-filterval3','value')])
def update_figure(value,xaxis,stacks,filtercol1,filterval1):#,filtercol2,filterval2,filtercol3,filterval3):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        fig=go.Figure()
    else:
        v=[]
        if type(filterval1)==str:
            v=[filterval1]
        else:
            for val in filterval1:
                v.append(val)
        data=data[data['Effect']=='Other-effects']
       
        data1=data[(data[filtercol1].isin(v))]
       
        # data1['flexa_Pstng Date']=data1['flexa_Pstng Date'].astype('category')
        if data1.empty:
            fig=go.Figure()
        else:
            # data1['new']=data1['bkpf_']
            fig=plot_stack(data1,xaxis,'flexa_LC Amount',stacks,'new')
            if (xaxis=='Posting date'):
                 fig.update_layout(xaxis = dict(type = "category"))
                 fig.update_layout(xaxis=dict(categoryarray=data1['Posting date']))
                 # fig.update_layout(hoverinfo=data1['flexa_Profit Ctr'])
   
    return fig


@app.callback(Output('v-data','children'),
              [Input('centres','value')])
def update_data(value):
    
    v=[]
    if type(value)==str:
        v=[value]
    else:
        for val in value:
            v.append(val)
    if not v:
        final={'pivot1':pd.DataFrame().to_json(orient='split',date_format='iso'),'pivot2':pd.DataFrame().to_json(orient='split',date_format='iso'),'pivot3':pd.DataFrame().to_json(orient='split',date_format='iso')}
    else:
        # v=['P059-OIL STF MADHUBAN']
        pclines2=pd.DataFrame()
        for a in v:
           pclines1=pd.read_pickle(r"C:\Users\arupnar.mim2013\AnacondaProjects\Profit Centre\{}.pkl".format(a))
           pclines2=pd.concat([pclines2,pclines1],ignore_index=True)
        pclines3=pclines2.drop_duplicates(keep='first')
        pclines3=pclines3[pclines3['bkpf_Reversal_x'].isnull()]
        vendordocs=pclines3[-pclines3['Vendor'].isna()]['flexa_key_x'].dropna().drop_duplicates(keep='first').reset_index()
        vendorlines=pclines3[pclines3['flexa_key_x'].isin(vendordocs['flexa_key_x'])]
        vendorlines=vendorlines[vendorlines['flexa_Profit Ctr'].isin(v)]
        # vendorlines['new']
        vendorselfeffects=vendorlines[-vendorlines['Vendor'].isna()]
        vendorselfeffects['Effect']='Self-effects'
        vendorothereffects=vendorlines[vendorlines['Vendor'].isna()]
        vendorothereffects['Effect']= 'Other-effects'
        vendordata=pd.concat([vendorselfeffects,vendorothereffects])
        pivot2=vendordata.groupby(['Vendor'])['flexa_LC Amount'].sum().reset_index()
        vendordata1 = vendordata.fillna('blank')
        pivot1=pd.pivot_table(vendordata1,index=['Effect','Vendor','flexa_Profit Ctr','glgroup_GL Type','glgroup_GL schedule','glgroup_Account head Grouping','glgroup_GL name'],values=['flexa_LC Amount'],aggfunc=np.sum,fill_value=0).reset_index()
        final={'pivot1':pivot1.to_json(orient='split',date_format='iso'),'pivot2':pivot2.to_json(orient='split',date_format='iso'),'pivot3':pd.DataFrame().to_json(orient='split',date_format='iso')}
    return json.dumps(final)
# print(pivot1.columns)
# data=pivot1    
    
@app.callback(Output('v-vendor','options'),
              [Input('v-data','children')])
def update_figure(value):
   b=json.loads(value)
   data=pd.read_json(b['pivot2'],orient='split')
   # v=[]
   # if type(value2)==str:
   #     v=[value2]
   # else:
   #      for val in value2:
   #          v.append(val)
   if data.empty:
       options=[]
   else:
       options=[{'label':i,'value':i} for i in data['Vendor']]

       # options=data
   return options

@app.callback(Output('v-data1','children'),
              [Input('v-vendor','value')])
def update_data(value):
    
    v=[]
    if type(value)==str:
        v=[value]
    elif type(value)==list:
        for val in value:
            v.append(val)
    if not v:
        final={'pivot1':pd.DataFrame().to_json(orient='split',date_format='iso'),'pivot2':pd.DataFrame().to_json(orient='split',date_format='iso'),'pivot3':pd.DataFrame().to_json(orient='split',date_format='iso')}
    else:
        # v=['SPARKON ENGINEERS-200834']
        vendorlines2=pd.DataFrame()
        for a in v:
           vendorlines1=pd.read_pickle(r"C:\Users\arupnar.mim2013\AnacondaProjects\Vendor\{}.pkl".format(a))
           vendorlines2=pd.concat([vendorlines2,vendorlines1],ignore_index=True)
        vendorlines3=vendorlines2.drop_duplicates(keep='first')
        vendorlines=vendorlines3[vendorlines3['bkpf_Reversal_x'].isnull()]
        # vendordocs=vendorlines3[-vendorlines3['vendor'].isna()]['flexa_key_x'].dropna().drop_duplicates(keep='first').reset_index()
        # vendorlines=vendorlines3[vendorlines3['flexa_key_x'].isin(vendordocs['flexa_key_x'])]
        # vendorlines=vendorlines[vendorlines['flexa_Profit Ctr'].isin(v)]
        # vendorlines['new']
        vendorselfeffects=vendorlines[vendorlines['Vendor'].isin(v)]
        vendorselfeffects['Effect']='Self-effects'
        vendorothereffects=vendorlines[-vendorlines['Vendor'].isin(v)]
        vendorothereffects['Effect']= 'Other-effects'
        vendordata=pd.concat([vendorselfeffects,vendorothereffects])
        # pivot2=vendordata.groupby(['vendor'])['flexa_LC Amount'].sum().reset_index()
        vendordata1 = vendordata.fillna('blank')
        # vendordata1=vendordata1.sort_values(by='flexa_Pstng Date')
        # vendordata1['Posting date']
        vendordata1[['bkpf_Reference','bkpf_HeaderText','bseg_Text']]=vendordata1[['bkpf_Reference','bkpf_HeaderText','bseg_Text']].astype(str)
        pivot1=pd.pivot_table(vendordata1,index=['flexa_Year','flexa_Pstng Date','Effect','Vendor','bkpf_Reference','bkpf_HeaderText','bseg_Text','flexa_key_x','flexa_Profit Ctr','glgroup_GL Type','glgroup_GL schedule','glgroup_Account head Grouping','glgroup_GL name'],values=['flexa_LC Amount'],aggfunc=np.sum,fill_value=0).reset_index()
        pivot1=pivot1.sort_values(by='flexa_Pstng Date')
        pivot1['Posting date']=pivot1['flexa_Pstng Date'].dt.strftime('%d/%m/%Y')
        pivot1['new']=pivot1['flexa_key_x'].astype(str)+"//"+pivot1['bkpf_Reference'].astype(str)+"//"+pivot1['bkpf_HeaderText'].astype(str)+"//"+pivot1['bseg_Text'].astype(str)
        
        pivot1=pivot1.drop(columns=['flexa_Pstng Date','bkpf_Reference','bkpf_HeaderText','bseg_Text','flexa_key_x'])
        
    # vendordata1.dtypes    
        # pivot1['flexa_Pstng Date']=pivot1['flexa_Pstng Date'].astype('category')
        final={'pivot1':pivot1.to_json(orient='split',date_format='iso'),'pivot2':pd.DataFrame().to_json(orient='split',date_format='iso'),'pivot3':pd.DataFrame().to_json(orient='split',date_format='iso')}
    return json.dumps(final)
# print (vendordata.columns)
# a=plot_stack(pivot1,'flexa_Pstng Date','flexa_LC Amount','flexa_Profit Ctr')
# a.update_layout(barmode='relative',xaxis = dict(type = "category"))
# plot(a)

@app.callback(Output('v-filtercol1','options'),
              [Input('v-data','children')])
def update_data(value2):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
        
    return options

@app.callback(Output('v-filterval1','options'),
              [Input('v-data','children'),
               Input('v-filtercol1','value')])
def update_data(value2,value3):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        data1=data[value3].dropna().drop_duplicates(keep='first').reset_index()
        options=[{'label':i,'value':i} for i in data1[value3]]
        
    return options

@app.callback(Output('v-filterval1','value'),
              [Input('v-data','children'),
               Input('v-filtercol1','value')])
def update_data(value2,value3):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        data1=data[value3].dropna().drop_duplicates(keep='first').reset_index()
        options=data1[value3]
        
    return options

@app.callback(Output('v-xaxis1','options'),
              [Input('v-data','children')])
def update_data(value2):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
        
    return options

@app.callback(Output('v-stacks1','options'),
              [Input('v-data','children')])
def update_data(value2):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
        
    return options

@app.callback(Output('v-fig1','figure'),
              [Input('v-data','children'),
               Input('v-xaxis1','value'),
               Input('v-stacks1','value'),
               Input('v-filtercol1','value'),
               Input('v-filterval1','value')])
def update_figure(value,xaxis,stacks,filtercol1,filterval1):#,filtercol2,filterval2,filtercol3,filterval3):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        fig=go.Figure()
    else:
        v=[]
        if type(filterval1)==str:
            v=[filterval1]
        else:
            for val in filterval1:
                v.append(val)
       
        data1=data[(data[filtercol1].isin(v))]#&(data[filtercol2].isin(w))]#&(data[filtercol3].isin(x))]
        if data1.empty:
            fig=go.Figure()
        else:
            fig=plot_stack(data1,xaxis,'flexa_LC Amount',stacks)
    return fig


@app.callback(Output('v-fig2','figure'),
              [Input('v-data','children')])
def update_figure(value):#,filtercol2,filterval2,filtercol3,filterval3):
    # b=json.loads(value)
    # data=pd.read_json(b['pivot2'],orient='split')
    # if data.empty:
    #     fig=go.Figure()
    # else:
    #     data1=data[data['flexa_LC Amount']>0]
    #     data1['All']='Positive values'
    #     fig=px.treemap(data1,path=['All','Vendor'],values='flexa_LC Amount')
  
    # return fig
    b=json.loads(value)
    data=pd.read_json(b['pivot2'],orient='split')
    if data.empty:
        fig=go.Figure()
    else:
        data1=data[data['flexa_LC Amount']>0]
        data1['All']='Positive values'
        data2=data[data['flexa_LC Amount']<0]
        data2['flexa_LC Amount']=data2['flexa_LC Amount']*-1
        data2['All']='Negative values'
        data3=pd.concat([data1,data2],ignore_index=True)
        # data3['Overall']='Customers'
        fig=px.treemap(data3,path=['All','Vendor'],values='flexa_LC Amount')
  
    return fig

# @app.callback(Output('v-fig3','figure'),
#               [Input('v-data','children')])
# def update_figure(value):#,filtercol2,filterval2,filtercol3,filterval3):
#     b=json.loads(value)
#     data=pd.read_json(b['pivot2'],orient='split')
#     if data.empty:
#         fig=go.Figure()
#     else:
#         data1=data[data['flexa_LC Amount']<0]
#         data1['flexa_LC Amount']=data1['flexa_LC Amount']*-1
#         data1['All']='Negative values'
#         fig=px.treemap(data1,path=['All','Vendor'],values='flexa_LC Amount')
  
#     return fig

@app.callback(Output('v-filtercol2','options'),
              [Input('v-data1','children')])
def update_data(value2):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
        
    return options

@app.callback(Output('v-filterval2','options'),
              [Input('v-data1','children'),
               Input('v-filtercol2','value')])
def update_data(value2,value3):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        data1=data[value3].dropna().drop_duplicates(keep='first').reset_index()
        options=[{'label':i,'value':i} for i in data1[value3]]
        
    return options

@app.callback(Output('c-filterval2','value'),
              [Input('c-data1','children'),
                Input('c-filtercol2','value')])
def update_data(value2,value3):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        data1=data[value3].dropna().drop_duplicates(keep='first').reset_index()
        options=data1[value3]
        
    return options

@app.callback(Output('c-filterval3','value'),
              [Input('c-data1','children'),
                Input('c-filtercol3','value')])
def update_data(value2,value3):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        data1=data[value3].dropna().drop_duplicates(keep='first').reset_index()
        options=data1[value3]
        
    return options

@app.callback(Output('v-xaxis2','options'),
              [Input('v-data1','children')])
def update_data(value2):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
        
    return options

@app.callback(Output('v-stacks2','options'),
              [Input('v-data1','children')])
def update_data(value2):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
        
    return options

@app.callback(Output('v-fig4','figure'),
              [Input('v-data1','children'),
               Input('v-xaxis2','value'),
               Input('v-stacks2','value'),
               Input('v-filtercol2','value'),
               Input('v-filterval2','value')])
def update_figure(value,xaxis,stacks,filtercol1,filterval1):#,filtercol2,filterval2,filtercol3,filterval3):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        fig=go.Figure()
    else:
        v=[]
        if type(filterval1)==str:
            v=[filterval1]
        else:
            for val in filterval1:
                v.append(val)
        data=data[data['Effect']=='Self-effects']
        data1=data[(data[filtercol1].isin(v))]
       
        # data1['flexa_Pstng Date']=data1['flexa_Pstng Date'].astype('category')
        if data1.empty:
            fig=go.Figure()
        else:
            # data1['new']=data1['bkpf_']
            fig=plot_stack(data1,xaxis,'flexa_LC Amount',stacks,'new')
            if (xaxis=='Posting date'):
                 fig.update_layout(xaxis = dict(type = "category"))
                 fig.update_layout(xaxis=dict(categoryarray=data1['Posting date']))
                 # fig.update_layout(hoverinfo=data1['flexa_Profit Ctr'])
   
    return fig

@app.callback(Output('v-filtercol3','options'),
              [Input('v-data1','children')])
def update_data(value2):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
        
    return options

@app.callback(Output('v-filterval3','options'),
              [Input('v-data1','children'),
               Input('v-filtercol3','value')])
def update_data(value2,value3):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        data1=data[value3].dropna().drop_duplicates(keep='first').reset_index()
        options=[{'label':i,'value':i} for i in data1[value3]]
        
    return options

@app.callback(Output('v-filterval2','value'),
              [Input('v-data1','children'),
                Input('v-filtercol2','value')])
def update_data(value2,value3):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        data1=data[value3].dropna().drop_duplicates(keep='first').reset_index()
        options=data1[value3]
        
    return options

@app.callback(Output('v-filterval3','value'),
              [Input('v-data1','children'),
                Input('v-filtercol3','value')])
def update_data(value2,value3):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        data1=data[value3].dropna().drop_duplicates(keep='first').reset_index()
        options=data1[value3]
        
    return options

@app.callback(Output('v-xaxis3','options'),
              [Input('v-data1','children')])
def update_data(value2):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
        
    return options

@app.callback(Output('v-stacks3','options'),
              [Input('v-data1','children')])
def update_data(value2):
    b=json.loads(value2)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        options=[]
    else:
        options=[{'label':i,'value':i} for i in data.columns]
        
    return options

@app.callback(Output('v-fig5','figure'),
              [Input('v-data1','children'),
               Input('v-xaxis3','value'),
               Input('v-stacks3','value'),
               Input('v-filtercol3','value'),
               Input('v-filterval3','value')])
def update_figure(value,xaxis,stacks,filtercol1,filterval1):#,filtercol2,filterval2,filtercol3,filterval3):
    b=json.loads(value)
    data=pd.read_json(b['pivot1'],orient='split')
    if data.empty:
        fig=go.Figure()
    else:
        v=[]
        if type(filterval1)==str:
            v=[filterval1]
        else:
            for val in filterval1:
                v.append(val)
        data=data[data['Effect']=='Other-effects']
        data1=data[(data[filtercol1].isin(v))]
       
        # data1['flexa_Pstng Date']=data1['flexa_Pstng Date'].astype('category')
        if data1.empty:
            fig=go.Figure()
        else:
            # data1['new']=data1['bkpf_']
            fig=plot_stack(data1,xaxis,'flexa_LC Amount',stacks,'new')
            if (xaxis=='Posting date'):
                 fig.update_layout(xaxis = dict(type = "category"))
                 fig.update_layout(xaxis=dict(categoryarray=data1['Posting date']))
                 # fig.update_layout(hoverinfo=data1['flexa_Profit Ctr'])
   
    return fig
# data1=pivot1
    # print (pivot1.columns)
# data1.dtypes
# pivot1['flexa_Pstng Date1']=pivot1['flexa_Pstng Date'].dt.strftime('%m/%d/%Y')
# pivot1.dtypes        
# pivot1
# # print(vendorlines.columns)
        
# if(__name__=='__main__'):
#     # app.run_server(debug=True,dev_tools_ui=False)
#     app.run_server(debug=True)

# Run the Dash app
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
