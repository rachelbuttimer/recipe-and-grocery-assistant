from langchain_core.prompts import ChatPromptTemplate
from backend import db
from prompt_templates.system_prompt import SYSTEM_PROMPT
from prompt_templates.user_prompt import USER_PROMPT_TEMPLATE

# combines the system prompt and user prompt template into a langchain ChatPromptTemplate
def get_prompt_template() -> ChatPromptTemplate:
  return ChatPromptTemplate.from_messages(
    [("system", SYSTEM_PROMPT), ("human", USER_PROMPT_TEMPLATE)]
  )

# formats the user profile for the prompt template
def build_prompt_input(user_query: str) -> dict:
  profile = db.get_user_profile() or {}

  return {
      "kitchen_equipment": ", ".join(profile.get("kitchen_equipment", [])) or "none",
      "pantry_ingredients": ", ".join(profile.get("pantry_ingredients", [])) or "none",
      "dietary_restrictions": ", ".join(profile.get("dietary_restrictions", [])) or "none",
      "weekly_budget": f"{profile.get('weekly_budget', 0.0):.2f}",
      "user_query": user_query,
  }