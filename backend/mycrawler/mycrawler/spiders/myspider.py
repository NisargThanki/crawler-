import os
import csv
import scrapy
import logging
import psycopg2
import re
import sys
sys.path.append(r"C:\Users\DELL\Desktop\mycrawler\backend\mycrawler\mycrawler\spiders")
from csv_handler import CSVHandler
from pattern_store import PatternStore

class MySpider(scrapy.Spider):
    name = "myspider"

    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)

        # Logger Setup
        self.log = logging.getLogger("spider_logger")
        if not self.log.hasHandlers():
            handler = logging.FileHandler("spider_log.log")
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.log.addHandler(handler)
            self.log.setLevel(logging.INFO)

        # Database Config
        self.db_config = {
            "host": os.environ.get("DB_HOST", "localhost"),
            "port": os.environ.get("DB_PORT", "5432"),
            "dbname": os.environ.get("DB_NAME", "crawler"),
            "user": os.environ.get("DB_USER", "postgres"),
            "password": os.environ.get("DB_PASSWORD", "root"),
        }

        # CSV Handler
        self.csv_handler = CSVHandler()
        
        # Load existing data & pending URLs
        self.crawled_data = self.csv_handler.load_existing_csv_data() or {}
        self.pending_urls = self.get_urls_from_csv()

        self.log.info(f"Spider initialized with {len(self.pending_urls)} URLs")

    def get_urls_from_csv(self):
        """Fetch URLs from the given CSV file."""
        urls = []
        csv_path = r"C:\Users\DELL\Desktop\mycrawler\backend\uploads\20_links.csv"
        if os.path.exists(csv_path):
            with open(csv_path, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header
                for row in reader:
                    if row and row[0].strip():
                        url = row[0].strip()
                        if not url.lower().startswith(('http://', 'https://')):
                            url = 'https://' + url
                        urls.append(url)
        return urls

    def start_requests(self):
        """Initiate crawling process."""
        for url in self.pending_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                errback=self.handle_error,
                meta={"original_url": url},
                dont_filter=True
            )

    def parse(self, response):
        """Extract data and update the CSV handler."""
        original_url = response.meta.get("original_url", response.url)
        
        if response.status != 200:
            self.log.warning(f"Skipping {original_url} due to HTTP status {response.status}")
            return

        extracted_data = {
            "url": response.url,
            "emails": self.extract_emails(response.text),
            "phones": self.extract_phone_numbers(response.text),
            "social_links": self.extract_social_links(response.text),
        }

        # Store data in memory and update CSV at the end
        self.crawled_data[original_url] = extracted_data
        self.log.info(f"Total crawled data before saving: {len(self.crawled_data)} entries")
        self.csv_handler.save_final_csv(self.crawled_data)
        

    def handle_error(self, failure):
        """Handle request failures without affecting existing data."""
        original_url = failure.request.meta.get("original_url", failure.request.url)
        self.log.error(f"Request failed for {original_url}")

    def extract_emails(self, text):
        """Extract email addresses using patterns from PatternStore."""
        emails = []
        for pattern in PatternStore.EMAIL_PATTERNS:
            emails.extend(re.findall(pattern, text))
        return list(set(emails))

    def extract_phone_numbers(self, text):
        """Extract phone numbers using patterns from PatternStore."""
        phone_numbers = []
        for pattern in PatternStore.PHONE_PATTERNS:
            phone_numbers.extend(re.findall(pattern, text))
        return list(set(phone_numbers))

    def extract_social_links(self, text):
        """Extract social media links using patterns from PatternStore."""
        social_links = []
        for pattern in PatternStore.SOCIAL_PATTERNS:
            social_links.extend(re.findall(pattern, text))
        return list(set(social_links))
