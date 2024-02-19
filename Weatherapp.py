import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import requests

app = dash.Dash(__name__)

current_dir = os.path.dirname(os.path.realpath(__file__))
css_path = os.path.join(current_dir, 'weather.css')
app = dash.Dash(__name__, external_stylesheets=[css_path])

API_KEY = "4838be71e119448408bc23c400bfdee0"


app.layout = html.Div([
    html.H1("Live Weather App", className='app-header'),
    html.Div([
        html.Label("Enter City Name:", className='city-label'),
        dcc.Input(id='city-input', type='text', value='Mississauga', className='city-input')
    ], className='input-container'),
    html.Div(id='weather-details', className='weather-info'),
    dcc.Graph(id='live-weather-map', className='map-container'),
    dcc.Interval(id='interval-component', interval=10*60*1000, n_intervals=0)
], className='app-container')

@app.callback(
    [Output('live-weather-map', 'figure'), Output('weather-details', 'children')],
    [Input('interval-component', 'n_intervals'), Input('city-input', 'value')]
)
def update_content(n, selected_city):
    def kelvin_to_celsius_to_fahrenheit(kelvin):
        celsius = kelvin - 273.15
        fahrenheit = celsius * (9/5) + 32
        return celsius, fahrenheit

    url = f"http://api.openweathermap.org/data/2.5/weather?q={selected_city}&appid={API_KEY}"
    response = requests.get(url).json()

    temp_kelvin = response['main']['temp']
    temp_celsius, temp_fahrenheit = kelvin_to_celsius_to_fahrenheit(temp_kelvin)


    fig = go.Figure(go.Scattermapbox(
        lat=[response['coord']['lat']],
        lon=[response['coord']['lon']],
        mode='markers',
        marker=dict(
            size=15,
            color=temp_celsius,
            colorscale='Viridis',
            colorbar=dict(title='Temperature (°C)'),
        ),
        text=[f"{selected_city}: {temp_celsius:.2f} °C"]
    ))

    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=10,
        mapbox_center={"lat": response['coord']['lat'], "lon": response['coord']['lon']},
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )

   
    weather_details = f"Temperature: {temp_celsius:.2f} °C, Humidity: {response['main']['humidity']}%, Wind Speed: {response['wind']['speed']} m/s"

    return fig, weather_details

if __name__ == '__main__':
    app.run_server(debug=True)
