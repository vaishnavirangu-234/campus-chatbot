#load_sample_data.py                                                                                                                                                 import json
from src.database import CampusDatabase
import json
import sqlite3
db = CampusDatabase()

# Clubs
with open("data/clubs.json", "r") as f:
    clubs = json.load(f)

for club in clubs:
    try:
        db.insert_club(
            name=club["name"],
            description=club["description"],
            coordinator_name=club["faculty_coordinator"],
            coordinator_email="club@college.edu"
        )
    except sqlite3.IntegrityError:
        pass

# Events
# Events
with open("data/events.json", "r") as f:
    events = json.load(f)

for event in events:
    try:
        db.insert_event(
            title=event["title"],
            description=event["description"],
            start_date=event["date"],
            location=event["venue"],
            organizer=event["organizer"]
        )
    except sqlite3.IntegrityError:
        pass
# Facilities
with open("data/facilities.json", "r") as f:
    facilities = json.load(f)

for facility in facilities:
    try:
        db.insert_facility(
            name=facility["name"],
            category=facility["category"],
            location=facility["location"],
            description=facility["description"]
        )
    except sqlite3.IntegrityError:
        pass

print("Data loaded successfully!")

