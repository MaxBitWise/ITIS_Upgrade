'''
Количество пользователей совершавших повторные покупки за определенный период

Нагрузка (число запросов) на сайт за астрономический час

Количество брошенных (не оплаченных) корзин имеется за определенный период?
'''

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import sqlite3
import main

connection = sqlite3.connect('database.db')
df = pd.read_sql("SELECT * from logs", connection)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='WebApp for ITIS Upgrade'),

    html.Div(),

    html.Label('Dropdown'),
        dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': 'Количество пользователей совершавших повторные покупки за определенный\
                 период(не учитывает дату)', 'value': 'tryes'},
                {'label': 'Нагрузка (число запросов) на сайт за астрономический\
                 час(учитывает дату)', 'value': 'counts'},
                {'label': 'Количество брошенных (не оплаченных) корзин за определённый\
                 период(не учитывает дату)', 'value': 'drops'}
            ],
            value='counts'
        ),
        dcc.Input(
            id='date',
            type='text',
            value='2018-08-01'
        ),

    dcc.Graph(id='graph')
])
@app.callback(Output('graph','figure'), [Input('dropdown', 'value'), Input('date','value')])
def update(selected_dropdown_value, date):

    if selected_dropdown_value == 'tryes':
        selectedDate = df
        resListOfIp = list()
        ips = list()
        dates = set()
        for a, x in selectedDate.iterrows():
            if x['success_pay'] != 'none':
                if (x['ip'] not in ips) and (x['ip'] not in resListOfIp):
                    ips.append(x['ip'])
                elif (x['ip'] in ips) and (x['ip'] not in resListOfIp):
                    resListOfIp.append(x['date'] + '/' + x['ip'])
            dates.add(x['date'])
        dates = list(dates)
        dates = sorted(dates)
        datesAmountDict = dict()
        for x in dates:
            datesAmountDict[x] = 0
        i = 0
        for x in resListOfIp:
            if (dates[i] in x):
                datesAmountDict[dates[i]] += 1
            else:
                i += 1
                if (dates[i] in x):
                    datesAmountDict[dates[i]] += 1
        return {
            'data':[
                {'x': list(datesAmountDict.keys()), 'y': list(datesAmountDict.values()), 'type': 'bar'}
            ],
            'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
        }
    elif selected_dropdown_value == 'counts':
        selectedDate = df[df['date'] == date]
        time = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0,
            10: 0,
            11: 0,
            12: 0,
            13: 0,
            14: 0,
            15: 0,
            16: 0,
            17: 0,
            18: 0,
            19: 0,
            20: 0,
            21: 0,
            22: 0,
            23: 0,
        }
        i = 0
        for a, x in selectedDate.iterrows():
            if (i == len(time) - 1) and (int(x['time'].split(':')[0]) >= list(time.keys())[i]):
                time[i] += 1
            elif (int(x['time'].split(':')[0]) >= list(time.keys())[i]):
                time[i] += 1
            if (i < len(time) - 1):
                if (int(x['time'].split(':')[0]) >= list(time.keys())[i + 1]):
                    i += 1
        return {
            'data': [
                {'x': list(time.keys()), 'y': list(time.values()), 'type': 'bar'},
            ],
            'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
        }
    else:
        resList = list()
        dates = set()
        selectedDate = df
        prePayedGoods = selectedDate[selectedDate['cart_id'] != 'none']
        successed_pay = selectedDate[selectedDate['success_pay'] != 'none']
        payCodes = set()
        for a, x in successed_pay.iterrows():
            payCodes.add(x['success_pay'])

        for a, x in prePayedGoods.iterrows():
            if (x['cart_id'] not in payCodes) and ((str(x['date']) + '/' + str(x['cart_id'])) not in resList):
                resList.append(str(x['date']) + '/' + str(x['cart_id']))
                dates.add(x['date'])
        dates = list(dates)
        dates = sorted(dates)

        datesAmountDict = dict()
        for x in dates:
            datesAmountDict[x] = 0
        i = 0
        for x in resList:
            if (dates[i] in x):
                datesAmountDict[dates[i]] += 1
            else:
                i += 1
                if (dates[i] in x):
                    datesAmountDict[dates[i]] += 1
        return {
            'data': [
                {'x': list(datesAmountDict.keys()), 'y': list(datesAmountDict.values()), 'type': 'bar'}
            ],
            'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
        }

if __name__ == '__main__':
    main.main()
    app.run_server(debug=True)