import streamlit as st
import components.authenticate as authenticate

st.set_page_config(
    page_title="Home",
)

st.write("# Welcome to PodNotes")

st.markdown(
"""

    PodNotes, your all-in-one solution for **transcription**, **speaker identification**, and **summarization**. 
    
    Our platform effortlessly handles **YouTube Videos**, **Podcast Links**, and **Uploaded Audio Files**, delivering accurate transcriptions and speaker labeling.

    PodNotes also generates concise summaries, perfect for grasping key points without listening to the entire audio. 
    Get started by providing a link or uploading an audio file, and let our platform do the work for you. 
    Experience the future of audio content management with PodNotes - the efficient, user-friendly choice.

"""
)

# Check authentication when user lands on the home page.
authenticate.set_st_state_vars()

# Add login/logout buttons
if st.session_state["authenticated"]:
    st.sidebar.markdown(" ")
    authenticate.button_logout()
else:
    st.sidebar.markdown(" ")
    authenticate.button_login()