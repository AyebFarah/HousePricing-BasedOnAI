from datetime import datetime
from .utils import normalize_price, calculate_discount
from scraping.base_scraper import BaseScraper

class CosmetiqueScraper(BaseScraper):
    """Scraper spécifique pour cosmetique.tn"""
    
    def find_product_cards(self, soup):
        products_div = soup.find("div", class_="products")
        return products_div.find_all("div", class_="js-product-miniature-wrapper") if products_div else []
    
    def extract_product_data(self, product, category_url):
        product_id = product.get("data-id-product")
        
        # URL du produit
        link_tag = product.find("a", class_="thumbnail product-thumbnail")
        url = link_tag["href"] if link_tag else None
        
        # Images
        img_tag = product.find("img")
        img_small = img_tag.get("src") if img_tag else None
        img_large = img_tag.get("data-full-size-image-url") if img_tag else None
        
        # Titre et marque
        title_tag = product.find("h2", class_="h3 product-title")
        title = title_tag.get_text(strip=True) if title_tag else None
        brand_tag = product.find("div", class_="product-brand")
        brand = brand_tag.get_text(strip=True) if brand_tag else None
        
        # Référence
        ref_tag = product.find("div", class_="product-reference")
        reference = ref_tag.get_text(strip=True) if ref_tag else None
        
        # Description
        desc_tag = product.find("div", class_="product-description-short")
        description = desc_tag.get_text(" ", strip=True) if desc_tag else None
        
        # Prix
        price_tag = product.find("span", class_="product-price")
        price_raw = price_tag.get_text(strip=True).replace("\xa0", " ") if price_tag else None
        price = normalize_price(price_raw)
        
        # Prix original
        original_tag = product.find("span", class_="regular-price")
        original_raw = original_tag.get_text(strip=True).replace("\xa0", " ") if original_tag else None
        price_original = normalize_price(original_raw)
        
        # Réduction
        discount_tag = product.find("li", class_="product-flag discount")
        discount_text = discount_tag.get_text(strip=True) if discount_tag else None
        discount_percent = None
        if discount_text:
            discount_percent = normalize_price(discount_text.replace("TND", "").replace("-", ""))
        else:
            discount_percent = calculate_discount(price, price_original)
        
        # Type de promo
        promo_type = "Black Friday" if "black-friday" in category_url.lower() else "Standard"
        
        return {
            "id": product_id,
            "title": title,
            "brand": brand,
            "reference": reference,
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
