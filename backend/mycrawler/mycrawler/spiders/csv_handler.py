import os
import csv
import logging

class CSVHandler:
    def __init__(self, output_path="output.csv", failed_path="failed_urls.csv"):
        self.output_path = output_path
        self.failed_path = failed_path

        # Logger
        self.logger = logging.getLogger("csv_logger")
        if not self.logger.handlers:
            handler = logging.FileHandler("csv_log.log")
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

        # Initialize CSV files
        self.initialize_csv_files()

    def initialize_csv_files(self):
        """Ensure CSV files exist with proper headers."""
        if not os.path.isfile(self.output_path):
            with open(self.output_path, mode="w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["URL", "Emails", "Phone Numbers", "Social Media Links"])

        if not os.path.isfile(self.failed_path):
            with open(self.failed_path, mode="w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["URL", "Error Reason"])

    def load_existing_csv_data(self):
        """Load existing crawled data to avoid overwriting."""
        data = {}
        if os.path.isfile(self.output_path):
            with open(self.output_path, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader, None)  # Skip header
                for row in reader:
                    if row and len(row) >= 4:
                        data[row[0]] = {
                            "emails": row[1],
                            "phones": row[2],
                            "social_links": row[3],
                        }
        return data

    def save_final_csv(self, crawled_data):
        """Save all extracted data to CSV without overwriting existing entries."""
        try:
            existing_data = self.load_existing_csv_data()
            existing_data.update(crawled_data)  # Merge new data with existing data

            with open(self.output_path, mode="w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["URL", "Emails", "Phone Numbers", "Social Media Links"])
                for url, data in existing_data.items():
                    writer.writerow([url, data.get("emails", ""), data.get("phones", ""), data.get("social_links", "")])

            self.logger.info(f"Successfully saved {len(existing_data)} entries to CSV")
        except Exception as e:
            self.logger.error(f"Error saving CSV: {e}")

    def log_failed_url(self, url, reason):
        """Log failed URLs into a separate CSV."""
        try:
            with open(self.failed_path, mode="a", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([url, reason])
            self.logger.warning(f"Logged failed URL: {url} - Reason: {reason}")
        except Exception as e:
            self.logger.error(f"Error logging failed URL: {e}")
