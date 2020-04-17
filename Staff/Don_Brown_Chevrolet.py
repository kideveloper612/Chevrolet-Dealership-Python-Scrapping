import csv
import requests
from bs4 import BeautifulSoup
import os


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


initial_url = 'https://www.donbrownchevrolet.com/MeetTheStaff'
res = requests.request(method='GET', url=initial_url)
soup = BeautifulSoup(res.text, 'html5lib')
cards = soup.find_all('section', attrs={'itemprop': "employee"})
for card in cards:
    name = card.find('div', {'class': 'title'}).h4.text.strip()
    title = card.find('div', {'class': 'title'}).p.text.strip()
    if card.find(attrs={'itemprop': 'telephone'}):
        phone = card.find(attrs={'itemprop': 'telephone'}).text.strip()
    else:
        phone = ''
    if card.find(attrs={'itemprop': 'email'}):
        email = card.find(attrs={'itemprop': 'email'})['href'].replace('mailto:', "").strip()
    else:
        email = ''
    if card.find('div', {'template': 'employeeMedia'}).img:
        image = card.find('div', {'template': 'employeeMedia'}).img['data-src']
    else:
        image = ''
    line = [name, title, phone, email, image]
    write_csv(lines=[line], filename='Don_Brown_Chevrolet.csv')
    print(line)
