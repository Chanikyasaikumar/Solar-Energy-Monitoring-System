import pandas as pd
import plotly
import plotly.express as px


data = pd.read_csv('static/csv/household_data_60min_singleindex.csv')
residential_cols=[col for col in data.columns if 'residential' in col.lower() ]
residential_consumption_cols = [col for col in residential_cols if 'pv' not in col.lower()]
# Filter appliance columns
appliance_keywords = ['dishwasher', 'freezer', 'refrigerator', 'washing_machine', 'heat_pump', 'circulation_pump']
appliance_cols = [col for col in data.columns if 'residential' in col and any(key in col for key in appliance_keywords)]

# energy usage per column
appliance_usage = data[appliance_cols].sum().reset_index()
print(appliance_usage)

appliance_usage.columns = ['appliance', 'total_energy']

# appliance labels
appliance_usage['appliance_type'] = appliance_usage['appliance'].apply(lambda x: x.split('_')[-1])
appliance_usage['residence'] = appliance_usage['appliance'].apply(lambda x: '_'.join(x.split('_')[2:3]))
appliance_usage


# Sort by total energy
appliance_usage = appliance_usage.sort_values(by='total_energy', ascending=False)

fig = px.bar(
    appliance_usage,
    x='appliance',
    y='total_energy',
    color='appliance_type',
    title='Total Appliance-Wise Energy Consumption (All Residences) - Sorted',
    labels={'total_energy': 'Energy (kWh)', 'appliance': 'Appliance (Household)'},
    height=600
)

fig.update_layout(xaxis_tickangle=-45)
plotly.offline.plot(fig, filename='static/html/appliances_graph2.html', auto_open=False)


