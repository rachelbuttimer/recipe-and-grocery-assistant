import json
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.prompt_engine import build_prompt_input, get_prompt_template

load_dotenv(ROOT_DIR / ".env")

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0.2)
chain = get_prompt_template() | llm | StrOutputParser()

def test_multi_turn_memory():
    chat_history = []

    # turn 1: initial recipe
    q1 = "Give me a classic chicken stir fry recipe."
    inputs_1 = build_prompt_input(q1)
    inputs_1["chat_history"] = chat_history
    res_1 = chain.invoke(inputs_1)

    chat_history.append(HumanMessage(content=q1))
    chat_history.append(AIMessage(content=res_1))

    # turn 2: follow-up that relies strictly on session memory
    q2 = "Make it vegetarian by swapping the protein, and keep everything else the same."
    inputs_2 = build_prompt_input(q2)
    inputs_2["chat_history"] = chat_history
    res_2 = chain.invoke(inputs_2)
    data_2 = json.loads(res_2.strip().removeprefix("```json").removesuffix("```").strip())
    recipe_text = json.dumps(data_2).lower()

    assert "stir fry" or "stir-fry" in recipe_text, "Failed: Lost original dish context from Turn 1"
    assert "chicken" not in recipe_text, "Failed: Did not apply Turn 2 modification"
    print("PASSED: Session memory preserved Turn 1 dish and applied Turn 2 modification.")

if __name__ == "__main__":
    test_multi_turn_memory()