import streamlit as st
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
external_dir = os.path.abspath(os.path.join(current_dir, "../backend"))

if external_dir not in sys.path:
    sys.path.insert(0, external_dir)

import db # type: ignore


db.init_db()

home = st.Page("pages/home.py", title="Home", icon=":material/home:")
profile = st.Page("pages/profile.py", title="Profile", icon=":material/person:")
page = st.navigation([home, profile])

profile_data = db.get_user_profile()
if db.get_user_profile() is None and page != profile:
    st.switch_page(profile)

page.run()