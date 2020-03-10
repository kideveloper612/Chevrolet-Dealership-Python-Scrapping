import csv
import os
from bs4 import BeautifulSoup
import re
import requests

class Dealer:
    def __init__(self):
        self.csv_header = [['NAME', 'REVIEWS', 'LINK', 'REVIEW_DATE', 'DEALERSHIP_RATING', 'SERVICE', 'VISIT', 'IAMGE_URL', 'REVIEW_TITLE', 'SALESMAN_NAME', 'REVIEW_CONTENT', 'CUSTOMER_NAME', 'CUSTOMER RATING', 'CUSTOMER_NAME', 'CUSTOMER RATING', 'CUSTOMER_NAME', 'CUSTOMER RATING', 'CUSTOMER_NAME', 'CUSTOMER RATING', 'CUSTOMER_NAME', 'CUSTOMER RATING']]
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

    def read_csv(self, file_path):
        with open(file=file_path, encoding='utf-8') as csv_reader:
            data = list(csv.reader(csv_reader))
            return data

    def get_review_detail(self, url, page=1, last_page_number=1, count=1, actions=1, count_line=1):
        if int(page) > int(last_page_number):
            return self.reviews
        if 'page' in url:
            page_index = url.find('page')
            url = url[:page_index]
        request_url = url + 'page%s' % page
        print(page, last_page_number, int(page) > int(last_page_number), count, actions, count_line)
        print(request_url)
        soup = BeautifulSoup(requests.request('GET', url=request_url).content, 'html5lib')
        review_images = soup.find_all('img', {'class': re.compile('margin-bottom-md pointer')})
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
            if 'VISIT' in sales_visit.upper():
                visit = sales_visit.upper().split('VISIT')[0].strip()
                new_old = sales_visit.upper().split('VISIT')[1].replace('-', '').strip()
            else:
                visit = ''
                new_old = ''
            image = review_image['src']
            title = review_entry.find_next(attrs={'class': re.compile('no-format')}).text.strip()
            salesman_name = review_entry.find_next(attrs={'class': 'notranslate'}).text.replace('-', '').strip()
            squares = review_entry.find_all(attrs={'class': 'square-image'})
            line = [review_date, sale_rating, visit, new_old, image, title, salesman_name, review_content]
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
        return self.get_review_detail(url=url, page=page+1, last_page_number=last_page_number, count=count, actions=actions, count_line=count_line)

    def get_dealers(self, html_file, save_name):
        count = 0
        if os.path.isfile('output/%s' % save_name):
            lines = self.read_csv(file_path='output/%s' % save_name)
        else:
            lines = []
        url = html_file
        page = open(url, encoding="utf8")
        soup = BeautifulSoup(page.read(), 'lxml')
        actions = soup.select('#islrg > div.islrc > div')
        for action in actions:
            count += 1
            if count < 816:
                print(count)
                continue
            # if action.img.has_attr('src'):
            #     image = action.find('img')['src']
            # elif action.img.has_attr('data-src'):
            #     image = action.find('img')['data-src']
            link = action.find('a', {'class': 'VFACy kGQAp'})['href'].split('page')[0]
            print(link)
            if '.pdf' in link:
                continue
            # if 'data:image' in image:
            #     if not soup.find('script', text=re.compile(link)):
            #         continue
            #     script_text = soup.find('script', text=re.compile(link)).text
            #     array_text = script_text.split('return')[1].replace('}', '').replace(')', '').replace(';', '').strip()
            #     index = array_text.find(link)
            #     for i in range(index-5, 1, -1):
            #         if array_text[i:i+5] == 'https':
            #             for j in range(i, index):
            #                 if array_text[j:j+3] == 'jpg':
            #                     data_image = array_text[i:j+3]
            #                     link_soup = BeautifulSoup(requests.request('GET', url=link).content, 'html5lib')
            #                     name_soup = link_soup.find('h1', {'class': 'h1-header'})
            #                     name = name_soup.get_text().split('|')[0].strip()
            #                     dealership = name_soup.find_next(class_='notranslate').get_text().strip()
            #                     if dealership in name:
            #                         dealership = name_soup.find_next(class_='notranslate').find_next(class_='notranslate').get_text().strip()
            #                     if link_soup.find('a', attrs={'href': '#reviews'}):
            #                         review = link_soup.find('a', {'href': '#reviews'}).text.split(' ')[1].replace('(', '').replace(')', '')
            #                     elif link_soup.select('.h2-header'):
            #                         review = link_soup.select('.h2-header')[0].text.split(' ')[0]
            #                     elif link_soup.select('h2 span.boldest'):
            #                         review = link_soup.select('h2 span.boldest')[0].text.strip()
            #                     last_page = link_soup.find_all(attrs={'class': 'page_active'})
            #                     if len(last_page) > 2:
            #                         last_page_number = last_page[-2].text.strip()
            #                     else:
            #                         last_page_number = 1
            #                     reviews = self.get_review_detail(url=link, last_page_number=last_page_number)
            #                     previous_line = [name, review, link]
            #                     for line in reviews:
            #                         for insert_index in range(4):
            #                             line.insert(insert_index, previous_line[insert_index])
            #                         if line not in lines:
            #                             lines.append(line)
            #                             self.write_csv(lines=[line], filename=save_name)
            #                         print(line)
            #                     self.reviews = []
            #                     break
            #             break
            # else:
            link_soup = BeautifulSoup(requests.request('GET', url=link).content, 'html5lib')
            if link_soup.find('h1', {'class': 'h1-header'}):
                name = link_soup.find('h1', {'class': 'h1-header'}).get_text().split('|')[0].strip()
            elif link_soup.find(attrs={'class': re.compile('review-title')}):
                name = link_soup.find(attrs={'class': re.compile('review-title')}).split('"')[0]
            # dealer_name = link_soup.find('h1', {'class': 'h1-header'}).find_next(attrs={'class': 'notranslate'})
            # if dealer_name.a or dealer_name.name == 'a':
            #     dealership = dealer_name.find_next(attrs={'class': 'notranslate'}).text.strip()
            # else:
            #     dealership = dealer_name.text.strip()
            if link_soup.find('a', attrs={'href': '#reviews'}):
                review = link_soup.find('a', {'href': '#reviews'}).text.split(' ')[1].replace('(', '').replace(')', '')
            elif link_soup.select('.h2-header'):
                review = link_soup.select('.h2-header')[0].text.split(' ')[0]
            elif link_soup.select('h2 span.boldest'):
                review = link_soup.select('h2 span.boldest')[0].text.strip()
            last_page = link_soup.find_all(attrs={'class': 'page_active'})
            if len(last_page) > 2:
                last_page_number = last_page[-2].text.strip()
            else:
                last_page_number = 1
            previous_line = [name, review, link]
            if int(last_page_number) > 960:
                over_res_reviews = self.get_review_detail(url=link, last_page_number=960, count=count, actions=len(actions), count_line=len(lines))
                for line in over_res_reviews:
                    for insert_index in range(3):
                        line.insert(insert_index, previous_line[insert_index])
                    if line not in lines:
                        lines.append(line)
                        self.write_csv(lines=[line], filename=save_name)
                again_res_reviews = self.get_review_detail(url=link, page=960, last_page_number=last_page_number, count=count, actions=len(actions), count_line=len(lines))
                for line in again_res_reviews:
                    for insert_index in range(3):
                        line.insert(insert_index, previous_line[insert_index])
                    if line not in lines:
                        lines.append(line)
                        self.write_csv(lines=[line], filename=save_name)
            else:
                res_reviews = self.get_review_detail(url=link, last_page_number=last_page_number, count=count, actions=len(actions), count_line=len(lines))
                for line in res_reviews:
                    for insert_index in range(3):
                        line.insert(insert_index, previous_line[insert_index])
                    if line not in lines:
                        lines.append(line)
                        self.write_csv(lines=[line], filename=save_name)
            self.reviews = []
        # lines.sort(key=lambda x: (x[0], x[1]))
        # self.write_csv(lines=lines, filename='Chevrolet_Dealer.csv')

    def arrange(self, file, new_name):
        path = 'output/%s' % file
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
                self.write_csv(lines=[d], filename=new_name)


print('============================= START =============================')
dealer = Dealer()
# dealer.get_dealers(html_file='HTML/chevrolet.html', save_name='Chevrolet/Chevrolet.csv')
dealer.arrange(file='Chevrolet/Chevrolet.csv', new_name='Chevrolet/again.csv')
print('============================= ENDED =============================')
