from src.web_scraper import CampusWebScraper
from src.knowledge_base import KnowledgeBase

scraper = CampusWebScraper(max_pages=5)
print("Scraping KUCET website...")

urls = [
    "http://kucet.ac.in/college.php",
    "http://kucet.ac.in/admissions.php",
    "http://kucet.ac.in/fee-details.php",
    "http://kucet.ac.in/placements.php",
    "http://kucet.ac.in/Extra_Curricular_Activities.php"
]

docs = []
for url in urls:
    docs.extend(
        scraper.scrape_site_recursive(url)
    )
print("Pages found:", len(docs))        

kb = KnowledgeBase()

chunks = kb.add_documents(docs)

print("Added chunks:", chunks)

import json

with open("data/kucet_docs.json", "w", encoding="utf-8") as f:
    json.dump(docs, f, ensure_ascii=False, indent=2)

print("Website data saved")