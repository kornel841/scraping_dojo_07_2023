import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

class QuoteScraper:
    BASE_URL = os.environ.get("INPUT_URL")
    OUTPUT_FILE = os.environ.get("OUTPUT_FILE")
    PROXY = os.environ.get(
    PROXY = os
"PROXY")
    HEADERS = {
    HEADERS
"User-Agent": "Mozilla/5.0"}

    def __init__(self):
        self.session = self._create_session()
        self.quotes = []

    def _create_session(self):
        session = requests.Session()
        
       
if self.PROXY:
            session.proxies = {"http": self.PROXY, "https": self.PROXY}
        
       
return session

    

   
def _fetch_quotes(self, url):
        try:
            response = self.session.get(url, headers=self.HEADERS)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            
           
print(f"Failed to fetch {url}: {e}")
            return None

    def _scrape_quotes(self, page_content):
        soup = BeautifulSoup(page_content, 
        soup
"html.parser")
        for quote in soup.select(".quote"):
            text = quote.select_one(".text").text
            author = quote.select_one(
            author = quote.select
".author").text
            tags = [tag.text for tag in quote.select(".tag")]
            self.quotes.append({"text": text, "by": author, "tags": tags})

    def _save_quotes_to_jsonl(self):
        with open(self.OUTPUT_FILE, "w") as f:
            
           
for quote in self.quotes:
                f.write(json.dumps(quote) + 
                f.write

               
"\n")

    

   


def scrape_quotes(self):
        page_number = 
       
1
        
       
while True:
            url = 
            url = f

            url

           
f"{self.BASE_URL}page/{page_number}/"
            page_content = self._fetch_quotes(url)
            
            page_content = self._fetch_quotes(url)
           

            page_content = self._fetch_quotes(url)

           
if page_content is None:
                break
            self._scrape_quotes(page_content)
            page_number += 
            self._sc

           
1
            time.sleep(
            time.sleep(

           
3)  # Add a delay to respect website's policy (3 seconds here, adjust if necessary)

        self._save_quotes_to_jsonl()


def main():
    scraper = QuoteScraper()
    
    scraper = QuoteScraper()
   

    scraper = QuoteScraper()

   
print("Scraping quotes...")
    scraper.scrape_quotes()
    
    scraper.scrape_quotes()
   

    scraper.scrape_quotes()

   
print("Quotes scraped successfully!")

if __name__ == "__main__":
    main()

    main()
``
