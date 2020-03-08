import csv
import os
from bs4 import BeautifulSoup
import re
import requests


class Dealer:
    def __init__(self):
        self.csv_header = [['NAME', 'REVIEWS', 'IMAGE', 'LINK']]
        self.reviews = []

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

    def get_review_detail(self, url, page=1, last_page_number=1):
        if int(page) > int(last_page_number):
            return self.reviews
        if 'page' in url:
            page_index = url.find('page')
            url = url[:page_index]
        request_url = url + 'page%s' % page
        print(request_url)
        soup = BeautifulSoup(requests.request('GET', url=request_url).content, 'html5lib')
        review_images = soup.find_all('img', {'class': 'margin-bottom-md pointer'})
        for review_image in review_images:
            review_entry = review_image.find_parent(attrs={'class': 'review-entry'})
            review_content = review_entry.find(attrs={'class': 'review-content'}).text.strip()
            review_date = review_entry.find('div', attrs={'class': 'review-date'}).next_element.next_element.text.strip()
            sale_ratings = review_entry.find('div', attrs={'class': 'review-date'}).find_next(attrs={'class': 'rating-static'})['class']
            for s in sale_ratings:
                if 'rating' in s:
                    sale = s.split('-')[1]
                    sale_rating = sale[:1] + '.' + sale[1:]
            sales_visit = review_entry.find('div', attrs={'class': 'review-date'}).find_next(attrs={'class': 'small-text'}).text.strip()
            image = review_image['src']
            salesman_name = review_entry.find_next(attrs={'class': 'notranslate'}).text.replace('-', '').strip()
            squares = review_entry.find_all(attrs={'class': 'square-image'})
            line = [review_date, sale_rating, sales_visit, image, salesman_name, review_content]
            for square in squares:
                table = square.find_parent(attrs={'class': 'table'})
                customer_name = table.find(attrs={'class': 'notranslate'}).text.strip()
                if table.find(attrs={'class': 'relative employee-rating-badge-sm'}):
                    customer_rating = table.find(attrs={'class': 'relative employee-rating-badge-sm'}).text.strip()
                else:
                    customer_rating = ''
                line.append(customer_name)
                line.append(customer_rating)
            print(line)
            self.reviews.append(line)
        return self.get_review_detail(url=url, page=page+1, last_page_number=last_page_number)

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
            print(link)
            if 'data:image' in image:
                script_text = soup.find('script', text=re.compile(link)).text
                array_text = script_text.split('return')[1].replace('}', '').replace(')', '').replace(';', '').strip()
                index = array_text.find(link)
                for i in range(index-5, 1, -1):
                    if array_text[i:i+5] == 'https':
                        for j in range(i, index):
                            if array_text[j:j+3] == 'jpg':
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
                                last_page = link_soup.find_all(attrs={'class': 'page_active'})
                                if last_page:
                                    last_page_number = last_page[-2].text.strip()
                                else:
                                    last_page_number = 1
                                reviews = self.get_review_detail(url=link, last_page_number=last_page_number)
                                previous_line = [name, review, data_image, link]
                                for line in reviews:
                                    for insert_index in range(4):
                                        line.insert(insert_index, previous_line[insert_index])
                                    if line not in lines:
                                        lines.append(line)
                                        self.write_csv(lines=[line], filename='Chevrolet_Dealer.csv')
                                    print(line)
                                self.reviews = []
                                break
                        break
            else:
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
                last_page = link_soup.find_all(attrs={'class': 'page_active'})
                if last_page:
                    last_page_number = last_page[-2].text.strip()
                else:
                    last_page_number = 1
                reviews = self.get_review_detail(url=link, last_page_number=last_page_number)
                previous_line = [name, review, data_image, link]
                for line in reviews:
                    for insert_index in range(4):
                        line.insert(insert_index, previous_line[insert_index])
                    if line not in lines:
                        lines.append(line)
                        self.write_csv(lines=[line], filename='Chevrolet_Dealer.csv')
                    print(line)
                    self.reviews = []
        lines.sort(key=lambda x: (x[0], x[1]))
        # self.write_csv(lines=lines, filename='Chevrolet_Dealer.csv')

    def arrange(self):
        path = 'output/Chevrolet.csv'
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
