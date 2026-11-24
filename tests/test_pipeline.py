import json
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from backend.prompt_engine import build_prompt_input, get_prompt_template

load_dotenv(ROOT_DIR / ".env")

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0.2)
chain = get_prompt_template() | llm | StrOutputParser()

TEST_QUERIES = [
    {
        "label": "Test 1: ChromaDB RAG",
        "query": "Make me a quick chicken and spinach dinner.",
        "expected_marker": "--- Reference Recipe 1 ---",
    },
    {
        "label": "Test 2: URL Scraper",
        "query": "What groceries do I need to buy for https://www.allrecipes.com/recipe/24074/alysias-basic-meat-lasagna/",
        "expected_marker": "Title:",
    },
]

def test_routing_and_generation():
    for test in TEST_QUERIES:
        print("-" * 60)
        print(test["label"])
        print(f"Query: {test['query']}\n")

        # inspect the assembled prompt inputs before calling Gemini
        prompt_inputs = build_prompt_input(test["query"])
        context = prompt_inputs["retrieved_context"]

        # verify which branch executed
        is_rag = "--- Reference Recipe 1 ---" in context
        route_used = "ChromaDB RAG" if is_rag else "URL Scraper"
        print(f"[Routing Check] Branch used: {route_used}")
        print(f"[Context Preview] {context[:250].replace(chr(10), ' ')}...\n")

        assert test["expected_marker"] in context, (
            f"Expected '{test['expected_marker']}' in retrieved_context, got:\n{context[:300]}"
        )

        # run through Gemini and verify valid JSON output
        raw_output = chain.invoke(prompt_inputs)
        parsed_json = json.loads(raw_output)
        print(f"[Gemini Output] Dish: {parsed_json.get('personalized_recipe', {}).get('title', 'Parsed OK')}")
        print(f"[Gemini Output] Groceries to buy: {len(parsed_json.get('grocery_items_to_buy', []))} items")
        print("STATUS: PASSED\n")

if __name__ == "__main__":
    test_routing_and_generation()