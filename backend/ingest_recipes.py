import csv
from pathlib import Path
import random
import time
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# anchor paths to project root
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT_DIR / "data" / "recipes.csv"
CHROMA_PATH = ROOT_DIR / "data" / "chroma_db"

load_dotenv(ROOT_DIR / ".env")

DIETARY_COLUMNS = {
    "is_vegan": "vegan",
    "is_vegetarian": "vegetarian",
    "is_halal": "halal",
    "is_kosher": "kosher",
    "is_nut_free": "nut free",
    "is_dairy_free": "dairy free",
    "is_gluten_free": "gluten free",
}

def load_recipes(max_recipes=500) -> list[Document]:
    """reads recipe dataset and converts each recipe into a langchain document"""
    documents = []

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        all_recipes = list(csv.DictReader(f))

        random.seed(0)
        sampled_recipes = random.sample(all_recipes, min(max_recipes, len(all_recipes)))

        for i, row in enumerate(sampled_recipes):
            if i >= max_recipes:
                break

            title = row.get("recipe_title") or "Untitled Recipe"
            cuisine = row.get("cuisine_list")
            ingredients = row.get("ingredients_raw")
            directions = row.get("directions_text")

            active_tags = [
                label
                for col, label in DIETARY_COLUMNS.items()
                if str(row.get(col, "")).strip().lower() == "true"
            ]

            dietary_tags_str = ", ".join(active_tags) if active_tags else "None"

            try:
                cook_time = int(float(row.get("est_cook_time_min") or 0))
            except ValueError:
                cook_time = 0

            page_content = (
                f"Title: {title}\n"
                f"Cuisine: {cuisine}\n"
                f"Dietary Tags: {dietary_tags_str}\n"
                f"Ingredients: {ingredients}\n"
                f"Directions: {directions}"
            )

            # used for filtering
            metadata = {
                "title": title,
                "cuisine": cuisine,
                "cook_time": cook_time,
                "dietary_tags": dietary_tags_str,
            }

            documents.append(Document(page_content=page_content, metadata=metadata))

    return documents

def ingest():
    docs = load_recipes()
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    chroma_db = Chroma(collection_name="recipes", embedding_function=embeddings, persist_directory=str(CHROMA_PATH))
    batch_size = 80
    total_batches = (len(docs) + batch_size - 1) // batch_size

    for batch_num, i in enumerate(range(0, len(docs), batch_size), start=1):
        batch = docs[i : i + batch_size]
        chroma_db.add_documents(batch)
        print(f"Embedded batch {batch_num}/{total_batches}")

        # pause 65 seconds before the next batch so the 1-minute quota resets
        if i + batch_size < len(docs):
            for t in range (65, 0, -1):
                print(f"{t}s...", end="\r", flush=True)
                time.sleep(1)

if __name__ == "__main__":
    ingest()