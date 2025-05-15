import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.today.com/life/inspiration/truth-or-dare-questions-rcna130237"

response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")

truths = []
dares = []

# We find all <h2> headings
headers = soup.find_all("h2")

for header in headers:
    title = header.get_text(strip=True).lower()
    # Truth sections
    if "truth questions" in title:
        next_el = header.find_next_sibling("ul")
        if next_el:
            truths = [li.get_text(strip=True) for li in next_el.find_all("li")]

    # Dare sections
    if "dare questions" in title:
        next_el = header.find_next_sibling("ul")
        if next_el:
            dares = [li.get_text(strip=True) for li in next_el.find_all("li")]

# bring to JSON format
questions = {
    "truth": truths,
    "dare": dares
}

# Add to questions
with open("questions.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"✅ {len(truths)} truth və {len(dares)} task were added.")
