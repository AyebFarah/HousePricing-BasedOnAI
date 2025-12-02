import requests
from bs4 import BeautifulSoup
import time
import os

def explore_tayara():
    """Script d'exploration pour parcourir toutes les pages de tayara.tn"""

    base_url = "https://www.tayara.tn/listing/c/immobilier/?page="
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    page_num = 1
    total_annonces = 0

    # Créer le dossier pour sauvegarder les HTML si non existant
    os.makedirs('../../data/raw', exist_ok=True)

    while True:
        url = base_url + str(page_num)
        print(f"\nConnexion à {url} ...")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            print(f"Status Code: {response.status_code}, Taille de la page: {len(response.content)} bytes")

            soup = BeautifulSoup(response.content, 'lxml')

            # Sauvegarder le HTML pour inspection
            html_file = f'../../data/raw/tayara_page_{page_num}.html'
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            print(f" HTML sauvegardé dans {html_file}")

            # Trouver les annonces
            articles = soup.find_all('article')
            if not articles:  # plus d'annonces → fin de la boucle
                print("\n Plus d'annonces trouvées, fin du scraping.")
                break

            print(f"Page {page_num} : {len(articles)} annonces trouvées")
            total_annonces += len(articles)

            # Optionnel : afficher première annonce pour vérification
            first = articles[0]
            print(f"Première balise: {first.name}, Classes: {first.get('class', [])}")

            page_num += 1
            time.sleep(1)  # pause pour ne pas surcharger le serveur

        except requests.exceptions.RequestException as e:
            print(f" Erreur de connexion: {e}")
            break
        except Exception as e:
            print(f" Erreur: {e}")
            break

    print(f"\nScraping terminé. Total d'annonces trouvées: {total_annonces}")

if __name__ == "__main__":
    explore_tayara()
