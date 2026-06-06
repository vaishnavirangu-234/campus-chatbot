import json
from datetime import datetime, timedelta

def generate_sample_clubs():
    clubs = [
        {
            "name": "Extra Curricular activities",
            "description": "Enhancing skills beyond academics",
            "coordinator_name": "V. Ramana Babu",
            "coordinator_email": "alice@college.edu",
            "coordinator_phone": "+1-555-0101",
            "meeting_day": "Wednesday",
            "meeting_time": "6:00 PM",
            "location": "Tech Building, Room 201",
            "members_count": 150,
            "website": "http://kucet.ac.in/Extra_Curricular_Activities"
        },
        {
            "name": "National Cadet Corps - NCC",
            "description": "NCC Army and Air Wing activities",
            "coordinator_name": "Lt. Dr. K. Vijay Kumar and Dr. B. Anil kumar",
            "coordinator_email": "bob@college.edu",
            "coordinator_phone": "+1-555-0102",
            "meeting_day": "Monday",
            "meeting_time": "7:00 PM",
            "location": "Auditorium Stage",
            "members_count": 80,
            "website": "http://kucet.ac.in/NccArmy&NccAirwing"
        },
        {
            "name": "Sports Committee",
            "description": "Organize and coordinate college sports events",
            "coordinator_name": "Dr. Kota Sridhar kumar",
            "coordinator_email": "maria@college.edu",
            "coordinator_phone": "+1-555-0103",
            "meeting_day": "Tuesday",
            "meeting_time": "5:00 PM",
            "location": "Sports Center, Meeting Room A",
            "members_count": 200,
            "website": "http://kucet.ac.in/sports"
        },
        {
            "name": "National Service Scheme - NSS",
            "description": "Promote sustainability and environmental awareness",
            "coordinator_name": "Dr. D. Sailaja and M. Soujanya",
            "coordinator_email": "rachel@college.edu",
            "coordinator_phone": "+1-555-0104",
            "meeting_day": "Thursday",
            "meeting_time": "6:30 PM",
            "location": "Science Building, Room 101",
            "members_count": 60,
            "website": "http://kucet.ac.in/nss"
        }
    ]
    
    with open('clubs.json', 'w') as f:
        json.dump(clubs, f, indent=2)
    
    print("Generated clubs.json")

def generate_sample_events():
    today = datetime.now()
    events = [
        {
            "title": "Orientation Week",
            "description": "Welcome freshers! Meet your seniors and explore campus",
            "start_date": (today + timedelta(days=5)).isoformat(),
            "end_date": (today + timedelta(days=9)).isoformat(),
            "location": "Main Auditorium",
            "organizer": "Student Affairs Office",
            "category": "Orientation"
        },
        {
            "title": "Annual Sports Day",
            "description": "Compete in various sports events and win prizes",
            "start_date": (today + timedelta(days=20)).isoformat(),
            "location": "Sports Complex",
            "organizer": "Sports Committee",
            "category": "Sports"
        },
        {
            "title": "Tech Hackathon 2024",
            "description": "24-hour coding competition with great prizes",
            "start_date": (today + timedelta(days=15)).isoformat(),
            "location": "Tech Building",
            "organizer": "Coding Club",
            "category": "Technical"
        },
        {
            "title": "Annual Fest",
            "description": "College's biggest event with concerts, competitions, and more",
            "start_date": (today + timedelta(days=30)).isoformat(),
            "end_date": (today + timedelta(days=32)).isoformat(),
            "location": "Campus Grounds",
            "organizer": "Student Council",
            "category": "Cultural"
        }
    ]
    
    with open('events.json', 'w') as f:
        json.dump(events, f, indent=2, default=str)
    
    print("Generated events.json")

def generate_sample_facilities():
    facilities = [
        {
            "name": "Central Library",
            "category": "Academic",
            "location": "Building A, Ground Floor",
            "description": "Main library with 50,000+ books",
            "hours_open": "8:00 AM",
            "hours_close": "10:00 PM",
            "contact_name": "Mr. Kumar",
            "contact_email": "library@college.edu",
            "contact_phone": "+1-555-0201",
            "capacity": 500,
            "amenities": "WiFi, Study Desks, Computer Lab, Reading Areas"
        },
        {
            "name": "Cafeteria",
            "category": "Food & Dining",
            "location": "Building C",
            "description": "Main dining facility with diverse food options",
            "hours_open": "7:00 AM",
            "hours_close": "8:00 PM",
            "contact_name": "Ms. Priya",
            "contact_email": "cafeteria@college.edu",
            "contact_phone": "+1-555-0202",
            "capacity": 300,
            "amenities": "Seating, WiFi, Vegan Options, Payment Systems"
        },
        {
            "name": "Medical Center",
            "category": "Health & Wellness",
            "location": "Building E",
            "description": "24/7 medical facility for student health",
            "hours_open": "24/7",
            "contact_name": "Dr. Sharma",
            "contact_email": "health@college.edu",
            "contact_phone": "+1-555-0203",
            "amenities": "Emergency Care, Consultation, Medicine Counter"
        },
        {
            "name": "Sports Complex",
            "category": "Recreation",
            "location": "Behind Main Building",
            "description": "Indoor and outdoor sports facilities",
            "hours_open": "6:00 AM",
            "hours_close": "9:00 PM",
            "contact_name": "Coach Rajesh",
            "contact_email": "sports@college.edu",
            "contact_phone": "+1-555-0204",
            "capacity": 1000,
            "amenities": "Gym, Basketball, Badminton, Tennis, Pool"
        }
    ]
    
    with open('facilities.json', 'w') as f:
        json.dump(facilities, f, indent=2)
    
    print("Generated facilities.json")

if _name_ == "_main_":
    generate_sample_clubs()
    generate_sample_events()
    generate_sample_facilities()