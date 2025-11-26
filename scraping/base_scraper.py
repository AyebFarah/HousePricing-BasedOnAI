import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from .utils import save_to_csv

class BaseScraper(ABC):
    """Classe de base pour tous les scrapers immobiliers"""

    def __init__(self, urls, output_file):
        self.urls = urls
        self.output_file = output_file
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.all_houses = []

    @abstractmethod
    def find_house_cards(self, soup):
        """Doit retourner la liste des div/article qui contiennent un bien"""
        pass

    @abstractmethod
    def extract_house_data(self, house):
        """Doit extraire les données d'un bien"""
        pass

    def scrape_page(self, page_url):
        """Scrape une page et retourne le BeautifulSoup"""
        try:
            response = requests.get(page_url, headers=self.headers, timeout=20)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(f"❌ Error loading {page_url}: {e}")
            return None

    def scrape_category(self, url):
        """Scrape toutes les pages d'une catégorie / ville"""
        print(f"=== Scraping category: {url} ===")
        page_num = 1

        while True:
            page_url = f"{url}?page={page_num}" if page_num > 1 else url
            soup = self.scrape_page(page_url)
            if not soup:
                break

            house_cards = self.find_house_cards(soup)
            if not house_cards:
                print(f"⚠️ Aucun bien trouvé sur la page {page_num}, fin de scraping.\n")
                break

            print(f"  → Page {page_num} : {len(house_cards)} biens trouvés")

            for house in house_cards:
                data = self.extract_house_data(house, url)
                print(data)
                self.all_houses.append(data)

            page_num += 1

    def run(self):
        """Lance le scraping complet"""
        print("=== SCRAPING START ===\n")
        for url in self.urls:
            self.scrape_category(url)

        print("\n=== SCRAPING END ===")
        print(f"Total biens scrapés: {len(self.all_houses)}")
        save_to_csv(self.all_houses, self.output_file)
        return self.all_houses
