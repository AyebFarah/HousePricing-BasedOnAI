import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from scraping.base_scraper import BaseScraper
from .utils import normalize_price, parse_relative_date, extract_number

class TayaraScraper(BaseScraper):
    """Scraper complet pour tayara.tn (listings + pages internes)"""

    def find_house_cards(self, soup):
        """Trouve tous les articles immobiliers dans la page"""
        return soup.find_all("article", class_="mx-0")

    def extract_house_data(self, house):
        """Extrait les données d'une annonce (page liste + page interne)"""
        # URL listing
        link_tag = house.find("a", href=True)
        url = f"https://www.tayara.tn{link_tag['href']}" if link_tag else None

        # Titre
        title_tag = house.find("h2", class_="card-title")
        title = title_tag.get_text(strip=True) if title_tag else None

        # Prix
        price_tag = house.find("data", {"value": True})
        price = normalize_price(price_tag.get("value")) if price_tag else None

        # Type de bien (peu fiable en page liste)
        type_tag = house.select_one("div.flex.items-center.space-x-1 span")
        property_type = type_tag.get_text(strip=True) if type_tag else None

        # Localisation + date
        location = None
        date_posted = None
        loc_tags = house.select("div.flex.items-center.space-x-1 span")
        if loc_tags and len(loc_tags) >= 2:
            text = loc_tags[-1].get_text(strip=True)
            parts = text.split(",")
            location = parts[0].strip()
            if len(parts) > 1:
                date_posted = parse_relative_date(parts[1].strip())

        # Image
        img_tag = house.find("img", src=True)
        image_url = img_tag["src"] if img_tag else None

        # Agence
        agency_tag = house.select_one("div.flex.flex-col.items-end span")
        agency = agency_tag.get_text(strip=True) if agency_tag else None

        # Date de scraping
        scrape_date = datetime.today().strftime("%Y-%m-%d")

        # Scraping de la page interne
        details = self.scrape_internal_page(url)

        return {
            "title": title,
            "price": price,
            "type": details.get("type", property_type),
            "transaction_type": details.get("transaction_type"),
            "surface": details.get("surface"),
            "bathrooms": details.get("bathrooms"),
            "rooms": details.get("rooms"),
            "options": details.get("options"),
            "description": details.get("description"),
            "location": location,
            "date_posted": date_posted,
            "image_url": image_url,
            "agency": agency,
            "url": url,
            "scrape_date": scrape_date,
        }

    # -------------------------
    # Parsing robuste des critères internes
    # -------------------------
    def parse_criteria(self, soup):
        """Parse les critères de la page interne (superficie, chambres, etc.)"""
        criteria = {
            "type": None,
            "transaction_type": None,
            "surface": None,
            "rooms": None,
            "bathrooms": None,
            "options": []
        }

        # Les critères sont dans des <li> avec structure complexe de spans
        li_elements = soup.select("ul li")
        
        if not li_elements:
            # Fallback: chercher dans toute la page
            li_elements = soup.find_all("li")
        
        for li in li_elements:
            # Cible UNIQUEMENT les spans avec classes spécifiques (évite span parent)
            label_span = li.select_one("span.text-gray-600\\/80")
            value_span = li.select_one("span.text-gray-700\\/80")
            
            if not label_span or not value_span:
                continue
            
            label = label_span.get_text(strip=True).lower()
            value = value_span.get_text(strip=True)

            # Skip valeurs vides ou zéro
            if not value or value == "0":
                continue

            # Matching intelligent des champs
            if "superficie" in label or "surface" in label:
                criteria["surface"] = extract_number(value)
            elif "chambre" in label or "pièce" in label:
                criteria["rooms"] = extract_number(value)
            elif "bain" in label or "salle" in label:
                criteria["bathrooms"] = extract_number(value)
            elif "transaction" in label:
                criteria["transaction_type"] = value
            elif any(x in label for x in ["type", "bien", "property", "catégorie"]):
                criteria["type"] = value
            else:
                # Stocker les autres infos dans options
                criteria["options"].append(f"{label_span.get_text(strip=True)}: {value}")

        return criteria

    # -------------------------
    # Scraping interne complet
    # -------------------------
    def scrape_internal_page(self, url):
        """Scrape les détails d'une page interne d'annonce"""
        if not url:
            return {}
        
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            print(f"  ⚠️  Erreur HTTP {url}: {e}")
            return {}

        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Parse les critères
        data = self.parse_criteria(soup)

        # Description - avec multiples fallbacks
        desc_tag = soup.select_one("p.whitespace-pre-line")
        if not desc_tag:
            # Fallback 1: chercher p avec text-sm
            desc_tag = soup.find("p", class_=lambda x: x and "text-sm" in x)
        if not desc_tag:
            # Fallback 2: chercher p avec dir="auto"
            desc_tag = soup.find("p", {"dir": "auto"})
        
        data["description"] = desc_tag.get_text(" ", strip=True) if desc_tag else None

        # Debug: afficher si des données manquent
        if not any([data.get("surface"), data.get("rooms"), data.get("bathrooms")]):
            print(f"  ⚠️  Aucun critère trouvé pour: {url}")

        return data