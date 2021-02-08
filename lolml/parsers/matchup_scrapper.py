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


def get_ally_matchup(champ1, champ2, role1, role2):
    url = 'https://u.gg/lol/champions/' + champ1 + '/duos'
    soup = get_javaHeavySite(url)
    print(soup)
    duo_list = soup.find('div', {'class': 'rt-tbody'}
                         ).find_all('div', {'class': 'rt-tr-group'})
    for duo in duo_list:
        duo_role = duo.find('img', {'class': 'tier-list-role'}).get('alt')
        duo_champ = duo.find('strong', {'class': 'champion-name'}).text
        duo_winrate = duo.findfind(
            'span', {'class': 'volxd-tier'}).get('b').text
        if duo_role == role2 and duo_champ == champ2:
            return duo_winrate


def get_foe_matchup(champ1, champ2, role1):
    url = 'https://u.gg/lol/champions/' + champ1 + '/matchups?role=' + role1
    soup = get_javaHeavySite(url)

    foe_list = soup.find('div', {'class': 'rt-tbody'}
                         ).find_all('div', {'class': 'rt-tr-group'})
    for foe in foe_list:
        print(foe.find('div', {'class': 'champion-name'}))
        foe_champ = foe.find(
            'div', {'class': 'champion-name'}).find('strong').text
        foe_winrate = foe.find(
            'div', {'class': 'rt-td winrate'}).find('b').text
        print(foe_champ, foe_winrate)
        if foe_champ == champ2:
            return foe_winrate


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


# get_ally_matchup_Ajax(62, 60, 4, 2, '10_6', '1.3.0')
get_foe_matchup_Ajax(62, 60, 4, '10_6', '1.3.0')
# print(get_overall_winrate('akali', 'top'))
# print(get_foe_matchup('akali', 'Fiora', 'top'))
# print(get_ally_matchup('akali', 'Vi', 'top', 'jungle'))

# results = []
# for directory in os.listdir('./user_data/'):
#     print(directory)
#     for filename in os.listdir('./user_data/' + directory + '/'):
#         results.extend(parse_user_datafile_bs('./user_data/'+ directory + '/' + filename))
# print(results)

# with open('games_data.json', 'w') as fp:
#     json.dump(results, fp, indent=4)
