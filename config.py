import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.url = os.getenv("URL", "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1")
        self.content_selector = os.getenv("CONTENT_SELECTOR", "div.mw-parser-output.ws-page-container")