from datetime import datetime
from .utils import normalize_price, calculate_discount
from scraping.base_scraper import BaseScraper

class CherryBeautyScraper(BaseScraper):
    """Scraper spécifique pour cherrybeauty.tn"""
    
    def find_product_cards(self, soup):
        return soup.find_all("div", class_="js-product-miniature")
    
    def extract_product_data(self, product, category_url):
        product_id = product.get("data-id-product")
        
        # URL et titre
        link_tag = product.select_one("div.product_name > a")
        url = link_tag["href"] if link_tag else None
        title = link_tag.get_text(strip=True) if link_tag else None
        
        # Images
        img_tag = product.select_one("picture img")
        img_small = img_tag.get("src") if img_tag else None
        img_large = img_tag.get("data-src") if img_tag else img_small
        
        # Prix
        price_tag = product.select_one("span.price")
        price_raw = price_tag.get_text(strip=True).replace("\xa0", " ") if price_tag else None
        price = normalize_price(price_raw)
        
        # Prix original
        original_tag = product.select_one("span.regular-price")
        original_raw = original_tag.get_text(strip=True).replace("\xa0", " ") if original_tag else None
        price_original = normalize_price(original_raw)
        
        # Réduction
        discount_tag = product.select_one("li.label-flag.type-discount > span")
        discount_percent = None
        if discount_tag:
            discount_percent = normalize_price(discount_tag.get_text(strip=True).replace("%", ""))
        else:
            discount_percent = calculate_discount(price, price_original)
        
        # Type de promo
        promo_type = "Standard"
        if discount_tag:
            promo_type = "Promotion"
        
        # Catégorie
        category_tag = product.select_one("div.ax-product-cats > a")
        category = category_tag.get_text(strip=True) if category_tag else None
        
        # Description courte
        description = title
        
        return {
            "id": product_id,
            "title": title,
            "category": category,
            "price_raw": price_raw,
            "price": price,
            "price_original_raw": original_raw,
            "price_original": price_original,
            "discount_percent": discount_percent,
            "url": url,
            "image_small": img_small,
            "image_large": img_large,
            "description": description,
            "promo_type": promo_type,
            "scrape_date": datetime.today().strftime("%Y-%m-%d")
        }
