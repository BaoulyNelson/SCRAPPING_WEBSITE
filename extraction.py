import requests
from bs4 import BeautifulSoup
import csv

# Fonction pour extraire les informations d'un article
def extract_article_info(article_url):
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraire les informations nécessaires
    title = soup.find('h1,h2').text.strip()
    image = soup.find('meta', property='og:image')['content']
    description = soup.find('meta', property='og:description')['content']

    return {
        'title': title,
        'url': article_url,
        'image': image,
        'description': description
    }

# Fonction principale pour extraire les données du site
def scrape_lenouvelliste():
    base_url = 'https://lenouvelliste.com'
    news_url = f'{base_url}/categorie/actualites'

    response = requests.get(news_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraire les liens des articles
    article_links = [f'{base_url}{link["href"]}' for link in soup.select('.news-list a')]

    # Liste pour stocker les données extraites
    extracted_data = []

    # Boucle pour extraire les informations de chaque article
    for link in article_links:
        try:
            article_info = extract_article_info(link)
            extracted_data.append(article_info)
        except Exception as e:
            print(f'Erreur lors de l\'extraction de l\'article {link}: {str(e)}')

    # Écrire les données dans un fichier CSV
    with open('lenouvelliste_donnee.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'url', 'image', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Écrire l'en-tête du fichier CSV
        writer.writeheader()

        # Écrire les données pour chaque article
        writer.writerows(extracted_data)

if __name__ == "__main__":
    scrape_lenouvelliste()
