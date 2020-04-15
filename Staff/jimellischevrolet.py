import os
import csv
from bs4 import BeautifulSoup


def read_file():
    path = 'jimellischevrolet.html'
    file = open(file=path, encoding='utf-8')
    reader = file.read()
    file.close()
    return reader


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


if __name__ == "__main__":
    file_content = read_file()
    soup = BeautifulSoup(file_content, 'html5lib')
    cards = soup.select('section.media-bleed-full.deck-listing.aspect-unknown.insight.media-bleed-full', limit=33)
    i = 0
    for card in cards:
        if i < 3:
            i = i + 1
            continue
        name = card.find(attrs={"template": "employeeTitle"}).h4.text.replace('.', '').strip()
        title = card.find(attrs={"template": "employeeTitle"}).p.text.strip()
        image = card.find(attrs={"template": "employeeMedia"}).img['src']
        email_tmp = card.find(attrs={"template": "employeeContactLinksLexus"})
        if email_tmp.a:
            email = email_tmp.select("a")[-1]['href'].replace("mailto:", "")
        else:
            email = ''
        line = [name, title, image, email]
        print(line)
        write_csv(lines=[line], filename="jimellischevrolet.csv")
