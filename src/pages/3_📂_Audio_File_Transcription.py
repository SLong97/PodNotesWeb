import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError
import components.authenticate as authenticate

st.set_page_config(page_title="Audio File Transcription", page_icon="📂")

# Check authentication
authenticate.set_st_state_vars()

# Add login/logout buttons
if st.session_state["authenticated"]:
    st.sidebar.markdown(" ")
    authenticate.button_logout()
else:
    st.sidebar.markdown(" ")
    authenticate.button_login()

st.markdown("# Audio File Transcription")
#st.sidebar.header("DataFrame Demo")

if(st.session_state["authenticated"]):

    st.write(
        """Upload your audio files and recieve precise transcriptions accompanied by concise summaries. 
        Facilitating the transformation of lectures, interviews, or any audio content into easily digestible text, making it more accessible and comprehensible."""
    )

    

else:
        
    st.write("Login For Access")