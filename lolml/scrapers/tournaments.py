# Import libraries
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import os
import re
import json


def contain_winners(item):
    winners_list = item.find(
        'div', {'class': 'tournament__winners'}).find('ul')
    # winners_ul = winners_list.find('ul', {'class': 'winners'})
    winners_items = winners_list.find_all('li', {'class': 'winners__item'})
    if len(winners_items) == 3:
        return winners_items
    else:
        return None


def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    return text


def parse_user_datafile_bs(filename):
    results = []
    text = read_file(filename)

    soup = BeautifulSoup(text, features="html.parser")
    tournament_list = soup.find('ul', {'class': 'tournaments__list'})
    items = tournament_list.find_all('li', {'class': ['tournaments__item']})
    for item in items[1:]:
        winners = contain_winners(item)
        if winners is not None:
            place1 = winners[0].find('a').find('img').get('alt')
            place2 = winners[1].find('a').find('img').get('alt')
            place3 = winners[2].find('a').find('img').get('alt')

            tournament_name = item.find(
                'div', {'class': 'tournament__name'}).find('a').find('strong').text
            tournament_date = item.find(
                'div', {'class': 'tournament__date'}).find('time').text
            date_matched = re.findall(
                r'(\d{2}\.\d{2}\.\d{4})', tournament_date)

            star_list = item.find('div', {'class': 'tournament__rating'})
            stars = star_list.find_all('svg', {'class': 'icon--13'})
            tournament_rating = 0
            print(stars)
            for star in stars:
                filled_star = star.find(
                    'use', {'class': 'icon-fill--brand-orange'})
                if filled_star:
                    print('+1 star')
                    tournament_rating += 1

            results.append({
                'tournament_name': tournament_name,
                'tournament_date_Start': date_matched[0],
                'tournament_date_End': date_matched[1],
                'rating': tournament_rating,
                '1st place': place1,
                '2nd place': place2,
                '3rd place': place3
            })
    return results


url = 'https://www.cybersport.ru/base/tournaments?sort=title&filterOrder=auto&disciplines=23955&status=past&page=1'

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
page = 1  # variable to track what line you are on

while page <= 5:  # code for text files starts at line 36
    download_url = 'https://www.cybersport.ru/base/tournaments?sort=start&filterOrder=desc&disciplines=23955&status=past&page=' + \
        str(page)
    print(str(page) + ' processing')
    urllib.request.urlretrieve(
        download_url, './user_data/' + 'page' + str(page))
    time.sleep(1)  # pause the code for a sec
# add 1 for next line
    page += 1


results = []
for filename in os.listdir('./user_data/'):
    results.extend(parse_user_datafile_bs('./user_data/' + filename))

with open('lol_data.json', 'w') as fp:
    json.dump(results, fp, indent=4)
