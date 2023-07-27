# RaspberryPi Dashboard

This program is a web-based dashboard designed to display and analyze temperature and humidity data collected from different sources: an inside Raspberry Pi sensor (Data_raspberry3), an ESP8266 sensor (Data_ESP8266), and an external weather data source (Data). The dashboard provides a visual representation of the collected data using interactive plots.

## Features
Display temperature and humidity data from Raspberry Pi and ESP8266 sensors.
Show external temperature and humidity data from an external weather data source.
Interactive Date Picker Range: Allows users to select a specific date range to visualize data.
Automatic Data Refresh: The dashboard automatically updates data and plots every hour using an interval component.
Requirements

The following Python libraries are required to run the dashboard:

- dash
- dash_bootstrap_components
- sqlalchemy
- plotly
- pandas
- astral
- pytz

To install the required libraries, use the following command:


```pip install requirements.txt ```

## Usage
- Ensure that the necessary Python libraries are installed.
- Modify the url_inside and url_outside variables in the code to connect to your respective database instances. Replace the placeholders with the actual connection URLs.
- Run the program by executing the Python script.
- The dashboard will be accessible in your web browser at http://0.0.0.0:8050/. The dashboard will display temperature and humidity data for the current day. Users can interact with the Date Picker Range to visualize data for specific date ranges.

## Data Sources
- Inside Raspberry Pi Sensor (Data_raspberry3): This data source collects temperature and humidity data from a sensor connected to the Raspberry Pi.
- ESP8266 Sensor (Data_ESP8266): This data source collects temperature and humidity data from an ESP8266 sensor.
- External Weather Data (Data): This data source provides temperature and humidity data from an external weather station.
- Data Visualization
The dashboard displays the following plots:

1. Temperature and Humidity Comparison
- This plot compares the temperature and humidity data from the inside Raspberry Pi sensor (Data_raspberry3) and the ESP8266 sensor (Data_ESP8266) on the same graph.
- The temperature and humidity data from the outside weather station (Data) are also included but initially hidden from the legend.
2. Temperature Inside vs. Temperature Outside
- This plot shows the temperature data from the inside Raspberry Pi sensor (Data_raspberry3) and the outside weather station (Data).
3. Humidity Inside vs. Humidity Outside
- This plot displays the humidity data from the inside Raspberry Pi sensor (Data_raspberry3) and the outside weather station (Data).
4. Sunrise and Sunset Times
- This section displays the current date, sunrise time, and sunset time for Budapest. The sunrise and sunset times are determined using the astral library.
5. Automatic Data Refresh
- The dashboard automatically refreshes the data and plots every hour using an interval component. This ensures that the displayed information is up-to-date with the latest data.

Please note that the data sources should be regularly updated to have relevant information in the database.

## Customization
Feel free to modify the dashboard layout, styling, or add additional functionalities based on your specific requirements. The Dash framework and Plotly library provide extensive customization options to create a personalized and visually appealing dashboard.

## Note
This dashboard is intended for educational and demonstration purposes and may require additional security measures if deployed in a production environment. Always ensure proper access controls and data security when working with sensitive data sources.

Happy dashboarding!
