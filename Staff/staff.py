import requests
import os
import csv
from bs4 import BeautifulSoup


csv_header = [['NAME', 'TITLE', 'RATING', 'REVIEWS', 'IMAGE']]
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


def parse():
    import re
    page = open(file='Chevrolet_Staff.html', encoding='utf-8')
    read = page.read()
    soup = BeautifulSoup(read, 'html5lib')
    cards = soup.select('.dr-col-sm-4.dr-col-xs-6.dr-margin-bottom-xl.employee-tile.dr-col-lg-4.dr-col-md-4')
    for card in cards:
        image_url = card.select('.dr-bolder.dr-font-13.dr-black.dr-underline')[0].img['src']
        name = card.find('h3', {'class': re.compile('dr-block')}).text.strip()
        role = card.find('span', {'class': 'dr-block'}).text.strip()
        rating = card.find('span', {'class': 'dr-pull-left'}).text.upper().strip()
        reviews = card.select('.view-emp-reviews-btn span.dr-boldest')[0].text
        line = [name, role, rating, reviews, image_url]
        print(line)
        write_csv(lines=[line], filename='Chevrolet_Staff.csv')


if __name__ == '__main__':
    print('=======================Start========================')
    parse()
    print('======================= End =========================')