import pandas as pd
import plotly
import plotly.express as px
final_data=pd.read_csv('static/csv/renewable_final.csv')
final_data['utc_timestamp'] = pd.to_datetime(final_data['utc_timestamp'])
final_data = final_data.set_index('utc_timestamp')
# Filter PV columns
pv_columns = [col for col in final_data.columns if 'pv' in col.lower()]
pv_data = final_data[pv_columns]
# Melt the data for plotly.express
pv_melted = pv_data.reset_index().melt(id_vars='utc_timestamp',
                                       value_vars=pv_columns,
                                       var_name='PV_Source',
                                       value_name='Power_Output')
# Create interactive line plot
fig = px.line(pv_melted,
              x='utc_timestamp',
              y='Power_Output',
              color='PV_Source',
              title='Interactive PV Generation Over Time')

fig.update_layout(xaxis_title='Time',
                  yaxis_title='Power Output (kW or MW)',
                  legend_title='PV Source')
fig.show()
# fig.write_image("generation.png")
plotly.offline.plot(fig, filename='generation.html')
