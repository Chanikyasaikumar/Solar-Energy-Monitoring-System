from flask import Flask, render_template, redirect, session, request
import pymysql
import requests
from datetime import datetime, timedelta
import pandas as pd
import pvlib
import pytz
import plotly
import plotly.express as px
from prophet import Prophet
import plotly.graph_objs as go
import numpy as np


conn = pymysql.connect(host=os.environ.get('your-solar-1234.d.render.domains'), user=os.environ.get('root'), password=os.environ.get('Chanikya@123'), db=os.environ.get('solar'))
cursor = conn.cursor()
app = Flask(__name__)
app.secret_key = "solar"
admin_username = "admin"
admin_password = "admin"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/admin_login_action", methods=['POST'])
def admin_login_action():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == admin_username and password == admin_password:
        session['role'] = "admin"
        return redirect("/admin_home")
    else:
        return render_template("message.html", message='Invalid Login Details')


@app.route("/admin_home")
def admin_home():
    return render_template("admin_home.html")


@app.route("/residents")
def residents():
    return render_template("residents.html")


@app.route("/resident_home")
def resident_home():
    return render_template("resident_home.html")


@app.route("/resident_registration")
def resident_registration():
    return render_template("resident_registration.html")


@app.route("/resident_registration_action", methods=['POST'])
def resident_registration_action():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')
    password = request.form.get('password')
    is_producer = request.form.get('is_producer')
    address = request.form.get('address')
    count = cursor.execute("select * from residents where email ='"+str(email)+"' ")
    if count > 0:
        return render_template("message.html", message='Email already registered')
    count = cursor.execute("select * from residents where phone ='" + str(phone) + "' ")
    if count > 0:
        return render_template("message.html", message='Number already registered')
    cursor.execute("insert into residents(name, email, phone, password,is_producer,address) values ('"+str(name)+"','"+str(email)+"','"+str(phone)+"','"+str(password)+"','"+str(is_producer)+"','"+str(address)+"')")
    conn.commit()
    return render_template("message.html", message='Resident Added Successfully')


@app.route("/residents_login_action", methods=['POST'])
def residents_login_action():
    email = request.form.get('email')
    password = request.form.get('password')
    count = cursor.execute("select * from residents where email ='"+str(email)+"' and password = '"+str(password)+"'  ")
    if count > 0:
        residents = cursor.fetchall()
        resident_id = residents[0][0]
        session['role'] = "resident"
        session['resident_id'] = resident_id
        return redirect("/resident_home")
    else:
        return render_template("message.html", message='Invalid Login Details')


@app.route("/solar_power")
def solar_power():
    return render_template("solar_power.html")
#
#
# @app.route("/solar_power_registration_action")
# def solar_power_registration_action():
#     session['resident'] = ['resident_id']
#     city = request.args.get("city")
#     panel_area = request.args.get("panel_area")
#     panel_area = int(panel_area)
#     panel_efficiency = request.args.get("efficiency")
#     panel_efficiency = float(panel_efficiency)
#     temperature_coefficient = request.args.get("temperature_coefficient")
#     temperature_coefficient = float(temperature_coefficient)
#     nominal_temp = request.args.get("nominal_temp")
#     nominal_temp = int(nominal_temp)
#     time_zone = request.args.get("time_zone")
#     latitude = request.args.get("latitude")
#     longitude = request.args.get("longitude")
#     latitude = float(latitude)
#     longitude = float(longitude)
#     data = weather(city)
#     cell_temp = data[3]
#     tz = pytz.timezone(time_zone)
#     today = datetime.now(tz).date()
#
#     ghi_series = get_ghi(city, latitude, longitude, time_zone)
#     times = pd.date_range(today, freq='h', periods=24, tz=time_zone)
#     ghi_series = pd.Series(ghi_series, index=times)
#     power_output = ghi_series * panel_area * panel_efficiency
#     temp_loss = (cell_temp - nominal_temp) * temperature_coefficient
#     power_output_with_temp = power_output * (1 + temp_loss)
#     power_output_kw = power_output_with_temp / 1000
#     output_df = pd.DataFrame({
#         'Time': power_output_kw.index,
#         'Power_Output_kW': power_output_kw.values
#     })
#     peak_power = output_df['Power_Output_kW'].max()
#     peak_power = round(peak_power, 2)
#     peak_time = output_df.loc[output_df['Power_Output_kW'].idxmax(), 'Time']
#     total_energy = output_df['Power_Output_kW'].sum()
#     total_energy2 = round(total_energy, 2)
#     total_energy = f" {round(total_energy, 2)} kWh "
#     avg_power = output_df['Power_Output_kW'].mean()
#     avg_power = round(avg_power, 2)
#     fig = px.line(output_df, x='Time', y='Power_Output_kW', title='Power Output Over Time')
#     fig.update_layout(
#         xaxis=dict(showgrid=False),
#         yaxis=dict(showgrid=False),
#         template='plotly_white'  # optional for a clean background
#     )
#     alert_message = ""
#     if data[4] == 0:
#         alert_message += "No, Cloud Cover today."
#     if data[4] > 80:
#         alert_message += "High cloud cover — significant drop in solar output expected."
#     elif 50 < data[4] <= 80:
#         alert_message += "Moderate cloud cover — slight reduction in solar efficiency."
#     else:
#         alert_message += "Low cloud cover — good conditions for solar generation."
#
#     plotly.offline.plot(fig, filename='static/html/power_hourly.html', auto_open=False)
#
#     cursor.execute("delete from residence_energy where resident_id ='"+str(session['resident_id'])+"' ")
#     conn.commit()
#
#     cursor.execute("insert into residence_energy(total_energy_produced,resident_id) values('"+str(total_energy2)+"','"+str(session['resident_id'])+"')")
#     conn.commit()
#     return render_template("solar_power_registration_action.html", alert_message=alert_message, data=data, total_energy=total_energy, avg_power=avg_power, output_df=output_df, city=city, temperature_coefficient=temperature_coefficient, time_zone=time_zone, peak_power=peak_power, peak_time=peak_time)


