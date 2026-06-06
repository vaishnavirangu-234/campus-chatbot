#load_sample_data.py                                                                                                                                                 import json
from src.database import CampusDatabase
import json
db = CampusDatabase()

# Clubs
with open("data/clubs.json", "r") as f:
    clubs = json.load(f)

for club in clubs:
    db.insert_club(
        name=club["name"],
        description=club["description"],
        coordinator_name=club["faculty_coordinator"],
        coordinator_email="club@college.edu"
    )

# Events
with open("data/events.json", "r") as f:
    events = json.load(f)

for event in events:
    db.insert_event(
        title=event["title"],
        description=event["description"],
        start_date=event["date"],
        location=event["venue"],
        organizer=event["organizer"]
    )

# Facilities
with open("data/facilities.json", "r") as f:
    facilities = json.load(f)

for facility in facilities:
    db.insert_facility(
        name=facility["name"],
        category="Academic",
        location=facility["location"],
        description=facility["description"]
    )

print("Data loaded successfully!")

