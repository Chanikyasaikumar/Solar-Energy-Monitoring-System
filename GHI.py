import pandas as pd
import pvlib
from datetime import datetime
import pytz
import plotly
import plotly.express as px


timezone = 'America/New_York'
city_name = 'New York'
latitude = 40.7128
longitude = -74.0060
tz = pytz.timezone(timezone)
today = datetime.now(tz).date()


def get_ghi(city_name,latitude,longitude,timezone):
    tz = pytz.timezone(timezone)
    today = datetime.now(tz).date()
    times = pd.date_range(today, freq='h', periods=24, tz=timezone)
    print(times)
    location = pvlib.location.Location(latitude, longitude, tz=timezone)
    clearsky = location.get_clearsky(times)
    ghi_df = pd.DataFrame({
        'Time': clearsky.index,
        'GHI': clearsky['ghi'].values
    })
    ghi_df.reset_index(drop=True, inplace=True)
    ghi_series=ghi_df['GHI'].values
    return ghi_series


print(get_ghi('New York',40.7128,-74.0060,'America/New_York'))


panel_area = 2
panel_efficiency = 0.18
temperature_coefficient = -0.003
nominal_temp = 25
cell_temp = 40
ghi_series=get_ghi('New York',40.7128,-74.0060,'America/New_York')
times = pd.date_range(today, freq='h', periods=24, tz=timezone)
ghi_series = pd.Series(ghi_series, index=times)
power_output = ghi_series * panel_area * panel_efficiency
temp_loss = (cell_temp - nominal_temp) * temperature_coefficient
power_output_with_temp = power_output * (1 + temp_loss)
power_output_kw = power_output_with_temp / 1000
print('power ouput')
print(type(power_output_kw))
output_df = pd.DataFrame({
    'Time': power_output_kw.index,
    'Power_Output_kW': power_output_kw.values
})
fig = px.line(output_df, x='Time', y='Power_Output_kW', title='Power Output Over Time')
fig.update_layout(
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=False),
    template='plotly_white'  # optional for a clean background
)
fig.show()
plotly.offline.plot(fig, filename='power_hourly.html')
