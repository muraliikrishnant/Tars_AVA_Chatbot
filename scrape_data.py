import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_tars_group():
    url = "https://tarsgroup.co/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract all text, cleaning up whitespace
        text_content = soup.get_text(separator=' ', strip=True)
        
        # Basic cleaning
        clean_text = " ".join(text_content.split())
        
        print(f"Successfully scraped {len(clean_text)} characters from {url}")
        
        # Save to a file for the backend to load
        os.makedirs("backend/data", exist_ok=True)
        with open("backend/data/company_info.txt", "w") as f:
            f.write(clean_text)
            
        return clean_text
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

if __name__ == "__main__":
    scrape_tars_group()
