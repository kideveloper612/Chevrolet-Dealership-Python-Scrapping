import csv
import os
from bs4 import BeautifulSoup
import re
import requests


class Dealer:
    def __init__(self):
        self.csv_header = [['NAME', 'REVIEWS', 'IMAGE', 'LINK']]

    def write_direct_csv(self, lines, filename):
        with open('output/%s' % filename, 'a', encoding="utf-8", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            writer.writerows(lines)
        csv_file.close()

    def write_csv(self, lines, filename):
        if not os.path.isdir('output'):
            os.mkdir('output')
        if not os.path.isfile('output/%s' % filename):
            self.write_direct_csv(lines=self.csv_header, filename=filename)
        self.write_direct_csv(lines=lines, filename=filename)

    def get_dealers(self):
        lines = []
        url = "chevrolet.html"
        page = open(url, encoding="utf8")
        soup = BeautifulSoup(page.read(), 'lxml')
        actions = soup.select('#islrg > div.islrc > div')
        for action in actions:
            if action.img.has_attr('src'):
                image = action.find('img')['src']
            elif action.img.has_attr('data-src'):
                image = action.find('img')['data-src']
            link = action.find('a', {'class': 'VFACy kGQAp'})['href']
            if 'data:image' in image:
                script_text = soup.find('script', text=re.compile(link)).text
                array_text = script_text.split('return')[1].replace('}', '').replace(')', '').replace(';', '').strip()
                index = array_text.find(link)
                for i in range(index-5, 1, -1):
                    if array_text[i:i+5] == 'https':
                        for j in range(i, index):
                            if array_text[j:j+3] == 'jpg':
                                print(link)
                                data_image = array_text[i:j+3]
                                link_soup = BeautifulSoup(requests.request('GET', url=link).content, 'html5lib')
                                name_soup = link_soup.find('h1', {'class': 'h1-header'})
                                name = name_soup.get_text().split('|')[0].strip()
                                dealership = name_soup.find_next(class_='notranslate').get_text().strip()
                                if dealership in name:
                                    dealership = name_soup.find_next(class_='notranslate').find_next(class_='notranslate').get_text().strip()
                                if link_soup.find('a', attrs={'href': '#reviews'}):
                                    review = link_soup.find('a', {'href': '#reviews'}).text.split(' ')[1].replace('(', '').replace(')', '')
                                elif link_soup.select('.h2-header'):
                                    review = link_soup.select('.h2-header')[0].text.split(' ')[0]
                                elif link_soup.select('h2 span.boldest'):
                                    review = link_soup.select('h2 span.boldest')[0].text.strip()
                                # line = [name, review, data_image, dealership.replace('\n', '').replace('  ', ''), link]
                                line = [name, review, data_image, link]
                                if line not in lines:
                                    lines.append(line)
                                    self.write_csv(lines=[line], filename='Chevrolet_Dealer.csv')
                                print(line)
                                break
                        break
            else:
                print(link)
                link_soup = BeautifulSoup(requests.request('GET', url=link).content, 'html5lib')
                name = link_soup.find('h1', {'class': 'h1-header'}).get_text().split('|')[0].strip()
                dealer = link_soup.find('h1', {'class': 'h1-header'}).find_next(attrs={'class': 'notranslate'})
                if dealer.a or dealer.name == 'a':
                    dealership = dealer.find_next(attrs={'class': 'notranslate'}).text.strip()
                else:
                    dealership = dealer.text.strip()
                if link_soup.find('a', attrs={'href': '#reviews'}):
                    review = link_soup.find('a', {'href': '#reviews'}).text.split(' ')[1].replace('(', '').replace(')', '')
                elif link_soup.select('.h2-header'):
                    review = link_soup.select('.h2-header')[0].text.split(' ')[0]
                elif link_soup.select('h2 span.boldest'):
                    review = link_soup.select('h2 span.boldest')[0].text.strip()
                line = [name, review, image, link]
                if line not in lines:
                    lines.append(line)
                    self.write_csv(lines=[line], filename='Chevrolet_Dealer.csv')
                print(line)
        lines.sort(key=lambda x: (x[0], x[1]))
        # self.write_csv(lines=lines, filename='Chevrolet_Dealer.csv')

    def arrange(self):
        path = 'output/Chevrolet_Dealer.csv'
        total = []
        count = False
        with open(path, newline='', encoding='utf-8') as csvfile:
            data = list(csv.reader(csvfile))
        for d in data:
            if not count:
                count = True
                continue
            if d not in total:
                total.append(d)
                self.write_csv(lines=[d], filename='again.csv')


print('============================= START =============================')
dealer = Dealer()
dealer.arrange()
print('============================= ENDED =============================')