@app.route("/solar_power_registration_action")
def solar_power_registration_action():
    session['resident'] = ['resident_id']
    city = request.args.get("city")
    panel_area = int(request.args.get("panel_area"))
    panel_efficiency = float(request.args.get("efficiency"))
    temperature_coefficient = float(request.args.get("temperature_coefficient"))
    nominal_temp = int(request.args.get("nominal_temp"))
    time_zone = request.args.get("time_zone")
    latitude = float(request.args.get("latitude"))
    longitude = float(request.args.get("longitude"))

    # Call both weather functions
    weather_data = weather(city)
    sunrise, sunset = weather2(city)

    # Extract needed values
    cell_temp = weather_data[3]
    cloud_cover = weather_data[4]

    # Combine into one data dictionary for template
    data = {
        'location': weather_data[0],
        'timezone': weather_data[1],
        'local_time': weather_data[2],
        'temp_celsius': cell_temp,
        'cloud_cover': cloud_cover,
        'sunrise': sunrise,
        'sunset': sunset
    }

    tz = pytz.timezone(time_zone)
    today = datetime.now(tz).date()

    ghi_series = get_ghi(city, latitude, longitude, time_zone)
    times = pd.date_range(today, freq='h', periods=24, tz=time_zone)
    ghi_series = pd.Series(ghi_series, index=times)

    power_output = ghi_series * panel_area * panel_efficiency
    temp_loss = (cell_temp - nominal_temp) * temperature_coefficient
    power_output_with_temp = power_output * (1 + temp_loss)
    power_output_kw = power_output_with_temp / 1000

    output_df = pd.DataFrame({
        'Time': power_output_kw.index,
        'Power_Output_kW': power_output_kw.values
    })

    peak_power = round(output_df['Power_Output_kW'].max(), 2)
    peak_time = output_df.loc[output_df['Power_Output_kW'].idxmax(), 'Time']
    total_energy2 = round(output_df['Power_Output_kW'].sum(), 2)
    total_energy = f"{total_energy2} kWh"
    avg_power = round(output_df['Power_Output_kW'].mean(), 2)

    fig = px.line(output_df, x='Time', y='Power_Output_kW', title='Power Output Over Time')
    fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False), template='plotly_white')
    plotly.offline.plot(fig, filename='static/html/power_hourly.html', auto_open=False)

    # Alert message logic
    alert_message = ""
    if cloud_cover == 0:
        alert_message += "No, Cloud Cover today."
    elif cloud_cover > 80:
        alert_message += "High cloud cover — significant drop in solar output expected."
    elif 50 < cloud_cover <= 80:
        alert_message += "Moderate cloud cover — slight reduction in solar efficiency."
    else:
        alert_message += "Low cloud cover — good conditions for solar generation."

    cursor.execute("DELETE FROM residence_energy WHERE resident_id = %s", (session['resident_id'],))
    conn.commit()
    cursor.execute("INSERT INTO residence_energy(total_energy_produced, resident_id) VALUES (%s, %s)",
                   (total_energy2, session['resident_id']))
    conn.commit()

    return render_template(
        "solar_power_registration_action.html",
        alert_message=alert_message,
        data=weather_data,
        total_energy=total_energy,
        avg_power=avg_power,
        output_df=output_df,
        city=city,
        temperature_coefficient=temperature_coefficient,
        time_zone=time_zone,
        peak_power=peak_power,
        peak_time=peak_time,
        sunrise=sunrise,
        sunset=sunset
    )


