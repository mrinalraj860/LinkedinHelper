import streamlit as st
import pandas as pd
from scraper.profile_scraper import save_to_excel
from messenger.message_sender import send_message, load_template

st.title("LinkedIn Automation Tool")

email = st.text_input("LinkedIn Email")
password = st.text_input("LinkedIn Password", type="password")
query_url = st.text_input("Search URL")
upload_people = st.file_uploader("Upload People Excel", type="xlsx")

if st.button("Start"):
    # Would integrate with actual backend
    st.success("Started scraping/sending process")