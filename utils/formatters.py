def format_event(event: dict) -> str:
    return f"""
Event: {event.get('title')}
Date: {event.get('date')}
Time: {event.get('time')}
Venue: {event.get('venue')}
Organizer: {event.get('organizer')}
Description: {event.get('description')}
""".strip()


def format_club(club: dict) -> str:
    return f"""
Club Name: {club.get('name')}
Category: {club.get('category')}
Faculty Coordinator: {club.get('faculty_coordinator')}
Description: {club.get('description')}
""".strip()


def format_facility(facility: dict) -> str:
    return f"""
Facility: {facility.get('name')}
Location: {facility.get('location')}
Timings: {facility.get('timings')}
Description: {facility.get('description')}
""".strip()