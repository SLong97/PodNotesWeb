import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
import components.authenticate as authenticate

st.set_page_config(page_title="Podcast Transcription", page_icon="🎙️")

# Check authentication
authenticate.set_st_state_vars()

# Add login/logout buttons
if st.session_state["authenticated"]:
    st.sidebar.markdown(" ")
    authenticate.button_logout()
else:
    st.sidebar.markdown(" ")
    authenticate.button_login()

st.markdown("# Podcast Transcription")
#st.sidebar.header("Mapping Demo")

if(st.session_state["authenticated"]):

    st.write(
        """Provide a link to the desired podcast episode and have it transcribed in its entirety while also creating a succinct, accurate summary of it. 
         Enabling you to absorb key information from your favorite podcasts with ease and efficiency."""
    )

    

else:
        
    st.write("Login For Access")