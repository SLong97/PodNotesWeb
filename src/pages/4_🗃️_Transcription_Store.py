import streamlit as st
import requests
from streamlit_player import st_player
import components.authenticate as authenticate
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Frame, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_LEFT
import io
from docx import Document
import os
import boto3
from dotenv import load_dotenv
import re
import pandas as pd
from awesome_table import AwesomeTable
from awesome_table.column import Column
from awesome_table.column import (Column, ColumnDType)
from streamlit_quill import st_quill
from io import StringIO

st.set_page_config(page_title="Transcription Store", page_icon="🗃️", layout='wide')

# Check authentication
authenticate.set_st_state_vars()

# Add login/logout buttons
if st.session_state["authenticated"]:
    st.sidebar.markdown(" ")
    authenticate.button_logout()
else:
    st.sidebar.markdown(" ")
    authenticate.button_login()

st.write('<style> .css-1fcdlhc.e1s6o5jp0 {width: 900px !important;} </style>', unsafe_allow_html=True)

st.markdown("# Transcription Store")

st.write(
    """Access saved Transcripts and Summaries for editing and downloading."""
)

if(st.session_state["authenticated"]):

    load_dotenv()
    S3_BUCKET = os.getenv("S3_BUCKET")
    BUCKET_REGION = os.getenv("BUCKET_REGION")

    s3_client = boto3.client('s3', region_name=BUCKET_REGION)
    cognito_client = boto3.client('cognito-identity', region_name=os.getenv("COGNITO_REGION"))

    def get_cognito_identity(jwt_token):
        response = cognito_client.get_id(
            IdentityPoolId=os.getenv("COGNITO_IDENTITY_POOL_ID"),
            Logins={
                os.getenv("COGNITO_IDENTITY_PROVIDER"): jwt_token
            }
        )
        return response["IdentityId"]
    
    def list_user_objects(user_identity):
        prefix = f"{user_identity}/"
        response = s3_client.list_objects_v2(
            Bucket=S3_BUCKET,
            Prefix=prefix
        )

        files = []
        if 'Contents' in response:
            for obj in response['Contents']:
                files.append(obj['Key'])

        return files
    
    def get_object_text(bucket, key):
        response = s3_client.get_object(
            Bucket=bucket,
            Key=key
        )
        content = response['Body'].read().decode('utf-8')

        return content

    def generate_presigned_url(bucket_name, object_key, filetype, expiration=3600):
 
        s3_client = boto3.client('s3')
        response = s3_client.generate_presigned_url('get_object',
            Params={'Bucket': bucket_name,
            'Key': object_key,
            'ResponseContentDisposition': 'attachment',
            'ResponseContentType': filetype},
            ExpiresIn=expiration)

        return response


    user_identity = get_cognito_identity(st.session_state["user_id"])

    try:

        obj = list_user_objects(user_identity)

        my_dict = {}
        file_types = ['text/plain', 'application/msword']
        url_links = []

        for o in obj:
            content = get_object_text(S3_BUCKET, o)
            for ft in file_types:
                print(ft)
                url = generate_presigned_url(S3_BUCKET, o, ft)
                url_links.append(url)
            title = o.split('/')
            my_dict[title[1]] = (content, url_links[0], url_links[1])
            url_links.clear()
        
        data = [{'Title': key, 'Content': value[0], 'TXT': value[1], 'DOC': value[2]} for key, value in my_dict.items()]

        df = pd.DataFrame(data)

        print(df)

        AwesomeTable(df, columns=[
            Column(name='Title', label='Title'),
            Column(name='TXT', label='TXT', dtype=ColumnDType.DOWNLOAD),
            Column(name='DOC', label='DOC', dtype=ColumnDType.DOWNLOAD)
        ], show_search=True)

        uploaded_file = st.file_uploader("**Load File For Editing**")
        if uploaded_file is not None:

            # To convert to a string based IO:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            # To read file as string:
            string_data = stringio.read()

            content = st_quill(key="quill",value=string_data)

            st.download_button('Download File', content, file_name=uploaded_file.name)

    except:

        _, col2, _ = st.columns([3, 3, 2])
        with col2:
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("")
            st.markdown("#### _You have no previous transcriptions_ 📝")
        pass        

else:
        
    st.write("**Login For Access**")