def weather(city):
    url = f'http://api.weatherapi.com/v1/current.json?key=6bab20eb12f642769cf184204252204&q={city}'
    response = requests.get(url)
    data = response.json()


    if data:
        location = data['location']['name']
        timezone = data['location']['tz_id']
        local_time = data['location']['localtime']
        temp_celsius = data['current']['temp_c']
        cloud_cover = data['current']['cloud']
        return location, timezone, local_time, temp_celsius, cloud_cover
    else:
        print('No data')
        return None


def weather2(city):
    url = f"http://api.weatherapi.com/v1/forecast.json?key=6bab20eb12f642769cf184204252204&q={city}&days=1"
    response = requests.get(url)
    data = response.json()

    astro = data['forecast']['forecastday'][0]['astro']
    sunrise = astro['sunrise']
    sunset = astro['sunset']
    return sunrise, sunset



def get_ghi(city_name, latitude, longitude, timezone):
    tz = pytz.timezone(timezone)
    today = datetime.now(tz).date()
    times = pd.date_range(today, freq='h', periods=24, tz=timezone)
    location = pvlib.location.Location(latitude, longitude, tz=timezone)
    clearsky = location.get_clearsky(times)
    ghi_df = pd.DataFrame({
        'Time': clearsky.index,
        'GHI': clearsky['ghi'].values
    })
    ghi_df.reset_index(drop=True, inplace=True)
    ghi_series = ghi_df['GHI'].values
    return ghi_series


@app.route("/home_appliances")
def home_appliances():
    count = cursor.execute("select * from appliances")
    conn.commit()
    appliances = cursor.fetchall()
    appliance_level_consumption = 0
    for appliance in appliances:
        appliance_level_consumption = appliance_level_consumption + float(appliance[4])
    appliance_level_consumption = appliance_level_consumption/1000
    resident_id = session['resident_id']
    cursor.execute("select * from residence_energy where resident_id='"+str(resident_id)+"'")
    residence_energies = cursor.fetchall()
    status = None
    grid_import = None
    carbon_emission_from_grid = None
    net_carbon_emission = None
    if len(residence_energies) == 0:
        residence_energy = None
    else:
        residence_energy = float(residence_energies[0][1])
        if appliance_level_consumption > residence_energy:
            status = "Grid Import"
            grid_import = appliance_level_consumption - residence_energy
            carbon_emission_saved = residence_energy * 0.42
            carbon_emission_from_grid = grid_import * 0.42
            net_carbon_emission = carbon_emission_saved - carbon_emission_from_grid
        else:
            status = "Grid Export"
            carbon_emission_saved = residence_energy * 0.42
            carbon_emission_saved = round(carbon_emission_saved, 2)
    reward_points = int(carbon_emission_saved*10)
    return render_template("home_appliances.html", appliances=appliances, int=int, residence_energy=residence_energy, round=round, reward_points=reward_points,
                           status=status, grid_import=grid_import, carbon_emission_saved=carbon_emission_saved, carbon_emission_from_grid=carbon_emission_from_grid, net_carbon_emission=net_carbon_emission)


@app.route("/add_appliances")
def add_appliances():
    appliances = pd.read_csv('static/csv/appliance_watts.csv')
    print(appliances.columns.values)
    for appliance in appliances.values:
        print(appliance)
    print(appliances.head())
    appliances.head()
    return render_template("add_appliances.html", appliances=appliances)


@app.route("/add_appliance_action")
def add_appliance_action():
    session['resident'] = ['resident_id']
    appliance = request.args.get('appliances')
    wattage = request.args.get('wattage')
    hrs_per_day = request.args.get('hrs_per_day')
    total = int(float(wattage))*int(hrs_per_day)
    cursor.execute("insert into appliances(appliances,wattage,Hours_Per_Day,total,resident_id) values('"+str(appliance)+"','"+str(wattage)+"','"+str(hrs_per_day)+"','"+str(total)+"','"+str(session['resident_id'])+"')")
    conn.commit()
    return redirect("home_appliances")


@app.route("/bill")
def bill():
    watts = request.args.get('watts')
    reward_points = request.args.get('reward_points')
    electricity_costs = pd.read_csv('static/csv/electricity_cost.csv')
    for electricity_cost in electricity_costs.values:
        print(electricity_cost)

    return render_template("bill.html", electricity_costs=electricity_costs, watts=watts, reward_points=reward_points)


