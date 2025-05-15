import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.today.com/life/inspiration/truth-or-dare-questions-rcna130237"

response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")

truths = []
dares = []

# Bütün <h2> başlıqlarını tapırıq
headers = soup.find_all("h2")

for header in headers:
    title = header.get_text(strip=True).lower()
    # Truth bölməsi
    if "truth questions" in title:
        next_el = header.find_next_sibling("ul")
        if next_el:
            truths = [li.get_text(strip=True) for li in next_el.find_all("li")]

    # Dare bölməsi
    if "dare questions" in title:
        next_el = header.find_next_sibling("ul")
        if next_el:
            dares = [li.get_text(strip=True) for li in next_el.find_all("li")]

# JSON formatına salırıq
questions = {
    "truth": truths,
    "dare": dares
}

# Fayla yazırıq
with open("questions.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"✅ {len(truths)} doğruluq və {len(dares)} cəsarət tapşırığı yadda saxlanıldı.")
