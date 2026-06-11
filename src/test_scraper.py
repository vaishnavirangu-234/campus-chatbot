import json
from web_scraper import CampusWebScraper

scraper = CampusWebScraper()

events = scraper.scrape_kucet_events()

print(f"Found {len(events)} events")

with open("../data/events.json", "w", encoding="utf-8") as f:
    json.dump(
        events,
        f,
        indent=4,
        ensure_ascii=False
    )

print("Events saved successfully!")