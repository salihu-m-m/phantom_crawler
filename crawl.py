from urllib import response
from urllib.parse import urlparse
from bs4 import BeautifulSoup, Tag
from urllib.parse import urlparse, urljoin
from typing import TypedDict
import requests

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]



  


def normalize_url(url):
    parsed_url = urlparse(url)
    full_path = f"{parsed_url.netloc}{parsed_url.path}"
    full_path = full_path.rstrip("/")
    return full_path.lower()
def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    h1_tag = soup.find("h1")
    if h1_tag and isinstance(h1_tag, Tag):
        return h1_tag.get_text(strip=True)
    h2_tag = soup.find("h2")
    if h2_tag and isinstance(h2_tag, Tag):
        return h2_tag.get_text()    
    return ""
def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    if main_tag := soup.find("main"):
        if p_tag := main_tag.find("p"):
            if isinstance(p_tag, Tag):
                return p_tag.get_text(strip=True)
    if p_tag := soup.find("p"):
        if isinstance(p_tag, Tag):
            return p_tag.get_text(strip=True)
    return ""
def get_urls_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    urls = [] 
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        urljoined = urljoin(base_url, href)
        urls.append(urljoined)
    return urls
def get_images_from_html(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    image_urls = []
    for img_tag in soup.find_all("img", src=True):
        src = img_tag["src"]
        urljoined = urljoin(base_url, src)
        image_urls.append(urljoined)
    return image_urls
def extract_page_data(html: str, base_url: str) -> PageData:
    return {
        "url": base_url,
        "heading": get_heading_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, base_url),
        "image_urls": get_images_from_html(html, base_url)  
    }
def get_html(url: str) -> str:

    try:
        response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"}, timeout=10)
    
        if response.status_code >= 400:
            raise ValueError(f"Error fetching {url}: HTTP {response.status_code}")
        if "text/html" not in response.headers.get("content-Type", ""):
            raise ValueError(f"Error fetching {url}: content-Type is not text/html")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error fetching {url}: {e}")
    return response.text
def crawl_page(base_url, current_url=None, page_data=None):
    if current_url is None:
        current_url = base_url
    if page_data is None:
        page_data = {}
    base_parsed = urlparse(base_url)
    current_parsed = urlparse(current_url)
    if current_parsed.netloc != base_parsed.netloc:
        return page_data
    normalized_current_url = normalize_url(current_url) 
    if normalized_current_url in page_data:
        return page_data
    try:
        html = get_html(current_url)
    except Exception as e:
        print(f"Error occurred while fetching {current_url}: {e}")
        return page_data
    print(f"html type: {type(html)}, value: {html[:100] if html else html}")

    
    page_data[normalized_current_url] = extract_page_data(html, current_url)
    for link in page_data[normalized_current_url]["outgoing_links"]:
        if link not in page_data:
            page_data =crawl_page(base_url, link, page_data)
    return page_data    
        
    




