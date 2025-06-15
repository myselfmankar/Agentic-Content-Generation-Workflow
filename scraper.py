from playwright.sync_api import sync_playwright 
from bs4 import BeautifulSoup
import re

def fetch_content(url, selector):
    with sync_playwright() as p:
        browser =  p.chromium.launch(headless=True)
        page =  browser.new_page()
        try:
            print(f"Fetching content from {url} with selector {selector}")
            page.goto(url, timeout=60000)
            print(f"Now taking a screenshot of the page")
            page.screenshot(path='chapter_screenshot.png', full_page=True)
            content_container = page.locator(selector)
            html_content =  content_container.inner_html()
            return html_content
        except Exception as e:
            print(e)
            return None
        finally:
            browser.close()


def clean_html(html_content):
    if not html_content:
        return "---NO_HTML_CONTENT---"
    print("Cleaning HTML content")
    soup = BeautifulSoup(html_content, 'html.parser')
    print("Removing unwanted elements")
    for pagenum in soup.select('span.pagenum'):
        pagenum.decompose()
    text = soup.get_text(separator=' ', strip=True)
    text = re.sub(r'\s+', ' ', text) 
    return text


def fetch_and_clean(url, selector):
    html_content =  fetch_content(url, selector)
    return clean_html(html_content)


