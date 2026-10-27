# UrbanWeathr Monitor 🌤️📊

A real-time urban weather monitoring application built with clean Python architecture, powered by high-precision data from the **Open-Meteo API**, and featuring an interactive, reactive UI built with **Streamlit**.

---

## 🚀 Project Overview

**UrbanWeathr Monitor** is designed to provide a lightweight, modern, and keyless dashboard to track, analyze, and visualize weather conditions and forecasts for urban areas. By leveraging Open-Meteo's open-source API, the application eliminates the need for commercial API keys or registrations, making it ideal for data engineering pipelines, urban climate analysis, or as a foundation for smart-city IoT projects.

---

## ✨ Key Features

* **Real-Time Data & Forecasts:** Instant access to temperature, humidity, wind speed, precipitation, and atmospheric pressure for any urban location.
* **Interactive UI (Streamlit):** Clean, intuitive dashboard featuring city selectors, time filters, and integrated dynamic charts.
* **Open-Meteo Integration:** Optimized REST endpoints for hourly and daily forecasts with no restrictive rate limits or subscription costs.
* **Production-Ready Structure:** Modular code design, robust error handling, and simple configuration.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **Frontend / UI:** Streamlit
* **Data Fetching & API:** `requests` / Open-Meteo REST API
* **Data Processing & Visualization:** Pandas, Plotly / Streamlit native charts

---

## 📦 Repository Structure

TODO: Modificare la struttura

```text
urbanweathr-monitor/
│
├── .streamlit/
│   └── config.toml         # Streamlit theme and settings
├── assets/                 # Images, logos, or dashboard screenshots
├── src/
│   ├── __init__.py
│   ├── api_client.py       # Open-Meteo API HTTP client handling
│   └── utils.py            # Data formatting and helper functions
├── .env.example            # Environment variables template
├── .gitignore
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
└── app.py                  # Main Streamlit application entrypoint
```
