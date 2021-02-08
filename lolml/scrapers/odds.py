# Import libraries
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # for suppressing the browser

import os
import re
import json


def get_odds(year):
    odd_results = []
    # specifies which leagues to download
    # top_leagues = {'LPL': 'lol-pro-league',
    #                     'LCK': 'champions-korea',
    #                     'LEC': 'european-championship',
    #                     'LCS': 'championship-series',
    #                     'MSI': 'mid-season-invitational',
    #                     'World': 'world-championship',
    #                     'LMS': 'lol-master-series'}
    top_leagues = {
        'World': 'world-championship'
    }

    # visit page of each league to get team names, match date
    for league in top_leagues.values():
        league_name = list(top_leagues.keys())[list(top_leagues.values()).index(league)]


        url = 'https://www.myscore.ru/esports/league-of-legends/' + \
            str(league) + '-' + str(year) + '/results/'
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        browser = webdriver.Chrome('/home/max/chromedriver/chromedriver_linux64/chromedriver', options=option)
        browser.get(url)
        html = browser.page_source
        #response = requests.get(url)
        soup = BeautifulSoup(html, "html.parser")

        matches = soup.find_all('div', {'class': 'event__match'})

        # go through all matches of selected league
        for match in matches:
            event_date = match.find('div', {'class': 'event__time'}).text
            print(event_date + ' event date')
            team_1 = match.find(
                'div', {'class': 'event__participant--home'}).text
            print(team_1, ' home')
            team_2 = match.find(
                'div', {'class': 'event__participant--away'}).text
            print(team_2, ' away')
            match_id = re.split('_', match.get('id'))[-1]
            print(match_id, ' match_id')

            # new soup for odds page of event
            # odds_url = 'https://www.myscore.ru/match/' + \
            #     str(match_id) + '/#odds-comparison;home-away;full-time'
            # print(odds_url)
            # option = webdriver.ChromeOptions()
            # option.add_argument('headless')
            # browser = webdriver.Chrome('/home/max/chromedriver/chromedriver_linux64/chromedriver', options=option)
            # browser.get(odds_url)
            # time.sleep(1)
            # html = browser.page_source
            # #response = requests.get(url)
            # soup = BeautifulSoup(html, "html.parser")

            odds_url = 'https://d.myscore.ru/x/feed/d_od_' + match_id + '_ru_1_eu'
            print(odds_url)
            headers = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                "accept-language": '*',
                "cookie": "__utmzz=utmcsr=google|utmcmd=organic|utmccn=(not set)|utmctr=(not provided); __utmzzses=1; _gid=GA1.2.1672280026.1582798034; _session_UA-821699-9=true; cto_bundle=sH7aBV9RTm85Mlpva3FaWXRYQmRYZW4yZXZiQWkzSGx4bXVMdGxPTk1BQ3lCaklYcFVWOHdNcFJ2NkZ5JTJCS2RoS1dzWjhUQWEwS1JuVko4YzNuaWRwVkhzZGRTM0VpRXdERVhNeHolMkZ0T2V3cEw3c3FUS2tXdVFWUUdvdFJZRHhrMDhsdWU0NTRhcmJGM05mdXljSFhudTZ5bXN3JTNEJTNE; _ga_JF1VRF7QHL=GS1.1.1583089725.15.1.1583091216.60; _ga_HRK2668K68=GS1.1.1583089725.15.1.1583091216.0; _ga=GA1.2.1380836082.1582390669; _sessionhits_UA-821699-9=4; _gat_UA-821699-9=1",
                "referer": "https://d.myscore.ru/x/feed/proxy-local",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Mobile Safari/537.36",
                "x-fsign": "SW9D1eZo",
                "x-geoip": "1",
                "x-referer": "https://www.myscore.ru/match/Y3mQpEMO/#odds-comparison;home-away;full-time",
                "x-requested-with": "XMLHttpRequest"
            }
            response = requests.get(odds_url, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")

            # get odds for event
            odds_table = soup.find(
                'table', {'class': 'odds sortable'})

            if not odds_table:
                # if odd_results[-1]['home_team'] == team_1 and odd_results[-1]['away_team'] == team_2:
                    continue

            odds_table = odds_table.find('tbody')

            bookmakers = odds_table.find_all('tr')
            xbet = bookmakers[1].find_all('td', {'class': 'kx'})
            xbet_home = xbet[0].find('span').text
            xbet_away = xbet[1].find('span').text
            print('xbet ',xbet_home, ' ',xbet_away)

            winline = bookmakers[0].find_all('td', {'class': 'kx'})
            winline_home = winline[0].find('span').text
            winline_away = winline[1].find('span').text
            print('winline ',winline_home, ' ',winline_away)

            parimatch = bookmakers[-1].find_all('td', {'class': 'kx'})
            pari_home = parimatch[0].find('span').text
            pari_away = parimatch[1].find('span').text
            print('parimatch ', pari_home, ' ',pari_away)

            odd_results.append({
                'league_name': league_name,
                'event_date': event_date,
                'home_team': team_1,
                'away_team': team_2,
                'xbet_home': xbet_home,
                'xbet_away': xbet_away,
                'winline_home': winline_home,
                'winline_away': winline_away,
                'pari_home': pari_home,
                'pari_away': pari_away
            })
    print(odd_results)
    return odd_results


def main(year):

    with open('odds_data.json', 'w') as fp:
        json.dump(get_odds(year), fp, indent=4)


if __name__ == '__main__':
    year = 2019
    main(year)
