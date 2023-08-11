from datetime import date, timedelta
from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import sqlalchemy
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
from astral import sun, Observer
import pytz


app = Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])


def init_clients(url1, url2):
    engine1 = sqlalchemy.create_engine(url1, pool_pre_ping=True)
    engine2 = sqlalchemy.create_engine(url2, pool_pre_ping=True)
    return [engine1, engine2]


def get_data(engine, table, start_date, end_date):
    sql = f"SELECT * FROM {table} WHERE date BETWEEN '{start_date}' AND '{end_date}';"
    try:
        with engine.connect() as conn:
            df = pd.read_sql(sql, conn)
            df["date"] = pd.to_datetime(df["date"])
            df["date"] = (
                df["date"].dt.tz_localize("UTC").dt.tz_convert("Europe/Budapest")
            )
    except Exception as e:
        print(f"Error: {e}")
        df = pd.DataFrame()
    return df


@app.callback(
    Output("graph-inside", "figure"),
    Input("my-date-picker-range", "start_date"),
    Input("my-date-picker-range", "end_date"),
)
def update_output(start_date, end_date):
    start_date_object = date.fromisoformat(start_date)
    end_date_object = date.fromisoformat(end_date)
    engines = init_clients(url_inside, url_outside)
    df_inside = get_data(engines[0], "Data_raspberry3", start_date, end_date)
    df_inside2 = get_data(engines[0], "Data_ESP8266", start_date, end_date)
    df_inside3 = get_data(engines[0], "Data_raspberry4", start_date, end_date)
    df_outside = get_data(engines[1], "Data", start_date, end_date)
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True)
    fig.add_trace(
        go.Scatter(
            x=df_inside["date"], y=df_inside["temperature"], name="temperature raspberry3"
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df_inside2["date"], y=df_inside2["temperature"], name="temperature ESP8266"
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df_inside3["date"], y=df_inside3["temperature"], name="temperature raspberry4"
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df_outside["date"],
            y=df_outside["temperature"],
            name="temperature outside",
            visible="legendonly",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df_inside["date"], y=df_inside["humidity"], name="humidity raspberry3"
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df_inside2["date"], y=df_inside2["humidity"], name="humidity ESP8266"
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df_inside3["date"], y=df_inside3["humidity"], name="humidity raspberry4"
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df_outside["date"],
            y=df_outside["humidity"],
            name="humidity outside",
            visible="legendonly",
        ),
        row=2,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df_outside["date"],
            y=df_outside["temperature"],
            name="temperature outside",
        ),
        row=3,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df_outside["date"], y=df_outside["humidity"], name="humidity outside"
        ),
        row=4,
        col=1,
    )
    fig.update_layout(
        height=1090,
        legend_title="Legend",
    )
    return fig


def get_daily_info():
    observer = Observer(47.49801, 19.03991)
    sunrise = sun.sunrise(observer, date=date.today(), tzinfo="Europe/Budapest")
    sunset = sun.sunset(observer, date=date.today(), tzinfo="Europe/Budapest")
    return f'Today: {date.today()}. Sunrise: {sunrise.strftime("%H:%M:%S")} Sunset: {sunset.strftime("%H:%M:%S")}'


def generate_layout():
    today = date.today()
    tomorrow = today + timedelta(days=1)
    return html.Div(
        [
            html.H1(
                children="RaspberryPi dashboard",
                style={
                    "textAlign": "center",
                },
            ),
            html.H3(f"{get_daily_info()}"),
            dcc.DatePickerRange(
                id="my-date-picker-range",
                min_date_allowed=date(2019, 5, 1),
                max_date_allowed=date(tomorrow.year, tomorrow.month, tomorrow.day),
                initial_visible_month=date(today.year, today.month, today.day),
                end_date=date(tomorrow.year, tomorrow.month, tomorrow.day),
                start_date=date(today.year, today.month, today.day),
            ),
            dcc.Graph(id="graph-inside", figure={}),
            dcc.Interval(
                id="interval-component", interval=60 * 60 * 1000, n_intervals=0
            ),
        ],
        id="layout",
    )


@app.callback(Output("layout", "children"), Input("interval-component", "n_intervals"))
def update_layout(n):
    return generate_layout()


if __name__ == "__main__":
    url_inside = "mariadb+mariadbconnector://root:my-secret-pw@0.0.0.0:3308/inside"
    url_outside = "mariadb+mariadbconnector://root:my-secret-pw@0.0.0.0:3308/outside"
    print("Start...")
    app.layout = generate_layout()

    app.run_server(debug=True, host="0.0.0.0")
