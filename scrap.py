import requests
from bs4 import BeautifulSoup
import csv

# Fonksyon pou grate entènèt
def scrape_lenouvelliste():
    url = "https://lenouvelliste.com/"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('div', class_='block-article')

        data_list = []

        for article in articles:
            # Ekstrè enfòmasyon yo nan chak atik
            title = article.find('h2', class_='title').text.strip()
            link = article.find('a')['href']
            image = article.find('img')['src']
            description = article.find('p', class_='description').text.strip()

            # Ajoute enfòmasyon yo nan yon list
            data_list.append([title, link, image, description])

        return data_list
    else:
        print(f"Erè {response.status_code} pandan ou ap aksede sit la.")
        return None

# Fonksyon pou ekri nan yon fichye CSV
def write_to_csv(data_list, filename='lenouvelliste_articles.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Ajoute tèt kolòn yo nan CSV la
        writer.writerow(['Tit', 'Link', 'Foto', 'Deskripsyon'])
        # Ekri chak liy nan CSV la
        writer.writerows(data_list)

# Ekzekite fonksyon yo
data_list = scrape_lenouvelliste()

if data_list:
    write_to_csv(data_list)
    print("Ekstraksyon ak ekri nan fichye CSV a sezi.")
else:
    print("Pwoblèm te genyen lè ou vle aksede sit la.")
