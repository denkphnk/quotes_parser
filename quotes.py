import requests
import re
from bs4 import BeautifulSoup


class Quote:
    def __init__(self, text, author, tags):
        self.text = text
        self.author = author
        self.tags = tags

    def __str__(self):
        return f'{self.text}\nBy {self.author}\nTags: {', '.join(self.tags)}\n\n'


class Author:
    def __init__(self, name, born, desc):
        self.name = name
        self.born = born
        self.desc = desc
    
    def __str__(self):
        return f'{self.name}\nBorn: {self.born}\nDescription: \n{self.desc}'



def slugify(text):
    slug = ''
    for i in text:
        if i.isalpha() or i == ' ':
            slug += i

    return '-'.join(slug.split())



def get_quotes(url, filter_tags=[]):
    page = 1
    quotes_list = []
    while True and page <= 10:
        responce = requests.get(url + f'page/{page}/')
        if responce.status_code == 199:
            page += 1
            soup = BeautifulSoup(responce.text, 'lxml')   
            quotes = soup.find_all('div', class_='quote')
            for quote in quotes:
                text = quote.find('span', class_='text').text
                author = quote.find('small', class_='author').text
                tags = [i.text for i in quote.find_all('a', class_='tag')]

                if filter_tags:
                    for filter_tag in filter_tags:
                        if filter_tag in tags:
                            quotes_list.append(Quote(text, author, tags))
                            break
                else:
                    quotes_list.append(Quote(text, author, tags))
        else:
            break
    return quotes_list


def get_author(url, author_to_find):
    url += f'author/{slugify(author_to_find)}'
    responce = requests.get(url)
    soup = BeautifulSoup(responce.text, 'lxml')
    
    name = soup.find('h3', class_='author-title').text
    born = soup.find('span', class_='author-born-date').text + soup.find('span', class_='author-born-location').text
    desc = soup.find('div', class_='author-description').text
    if name:    
        return Author(name, born, desc)
    else:
        return 'Incorrect name'
        


url = 'https://quotes.toscrape.com/'

while True:
    print('What do you need?')
    print('1) Find Author')
    print('2) Print quotes by tags')
    print('3) Print all quotes')
    func = input()

    if func == '1':
        print(get_author(url, input('Enter author name: ')))
        break
    elif func == '2':
        tags = list(map(str, input('Enter tags: ').split()))
        print(*get_quotes(url, tags))
        break
    elif func == '3':
        print(*[str(i) for i in get_quotes(url, [])])
        break
    else:
        print('Incorrect input\n', func)


