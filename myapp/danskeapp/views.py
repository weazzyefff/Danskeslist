from django.shortcuts import render
from requests.compat import quote_plus
import requests
from bs4 import BeautifulSoup
from . import models

BASE_CRAIGSLIST_URL = 'https://auckland.craigslist.org/search/sss?query={}'


# Create your views here.

def home(request):
    return render(request, 'base.html')


def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result=price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        final_postings.append((post_title, post_url, post_price))

    # print(post_title)  # Commenting these out for now but they
                         # came in really helpful when testing FYI
    # print(post_url)
    # print(post_price)

    # print(post_titles[0].get('href'))  # This gets link, text gets Title.

    # print(data)
    # Dictionary for something

    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'myapp/new_search.html', stuff_for_frontend)
