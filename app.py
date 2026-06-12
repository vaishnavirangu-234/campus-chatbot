# app.py
import streamlit as st
import base64
import uuid
from datetime import datetime
from config import Config
from src.database import CampusDatabase
from src.document_processor import DocumentProcessor
from src.web_scraper import CampusWebScraper
from src.knowledge_base import KnowledgeBase
from src.llm_handler import LLMHandler
from src.location_service import LocationService
from streamlit_option_menu import option_menu
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

def get_base64_image(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

logo_base64 = get_base64_image("assets/logo.png")

# Custom CSS
st.markdown("""
<style>

.block-container {
    max-width: 1200px;
}

.stMetric {
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="
        text-align:center;
        padding:20px;
        border-radius:15px;
        background: linear-gradient(135deg, #111827, #1E3A8A);
        color:white;
        margin-bottom:20px;
    ">
        <h1 style="margin-bottom:5px;">🎓Campus Chatbot</h1>
        <p style="font-size:18px;">
            AI-Powered Campus Assistant
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(
        """
        <div style='text-align:center; color:#9CA3AF; font-size:14px;'>
            👨‍💻 Developed by Team SreNiV❤️
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    menu_option = option_menu(
        menu_title=None,
        options=[
            "Chat",
            "Events",
            "Clubs",
            "Facilities",
            "Locations",
            "FAQs",
            "Admin"
        ],
        icons=[
            "chat-dots",
            "calendar-event",
            "people",
            "building",
            "geo-alt",
            "question-circle",
            "gear"
        ],
        default_index=0
    )

    st.divider()

    st.markdown("### 📊 Dashboard")

    st.metric(
        "Questions Asked",
        len(st.session_state.chat_history) // 2
    )

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):
        st.session_state.chat_history = []
        st.rerun()
# Main content
if menu_option == "Chat":

    st.markdown(f"""
        <style>
        .logo-container {{
            position: fixed;
            top: 30px;
            right: 20px;
            z-index: 9999;
        }}

        .logo-container img {{
            width: 90px;
        }}
        </style>

        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}">
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        # 🎓Campus Chatbot
        ###  Intelligent Campus Assistant
        Get instant information about:
        -  🗓️Events
        -  👥Clubs
        -  🏛️Facilities
        -  📌Campus Locations
        -  💼Placements
        """)

    # Display chat history
    for message in st.session_state.chat_history:

        if message["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(message["content"])

        else:
            with st.chat_message("assistant", avatar="✨"):
                st.markdown(message["content"])
    # for message in st.session_state.chat_history:

    #     role = "assistant"

    #     if message["role"] == "user":
    #         role = "user"

    #     with st.chat_message(role):
    #         st.markdown(message["content"])
    
    # Input section
    st.markdown("---")
    user_input = st.chat_input(
        "Ask anything about campus..."
    )

    if user_input:
        # Search knowledge base
        search_results = st.session_state.kb.search(user_input, k=3)
        context = "\n".join([r['content'] for r in search_results])
        
        # Get LLM response
        with st.chat_message("assistant"):
            with st.spinner("Chatbot is thinking..."):
                response, _ = st.session_state.llm_handler.get_response(
                    user_input,
                    context=context,
                    chat_history=st.session_state.chat_history
                )
                st.markdown(response)
        
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

elif menu_option == "Events":
    st.header("🗓️ Events")
    
    #events = st.session_state.db.get_upcoming_events(limit=20)
    with open("./data/events.json", "r", encoding="utf-8") as f:
      events = json.load(f)
    
    if events:
        for event in events:
            with st.container():
                col1, col2 = st.columns([0.7, 0.3])
                
                with col1:
                    st.markdown(f"### 📢 {event['title']}")
                    st.caption("Source: KUCET Official Website")

                with col2:
                    if event.get('registration_link'):
                        st.link_button(
                            "🔗 View Official Notice",
                            event['registration_link'],
                            use_container_width=True
                        )             
            st.divider()
    else:
        st.info("No events found.")

elif menu_option == "Clubs":
    st.header("👥 Student Clubs")
    
    #clubs = st.session_state.db.get_all_clubs()
    with open("./data/clubs.json", "r", encoding="utf-8") as f:
     clubs = json.load(f)
    
    if clubs:
        # Search/filter
        search_term = st.text_input("Search clubs...", placeholder="e.g., NCC, NSS")
        
        filtered_clubs = [
            club for club in clubs
            if search_term.lower() in club['name'].lower() or
               search_term.lower() in club['description'].lower()
        ] if search_term else clubs
        
        for club in filtered_clubs:
            with st.container():
                if club["category"] == "Defence":
                    icon = "🪖"
                elif club["category"] == "Technical":
                    icon = "💡"
                elif club["category"] == "Academic":
                    icon = "📚"
                elif club["category"] == "Sports":
                    icon = "🏆"
                else:
                    icon = "🌟"

                st.subheader(f"{icon} {club['name']}")
                st.write(club['description'])
                
                col1, col2, col3 = st.columns(3)
                
                # with col1:
                #     st.write(f"**Coordinator:** {club['coordinator_name']}")
                #     st.write(f"**Email:** {club['coordinator_email']}")
                
                # with col2:
                #     if club['coordinator_phone']:
                #         st.write(f"**Phone:** {club['coordinator_phone']}")
                #     if club['meeting_day']:
                #         st.write(f"**Meets:** {club['meeting_day']} at {club['meeting_time']}")
                
                # with col3:
                #     if club['location']:
                #         st.write(f"**Location:** {club['location']}")
                #     st.write(f"**Members:** {club['members_count']}")
                st.write(f"**Category:** {club['category']}")

                st.write(
                    f"**Faculty Coordinator:** "
                    f"{club['faculty_coordinator']}"
                )
                if "contact_email" in club:
                   st.write(f"📧 Email: {club['contact_email']}")

                if "contact_phone" in club:
                   st.write(f"📞 Phone: {club['contact_phone']}")

                   st.write(club['description'])
                # if st.button(f"Contact {club['name']}", key=f"contact_{club['id']}"):
                #     st.success(f"Email: {club['coordinator_email']}")
            
            st.divider()
    else:
        st.info("No clubs found. Check back soon!")

elif menu_option == "Facilities":
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

elif menu_option == "Locations":
    st.header("📌 Campus Locations")

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

elif menu_option == "FAQs":
    st.header("💬 Frequently Asked Questions")
    
    faqs = [
        {
            "question": "Is hostel accommodation available for first-year students?",
            "answer": "No, hostel accommodation is not available for first-year students. Hostel facilities are available starting from the second year."
        },
        {
            "question": "What are the library hours?",
            "answer": "The library is open from 10:30 AM to 5:00 PM. There is a lunch break from 1:30 PM to 2:30 PM."
        },
        {
            "question": "Who should I contact to join NCC?",
            "answer": "To join NCC, please contact the Associate NCC Officer Lt. Dr. K. Vijay Kumar sir. They can provide information about eligibility, enrollment procedures, and training schedules."
        }, 
        {
            "question": "Who should I contact for placement-related information?",
            "answer": "For placement-related information, please contact the Direcor of Training and Placement Placement Officer V. Ramana Babu sir or T&PO Pakala Santhosh Kumar sir. They can provide details about recruitment drives, eligibility criteria, internships, and placement activities."
        },
        {
            "question": "How much is the semester fee?",
            "answer": "The semester fee is ₹1,200. If the fee is paid after the due date, a late fee of ₹250 will be charged, making the total ₹1,450."
        }
    ]
    
    for i, faq in enumerate(faqs):
        with st.expander(faq['question']):
            st.write(faq['answer'])

elif menu_option == "Admin":
    st.header("⚙️ Admin Panel")
    
    # Authentication
    admin_password = st.text_input("Enter admin password:", type="password")
    
    if admin_password == "admin123":  # Change this in production
        st.success("Admin access granted")
        st.subheader("Website Sync")

        if st.button("🔄 Refresh Events From KUCET"):

           scraper = CampusWebScraper()

           events = scraper.scrape_kucet_events()
 
           with open("./data/events.json", "w", encoding="utf-8") as f:
                json.dump(
                  events,
                  f,
                  indent=4,
                  ensure_ascii=False
                )

           st.success(f"Updated {len(events)} events!")

        admin_option = st.radio(
           "Admin Options",
           [
              "Upload Documents", "Add Event", "Add Club", "Add Facility", "View Analytics"
           ]
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

                category = st.selectbox(
                "Category",
                ["Academic", "Sports", "Cultural", "Technical", "Social"]
                )

                submit_event = st.form_submit_button("Add Event")

            if submit_event:
               st.session_state.db.insert_event(
               title,
               description,
               str(start_date),
               location,
               organizer,
               category
               )
               st.success("Event added successfully!")

            st.markdown("---")
            st.subheader("Delete Events")

            events = st.session_state.db.get_upcoming_events(limit=100)

            for event in events:
               col1, col2 = st.columns([4, 1])

               with col1:
                    st.write(f"📅 {event['title']}")

               with col2:
                    if st.button(
                       "🗑 Delete",
                       key=f"event_{event['id']}"
                    ):
                     st.session_state.db.delete_event(event['id'])
                     st.rerun()

        elif admin_option == "Add Club":
           st.subheader("Add New Club")

           with st.form("add_club_form"):
             name = st.text_input("Club Name")
             description = st.text_area("Description")
             coordinator_name = st.text_input("Coordinator Name")
             coordinator_email = st.text_input("Coordinator Email")
             coordinator_phone = st.text_input("Coordinator Phone")

             meeting_day = st.selectbox(
                "Meeting Day",
                 ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
             )

             meeting_time = st.time_input("Meeting Time")
             location = st.text_input("Location")

             submit_club = st.form_submit_button("Add Club")

           if submit_club:
               st.session_state.db.insert_club(
               name,
               description,
               coordinator_name,
               coordinator_email,
               coordinator_phone,
               meeting_day,
               str(meeting_time),
               location
              )
               st.success("Club added successfully!")

           st.markdown("---")
           st.subheader("Delete Clubs")

           clubs = st.session_state.db.get_all_clubs()

           for club in clubs:
              col1, col2 = st.columns([4, 1])

              with col1:
                 st.write(f"🏫 {club['name']}")

              with col2:
                if st.button(
                    "🗑 Delete",
                     key=f"club_{club['id']}"
                ):
                    st.session_state.db.delete_club(club['id'])
                    st.rerun()

        elif admin_option == "Add Facility":
            st.subheader("Add New Facility")

            with st.form("add_facility_form"):
                name = st.text_input("Facility Name")

                category = st.selectbox(
                    "Category",
                    [
                    "Academic",
                    "Food & Dining",
                    "Health & Wellness",
                    "Recreation",
                    "Administrative"
                   ]
                )

                location = st.text_input("Location")
                description = st.text_area("Description")

                hours_open = st.text_input("Open Time")
                hours_close = st.text_input("Close Time")
 
                contact_name = st.text_input("Contact Person")
                contact_phone = st.text_input("Contact Phone")
 
                capacity = st.number_input(
                 "Capacity",
                 min_value=0
                )

                amenities = st.text_input(
                "Amenities (comma separated)"
                )

                submit_facility = st.form_submit_button(
                "Add Facility"
                )

            if submit_facility:
               st.session_state.db.insert_facility(
               name,
               category,
               location,
               description,
               hours_open,
               hours_close,
               contact_name,
               None,
               contact_phone,
               capacity,
               amenities
               )

               st.success("Facility added successfully!")

            st.markdown("---")
            st.subheader("Delete Facilities")

            facilities = []

            for cat in [
               "Academic",
               "Food & Dining",
               "Health & Wellness",
               "Recreation",
               "Administrative"
             ]:
             facilities.extend(
             st.session_state.db.get_facilities_by_category(cat)
            )

            for facility in facilities:
              col1, col2 = st.columns([4, 1])

              with col1:
                 st.write(
                    f"🏢 {facility['name']} ({facility['category']})"
                 )

              with col2:
                 if st.button(
                 "🗑 Delete",
                 key=f"facility_{facility['id']}"
                ):
                  st.session_state.db.delete_facility(
                    facility['id']
                  )
                  st.rerun()

        elif admin_option == "View Analytics":
            st.subheader("📊 Analytics")

            recent_queries = st.session_state.db.get_query_history(limit=10)

            st.metric(
              "Total Queries",
               len(recent_queries)
               )

            st.metric(
               "Active Clubs",
               len(st.session_state.db.get_all_clubs())
              )

            st.metric(
            "Upcoming Events",
            len(st.session_state.db.get_upcoming_events())
            )

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