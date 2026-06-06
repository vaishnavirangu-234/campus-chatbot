# # src/location_service.py
# from typing import List, Dict, Tuple
# import math

# class LocationService:
#     def __init__(self, db):
#         self.db = db
#         self.campus_center = (40.1105, -88.2073)  # Example coordinates (Champaign, IL)
    
#     def add_location(self, place_name: str, building: str, floor: str,
#                     latitude: float, longitude: float, description: str = "",
#                     access_info: str = ""):
#         """Add a location to the database"""
#         self.db.insert_location(place_name, building, floor, 
#                                latitude, longitude, description, access_info)
    
#     def find_nearby_locations(self, latitude: float, longitude: float, 
#                              radius_km: float = 0.5) -> List[Dict]:
#         """Find locations within radius"""
#         all_locations = self.db.search_location("")
#         nearby = []
        
#         for location in all_locations:
#             if location['latitude'] and location['longitude']:
#                 distance = self._calculate_distance(
#                     latitude, longitude,
#                     location['latitude'], location['longitude']
#                 )
#                 if distance <= radius_km:
#                     location['distance_km'] = round(distance, 2)
#                     nearby.append(location)
        
#         return sorted(nearby, key=lambda x: x['distance_km'])
    
#     def _calculate_distance(self, lat1: float, lon1: float, 
#                            lat2: float, lon2: float) -> float:
#         """Calculate distance between two coordinates (Haversine formula)"""
#         R = 6371  # Earth's radius in km
        
#         lat1_rad = math.radians(lat1)
#         lat2_rad = math.radians(lat2)
#         delta_lat = math.radians(lat2 - lat1)
#         delta_lon = math.radians(lon2 - lon1)
        
#         a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * \
#             math.cos(lat2_rad) * math.sin(delta_lon/2)**2
#         c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
#         return R * c
    
#     def get_directions(self, from_place: str, to_place: str) -> Dict:
#         """Get directions between two campus locations"""
#         from_location = self.db.search_location(from_place)
#         to_location = self.db.search_location(to_place)
        
#         if not from_location or not to_location:
#             return {'error': 'One or both locations not found'}
        
#         from_loc = from_location[0]
#         to_loc = to_location[0]
        
#         if from_loc['latitude'] and to_loc['latitude']:
#             distance = self._calculate_distance(
#                 from_loc['latitude'], from_loc['longitude'],
#                 to_loc['latitude'], to_loc['longitude']
#             )
            
#             return {
#                 'from': from_place,
#                 'to': to_place,
#                 'distance_km': round(distance, 2),
#                 'estimated_walk_time_min': int(distance * 13)  # ~13 min per km
#             }
        
#         return {'error': 'Coordinates not available'}
import json

class LocationService:
    def __init__(self, file_path="data/locations.json"):
        with open(file_path, "r", encoding="utf-8") as f:
            self.raw_data = json.load(f)

        self.locations = self._expand_locations()

    # 🔧 Expand blocks (labs, LH, staff rooms)
    def _expand_locations(self):
        locations = []

        for item in self.raw_data:

            # normal entry
            if "range" not in item:
                locations.append(item)

            else:
                r = item["range"]

                # list type (labs, lecture halls)
                if r["type"] == "list":
                    for name in r["values"]:
                        locations.append({
                            "place_name": name,
                            "building": item["building"],
                            "floor": item["floor"],
                            "category": item.get("category", "")
                        })

                # count type (staff rooms)
                elif r["type"] == "count":
                    for i in range(1, r["values"] + 1):
                        locations.append({
                            "place_name": f"{item['place_name']} {i}",
                            "building": item["building"],
                            "floor": item["floor"],
                            "category": item.get("category", "")
                        })

        return locations

    # 🔍 THIS IS THE METHOD YOUR APP IS CALLING
    def search_location(self, query):
        query = query.lower().strip()

        results = []

        for loc in self.locations:
            if (
                query in loc["place_name"].lower()
                or query in loc.get("category", "").lower()
                or query in loc.get("floor", "").lower()
                or query in loc.get("building", "").lower()
            ):
                results.append(loc)

        return results

    # 📍 optional helper
    def get_all_locations(self):
        return self.locations