from .scraper_tayaratn import TayaraScraper
from .scraper_mubawab import MubawabScraper

if __name__ == "__main__":
    
    # URLs
    tayara_urls = [
        "https://www.tayara.tn/listing/c/immobilier",
        "https://www.tayara.tn/listing/c/immoneuf",
    ]
    
    mubawab_urls = [
        "https://www.mubawab.tn/fr/sc/appartements-a-vendre",
        "https://www.mubawab.tn/fr/sc/appartements-a-louer"
    ]
    
    # Scraping tayaratn
    # tayara_scraper = TayaraScraper(tayara_urls, 'tayaratn_data.csv')
    # tayara_scraper.run()
    
    # Scraping mubawab
    mubawab_scraper = MubawabScraper(mubawab_urls, 'mubawab_data.csv')
    mubawab_scraper.run()
    
    