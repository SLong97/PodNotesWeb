import streamlit as st
import requests
from streamlit_player import st_player
import components.authenticate as authenticate

st.set_page_config(page_title="YouTube Transcription", page_icon="▶️")

# Check authentication
authenticate.set_st_state_vars()

# Add login/logout buttons
if st.session_state["authenticated"]:
    st.sidebar.markdown(" ")
    authenticate.button_logout()
else:
    st.sidebar.markdown(" ")
    authenticate.button_login()

st.markdown("# YouTube Transcription")

if(st.session_state["authenticated"]):

    st.write(
        """Effortlessly transform video content into easily digestible text, making it more accessible and convenient to consume. 
        Simply input the link to any YouTube video and its audio will be transcribed and an accurate, concise summary will be generated."""
    )

    st.write("")
    url = st.text_input("**Enter YouTube Video URL**")
    PROCESS_VIDEO_AUDIO_ENDPOINT = "http://0.0.0.0:3000/process_video_audio"

    @st.cache(allow_output_mutation=True, show_spinner=False)
    def predict(url):
        response = requests.post(PROCESS_VIDEO_AUDIO_ENDPOINT, json={"url": url},)
        response = response.json()
        print(response)
        return response
    
    if url != "":

        st_player(url=url)

        with st.spinner("Transcribing Audio..."):
            response = predict(url)
            transcript = response["transcript"]
            diarization = response["diarization"]
            summary = response["summary"]

        st.markdown("### Transcription")

        with st.expander("**Transcript**", expanded=True):
            st.write(transcript)

        st.write("")
        # Get the speaker tag and custom name from the user
        speaker_tag = st.text_input("Enter speaker tag to replace:", "")
        custom_name = st.text_input("Enter replacement name:", "")

        # Add a button to trigger the replacement
        replace_button = st.button("Replace")    

        with st.expander("**Speaker Identification**", expanded=True):
            if "sentences" not in st.session_state:
                st.session_state.sentences = []
                current_sentence = ''

                for character in diarization:
                    current_sentence += character
                    if character in ['.', '?', '!']:
                        st.session_state.sentences.append(current_sentence.strip())
                        current_sentence = ''

            # If the button is clicked and both inputs are not empty, replace the speaker tag with the custom name
            if replace_button and speaker_tag and custom_name:
                st.session_state.sentences = [s.replace(speaker_tag, custom_name) for s in st.session_state.sentences]

            # Display the text with custom speaker names and each sentence on a new line
            for sentence in st.session_state.sentences:
                st.write(sentence)

        st.markdown("### Summarization")

        with st.expander("**Summary**", expanded=True):
                st.write(summary[0]["Summary"])

else:
        
    st.write("Login For Access")