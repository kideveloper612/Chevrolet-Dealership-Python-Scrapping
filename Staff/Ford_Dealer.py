import os
import csv
import requests
from bs4 import BeautifulSoup

csv_header = [['NAME', 'TITLE', 'Phone', 'Email', 'IMAGE']]


def write_direct_csv(lines, filename):
    with open('output/%s' % filename, 'a', encoding="utf-8", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(lines)
    csv_file.close()


def write_csv(lines, filename):
    if not os.path.isdir('output'):
        os.mkdir('output')
    if not os.path.isfile('output/%s' % filename):
        write_direct_csv(lines=csv_header, filename=filename)
    write_direct_csv(lines=lines, filename=filename)


initial_url = 'https://www.bobeuckmanford.com/dealership/staff.htm'
header = {
    'user-agent': "mozila/5.0"
}
res = requests.request(method='GET', url=initial_url, headers=header)
soup = BeautifulSoup(res.text, 'html5lib')
cards = soup.find_all('li', {'class': "staff"})
for card in cards:
    name = card.find('dt', {'class': 'fn'}).text.strip()
    title = card.find('dd', {'class': 'title'}).text.strip()
    phone = card.find('dd', {'class': 'phone'}).text.strip()
    email = card.find('dd', {'class': 'email'}).text.strip()
    image = card.find('dd', {'class': 'photo'}).img['data-src'].split('?')[0]
    line = [name, title, phone, email, image]
    write_csv(lines=[line], filename='Ford_Dealer.csv')
