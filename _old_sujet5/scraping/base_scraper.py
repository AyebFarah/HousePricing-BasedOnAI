import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from .utils import save_to_csv


class BaseScraper(ABC):
    """Classe de base pour tous les scrapers"""
    
    def __init__(self, urls, output_file):
        self.urls = urls
        self.output_file = output_file
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        self.all_products = []
    
    @abstractmethod
    def extract_product_data(self, product, category_url):
        """Méthode abstraite à implémenter par chaque scraper"""
        pass
    
    @abstractmethod
    def find_product_cards(self, soup):
        """Méthode abstraite pour trouver les cartes produits"""
        pass
    
    def scrape_page(self, page_url):
        """Scrape une page et retourne le soup"""
        try:
            response = requests.get(page_url, headers=self.headers, timeout=20)
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except Exception as e:
            print(f"❌ Error loading {page_url}: {e}")
            return None
    
    def scrape_category(self, url):
        """Scrape toutes les pages d'une catégorie"""
        print(f"Category URL: {url}")
        page_num = 1
        
        while True:
            page_url = f"{url}?page={page_num}" if page_num > 1 else url
            soup = self.scrape_page(page_url)
            
            if not soup:
                break
            
            products_div = soup.find("div", class_="products")
            if not products_div:
                print("⚠️ Aucun div.products trouvé — fin de pagination.\n")
                break
            
            product_cards = self.find_product_cards(soup)
            if not product_cards:
                print("⚠️ Aucun produit trouvé sur cette page — fin de pagination.\n")
                break
            
            print(f"  → Page {page_num} : {len(product_cards)} produits trouvés")
            
            for product in product_cards:
                data = self.extract_product_data(product, url)
                self.all_products.append(data)
            
            page_num += 1
    
    def run(self):
        """Lance le scraping complet"""
        print("=== SCRAPING START ===\n")
        
        for url in self.urls:
            self.scrape_category(url)
        
        print("\n=== SCRAPING END ===")
        print(f"Total produits scrapés: {len(self.all_products)}")
        
        save_to_csv(self.all_products, self.output_file)
        return self.all_products

