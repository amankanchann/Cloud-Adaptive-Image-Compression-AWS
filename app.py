import streamlit as st

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        password = st.text_input("Enter password", type="password")
        if st.button("Login"):
            if password == st.secrets["APP_PASSWORD"]:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password")
        st.stop()

check_password()

from uploader import render_upload_section
from dashboard import render_dashboard

st.set_page_config(page_title="Image Compression Dashboard", layout="wide")

st.title("Cloud-Based Image Compression Dashboard")

if st.button("Refresh Dashboard"):
    st.rerun()

render_upload_section()
render_dashboard()