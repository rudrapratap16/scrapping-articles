import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# For bbc content --> WORKING
def bbc(url):
  bbc_html = requests.get(url)
  soup = BeautifulSoup(bbc_html.text, 'html.parser')
  text_blocks = soup.find_all(attrs={'data-component': 'text-block'})
  texts = ''
  for ele in text_blocks:
    texts += ele.get_text()
  return texts

# For Times Of India --> WORKING
def toi(url):
  toi_html = requests.get(url)
  soup = BeautifulSoup(toi_html.text, 'html.parser')
  text_blocks = soup.find_all(attrs={'data-articlebody': '1'})
  texts = ''
  for ele in text_blocks:
    texts += ele.get_text()
  return texts

# For Indian Express --> WORKING
def indianexpress(url):
  indianexpress_html = requests.get(url)
  soup = BeautifulSoup(indianexpress_html.text, 'html.parser')
  text_blocks = soup.find_all(attrs={'class': 'leftpanel'})
  texts = ''
  for ele in text_blocks:
    texts += ele.get_text()
    return texts

# For ndtv news --> Not Working : Reason --> NDTV blocks all scrapers from its website.
def ndtv(url):
  ndtv_html = requests.get(url)
  soup = BeautifulSoup(ndtv_html.text, 'html.parser')
  text_blocks = soup.find_all(attrs={'class': 'stp-wr'})
  texts = ''
  for ele in text_blocks:
    texts += ele.get_text()
  return texts

def fetch_articles(sites):
    load_dotenv()
    api_key = os.getenv('API_KEY')
    search_engine_id = os.getenv('SEARCH_ENGINE_ID')

    # sites = ['indianexpress.com', 'bbc.com', 'timesofindia.indiatimes.com']

    query = 'bjp ' + ' OR '.join(f"site:{site}" for site in sites)
    url = 'https://www.googleapis.com/customsearch/v1'

    # dateRestrict -> 1 year
    # tbm -> Returns only articles

    params = {
        'q': query,
        'key': api_key,
        'cx': search_engine_id,
        "dateRestrict": "y1",
        "tbm": "nws"
    }
    html = requests.get(url, params=params)
    result = html.json()

    links = []

    if 'items' in list(result.keys()):
        for element in result['items']:
            links.append(element['link'])
    
    print(f'Links : {links}')

    articles = {}

    for link in links:
        if 'timesofindia.indiatimes.com' in link:
            if 'TimesOfIndia' not in articles:
                articles['TimesOfIndia'] = [(link, toi(link))]
            else:
                articles['TimesOfIndia'].append((link, toi(link)))
        elif 'bbc.com' in link:
            if 'bbc' not in articles:
                articles['bbc'] = [(link, bbc(link))]
            else:
                articles['bbc'].append((link, bbc(link)))
        elif 'indianexpress.com' in link:
            if 'IndianExpress' not in articles:
                articles['IndianExpress'] = [(link, indianexpress(link))]
            else:
                articles['IndianExpress'].append((link, indianexpress(link)))
    
    return articles