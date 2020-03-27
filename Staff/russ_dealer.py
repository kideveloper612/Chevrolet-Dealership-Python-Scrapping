import requests
import os
import csv
from bs4 import BeautifulSoup


csv_header = [['NAME', 'TITLE', 'EMAIL', 'IMAGE']]


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
    url = 'https://www.russdarrowchryslerdodgejeep.com/dealership/staff.htm#'
    header = {
        'user-agent': 'mozila/5.0'
    }
    soup = BeautifulSoup(requests.get(url=url, headers=header).content, 'html5lib')
    cards = soup.find_all('li', {'class': 'yui3-u-1-6 staff'})
    for card in cards:
        name = card.find('a', attrs={'name': True}).text.strip()
        if card.img.has_attr('src'):
            image = card.img['src']
        elif card.img.has_attr('data-src'):
            image = card.img['data-src']
        email_tmp = card.find('dd', {'class': 'email'})
        if email_tmp and email_tmp.text.strip() != '':
            email = card.find('dd', {'class': 'email'}).text.strip()
            line = [name, '', email, image]
            print(line)
            write_csv(lines=[line], filename='Jeep_Dealer.csv')
        else:
            title = card.find('dd', {'class': 'title'}).text.strip()
            line = [name, title, '', image]
            print(line)
            write_csv(lines=[line], filename='Jeep_Dealer.csv')


if __name__ == '__main__':
    print('=======================Start========================')
    parse()
    print('======================= End =========================')