@app.route("/get_prices")
def get_prices():
    region = request.args.get("region")
    electricity_costs = pd.read_csv('static/csv/electricity_cost.csv')
    for electricity_cost in electricity_costs.values:
        if electricity_cost[0] == region:
            return {"residential": electricity_cost[1], "commercial": electricity_cost[2]}


@app.route("/subscriptions")
def subscriptions():
    if session['role'] == 'resident':
        resident_id = session['resident_id']
        count = cursor.execute("select * from subscriptions where resident_id = '"+str(resident_id)+"' ")
        if count > 0:
            subscriptions = cursor.fetchall()
            return render_template("active_subscription.html", subscription=subscriptions[0])
    return render_template("subscriptions.html")


@app.route("/subscribers")
def subscribers():
    cursor.execute("select * from subscriptions")
    subscribers = cursor.fetchall()
    return render_template("subscribers.html", subscribers=subscribers)


@app.route("/subscribe_package")
def subscribe_package():
    package_title = request.args.get('package_title')
    return render_template("subscribe_package.html", package_title=package_title)


@app.route("/add_subscription_action")
def add_subscription_action():
    session['resident'] = ['resident_id']
    package_title = request.args.get('package_title')
    street_name = request.args.get('street_name')
    apartment_name = request.args.get('apartment_name')
    zip_code = request.args.get('zip_code')
    contact = request.args.get('contact')
    purchase_date = datetime.now().date()
    plan_expire_date = purchase_date + timedelta(days=30)
    card_number = request.args.get('card_number')
    holder_name = request.args.get('holder_name')
    expire_date = request.args.get('expire_date')
    cvv = request.args.get('cvv')
    cursor.execute("insert into subscriptions(package_title,street_name,appartment_name,zip_code,contact,card_number,name,expire_date,cvv,purchase_date,plan_expire_date,resident_id)"
                   " values('"+str(package_title)+"','"+str(street_name)+"','"+str(apartment_name)+"','"+str(zip_code)+"','"+str(contact)+"','"+str(card_number)+"','"+str(holder_name)+"','"+str(expire_date)+"','"+str(cvv)+"','"+str(purchase_date)+"','"+str(plan_expire_date)+"','"+str(session['resident_id'])+"')")
    conn.commit()
    return render_template("subscribe_package.html", message="Payment Successful")


@app.route("/appliances_graph")
def appliances_graph():
    data = pd.read_csv('static/csv/household_data_60min_singleindex.csv')
    residential_cols = [col for col in data.columns if 'residential' in col.lower()]
    residential_consumption_cols = [col for col in residential_cols if 'pv' not in col.lower()]
    # Filter appliance columns
    appliance_keywords = ['dishwasher', 'freezer', 'refrigerator', 'washing_machine', 'heat_pump', 'circulation_pump']
    appliance_cols = [col for col in data.columns if
                      'residential' in col and any(key in col for key in appliance_keywords)]

    # energy usage per column
    appliance_usage = data[appliance_cols].sum().reset_index()
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
    return render_template("appliances_graph.html")


@app.route("/forecast_graph")
def forecast_graph():
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

    plotly.offline.plot(fig, filename='static/html/forecast.html', auto_open=False)
    return render_template("forecast_graph.html")


@app.route("/generation_graph")
def generation_graph():
    final_data = pd.read_csv('static/csv/renewable_final.csv')
    final_data['utc_timestamp'] = pd.to_datetime(final_data['utc_timestamp'])
    final_data = final_data.set_index('utc_timestamp')
    pv_columns = [col for col in final_data.columns if 'pv' in col.lower()]
    pv_data = final_data[pv_columns]
    pv_melted = pv_data.reset_index().melt(id_vars='utc_timestamp',
                                           value_vars=pv_columns,
                                           var_name='PV_Source',
                                           value_name='Power_Output')
    fig = px.line(pv_melted,
                  x='utc_timestamp',
                  y='Power_Output',
                  color='PV_Source',
                  title='Interactive PV Generation Over Time')

    fig.update_layout(xaxis_title='Time',
                      yaxis_title='Power Output (kW or MW)',
                      legend_title='PV Source')
    plotly.offline.plot(fig, filename='static/html/generation.html', auto_open=False)
    return render_template("generation_graph.html")


@app.route("/graph")
def graph():
    service = request.args.get('service')
    if service == "forecast_graph":
        return render_template("forecast_graph.html", service=service)
    elif service == "generation_graph":
        return render_template("generation_graph.html", service=service)
    elif service == "appliances_graph":
        return render_template("appliances_graph.html", service=service)
    else:
        return render_template("admin_home.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


app.run(debug=True)
