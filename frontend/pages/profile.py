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
saved_kitchen_equipment = profile.get("kitchen_equipment", []) if profile else []
saved_pantry_ingredients = profile.get("pantry_ingredients", []) if profile else []
saved_dietary_restrictions = profile.get("dietary_restrictions", []) if profile else []
saved_weekly_budget = profile.get("weekly_budget", 0.0) if profile else 0.0

# view profile
if not st.session_state.editing_profile:
    st.title("Your Profile")

    if profile:
        st.write(
            f"**Kitchen Equipment:** {
                ', '.join(profile['kitchen_equipment']) if profile.get('kitchen_equipment') else 'none'
            }"
        )
        st.write(
            f"**Pantry Ingredients:** {
                ', '.join(profile['pantry_ingredients']) if profile.get('pantry_ingredients') else 'none'
            }"
        )
        st.write(
            f"**Dietary Restrictions:** {
                ', '.join(profile['dietary_restrictions']) if profile.get('dietary_restrictions') else 'none'
            }"
        )
        st.write(f"**Weekly Budget:** ${profile['weekly_budget']:.2f}")

    if st.button("Edit profile"):
        st.session_state.editing_profile = True
        st.rerun()

# edit profile
else:
    if st.button("Back"):
        st.session_state.editing_profile = False
        st.rerun()

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

    kitchen_equipment = st.pills(
        "What kitchen equipment do you have?", 
        kitchen_equipment_options, 
        default=[item for item in saved_kitchen_equipment if item in kitchen_equipment_options], 
        selection_mode="multi", 
        key="edit_kitchen_equipment"
    ) or []

    st.write("<small>What pantry ingredients do you have?</small>", unsafe_allow_html=True)
    with st.container(border=True):
        dairy = st.pills(
            "Dairy", 
            dairy_options, 
            default=[item for item in saved_pantry_ingredients if item in dairy_options],
            selection_mode="multi",
            key="edit_dairy"
        ) or []
        meat = st.pills(
            "Meat", 
            meat_options, 
            default=[item for item in saved_pantry_ingredients if item in meat_options],
            selection_mode="multi",
            key="edit_meat"
        ) or []
        fruit = st.pills(
            "Fruit", 
            fruit_options, 
            default=[item for item in saved_pantry_ingredients if item in fruit_options],
            selection_mode="multi",
            key="edit_fruit"
        ) or []
        vegetables = st.pills(
            "Vegetables", 
            vegetable_options, 
            default=[item for item in saved_pantry_ingredients if item in vegetable_options],
            selection_mode="multi",
            key="edit_vegetables"
            ) or []
        oils = st.pills(
            "Oils",
            oil_options, 
            default=[item for item in saved_pantry_ingredients if item in oil_options],
            selection_mode="multi",
            key="edit_oils"
        ) or []
    pantry_ingredients = dairy + meat + fruit + vegetables + oils

    dietary_restrictions = st.pills(
        "What dietary restrictions do you have?",
        dietary_restriction_options, 
        default=[item for item in saved_dietary_restrictions if item in dietary_restriction_options],
        selection_mode="multi",
        key="edit_dietary_restrictions"
    ) or []

    weekly_budget_label = f"${int(saved_weekly_budget)}" if saved_weekly_budget else None
    weekly_budget = st.pills(
        "What is your weekly budget?", 
        weekly_budget_options, 
        default=weekly_budget_label if weekly_budget_label in weekly_budget_options else None,
        selection_mode="single",
        key="edit_weekly_budget"
    ) or []
    weekly_budget_float = float(str(weekly_budget).replace("$", "").strip()) if weekly_budget else 0.0

    if st.button("Save profile"):
        db.save_user_profile(kitchen_equipment, pantry_ingredients, dietary_restrictions, weekly_budget_float)
        st.session_state.editing_profile = False
        st.rerun()

