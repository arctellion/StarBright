import streamlit as st
import math as m

st.title('Traveller Travel Time Calculator')
with st.form("travel_time_form"):
    st.write("Enter the number of Diameters from planet (default: 100):")
    a_dia = st.number_input("Departure / Arrival Diameters", min_value=0, step=1, value=100)
    
    st.write("Enter the diameter of the planet in  km:")
    p_dia = st.number_input("Planet Diameter (km)", min_value=1000, step=1, value=5000)

    st.write("Enter the Speed in G of the ship:")
    s_spd = st.number_input("Speed of Ship", min_value=1, step=1, value=1, max_value=9)
    
    submitted = st.form_submit_button("Calculate")
    
    if submitted:
        time = m.sqrt( (a_dia * p_dia) / (s_spd * 32400))
        hr = int(time)
        min = int((time - hr) * 60)
        st.write(f"Estimated travel time: {hr} hours and {min} minutes")