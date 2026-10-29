import streamlit as st
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
external_dir = os.path.abspath(os.path.join(current_dir, "../../backend"))

if external_dir not in sys.path:
    sys.path.insert(0, external_dir)

import db # type: ignore

st.title("Your Profile")

profile = db.get_user_profile()

if profile:
    st.write(f"**Kitchen Equipment:** {profile['kitchen_equipment']}")
    st.write(f"**Pantry Ingredients:** {profile['pantry_items']}")
    st.write(f"**Dietary Restrictions:** {profile['dietary_restrictions']}")
    st.write(f"**Weekly Budget:** ${profile['weekly_budget']:.2f}")
else:
    st.button("Edit profile")