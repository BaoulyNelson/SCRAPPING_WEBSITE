import requests
from bs4 import BeautifulSoup
import csv

def scrap_lenouvelliste():
    # URL du site à scraper
    url = 'https://lenouvelliste.com/'

    # Envoyer une requête GET à l'URL
    response = requests.get(url)

    # Vérifier si la requête a réussi (statut HTTP 200)
    if response.status_code == 200:
        # Analyser le contenu de la page avec BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Liste pour stocker les données extraites
        articles_data = []

        # Trouver tous les éléments d'article sur la page
        articles = soup.find_all('article')

        for article in articles:
            # Extraire le titre de l'article
            title = article.find('h2').text.strip()

            # Extraire le lien de l'article
            link = article.find('a')['href']

            # Extraire l'image de l'article s'il y en a une
            image_tag = article.find('img')
            image = image_tag['src'] if image_tag else None

            # Extraire la description de l'article
            description = article.find('p').text.strip()

            # Ajouter les données extraites à la liste
            articles_data.append([title, link, image, description])

        return articles_data

    else:
        # En cas d'échec de la requête
        print(f"La requête a échoué avec le statut {response.status_code}")
        return None

def save_to_csv(data, filename='lenouvelliste_articles.csv'):
    # Écrire les données extraites dans un fichier CSV
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Écrire l'en-tête
        csv_writer.writerow(['Titre', 'Lien', 'Image', 'Description'])
        
        # Écrire les lignes de données
        csv_writer.writerows(data)

if __name__ == "__main__":
    # Appeler la fonction de scraping
    scraped_data = scrap_lenouvelliste()

    if scraped_data:
        # Enregistrer les données extraites dans un fichier CSV
        save_to_csv(scraped_data)
        print("Extraction et sauvegarde réussies.")
    else:
        print("Échec de l'extraction des données.")
