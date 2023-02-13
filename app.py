from datetime import date, timedelta
from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.tools as tls
import sqlalchemy
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from sqlalchemy.sql import text
import pandas as pd


url_inside = "mariadb+mariadbconnector://root:my-secret-pw@0.0.0.0:3308/inside"
url_outside = "mariadb+mariadbconnector://root:my-secret-pw@0.0.0.0:3308/outside"
engine_inside = sqlalchemy.create_engine(url_inside)
engine_outside = sqlalchemy.create_engine(url_outside)
app = Dash(__name__, external_stylesheets = [dbc.themes.SOLAR])

today = date.today() 
tomorrow = today + timedelta(days = 1)

app.layout = html.Div([
    html.H1(children = "RaspberryPi dashboard",
        style={
            'textAlign': 'center',
        }
    ),
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=date(2019, 5, 1),
        max_date_allowed=date(tomorrow.year, tomorrow.month, tomorrow.day),
        initial_visible_month=date(today.year, today.month, today.day),
        end_date=date(tomorrow.year, tomorrow.month, tomorrow.day),
        start_date=date(today.year, today.month, today.day)
    ),
    html.Div(id='output-container-date-picker-range'),
    dcc.Graph(id="graph-inside", figure = {}),
    #dash_table(id="dash-table") 
    ]

)


@app.callback(
Output('output-container-date-picker-range', 'children'),
Output('graph-inside', 'figure'),
Input('my-date-picker-range', 'start_date'),
Input('my-date-picker-range', 'end_date'),
)
def update_output(start_date, end_date):
    today = date.today()
    tomorrow = today + timedelta(days = 1)
    start_date_object = date.fromisoformat(start_date)
    end_date_object = date.fromisoformat(end_date)
    sql = f"SELECT * FROM Data WHERE date BETWEEN '{start_date_object}' AND '{end_date_object}';"
    with engine_inside.connect() as conn:
        query = conn.execute(text(sql))
        print("Fetched from inside")
        df_inside = pd.DataFrame(query.fetchall())
    with engine_outside.connect() as conn: 
        query = conn.execute(text(sql))
        print("Fetched from outside")
        df_outside = pd.DataFrame(query.fetchall())

    fig = make_subplots(rows=4, cols=1, shared_xaxes=True)
    fig.add_trace(go.Scatter(x=df_inside["date"], y=df_inside["temperature"],name="temperature inside"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_outside["date"], y=df_outside["temperature"],name="temperature outside", visible = "legendonly"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_inside["date"], y=df_inside["humidity"], name="humidity inside"), row=2, col=1)
    fig.add_trace(go.Scatter(x=df_outside["date"], y=df_outside["humidity"], name="humidity outside", visible="legendonly"), row=2, col=1)
    fig.add_trace(go.Scatter(x=df_outside["date"], y=df_outside["temperature"], name="temperature outside"), row=3, col=1)
    fig.add_trace(go.Scatter(x=df_outside["date"], y=df_outside["humidity"], name="humidity outside"), row=4, col=1)
    fig.update_layout(height=1090,
            legend_title="Legend",)
    return f"{start_date_object}-{end_date_object}",fig 


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0')
