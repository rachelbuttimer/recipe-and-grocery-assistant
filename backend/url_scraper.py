import re
import requests
from bs4 import BeautifulSoup
from recipe_scrapers import scrape_html

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}

def extract_url(text: str) -> str | None:
    """finds the first http/https URL inside a user's message, if any"""
    match = re.search(r"https?://[^\s]+", text)
    
    return match.group(0).rstrip(".,)") if match else None

def scrape_recipe_url(url: str) -> str:
    """
    fetches a recipe webpage and extracts structured recipe details using
    recipe-scrapers, or cleaned BeautifulSoup text if unsupported
    """
    response = requests.get(url, headers=HEADERS, timeout=10)

    response.raise_for_status()

    html = response.text

    # structured extraction with recipe-scrapers
    try:
        scraper = scrape_html(html, org_url=url)
        ingredients = "\n".join(f"- {item}" for item in scraper.ingredients())
        instructions = scraper.instructions()

        return (
            f"Title: {scraper.title()}\n"
            f"Total Time: {scraper.total_time()} mins\n"
            f"Yields: {scraper.yields()}\n"
            f"Ingredients:\n{ingredients}\n\n"
            f"Directions:\n{instructions}"
        )
    except Exception:
        # strip scripts/styles and pass clean page text to Gemini
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        clean_text = "\n".join(line.strip() for line in soup.get_text().splitlines() if line.strip())

        # max length to protect token budget
        return f"Extracted Webpage Text ({url}):\n{clean_text[:6000]}"