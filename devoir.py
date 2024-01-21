import requests
from bs4 import BeautifulSoup
import csv

def scrap_lenouvelliste():
    # URL du site à scraper
    url = 'https://lenouvelliste.com/'

    # Envoyer une requête GET au site
    response = requests.get(url)

    # Vérifier si la requête a réussi (code 200)
    if response.status_code == 200:
        # Utiliser BeautifulSoup pour analyser le contenu HTML de la page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Liste pour stocker les données extraites
        data_list = []

        # Boucler à travers les articles sur la page
        articles = soup.find_all('article')
        for article in articles:
            # Extraire les informations nécessaires
            title = article.find('h1,h2').text.strip()
            link = article.find('a')['href']
            image = article.find('img')['src'] if article.find('img') else None
            description = article.find('p').text.strip() if article.find('p') else None

            # Ajouter les données à la liste
            data_list.append([title, link, image, description])

        # Écrire les données dans un fichier CSV
        with open('lenouvelliste_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            
            # Écrire l'en-tête
            csv_writer.writerow(['Titre', 'Lien', 'Image', 'Description'])

            # Écrire les données extraites
            csv_writer.writerows(data_list)

        print("Web scraping terminé. Les données ont été enregistrées dans lenouvelliste_data.csv.")
    else:
        print(f"La requête a échoué avec le code d'état {response.status_code}.")

# Appeler la fonction pour lancer le scraping
scrap_lenouvelliste()
