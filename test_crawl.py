
import unittest
from crawl import get_first_paragraph_from_html, get_heading_from_html, normalize_url, get_urls_from_html, get_images_from_html, extract_page_data  

class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    def test_normalize_url_trailing_slash(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    def test_normalize_url_http(self):
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    def test_normalize_url_no_path(self):
        input_url = "https://www.boot.dev"
        actual = normalize_url(input_url)
        expected = "www.boot.dev"
        self.assertEqual(actual, expected)  
    def test_normalize_url_capitalization(self):
        input_url = "HTTPS://WWW.BOOT.DEV/BLOG/PATH"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)
    def test_get_heading_from_html(self):
     input_html = "<html><body><h1>Test Heading</h1></body></html>"
     actual = get_heading_from_html(input_html)
     expected = "Test Heading"
     self.assertEqual(actual, expected)
    def test_get_heading_from_html_no_h1(self):
     input_html = "<html><body><h2>Test Heading</h2></body></html>"
     actual = get_heading_from_html(input_html)
     expected = "Test Heading"
     self.assertEqual(actual, expected)
    def test_get_heading_from_html_no_headings(self):
     input_html = "<html><body><p>No headings here</p></body></html>"
     actual = get_heading_from_html(input_html)
     expected = ""
     self.assertEqual(actual, expected) 
    def test_get_heading_from_html_whitespace(self):
     input_html = "<html><body><h1>   Test Heading   </h1></body></html>"
     actual = get_heading_from_html(input_html)
     expected = "Test Heading"
     self.assertEqual(actual, expected)
    def test_get_heading_from_html_nested_headings(self):
     input_html = "<html><body><h1>Outer Heading</h1><div><h2>Inner Heading</h2></div></body></html>"
     actual = get_heading_from_html(input_html)
     expected = "Outer Heading"
     self.assertEqual(actual, expected)
    
    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = '''<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)
    def test_get_first_paragraph_from_html_no_main(self):
        input_body = '''<html><body>
            <p>First paragraph.</p>
            <p>Second paragraph.</p>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "First paragraph."
        self.assertEqual(actual, expected)
    def test_get_first_paragraph_from_html_no_paragraphs(self):
        input_body = '''<html><body>
            <div>No paragraphs here.</div>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)
    def test_get_urls_from_html(self):
        input_body = '''<html><body>
            <a href="https://www.example.com">Example</a>
            <a href="https://www.test.com">Test</a>
        </body></html>'''
        base_url = "https://www.example.com"
        actual = get_urls_from_html(input_body, base_url)
        expected = ["https://www.example.com", "https://www.test.com"]
        self.assertEqual(actual, expected)
    def test_get_urls_from_html_relative_urls(self):
        input_body = '''<html><body>
            <a href="/about">About</a>
            <a href="/contact">Contact</a>
        </body></html>'''
        base_url = "https://www.example.com"
        actual = get_urls_from_html(input_body, base_url)
        expected = ["https://www.example.com/about", "https://www.example.com/contact"]
        self.assertEqual(actual, expected)
    def test_get_urls_from_html_a_without_href(self):
        input_body = '''<html><body>
            <a>Missing href</a>
            <a href="https://www.valid.com">Valid Link</a>
        </body></html>'''
        base_url = "https://www.example.com"
        actual = get_urls_from_html(input_body, base_url)
        expected = ["https://www.valid.com"]
        self.assertEqual(actual, expected)
    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)
    def test_get_images_from_html(self):
        input_body = '''<html><body>
            <img src="https://www.example.com/image1.jpg" />
            <img src="https://www.example.com/image2.png" />
        </body></html>'''
        base_url = "https://www.example.com"
        actual = get_images_from_html(input_body, base_url)
        expected = ["https://www.example.com/image1.jpg", "https://www.example.com/image2.png"]
        self.assertEqual(actual, expected)
    def test_get_images_from_html_relative_urls(self):
        input_body = '''<html><body>
            <img src="/images/image1.jpg" />
            <img src="/images/image2.png" />
        </body></html>'''
        base_url = "https://www.example.com"
        actual = get_images_from_html(input_body, base_url)
        expected = ["https://www.example.com/images/image1.jpg", "https://www.example.com/images/image2.png"]
        self.assertEqual(actual, expected)
    def test_get_images_from_html_multiple_images(self):
        input_body = '''<html><body>
            <img src="https://www.example.com/image1.jpg" />
            <img src="https://www.example.com/image2.png" />
            <img src="https://www.example.com/image3.gif" />
        </body></html>'''
        base_url = "https://www.example.com"
        actual = get_images_from_html(input_body, base_url)
        expected = [
            "https://www.example.com/image1.jpg",
            "https://www.example.com/image2.png",
            "https://www.example.com/image3.gif"
        ]
        self.assertEqual(actual, expected)
    def test_get_images_from_html_mixed_content(self):
        input_body = '''<html><body>
            <img src="https://www.example.com/image1.jpg" />
            <p>Some text here.</p>
            <img src="/images/image2.png" />
        </body></html>'''
        base_url = "https://www.example.com"
        actual = get_images_from_html(input_body, base_url)
        expected = [
            "https://www.example.com/image1.jpg",
            "https://www.example.com/images/image2.png"
        ]
        self.assertEqual(actual, expected)
    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"]
        }
        self.assertEqual(actual, expected)
    def test_extract_page_data_no_heading(self):
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"]
        }
        self.assertEqual(actual, expected)
    def test_extract_page_data_no_paragraph(self):
       input_url = "https://crawler-test.com"
       input_body = '''<html><body>
           <h1>Test Title</h1>
           <a href="/link1">Link 1</a>
           <img src="/image1.jpg" alt="Image 1">
       </body></html>'''
       actual = extract_page_data(input_body, input_url)
       expected = {
           "url": "https://crawler-test.com",
           "heading": "Test Title",
           "first_paragraph": "",
           "outgoing_links": ["https://crawler-test.com/link1"],
           "image_urls": ["https://crawler-test.com/image1.jpg"]
       }
       self.assertEqual(actual, expected)
    def test_extract_page_data_no_links_or_images(self):
       input_url = "https://crawler-test.com"
       input_body = '''<html><body>
           <h1>Test Title</h1>
           <p>This is the first paragraph.</p>
       </body></html>'''
       actual = extract_page_data(input_body, input_url)
       expected = {
           "url": "https://crawler-test.com",
           "heading": "Test Title",
           "first_paragraph": "This is the first paragraph.",
           "outgoing_links": [],
           "image_urls": []
       }
       self.assertEqual(actual, expected)
        
    

    
  
if __name__ == "__main__":
    unittest.main()