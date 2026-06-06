import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Dict
import time

class CampusWebScraper:
    def _init_(self, timeout: int = 10, max_pages: int = 50):
        self.timeout = timeout
        self.max_pages = max_pages
        self.visited_urls = set()
        self.headers = {
            'User-Agent': 'Campus Chatbot/1.0 (+https://yoursite.com/bot)'
        }
    
    def fetch_page(self, url: str) -> str:
        """Fetch webpage content"""
        try:
            response = requests.get(url, timeout=self.timeout, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_text_from_html(self, html: str) -> str:
        """Extract text from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def scrape_events_page(self, events_url: str) -> List[Dict]:
        """Scrape events from a specific page"""
        html = self.fetch_page(events_url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        events = []
        
        # This is flexible - adapt selectors to your campus website
        event_elements = soup.find_all('div', class_='event-item')
        
        for event in event_elements:
            try:
                title = event.find('h3', class_='event-title')
                date = event.find('span', class_='event-date')
                location = event.find('span', class_='event-location')
                description = event.find('p', class_='event-description')
                
                events.append({
                    'title': title.text.strip() if title else 'N/A',
                    'date': date.text.strip() if date else 'N/A',
                    'location': location.text.strip() if location else 'N/A',
                    'description': description.text.strip() if description else 'N/A',
                    'source': events_url
                })
            except Exception as e:
                print(f"Error parsing event: {e}")
                continue
        
        return events
    
    def scrape_clubs_page(self, clubs_url: str) -> List[Dict]:
        """Scrape clubs information"""
        html = self.fetch_page(clubs_url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        clubs = []
        
        club_elements = soup.find_all('div', class_='club-card')
        
        for club in club_elements:
            try:
                name = club.find('h3', class_='club-name')
                description = club.find('p', class_='club-description')
                contact = club.find('span', class_='club-contact')
                
                clubs.append({
                    'name': name.text.strip() if name else 'N/A',
                    'description': description.text.strip() if description else 'N/A',
                    'contact': contact.text.strip() if contact else 'N/A',
                    'source': clubs_url
                })
            except Exception as e:
                print(f"Error parsing club: {e}")
                continue
        
        return clubs
    
    def scrape_site_recursive(self, start_url: str, domain_only: bool = True) -> List[Dict]:
        """Recursively scrape campus website"""
        documents = []
        to_visit = [start_url]
        
        while to_visit and len(self.visited_urls) < self.max_pages:
            url = to_visit.pop(0)
             
            if url in self.visited_urls: 
                continue
            
            # Check if URL is in same domain
            if domain_only:
                start_domain = urlparse(start_url).netloc 
                current_domain = urlparse(url).netloc
                if start_domain != current_domain:
                    continue
            
            print(f"Scraping: {url}")
            html = self.fetch_page(url)
            
            if not html:
                continue
            
            self.visited_urls.add(url)
            
            # Extract text
            text = self.extract_text_from_html(html)
            documents.append({
                'page_content': text,
                'metadata': {
                    'source': url,
                    'type': 'website'
                }
            })
            
            # Extract links
            soup = BeautifulSoup(html, 'html.parser')
            for link in soup.find_all('a', href=True):
                new_url = urljoin(url, link['href'])
                if new_url not in self.visited_urls:
                    to_visit.append(new_url)
            
            time.sleep(1)  # Be respectful
        
        return documents