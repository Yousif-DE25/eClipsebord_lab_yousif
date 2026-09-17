
import httpx
import pandas as pd
import streamlit as st
import os

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="eClipseBord", page_icon="🌘", layout="wide")
st.title("eClipseBord")

tab_next, tab_history = st.tabs(["Nästa förmörkelse", "Utforska historik"])

# - Sida 1: Nästa förmörkelse -
with tab_next:
    st.subheader("Nästa solförmörkelse")
    try:
        response = httpx.get(f"{BACKEND_URL}/eclipses/next", timeout=5)
        response.raise_for_status()
        data = response.json()
    except httpx.HTTPError as e:
        st.error(f"Kunde inte nå backend: {e}")
        data = None

    if data and "date" in data:
        col1, col2, col3 = st.columns(3)
        col1.metric("Datum", data["date"])
        col2.metric("Typ", data["type"])
        col3.metric("Magnitud", data["magnitude"])

        st.write(f"**Tid:** {data['time']}")
        st.write(f"**Position:** {data['latitude']}, {data['longitude']}")
        if data.get("path_width_km"):
            st.write(f"**Bredd på skuggbana:** {data['path_width_km']} km")
    elif data:
        st.info(data.get("message", "Ingen data tillgänglig."))

    st.divider()
    st.subheader("lite om månförmörkelser")
    try:
        lunar_response = httpx.get(f"{BACKEND_URL}/eclipses/lunar/summary", timeout=5)
        lunar_response.raise_for_status()
        lunar_data = lunar_response.json()

        st.write(f"Totalt antal månförmörkelser i datasetet: **{lunar_data['total_count']}**")

        if lunar_data.get("next_lunar_eclipse"):
            nxt = lunar_data["next_lunar_eclipse"]
            st.write(f"Näst kommande månförmörkelse: **{nxt['date']}** ({nxt['type']})")

        st.bar_chart(pd.Series(lunar_data["type_counts"], name="Antal"))
    except httpx.HTTPError as e:
        st.error(f"Kunde inte hämta månförmörkelsedata: {e}")

# - Sida 2: Utforska historik -
with tab_history:
    st.subheader("Filtrera historiska solförmörkelser")

    col1, col2 = st.columns(2)
    with col1:
        eclipse_type = st.selectbox(
            "Typ",
            options=[None, "T", "A", "P", "H"],
            format_func=lambda x: "Alla" if x is None else x,
        )
    with col2:
        year_min, year_max = st.slider(
            "Årsintervall",
            min_value=-1999,
            max_value=3000,
            value=(2000, 2050),
        )

    params = {"year_min": year_min, "year_max": year_max, "limit": 500}
    if eclipse_type:
        params["type"] = eclipse_type

    try:
        response = httpx.get(f"{BACKEND_URL}/eclipses", params=params, timeout=5)
        response.raise_for_status()
        eclipses_data = response.json()
    except httpx.HTTPError as e:
        st.error(f"Kunde inte hämta data: {e}")
        eclipses_data = []

    st.write(f"Hittade **{len(eclipses_data)}** förmörkelser")
    if eclipses_data:
        st.dataframe(pd.DataFrame(eclipses_data), use_container_width=True)
