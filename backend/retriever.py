from pathlib import Path
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

ROOT_DIR = Path(__file__).resolve().parent.parent
CHROMA_PATH = ROOT_DIR / "data" / "chroma_db"

load_dotenv(ROOT_DIR / ".env")

def get_vectorstore() -> Chroma:
    """connects to the ChromaDB recipe collection"""
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    return Chroma(collection_name="recipes", embedding_function=embeddings, persist_directory=str(CHROMA_PATH))

def retrieve_relevant_recipes(user_query: str, k: int = 3) -> str:
    """
    searches ChromaDB for the top-k recipes matching the user's query
    and formats them into a single context string for prompt injection.
    """
    if not CHROMA_PATH.exists():
        return "No local recipe knowledge base found."

    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search(user_query, k=k)

    if not docs:
        return "No matching reference recipes found in the database."

    formatted_recipes = []

    for i, doc in enumerate(docs, start=1):
        formatted_recipes.append(f"--- Reference Recipe {i} ---\n{doc.page_content}")

    return "\n\n".join(formatted_recipes)