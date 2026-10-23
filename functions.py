import requests
from bs4 import BeautifulSoup as bs

def retrieve_data(link):
    request_response = requests.get(link)
    if request_response.status_code == 200:
        return bs(request_response.content, 'html.parser')
    else:
        print('Error')
        return None


def find_details(soup, collection, category):
    title = soup.find('h1').text.strip()
    image = 'http://books.toscrape.com/' + soup.find('img').get('src')[6:]
    description = soup.find('article', class_="product_page").find_all('p')[3].text.strip()
    if description[-8:] == " ...more":
        description = description[:-8]
    idx = description.find(description[:40], 1)
    if idx > 0:
        description = description[idx:]
    collection.append({"title" : title,
                        "image" : image,
                        "description" : description,
                        "category" : category})


def calc_books_pages(soup):
    nr_books = soup.find('form', class_="form-horizontal").find_all('strong')[0].text.strip()
    nr_pages = int(nr_books) // 20
    if int(nr_books) % 20 != 0:
        nr_pages += 1
    return nr_books, nr_pages


def gather_data_books(books, link, soup, collection, category):
    for b in books:
        book_link = link + b.find('a').get('href')[9:]
        soup = retrieve_data(book_link)
        find_details(soup, collection, category)
