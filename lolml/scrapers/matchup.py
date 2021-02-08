# Import libraries
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import os
import re
import json
from requests_html import HTMLSession
from prettyjson import prettyjson


def get_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    return text


def get_overall_winrate(champ1, role1):
    url = 'https://u.gg/lol/champions/' + champ1 + '/build?role=' + role1
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    champ_stats = soup.find('div', {'class': 'champion-ranking-stats'})
    champ_winrate = champ_stats.find('div', {'class': 'win-rate'}).text
    return champ_winrate


def get_foe_matchup_Ajax(champ1, champ2, role1, patch, version):
    url = 'https://stats2.u.gg/lol/1.1/matchups/' + patch + \
        '/ranked_solo_5x5/' + str(champ1) + '/' + version + '.json'
    headers = {
        # :scheme: https
        # 'accept': '*/*',
        # 'accept-encoding': 'gzip, deflate, br',
        # 'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        'origin': 'https://u.gg',
        'referer': 'https://u.gg/lol/champions/wukong/matchups',
        'sec-fetch-dest': 'empty',
        # 'sec-fetch-mode': 'cors',
        # 'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/80.0.3987.87 Chrome/80.0.3987.87 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    result = response.json()
    with open('./matchups/foe/' + str(champ1), 'w') as f:
        json.dump(result, f)


def get_ally_matchup_Ajax(champ1, champ2, role1, role2, patch, version):
    url = 'https://stats2.u.gg/lol/1.1/champion_duos/' + patch + \
        '/ranked_solo_5x5/' + str(champ1) + '/' + version + '.json'
    headers = {
        # :scheme: https
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        'origin': 'https://u.gg',
        'referer': 'https://u.gg/lol/champions/wukong/duos',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/80.0.3987.87 Chrome/80.0.3987.87 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    result = response.json()
    with open('./matchups/ally/' + str(champ1), 'w') as f:
        json.dump(result, f)


def main(champ1, champ2, role1, role2):
    print(get_overall_winrate(champ1, role1))
    print(get_ally_matchup(champ1, champ2, role1, role2))
    print(get_foe_matchup(champ1, champ2, role1, role2))


get_foe_matchup_Ajax(62, 60, 4, '10_6', '1.3.0')
