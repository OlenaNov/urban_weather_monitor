
# USEFUL APIs:
# https://api.open-meteo.com/v1/forecast

# current: temperatura, vento
# hourly: temperatura, vento
# daily: temperatura_max, temperatura_min, somma precipitazioni

import requests
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# !!!TODO
# Export in Client folder
import streamlit as st


FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

FORECAST_DAYS = 7
FIG_SIZE = (6, 4)

# !!!TODO
# Export in Client folder
st.set_page_config(page_title="CityClime Analytics", page_icon="🌦️", layout="wide")
citta_scelta = None


# st.title(f"Previsioni Meteo: {citta_scelta['name']}" if citta_scelta else "Previsioni Meteo ☀️")


#     st.title("Previsioni Meteo ☀️")
#     st.write("Seleziona una città dalla barra laterale")

with st.sidebar:
    st.title("🔍 Ricerca")
    citta = st.text_input("Città", placeholder="Es. Milano, Roma, Napoli ecc...").strip()
    giorni = st.slider("Giorni di previsione", min_value=3, max_value=14, value=FORECAST_DAYS)

    
    # 1. From city name to (latitude, longitude)

    if citta:
        params_geo = {
        "name": citta,
        "count": 5,
        "countryCode": "it",   # or "language"
        }
        response_geo = requests.get(GEOCODING_URL, params=params_geo)
        data_geo = response_geo.json()
        citta_scelta = st.selectbox("Risultati", options=data_geo["results"], format_func=lambda result: f"{result["name"]}, {result["admin1"]}, {result["country_code"]}")

        # 2. From (latitude, longitude) to meteo info
        if citta_scelta:
            params_forecast = {
                "latitude": citta_scelta["latitude"],
                "longitude": citta_scelta["longitude"],
                "forecast_days": giorni,
                "current": ["temperature_2m", "wind_speed_10m"],
                "hourly": ["temperature_2m", "wind_speed_10m"],
                "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum"]
            }
            response_forecast = requests.get(FORECAST_URL, params=params_forecast)
            data_forecast = response_forecast.json()


            # 3. Data Frame
            df_hourly = pd.DataFrame(data_forecast["hourly"])
            df_hourly["time"] = pd.to_datetime(df_hourly["time"])

            df_daily = pd.DataFrame(data_forecast["daily"])
            df_daily["time"] = pd.to_datetime(df_daily["time"])

            times, temps, wind_speeds = df_hourly["time"], df_hourly["temperature_2m"], df_hourly["wind_speed_10m"]
            times_daily, precipitation_sums = df_daily["time"], df_daily["precipitation_sum"]



if citta_scelta:
    st.title(f"{citta_scelta["name"]}")
    st.write(f"""{citta_scelta["admin1"]}, {citta_scelta["country_code"]}. Aggiornamento {
        pd.to_datetime(data_forecast["current"]["time"])
    }""")
    # TODO
# Per aggiungere informazioni su temperatura attuale, max e min, vento e precipitazioni, creare 4 colonne con st.columns(4)
# e in ciascuna st.metric(label="Temperatura Attuale", value="22.5 °C", delta="+1.2 °C")

    p1, p2 = st.columns(2)
    with p1:
        # 4. Plot
        # 4a. Andamento orario della temoperatura
        fig1, ax1 = plt.subplots(figsize=FIG_SIZE)
        ax1.plot(times, temps, color="tab:red", linewidth=1)
        ax1.fill_between(times, temps, color="tab:red", alpha=0.2)
        ax1.set_title("Andamento Orario Temperatura", fontweight="bold")
        ax1.set_ylabel("Temperatura (C)")
        ax1.grid(linestyle=":", alpha=0.5)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b"))
        st.pyplot(fig1)
        # plt.show()

        # 4b. Andamento orario della velocità vento (CORRETTO)
        fig2, ax2 = plt.subplots(figsize=FIG_SIZE)
        ax2.plot(times, wind_speeds, color="tab:green", linewidth=1)
        ax2.fill_between(times, wind_speeds, color="tab:green", alpha=0.2)
        ax2.set_title("Andamento Orario Velocità Vento", fontweight="bold")
        ax2.set_ylabel("Velocità (km/h)")
        ax2.grid(linestyle=":", alpha=0.5)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b"))
        st.pyplot(fig2)
        # plt.show()

    with p2:
        # 4c. Temperature massime e minime giornaliere
        fig3, ax3 = plt.subplots(figsize=FIG_SIZE)
        col_width = 0.4
        x = np.arange(giorni) #[0,1,2,3,4,5,6]
        ax3.bar(x - col_width / 2, df_daily["temperature_2m_max"], width=col_width, color="tab:orange", label="Temp. Massima")
        ax3.bar(x + col_width / 2, df_daily["temperature_2m_min"], width=col_width, color="tab:blue", label="Temp. Minima")
        ax3.set_title("Temperature Massime e Minime Giornagliere", fontweight="bold")
        ax3.set_ylabel("Temperatura (C°)")
        ax3.grid(axis="y", linestyle=":", alpha=0.5)
        ax3.set_axisbelow(True)
        # to change tick lables
        ax3.set_xticks(x)
        ax3.set_xticklabels(times_daily.dt.strftime("%d-%b"))
        ax3.legend()
        # plt.show()
        st.pyplot(fig3)


        # 4d. Precipitazioni giornagliere
        fig4, ax4 = plt.subplots(figsize=FIG_SIZE)
        ax4.bar(times_daily, precipitation_sums, width=0.6, color="tab:blue")
        ax4.set_title("Precipitazioni Giornaliere", fontweight="bold")
        ax4.set_ylabel("Precipitazioni (mm)")
        ax4.grid(axis="y", linestyle=":", alpha=0.5)
        ax4.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b"))
        # plt.show()
        st.pyplot(fig4)

else:
    st.title("Previsioni Meteo ☀️")
    st.write("Seleziona una città dalla barra laterale")