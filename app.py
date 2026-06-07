# app.py
import streamlit as st
import uuid
from datetime import datetime
from config import Config
from src.database import CampusDatabase
from src.document_processor import DocumentProcessor
from src.web_scraper import CampusWebScraper
from src.knowledge_base import KnowledgeBase
from src.llm_handler import LLMHandler
from src.location_service import LocationService
import json
import os

# Page configuration
st.set_page_config(
    page_title="Campus Info Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'db' not in st.session_state:
    st.session_state.db = CampusDatabase()

if 'kb' not in st.session_state:
    st.session_state.kb = KnowledgeBase()

if 'llm_handler' not in st.session_state:
    st.session_state.llm_handler = LLMHandler()

if 'location_service' not in st.session_state:
    st.session_state.location_service = LocationService()

# Custom CSS
st.markdown("""
    <style>
    .main {
        max-width: 1200px;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        gap: 1rem;
    }
    .chat-message.user {
        background-color: #e3f2fd;
    }
    .chat-message.bot {
        background-color: #f5f5f5;
    }
    .card {
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        background-color: #f9f9f9;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🎓 Campus Info Chatbot")
    
    menu_option = st.radio(
        "Navigation",
        ["💬 Chat", "📅 Events", "🎭 Clubs", "🏢 Facilities", 
         "📍 Locations", "❓ FAQs", "⚙️ Admin Panel"]
    )
    
    st.markdown("---")
    
    # Session info
    st.subheader("Session Info")
    st.caption(f"Session ID: {st.session_state.session_id[:8]}...")
    st.caption(f"Messages: {len(st.session_state.chat_history)}")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# Main content
if menu_option == "💬 Chat":
    st.header("Chat with Campus Assistant")
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"**You:** {message['content']}")
            else:
                st.markdown(f"**Bot:** {message['content']}")
    
    # Input section
    st.markdown("---")
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([0.9, 0.1])

        with col1:
            user_input = st.text_input(
                "Ask me anything about campus...",
                placeholder="e.g., Where is the library? How to join coding club?"
            )

        with col2:
            send_button = st.form_submit_button(
                "Send",
                use_container_width=True
            )

    if send_button and user_input:
        # Search knowledge base
        search_results = st.session_state.kb.search(user_input, k=3)
        context = "\n".join([r['content'] for r in search_results])
        
        # Get LLM response
        with st.spinner("Thinking..."):
            response, _ = st.session_state.llm_handler.get_response(
                user_input,
                context=context,
                chat_history=st.session_state.chat_history
            )
        
        # Update chat history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input
        })
        st.session_state.chat_history.append({
            'role': 'bot',
            'content': response
        })
        
        # Save to database
        st.session_state.db.save_query(
            user_input,
            response,
            st.session_state.session_id
        )
        
        st.rerun()

elif menu_option == "📅 Events":
    st.header("📅 Upcoming Events")
    
    events = st.session_state.db.get_upcoming_events(limit=20)
    
    if events:
        for event in events:
            with st.container():
                col1, col2 = st.columns([0.7, 0.3])
                
                with col1:
                    st.subheader(event['title'])
                    st.write(f"**Date:** {event['start_date']}")
                    st.write(f"**Location:** {event['location']}")
                    if event['description']:
                        st.write(f"**Description:** {event['description']}")
                    if event['organizer']:
                        st.write(f"**Organizer:** {event['organizer']}")
                
                with col2:
                    if event['registration_link']:
                        st.markdown(f"[Register →]({event['registration_link']})")
                    st.caption(f"Category: {event['category']}")
            
            st.divider()
    else:
        st.info("No upcoming events found.")

elif menu_option == "🎭 Clubs":
    st.header("🎭 Student Clubs")
    
    clubs = st.session_state.db.get_all_clubs()
    
    if clubs:
        # Search/filter
        search_term = st.text_input("Search clubs...", placeholder="e.g., Coding, Drama")
        
        filtered_clubs = [
            club for club in clubs
            if search_term.lower() in club['name'].lower() or
               search_term.lower() in club['description'].lower()
        ] if search_term else clubs
        
        for club in filtered_clubs:
            with st.container():
                st.subheader(f"🎭 {club['name']}")
                st.write(club['description'])
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Coordinator:** {club['coordinator_name']}")
                    st.write(f"**Email:** {club['coordinator_email']}")
                
                with col2:
                    if club['coordinator_phone']:
                        st.write(f"**Phone:** {club['coordinator_phone']}")
                    if club['meeting_day']:
                        st.write(f"**Meets:** {club['meeting_day']} at {club['meeting_time']}")
                
                with col3:
                    if club['location']:
                        st.write(f"**Location:** {club['location']}")
                    st.write(f"**Members:** {club['members_count']}")
                
                if st.button(f"Contact {club['name']}", key=f"contact_{club['id']}"):
                    st.success(f"Email: {club['coordinator_email']}")
            
            st.divider()
    else:
        st.info("No clubs found. Check back soon!")

elif menu_option == "🏢 Facilities":
    st.header("🏢 Campus Facilities")
    
    # Category filter
    categories = [
        "All",
        "Academic",
        "Food & Dining",
        "Health & Wellness",
        "Recreation",
        "Administrative"
    ]
    
    selected_category = st.selectbox("Filter by category:", categories)
    
    if selected_category == "All":
        # Get all facilities (you'll need to add this method)
        facilities = []
        for cat in categories[1:]:
            facilities.extend(st.session_state.db.get_facilities_by_category(cat))
    else:
        facilities = st.session_state.db.get_facilities_by_category(selected_category)
    
    if facilities:
        for facility in facilities:
            with st.container():
                st.subheader(f"📍 {facility['name']}")
                st.write(f"**Category:** {facility['category']}")
                st.write(f"**Location:** {facility['location']}")
                
                if facility['description']:
                    st.write(f"**Description:** {facility['description']}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if facility['hours_open']:
                        st.write(f"⏰ **Hours:** {facility['hours_open']} - {facility['hours_close']}")
                    if facility['capacity']:
                        st.write(f"**Capacity:** {facility['capacity']}")
                
                with col2:
                    if facility['contact_name']:
                        st.write(f"**Contact:** {facility['contact_name']}")
                    if facility['contact_phone']:
                        st.write(f"**Phone:** {facility['contact_phone']}")
                
                if facility['amenities']:
                    amenities = facility['amenities'].split(',')
                    st.write("**Amenities:** " + ", ".join([a.strip() for a in amenities]))
            
            st.divider()
    else:
        st.info("No facilities found in this category.")

# elif menu_option == "📍 Locations":
#     st.header("📍 Campus Locations")
    
#     location_search = st.text_input("Search location...", placeholder="e.g., Library, Cafeteria")
    
#     if location_search:
#         locations = st.session_state.db.search_location(location_search)
        
#         if locations:
#             for location in locations:
#                 with st.container():
#                     st.subheader(location['place_name'])
                    
#                     col1, col2 = st.columns(2)
                    
#                     with col1:
#                         st.write(f"**Building:** {location['building']}")
#                         st.write(f"**Floor:** {location['floor']}")
                    
#                     with col2:
#                         if location['latitude']:
#                             st.write(f"**Coordinates:** {location['latitude']}, {location['longitude']}")
                    
#                     if location['description']:
#                         st.write(f"**Info:** {location['description']}")
                    
#                     if location['access_info']:
#                         st.info(f"**Access:** {location['access_info']}")
                
#                 st.divider()
#         else:
#             st.warning("Location not found.")
#     else:
#         st.info("Enter a location name to search.")
elif menu_option == "📍 Locations":
    st.header("📍 Campus Locations")

    location_search = st.text_input(
        "Search location...",
        placeholder="e.g., Library, LH 105, Chemistry Lab"
    )

    service = st.session_state.location_service

    if location_search:
        locations = service.search_location(location_search)

        if locations:
            for location in locations:
                st.subheader(location["place_name"])
                st.write("Floor:", location.get("floor", "N/A"))
                st.write("Building:", location.get("building", "N/A"))
                st.write("Category:", location.get("category", "N/A"))
                st.divider()
        else:
            st.warning("Location not found")
    else:
        st.info("Enter a location name to search")

elif menu_option == "❓ FAQs":
    st.header("❓ Frequently Asked Questions")
    
    faqs = [
        {
            "question": "How do I register for a club?",
            "answer": "Visit the club's location during their meeting time or contact the coordinator. Most clubs have online registration forms on the student portal."
        },
        {
            "question": "What are the library hours?",
            "answer": "The central library is open from 8:00 AM to 10:00 PM on weekdays. Weekend hours are 9:00 AM to 8:00 PM."
        },
        {
            "question": "How do I access campus WiFi?",
            "answer": "Connect to the 'CampusWifi' network and log in with your student ID and password."
        },
        {
            "question": "Where is the placement cell?",
            "answer": "The Placement Cell is located in Building B, Room 301. Contact: placements@college.edu"
        },
        {
            "question": "How do I request a leave of absence?",
            "answer": "Submit a leave application through the student portal at least 7 days in advance. You'll need approval from your faculty advisor and dean."
        }
    ]
    
    for i, faq in enumerate(faqs):
        with st.expander(faq['question']):
            st.write(faq['answer'])

elif menu_option == "⚙️ Admin Panel":
    st.header("⚙️ Admin Panel")
    
    # Authentication
    admin_password = st.text_input("Enter admin password:", type="password")
    
    if admin_password == "admin123":  # Change this in production
        st.success("Admin access granted")
        
        admin_option = st.radio(
        "Admin Options",
        ["Upload Documents", "Add Event", "Add Club", "Add Facility", "View Analytics"]
        )
        
        if admin_option == "Upload Documents":
            st.subheader("Upload Campus Documents")
            
            uploaded_files = st.file_uploader(
                "Upload PDF documents",
                type=['pdf'],
                accept_multiple_files=True
            )
            
            if uploaded_files and st.button("Process Documents"):
                processor = DocumentProcessor()
                doc_processor = DocumentProcessor()
                
                for uploaded_file in uploaded_files:
                    with st.spinner(f"Processing {uploaded_file.name}..."):
                        # Save temporarily
                        temp_path = f"./temp/{uploaded_file.name}"
                        os.makedirs("./temp", exist_ok=True)
                        with open(temp_path, 'wb') as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Process
                        documents = doc_processor.process_handbook(temp_path)
                        num_docs = st.session_state.kb.add_documents(documents)
                        
                        st.success(f"Added {num_docs} chunks from {uploaded_file.name}")
        
        elif admin_option == "Add Event":
            st.subheader("Add New Event")
            
            with st.form("add_event_form"):
                title = st.text_input("Event Title")
                description = st.text_area("Description")
                start_date = st.date_input("Start Date")
                location = st.text_input("Location")
                organizer = st.text_input("Organizer")
                category = st.selectbox("Category", ["Academic", "Sports", "Cultural", "Technical", "Social"])
                
                if st.form_submit_button("Add Event"):
                    st.session_state.db.insert_event(
                        title, description, str(start_date),
                        location, organizer, category
                    )
                    st.success("Event added successfully!")
        
        elif admin_option == "Add Club":
            st.subheader("Add New Club")
            
            with st.form("add_club_form"):
                name = st.text_input("Club Name")
                description = st.text_area("Description")
                coordinator_name = st.text_input("Coordinator Name")
                coordinator_email = st.text_input("Coordinator Email")
                coordinator_phone = st.text_input("Coordinator Phone")
                meeting_day = st.selectbox("Meeting Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
                meeting_time = st.time_input("Meeting Time")
                location = st.text_input("Location")
                
                if st.form_submit_button("Add Club"):
                    st.session_state.db.insert_club(
                        name, description, coordinator_name,
                        coordinator_email, coordinator_phone,
                        meeting_day, str(meeting_time), location
                    )
                    st.success("Club added successfully!")
        elif admin_option == "Add Facility":
            st.subheader("Add New Facility")

            with st.form("add_facility_form"):
               name = st.text_input("Facility Name")
               category = st.selectbox(
              "Category",
              ["Academic", "Food & Dining", "Health & Wellness",
              "Recreation", "Administrative"]
            )

            location = st.text_input("Location")
            description = st.text_area("Description")

            hours_open = st.text_input("Open Time")
            hours_close = st.text_input("Close Time")

            contact_name = st.text_input("Contact Person")
            contact_phone = st.text_input("Contact Phone")

            capacity = st.number_input("Capacity", min_value=0)

            amenities = st.text_input(
            "Amenities (comma separated)"
            )

            if st.form_submit_button("Add Facility"):

                 st.session_state.db.insert_facility(
                   name,
                   category,
                   location,
                   description,
                   hours_open,
                   hours_close,
                   contact_name,
                   contact_phone,
                   capacity,
                   amenities
               )

            st.success("Facility added successfully!")
        elif admin_option == "View Analytics":
            st.subheader("Analytics")
            
            recent_queries = st.session_state.db.get_query_history(limit=10)
            
            st.metric("Total Queries", len(recent_queries))
            st.metric("Active Clubs", len(st.session_state.db.get_all_clubs()))
            st.metric("Upcoming Events", len(st.session_state.db.get_upcoming_events()))
            
            if recent_queries:
                st.subheader("Recent Queries")
                for query in recent_queries:
                    st.write(f"**Q:** {query['query']}")
                    st.write(f"**A:** {query['response'][:100]}...")
                    st.caption(query['timestamp'])
                    st.divider()
    else:
        if admin_password:
            st.error("Invalid password")

# Footer
st.markdown("---")
st.markdown("👨‍💻 Campus Info Chatbot | By Vaishnavi, Sreshta, and Nithya")