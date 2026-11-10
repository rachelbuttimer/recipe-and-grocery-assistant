import streamlit as st
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
external_dir = os.path.abspath(os.path.join(current_dir, "../../backend"))

if external_dir not in sys.path:
    sys.path.insert(0, external_dir)

import db # type: ignore

st.set_page_config(layout="wide")

icon_col, title_col = st.columns([1, 10], vertical_alignment="center")

with icon_col:
    st.image("assets/egg_chef.jpg", width=200)

with title_col:
    st.title("Recipe & Grocery Assistant")

st.html("""
    <style>
        /* lined notebook paper */
        .notebook-page {
            background-color: #fffdf5;
            background-image: 
                /* vertical red margin */
                linear-gradient(90deg, transparent 40px, #f5a9b8 40px, #f5a9b8 42px, transparent 42px),
                /* horizontal blue ruled lines */
                linear-gradient(#d8e8f8 1px, transparent 1px);
            background-size: 100% 100%, 100% 28px;
            line-height: 28px;
            padding: 24px 20px 24px 54px;
            border-radius: 6px;
            box-shadow: 2px 4px 12px rgba(0, 0, 0, 0.08);
            border: 1px solid #e8e2d5;
            font-family: 'Courier New', Courier, monospace;
            color: #2b2b2b;
            min-height: 380px;
        }

        /* ripped paper */
        .ripped-paper {
            background: #faf8f0;
            padding: 28px 22px 24px 22px;
            font-family: 'Comic Sans MS', 'Chalkboard SE', 'Segoe UI', cursive, sans-serif;
            color: #333333;
            box-shadow: 3px 5px 14px rgba(0, 0, 0, 0.12);
            min-height: 380px;
            position: relative;
            /* torn paper edge at top and bottom */
            --mask: 
                radial-gradient(10px at 50% 100%, #0000 98%, #000) 0 0/20px 100%,
                radial-gradient(10px at 50% 0, #0000 98%, #000) 0 100%/20px 100%;
            -webkit-mask: var(--mask);
            mask: var(--mask);
        }

        .paper-title {
            font-size: 1.25rem;
            font-weight: bold;
            margin-bottom: 12px;
            border-bottom: 2px dashed #bbb;
            padding-bottom: 6px;
        }
    </style>
""")

recipe_col, groceries_col = st.columns(2, gap="large")

# recipe on notebook paper
with recipe_col:
    st.markdown("""
    <div class="notebook-page">
        <div class="paper-title">Personalized Recipe</div>
        <p>Your personalized recipe will appear here.</p>
    </div>
    """, unsafe_allow_html=True)

# groceries on ripped page
with groceries_col:
    st.markdown("""
    <div class="ripped-paper">
        <div class="paper-title">Grocery List</div>
        <p>Your grocery list will appear here.</p>
    </div>
    """, unsafe_allow_html=True)

user_prompt = st.chat_input("Ask for a recipe or paste a URL...", max_chars=1000)

if user_prompt:
    # update this calculation. currently ~1 token per 4 characters
    estimated_tokens = round(len(user_prompt) / 4)
    st.caption(f"Input received: {len(user_prompt)} characters (~{estimated_tokens} tokens)")