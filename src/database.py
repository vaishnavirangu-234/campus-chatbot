# src/database.py
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

class CampusDatabase:
    def __init__(self, db_path: str = "./data/campus_chatbot.db"):
        self.db_path = db_path
        self._initialize_db()
    
    def _initialize_db(self):
        """Create database tables if they don't exist"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Queries history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_query TEXT NOT NULL,
                bot_response TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_satisfaction INTEGER,
                session_id TEXT
            )
        ''')
        
        # Campus information cache
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campus_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                subcategory TEXT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                source TEXT,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                start_date DATETIME NOT NULL,
                end_date DATETIME,
                location TEXT,
                organizer TEXT,
                category TEXT,
                image_url TEXT,
                registration_link TEXT,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Clubs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clubs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                coordinator_name TEXT,
                coordinator_email TEXT,
                coordinator_phone TEXT,
                meeting_day TEXT,
                meeting_time TEXT,
                location TEXT,
                members_count INTEGER,
                logo_url TEXT,
                website TEXT,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Facilities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS facilities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                category TEXT NOT NULL,
                location TEXT NOT NULL,
                description TEXT,
                hours_open TEXT,
                hours_close TEXT,
                contact_name TEXT,
                contact_email TEXT,
                contact_phone TEXT,
                capacity INTEGER,
                amenities TEXT,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Locations table (for map-based queries)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                place_name TEXT NOT NULL UNIQUE,
                building TEXT,
                floor TEXT,
                latitude REAL,
                longitude REAL,
                description TEXT,
                access_info TEXT
            )
        ''')
        
        # FAQs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS faqs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                category TEXT,
                view_count INTEGER DEFAULT 0,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_query(self, user_query: str, bot_response: str, 
                   session_id: str = None, satisfaction: int = None):
        """Save query and response to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO queries (user_query, bot_response, session_id, user_satisfaction)
            VALUES (?, ?, ?, ?)
        ''', (user_query, bot_response, session_id, satisfaction))
        
        conn.commit()
        conn.close()
    
    def get_query_history(self, limit: int = 50, session_id: str = None) -> List[Dict]:
        """Retrieve query history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if session_id:
            cursor.execute('''
                SELECT user_query, bot_response, timestamp 
                FROM queries 
                WHERE session_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (session_id, limit))
        else:
            cursor.execute('''
                SELECT user_query, bot_response, timestamp 
                FROM queries 
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                "query": row[0],
                "response": row[1],
                "timestamp": row[2]
            }
            for row in results
        ]
    
    def insert_campus_info(self, category: str, title: str, content: str,
                          subcategory: str = None, source: str = None):
        """Insert campus information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO campus_info (category, subcategory, title, content, source)
            VALUES (?, ?, ?, ?, ?)
        ''', (category, subcategory, title, content, source))
        
        conn.commit()
        conn.close()
    
    def get_campus_info_by_category(self, category: str) -> List[Dict]:
        """Get all campus info for a category"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM campus_info 
            WHERE category = ? AND is_active = 1
        ''', (category,))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results
    
    def insert_event(self, title: str, description: str, start_date: str,
                    location: str, organizer: str = None, category: str = None,
                    end_date: str = None, image_url: str = None,
                    registration_link: str = None):
        """Insert event"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO events 
            (title, description, start_date, end_date, location, organizer, category, image_url, registration_link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, start_date, end_date, location, organizer, category, image_url, registration_link))
        
        conn.commit()
        conn.close()
    
    def get_upcoming_events(self, limit: int = 10) -> List[Dict]:
        """Get upcoming events"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM events 
            WHERE is_active = 1 AND start_date >= datetime('now')
            ORDER BY start_date ASC
            LIMIT ?
        ''', (limit,))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results
    def delete_event(self, event_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
        "DELETE FROM events WHERE id = ?",
        (event_id,)
       )

        conn.commit()
        conn.close()
    def insert_club(self, name: str, description: str, coordinator_name: str,
                   coordinator_email: str, coordinator_phone: str = None,
                   meeting_day: str = None, meeting_time: str = None,
                   location: str = None, members_count: int = 0,
                   logo_url: str = None, website: str = None):
        """Insert club information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO clubs 
            (name, description, coordinator_name, coordinator_email, coordinator_phone,
             meeting_day, meeting_time, location, members_count, logo_url, website)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, description, coordinator_name, coordinator_email, coordinator_phone,
              meeting_day, meeting_time, location, members_count, logo_url, website))
        
        conn.commit()
        conn.close()
    
    def get_all_clubs(self) -> List[Dict]:
        """Get all clubs"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM clubs WHERE is_active = 1')
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results
    def delete_club(self, club_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM clubs WHERE id = ?",
            (club_id,)
         )

        conn.commit()
        conn.close()
    def insert_facility(self, name: str, category: str, location: str,
                       description: str = None, hours_open: str = None,
                       hours_close: str = None, contact_name: str = None,
                       contact_email: str = None, contact_phone: str = None,
                       capacity: int = None, amenities: str = None):
        """Insert facility information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO facilities 
            (name, category, location, description, hours_open, hours_close,
             contact_name, contact_email, contact_phone, capacity, amenities)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, category, location, description, hours_open, hours_close,
              contact_name, contact_email, contact_phone, capacity, amenities))
        
        conn.commit()
        conn.close()
    
    def get_facilities_by_category(self, category: str) -> List[Dict]:
        """Get facilities by category"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM facilities 
            WHERE category = ? AND is_active = 1
        ''', (category,))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results
    def delete_facility(self, facility_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
        "DELETE FROM facilities WHERE id = ?",
        (facility_id,)
       )

        conn.commit()
        conn.close()
    def insert_location(self, place_name: str, building: str, floor: str,
                       latitude: float = None, longitude: float = None,
                       description: str = None, access_info: str = None):
        """Insert location information"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO locations 
            (place_name, building, floor, latitude, longitude, description, access_info)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (place_name, building, floor, latitude, longitude, description, access_info))
        
        conn.commit()
        conn.close()
    
    def search_location(self, query: str) -> List[Dict]:
        """Search locations"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        search_term = f"%{query}%"
        cursor.execute('''
            SELECT * FROM locations 
            WHERE place_name LIKE ? OR building LIKE ? OR description LIKE ?
        ''', (search_term, search_term, search_term))
        
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results