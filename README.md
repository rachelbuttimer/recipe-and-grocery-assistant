# Recipe and Grocery Assistant

An AI-powered culinary and meal-planning web application built with Streamlit, LangChain, Google Gemini, ChromaDB, and SQLite. Users save their kitchen equipment, pantry inventory, dietary restrictions, and weekly budget, and the assistant generates personalized recipes and grocery lists.

---

## Prerequisites and Setup

### 1. Clone the Repository & Install Dependencies
This project uses uv for dependency management (Python 3.11+):

```bash
git clone <https://github.com/rachelbuttimer/recipe-and-grocery-assistant.git>
cd recipe-and-grocery-assistant
uv sync
```

### 2. Configure Environment Variables
Create a .env file in the project root directory and add your Google Gemini API key:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Download the Foundational Recipe Dataset
Download the recipe dataset from Kaggle: https://www.kaggle.com/datasets/wafaaelhusseini/extended-recipes-dataset-64k-dishes

Extract the CSV file, rename it to "recipes.csv", and place it inside the data/ directory

### 4. Build the Local ChromaDB Vector Store
Run the ingestion script (backend/ingest_recipes.py) once to sample 500 diverse recipes from the dataset, extract dietary tags, and generate embeddings:

```bash
uv run --no-project python backend/ingest_recipes.py
```

## Running and Testing

### Launch the Streamlit web app

```bash
uv run --no-project streamlit run app.py
```

### Run Backend Verification Scripts

Verify Gemini API connection:

```bash
uv run --no-project python backend/test_api.py
```

Run the prompt & JSON validation:

```bash
uv run --no-project python backend/test_prompts.py
```

Test semantic recipe retrieval from ChromaDB:
```bash
uv run --no-project python -c "from backend.retriever import retrieve_relevant_recipes; print(retrieve_relevant_recipes('quick vegetarian dinner', k=2))"
```
