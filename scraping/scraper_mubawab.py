import requests
from bs4 import BeautifulSoup
from datetime import datetime
from scraping.base_scraper import BaseScraper
from .utils import normalize_price, extract_number

class MubawabScraper(BaseScraper):
    """Scraper complet pour mubawab.tn (listings + pages internes)"""

    def find_house_cards(self, soup):
        """Trouve toutes les annonces dans la page"""
        return soup.find_all("div", class_="listingBox")
    
    def _get_transaction_type_from_url(self, scraped_url):
        """Détermine le type de transaction depuis l'URL"""
        if "appartements-a-vendre" in scraped_url.lower() or "a-vendre" in scraped_url.lower():
            return "vente"
        elif "appartements-a-louer" in scraped_url.lower() or "a-louer" in scraped_url.lower():
            return "location"
        return "unknown"

    def extract_house_data(self, house, scraped_url=None):
        """Extrait les données d'une annonce"""
        # URL listing
        url = house.get("linkref")
        
        # Transaction type depuis l'URL principale
        if scraped_url:
            transaction_type = self._get_transaction_type_from_url(scraped_url)
        else:
            transaction_type = None

        # Titre
        title_tag = house.select_one("h2.listingTit a")
        title = title_tag.get_text(strip=True) if title_tag else None

        # Prix
        price_tag = house.select_one(".priceTag")
        price = normalize_price(price_tag.get_text(strip=True)) if price_tag else None

        # Localisation
        location_tag = house.select_one(".listingH3")
        location = location_tag.get_text(strip=True).replace("\n", " ") if location_tag else None

        # Image principale
        img_tag = house.select_one("div.adSlider img.firstPicture")
        if not img_tag:
            # fallback: première image du slider
            img_tag = house.select_one("div.adSlider img")
        if not img_tag:
            # fallback ultime: n'importe quelle image dans la box
            img_tag = house.find("img")
        image_url = img_tag.get("src") or img_tag.get("data-lazy") if img_tag else None

        # Date de scraping
        scrape_date = datetime.today().strftime("%Y-%m-%d")

        # Données de base depuis la page liste
        list_data = self._extract_list_page_data(house)

        # Scraping page interne pour données complètes
        details = self.scrape_internal_page(url)

        # Fusionner les données (priorité aux détails internes)
        return {
            "title": title,
            "price": price,
            "type": details.get("type") or list_data.get("type"),
            "transaction_type": transaction_type,
            "surface": details.get("surface") or list_data.get("surface"),
            "rooms": details.get("rooms") or list_data.get("rooms"),
            "bathrooms": details.get("bathrooms") or list_data.get("bathrooms"),
            "options": details.get("options", []),
            "description": details.get("description"),
            "location": location,
            "image_url": image_url,
            "url": url,
            "scrape_date": scrape_date,
        }

    def _extract_list_page_data(self, house):
        """Extrait les données basiques depuis la page liste"""
        data = {
            "type": None,
            "surface": None,
            "rooms": None,
            "bathrooms": None
        }
        
        # Chercher dans adDetails
        ad_details = house.select(".adDetailFeature")
        for detail in ad_details:
            text = detail.get_text(strip=True)
            
            if "m²" in text:
                data["surface"] = extract_number(text)
            elif "Chambre" in text:
                data["rooms"] = extract_number(text)
            elif "bain" in text:
                data["bathrooms"] = extract_number(text)
        
        return data

    def parse_internal_page(self, soup):
        """Parse les critères d'une page interne"""
        data = {
            "type": None,
            "surface": None,
            "rooms": None,
            "bathrooms": None,
            "options": [],
            "description": None,
        }

        # === Détails principaux (surface, chambres, salles de bain) ===
        ad_details = soup.select(".adDetailFeature")
        for detail in ad_details:
            text = detail.get_text(strip=True)
            
            if "m²" in text:
                data["surface"] = extract_number(text)
            elif "Chambre" in text:
                data["rooms"] = extract_number(text)
            elif "Salle de bain" in text:
                data["bathrooms"] = extract_number(text)

        # === Caractéristiques générales ===
        # Type de bien
        type_element = soup.select_one(".adMainFeatureContent .adMainFeatureContentLabel:-soup-contains('Type de bien') + .adMainFeatureContentValue")
        if type_element:
            data["type"] = type_element.get_text(strip=True)

        # === Options/Équipements ===
        # Chercher les icônes de caractéristiques
        feature_divs = soup.select(".adFeature")
        for feature in feature_divs:
            if feature.select_one(".extraFeatures"):
                continue
            
            text = feature.get_text(strip=True)
            if text and not text.startswith("+") and len(text) > 2:
                data["options"].append(text)

        # Aussi chercher dans les adMainFeature (État, Étage, etc.)
        main_features = soup.select(".adMainFeature")
        for feature in main_features:
            label = feature.select_one(".adMainFeatureContentLabel")
            value = feature.select_one(".adMainFeatureContentValue")
            if label and value:
                label_text = label.get_text(strip=True)
                value_text = value.get_text(strip=True)
                # Ne pas répéter le type de bien
                if label_text != "Type de bien":
                    data["options"].append(f"{label_text}: {value_text}")

        # === Description ===
        desc_block = soup.select_one(".blockProp p")
        if desc_block:
            data["description"] = desc_block.get_text(" ", strip=True)

        return data

    def scrape_internal_page(self, url):
        """Scrape les détails d'une page interne"""
        if not url:
            return {}

        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            print(f"⚠️  Erreur HTTP {url}: {e}")
            return {}

        soup = BeautifulSoup(resp.text, "html.parser")
        return self.parse_internal_page(soup)