USER_PROMPT_TEMPLATE = """
    User Profile:
        - Kitchen Equipment: {kitchen_equipment}
        - On-Hand Pantry: {pantry_ingredients}
        - Dietary Restrictions: {dietary_restrictions}
        - Weekly Budget: ${weekly_budget}

    Reference Recipe Context: {retrieved_context}

    User Request: {user_query}
"""