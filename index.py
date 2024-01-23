import requests
from bs4 import BeautifulSoup
import csv

url = 'https://lenouvelliste.com/'

response = requests.get(url)

if response.ok:
    soup = BeautifulSoup(response.text, "html.parser")
    titles = soup.find_all('h1')  
    links = soup.find_all('a')
    article_divs = soup.find_all('div', class_='lnv-featured-article-lg')

    print(len(titles))
    print(len(links))
    print(len(article_divs))

    img_links = []

    for div in article_divs:
        img_tag = div.find('img')
        if img_tag:
            src_value = img_tag.get('src')
            img_links.append(src_value)

    with open('Stan.csv', mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow(['Titles'])  
        for title in titles:
            writer.writerow([title.text.strip()])  
            
        writer.writerow(['Links'])
        for link in links: 
            writer.writerow([link.get('href').strip()])
    
        writer.writerow(['Image Links']) 
        for img_link in img_links:
            writer.writerow([img_link])
