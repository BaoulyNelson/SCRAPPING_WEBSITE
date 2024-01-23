import requests
from bs4 import BeautifulSoup
import csv

def extraire_info_article(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraction des informations
        titre = soup.find('h1').text.strip()
        lien = url

        # Vérification de l'existence de la balise meta avec property='og:image'
        image_tag = soup.find('meta', property='og:image')
        image = image_tag['content'] if image_tag else None

        # Vérification de l'existence de la balise meta avec property='og:description'
        description_tag = soup.find('meta', property='og:description')
        description = description_tag['content'] if description_tag else None

        return {'Titre': titre, 'Lien': lien, 'Image': image, 'Description': description}
    else:
        print(f"Erreur {response.status_code} lors de la récupération de {url}")
        return None

# Fonction principale pour extraire toutes les informations de lenouvelliste.com
def web_scraping_lenouvelliste():
    # URL de la page principale
    url_principale = 'https://lenouvelliste.com/'

    # Récupération du contenu HTML
    response_principale = requests.get(url_principale)

    if response_principale.status_code == 200:
        soup_principale = BeautifulSoup(response_principale.text, 'html.parser')

        # Récupération des liens vers les articles
        liens_articles = [a['href'] for a in soup_principale.select('a[href^="/article/"]')]

        # Liste pour stocker les données extraites
        donnees_articles = []

        # Boucle à travers les liens des articles
        for lien_article in liens_articles:
            url_article = f"https://lenouvelliste.com{lien_article}"
            info_article = extraire_info_article(url_article)

            if info_article:
                donnees_articles.append(info_article)

        # Écriture des données dans un fichier CSV
        with open('donnees_lenouvelliste.csv', mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Titre', 'Lien', 'Image', 'Description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for article in donnees_articles:
                writer.writerow(article)

    else:
        print(f"Erreur {response_principale.status_code} lors de la récupération de {url_principale}")

# Appel de la fonction principale
web_scraping_lenouvelliste()
