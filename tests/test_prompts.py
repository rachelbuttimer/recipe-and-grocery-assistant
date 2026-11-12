import json
from pathlib import Path
import sys
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

# find project root
ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
  sys.path.insert(0, str(ROOT_DIR))

from dotenv import load_dotenv
from backend.prompt_engine import get_prompt_template, build_prompt_input 


load_dotenv()

# initialize gemini
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0.2)
chain = get_prompt_template() | llm | StrOutputParser()

test_cases = [
    {
        "name": "Standard Request",
        "query": "Make me a quick chicken and rice dinner.",
        "profile": {
            "kitchen_equipment": ["pan", "pot", "stove"],
            "pantry_ingredients": ["chicken", "olive oil", "salt", "pepper", "white rice"],
            "dietary_restrictions": [],
            "weekly_budget": 50.00,
        },
    },
    {
        "name": "Strict Vegan and Nut-Free Diet",
        "query": "I want a creamy pasta dish for dinner.",
        "profile": {
            "kitchen_equipment": ["pot", "stove"],
            "pantry_ingredients": ["olive oil", "tomatoes", "spinach"],
            "dietary_restrictions": ["vegan", "nut free"],
            "weekly_budget": 40.00,
        },
    },
    {
        "name": "Tight Budget",
        "query": "Give me a filling breakfast idea.",
        "profile": {
            "kitchen_equipment": ["pan", "stove"],
            "pantry_ingredients": ["butter"],
            "dietary_restrictions": [],
            "weekly_budget": 10.00,
        },
    },
    {
        "name": "Limited Kitchen Equipment",
        "query": "Make me a healthy lunch with beef and vegetables.",
        "profile": {
            "kitchen_equipment": ["air fryer", "microwave"],
            "pantry_ingredients": ["salmon", "broccoli", "olive oil"],
            "dietary_restrictions": ["gluten free"],
            "weekly_budget": 60.00,
        },
    },
    {
        "name": "Empty Pantry",
        "query": "Suggest an easy vegetarian stir-fry.",
        "profile": {
            "kitchen_equipment": ["pan", "stove"],
            "pantry_ingredients": [],
            "dietary_restrictions": ["vegetarian"],
            "weekly_budget": 35.00,
        },
    },
]


def run_validation():
  log_path = ROOT_DIR / "logs" / "prompt_validation_log.log"
  log_path.parent.mkdir(parents=True, exist_ok=True)

  with open(log_path, "w", encoding="utf-8") as log_file:
    log_file.write(f"Baseline Prompt Validation Log\n")

    for case in test_cases:
        print(f"Running test case: {case['name']}...\n")

        # mock profile
        profile = case["profile"]
        input = {
            "kitchen_equipment": (", ".join(profile["kitchen_equipment"]) or "none"),
            "pantry_ingredients": (", ".join(profile["pantry_ingredients"]) or "none"),
            "dietary_restrictions": (", ".join(profile["dietary_restrictions"]) or "none"),
            "weekly_budget": f"{profile['weekly_budget']:.2f}",
            "user_query": case["query"],
        }
        response = chain.invoke(input)

        log_file.write(f"{case['name']}\n")
        log_file.write(f"- Query: {case['query']}\n")
        log_file.write(f"- Profile Inputs: `{json.dumps(input)}`\n")
        log_file.write(f" Model Output:\n{response}\n")
        log_file.write("\n\n")

  print(f"\nTests complete. Results saved to {log_path}")

if __name__ == "__main__":
  run_validation()