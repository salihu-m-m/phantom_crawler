from urllib.parse import urlparse
from bs4 import BeautifulSoup, Tag
from urllib.parse import urlparse, urljoin


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