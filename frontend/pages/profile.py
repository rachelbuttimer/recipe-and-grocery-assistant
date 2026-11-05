import streamlit as st
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
external_dir = os.path.abspath(os.path.join(current_dir, "../../backend"))

if external_dir not in sys.path:
    sys.path.insert(0, external_dir)

import db # type: ignore

if "editing_profile" not in st.session_state:
  st.session_state.editing_profile = False

profile = db.get_user_profile()

# view profile
if not st.session_state.editing_profile:
    st.title("Your Profile")

    if profile:
        st.write(f"**Kitchen Equipment:** {profile['kitchen_equipment']}")
        st.write(f"**Pantry Ingredients:** {profile['pantry_ingredients']}")
        st.write(f"**Dietary Restrictions:** {profile['dietary_restrictions']}")
        st.write(f"**Weekly Budget:** ${profile['weekly_budget']:.2f}")

    if st.button("Edit profile"):
        st.session_state.editing_profile = True
        st.rerun()

else:
    st.title("Edit Profile")
    
    kitchen_equipment_options = ["air fryer", "oven", "microwave", "pan", "pot", "stove"]
    dairy_options = ["butter", "cheese", "greek yogurt", "milk"]
    meat_options = ["beef", "chicken", "pork", "salmon"]
    fruit_options = ["apples", "bananas", "oranges", "tomatoes"]
    vegetable_options = ["broccoli", "carrots", "corn", "green beans", "potatoes", "spinach", "sweet potatoes"]
    oil_options = ["canola oil", "olive oil", "vegetable oil"]
    spice_options = ["basil", "cumin", "salt", "oregano", "paprika", "parsley", "pepper"]
    dietary_restriction_options = [
        "dairy free", "gluten free", "lactose free", "nut free", "vegan", "vegetarian", "low sugar", "zero sugar"
    ]
    weekly_budget_options = ["$25", "$50", "$75", "$100", "$125", "$150", "$200", "$300", "$400", "$500"]

    kitchen_equipment = st.pills("What kitchen equipment do you have?", kitchen_equipment_options, selection_mode="multi") or []

    st.write("<small>What pantry ingredients do you have?</small>", unsafe_allow_html=True)
    with st.container(border=True):
        dairy = st.pills("Dairy", dairy_options, selection_mode="multi") or []
        meat = st.pills("Meat", meat_options, selection_mode="multi") or []
        fruit = st.pills("Fruit", fruit_options, selection_mode="multi") or []
        vegetables = st.pills("Vegetables", vegetable_options, selection_mode="multi") or []
        oils = st.pills("Oils", oil_options, selection_mode="multi") or []
    pantry_ingredients = dairy + meat + fruit + vegetables + oils

    dietary_restrictions = st.pills(
        "What dietary restrictions do you have?", dietary_restriction_options, selection_mode="multi"
    ) or []

    weekly_budget_list = st.pills("What is your weekly budget?", weekly_budget_options, selection_mode="multi") or []
    weekly_budget = weekly_budget_list[0] if len(weekly_budget_list) > 0 else 0.0
    weekly_budget_float = float(str(weekly_budget).replace("$", "").strip()) if weekly_budget_list is not [] else 0.0

    if st.button("Save profile"):
        db.save_user_profile(kitchen_equipment, pantry_ingredients, dietary_restrictions, weekly_budget_float)
        st.session_state.editing_profile = False
        st.rerun()

