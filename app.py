import streamlit as st
from backend import db

db.init_db()

home = st.Page("pages/home.py", title="Home", icon=":material/home:")
profile = st.Page("pages/profile.py", title="Profile", icon=":material/person:")
page = st.navigation([home, profile])
profile_data = db.get_user_profile()

page.run()