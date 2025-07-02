import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract title + paragraph content
        paragraphs = soup.find_all('p')
        page_text = "\n".join(p.get_text() for p in paragraphs if len(p.get_text()) > 40)

        return page_text.strip()
    except Exception as e:
        print("URL error:", e)
        return None
