import streamlit as st
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
external_dir = os.path.abspath(os.path.join(current_dir, "../../backend"))

if external_dir not in sys.path:
    sys.path.insert(0, external_dir)

import db # type: ignore

st.title("Recipe and Grocery Assistant")