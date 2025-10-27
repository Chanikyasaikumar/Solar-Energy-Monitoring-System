import pandas as pd
import numpy as np
from prophet import Prophet
import plotly.graph_objs as go
import plotly
df = pd.read_csv('static/csv/renewable_final.csv')
df['utc_timestamp'] = pd.to_datetime(df['utc_timestamp']).dt.tz_localize(None)

# base
df_prophet = df[['utc_timestamp', 'DE_KN_residential1_pv',
                 'DE_temperature',
                 'DE_radiation_direct_horizontal',
                 'DE_radiation_diffuse_horizontal']].copy()

df_prophet.rename(columns={
    'utc_timestamp': 'ds',
    'DE_KN_residential1_pv': 'y'
}, inplace=True)



# add regressors
m = Prophet()
m.add_regressor('DE_temperature')
m.add_regressor('DE_radiation_direct_horizontal')
m.add_regressor('DE_radiation_diffuse_horizontal')

# Fit model
m.fit(df_prophet)

# Future dataframe
future = m.make_future_dataframe(periods=48, freq='H')

# future weather values
future['DE_temperature'] = np.random.uniform(10, 35, len(future))
future['DE_radiation_direct_horizontal'] = np.random.uniform(0, 1000, len(future))
future['DE_radiation_diffuse_horizontal'] = np.random.uniform(0, 300, len(future))

# Forecast
forecast = m.predict(future)
forecast_only = forecast[forecast['ds'] > df_prophet['ds'].max()]

fig = go.Figure()

# Forecast line
fig.add_trace(go.Scatter(
    x=forecast_only['ds'],
    y=forecast_only['yhat'],
    mode='lines',
    name='Forecast PV',
    line=dict(color='orange')
))

# Uncertainty interval
fig.add_trace(go.Scatter(
    x=forecast_only['ds'],
    y=forecast_only['yhat_upper'],
    mode='lines',
    line=dict(width=0),
    showlegend=False
))
fig.add_trace(go.Scatter(
    x=forecast_only['ds'],
    y=forecast_only['yhat_lower'],
    mode='lines',
    fill='tonexty',
    fillcolor='rgba(255,165,0,0.2)',
    line=dict(width=0),
    name='Lower Bound'
))

fig.update_layout(
    title='48-Hour PV Forecast (Weather-Aware)',
    xaxis_title='Time',
    yaxis_title='PV Generation (kW)',
    template='plotly_white',
    hovermode='x unified',
    xaxis=dict(
        tickformat="%Y-%m-%d %H:%M",
        tickangle=45
    )
)

fig.show()
plotly.offline.plot(fig, filename='forecast.html')
