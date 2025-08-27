import csv
import requests
from bs4 import BeautifulSoup
from pathlib import Path

class CountryCodeExtractor:
    def __init__(self):
        self.url = "https://www.iban.com/country-codes"
        self.output_file = Path("country_codes.csv")
    
    def fetch_html(self):
        response = requests.get(self.url)
        response.raise_for_status()
        return response.text
    
    def extract_table_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')
        
        headers = []
        header_row = table.find('thead').find('tr') if table.find('thead') else table.find('tr')
        if header_row:
            headers = [th.get_text(strip=True) for th in header_row.find_all('th')]
        
        rows = []
        table_body = table.find('tbody') if table.find('tbody') else table
        for row in table_body.find_all('tr'):
            if row.find('th'):
                continue
            cells = [td.get_text(strip=True) for td in row.find_all('td')]
            if cells and len(cells) == len(headers):
                rows.append(dict(zip(headers, cells)))
        
        return rows
    
    def save_to_csv(self, data):
        with open(self.output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"CSV file saved: {self.output_file}")
    
    def extract(self):
        html = self.fetch_html()
        table_data = self.extract_table_data(html)
        self.save_to_csv(table_data)
        print("Extraction completed successfully")

if __name__ == "__main__":
    extractor = CountryCodeExtractor()
    extractor.extract()
