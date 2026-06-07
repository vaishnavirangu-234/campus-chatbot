from src.database import CampusDatabase
from src.location_service import LocationService


class ContextBuilder:

    def __init__(self):
        self.db = CampusDatabase()
        self.location_service = LocationService()

    def build_context(self, query):

        context_parts = []

        query_lower = query.lower()

        # Clubs
        if "club" in query_lower:
            clubs = self.db.get_all_clubs()

            club_text = "\n".join([
                f"{club['name']} - {club['description']}"
                for club in clubs
            ])

            context_parts.append(
                f"Available Clubs:\n{club_text}"
            )

        # Events
        if "event" in query_lower:
            events = self.db.get_upcoming_events()

            event_text = "\n".join([
                f"{event['title']} on {event['start_date']}"
                for event in events
            ])

            context_parts.append(
                f"Upcoming Events:\n{event_text}"
            )

        # Locations
        locations = self.location_service.search_location(query)

        if locations:

            location_text = "\n".join([
                f"{loc['place_name']} - "
                f"{loc['building']} - "
                f"{loc['floor']}"
                for loc in locations
            ])

            context_parts.append(
                f"Location Information:\n{location_text}"
            )

        return "\n\n".join(context_parts)