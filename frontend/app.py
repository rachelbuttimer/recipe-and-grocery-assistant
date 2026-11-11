import streamlit as st
import sys
from pathlib import Path

# find root directory
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
  sys.path.insert(0, str(root_dir))

from backend import db

db.init_db()

home = st.Page("pages/home.py", title="Home", icon=":material/home:")
profile = st.Page("pages/profile.py", title="Profile", icon=":material/person:")
page = st.navigation([home, profile])
profile_data = db.get_user_profile()

page.run()