from .beautystore_scraper import BeautyStoreScraper
from .cherrybeauty_scraper import CherryBeautyScraper
from .cosmetique_scraper import CosmetiqueScraper

if __name__ == "__main__":
    
    # URLs
    cosmetique_urls = [
        "https://cosmetique.tn/promotions",
        "https://cosmetique.tn/10-maquillage",
        "https://cosmetique.tn/242-visages",
        "https://cosmetique.tn/226-corps_Corps",
        "https://cosmetique.tn/76-cheveux-soins-cosmetique",
        "https://cosmetique.tn/12-produit-solaires-tunisie",
        "https://cosmetique.tn/84-maman-bebe",
        "https://cosmetique.tn/82-parfums",
        "https://cosmetique.tn/91-para-tun",
    ]
    
    beautystore_urls = [
        "https://beautystore.tn/164-promos",
        "https://beautystore.tn/363-coffrets",
        "https://beautystore.tn/10-ongles",
        "https://beautystore.tn/12-levres",
        "https://beautystore.tn/11-yeux",
        "https://beautystore.tn/6-teint",
        "https://beautystore.tn/14-soin",
        "https://beautystore.tn/272-cheveux",
        "https://beautystore.tn/7-accessoires",
        "https://beautystore.tn/330-solaire",
        "https://beautystore.tn/404-black-friday-"
    ]
    
    cherrybeauty_urls = [
        "https://cherrybeauty.tn/promotions", 
        "https://cherrybeauty.tn/6-visage",
        "https://cherrybeauty.tn/3-onglerie",
        "https://cherrybeauty.tn/81-parfums",
        "https://cherrybeauty.tn/83-hygiene",
        "https://cherrybeauty.tn/8-soins-bebe",
        "https://cherrybeauty.tn/4-epilation-rasage",
        "https://cherrybeauty.tn/7-corps-mains-pieds",
        "https://cherrybeauty.tn/61-maquillage-teint",
        "https://cherrybeauty.tn/60-maquillage-levres",
        "https://cherrybeauty.tn/59-cherry-beauty-maquillage-yeux",
        "https://cherrybeauty.tn/46-cheveux-coiffure",
        "https://cherrybeauty.tn/10-homme"
    ] 
    
    # # Scraping Cosmetique
    cosmetique_scraper = CosmetiqueScraper(cosmetique_urls, 'cosmetiquetn_data.csv')
    cosmetique_scraper.run()
    
    # # Scraping BeautyStore
    beautystore_scraper = BeautyStoreScraper(beautystore_urls, 'beautystore_products.csv')
    beautystore_scraper.run()
    
    # # Scraping CherryBeauty
    cherrybeauty_scraper = CherryBeautyScraper(cherrybeauty_urls, 'cherrybeauty_data.csv')
    cherrybeauty_scraper.run()
    
    
    