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
import datetime
import pprint


def search_partial_text(src, dst):
    dst_buf = dst
    result = 0
    for char in src:
        if char in dst_buf:
            dst_buf = dst_buf.replace(char, '', 1)
            result += 1
    r1 = int(result / len(src) * 100)
    r2 = int(result / len(dst) * 100)
    if r1 < r2:
        return r1
    else:
        return r2


# load data from json files
def load_json():
    with open('games_data.json', 'r') as json_file:
        games_dict = json.load(json_file)

    with open('odds_data.json', 'r') as json_file:
        odds_dict = json.load(json_file)

    frm_date(odds_dict)
    return games_dict, odds_dict


# load sorted by date data from json files
def load_json_sorted():
    with open('games_data.json', 'r') as json_file:
        games_dict = json.load(json_file)

    with open('odds_data.json', 'r') as json_file:
        odds_dict = json.load(json_file)

    frm_date(odds_dict)

    sorted_odds = sorted(odds_dict, key=lambda i: i['event_date'])
    sorted_games = sorted(games_dict, key=lambda i: i['game_date'])

    return sorted_games, sorted_odds


# check if it's an msi league, if so --> try acronim, then full name
def check_for_msi(name_odds, name_stats):
    if name_odds == 'MSI':
        multi_name = ['MSI', 'Mid-Season Invitational']
        for name in multi_name:
            league_pattern = re.compile(name)
            if league_pattern.search(name_stats):
                return True
            else:
                return None
    else:
        league_pattern = re.compile(name_odds)
        if league_pattern.search(name_stats):
            return True
        else:
            return None



def removew(obj):
    for d in obj:
        for k, v in d.items():
            d[k] = v.strip()


# make sure time zones difference are taken into account
def date_dispersion(date_try, date_const):
    day = int(date_try[:1])
    if date_try == date_const:
        return 1
    elif date_try[:-1] + str(day + 1) == date_const:
        return 1
    elif date_try[:-1] + str(day - 1) == date_const:
        return 1
    else:
        return 0


# format date to Y-m-d
def frm_date(odds):
    for j in range(len(odds)):
        frmt_date = re.split(r' ', odds[j]['event_date'])[0] + '2019'
        odds[j]['event_date'] = datetime.datetime.strptime(
            frmt_date, '%d.%m.%Y').strftime('%Y-%m-%d')


# get odds from 'odds_dict' and merge into 'games_dict'
def merge_data(games_orig, odds):
    games = games_orig.copy()
    for i in range(len(games)):
        for j in range(len(odds)):

            # check if dict params are equal
            if check_for_msi(odds[j]['league_name'], games[i]['tournament_name']):
                if odds[j]['home_team'].lower() == games[i]['team_1'].lower():
                    print('yay home')
                else:
                    print('fuck home')
                if odds[j]['away_team'].lower() == games[i]['team_2'].lower():
                    print('yay away')
                else:
                    print('fuck away')

                print(odds[j]['home_team'].lower() + ' ---- ' + games[i]['team_1'].lower())
                print(odds[j]['away_team'].lower() + ' ---- ' + games[i]['team_2'].lower() + '\n')

                if odds[j]['home_team'].lower() == games[i]['team_1'].lower() and odds[j]['away_team'].lower() == games[i]['team_2'].lower():
                    print('names checked')
                    if date_dispersion(odds[j]['event_date'], games[i]['game_date']):
                        print('date checked')
                        new_params = list(odds[j].items())[4:]
                        games[i].update(new_params)
                        print('updated')
                    break
    return games


def main(data):

    with open('dateSorted_games.json', 'r') as json_file:
        games_orig = json.load(json_file)

    with open('dateSorted_odds.json', 'r') as json_file:
        odds = json.load(json_file)

    # games_orig, odds = load_json_sorted()

    removew(games_orig)
    removew(odds)

    # print(len(sorted_odds))
    # print(len(sorted_games))

    games_updated = merge_data(games_orig, odds)

    err_dicts = []

    for d in games_updated:
        if 'pari_home' not in d:
            err_dicts.append(d)

    games_updated = [i for i in games_updated if not ('pari_home' not in i)]

    with open('err_data.json', 'w') as fp:
            json.dump(err_dicts, fp, indent=4)

    with open('updated_data.json', 'w') as fp:
        json.dump(games_updated, fp, indent=4)


if __name__ == '__main__':
    data = [
        {
            "tournament_name": "World Championship 2019",
            "game_date": "2019-10-13",
            "game_time": "33:47",
            "team_1": "Team Liquid",
            "top": "Impact",
            "jungle": "Xmithie",
            "mid": "Jensen",
            "adc": "Doublelift",
            "support": "CoreJJ",
            "top_champ": "Gangplank",
            "jungle_champ": "Gragas",
            "mid_champ": "Akali",
            "adc_champ": "Xayah",
            "support_champ": "Rakan",
            "team_2": "Invictus Gaming ",
            "top_2": "TheShy",
            "jungle_2": "Leyan",
            "mid_2": "RooKie",
            "adc_2": "JackeyLove",
            "support_2": "Baolan",
            "top_champ_2": "Vladimir",
            "jungle_champ_2": "Olaf",
            "mid_champ_2": "Orianna",
            "adc_champ_2": "Kaisa",
            "support_champ_2": "Fiddlesticks",
            "winner": "Invictus Gaming ",
            "kills_team1": " 11",
            "kills_team2": " 17"
        },
        {
            "tournament_name": "World Championship 2019",
            "game_date": "2019-11-02",
            "game_time": "25:49",
            "team_1": "Funplus Phoenix ",
            "top": "GimGoon",
            "jungle": "Tian",
            "mid": "Doinb",
            "adc": "Lwx",
            "support": "Crisp",
            "top_champ": "Gangplank",
            "jungle_champ": "Qiyana",
            "mid_champ": "Nautilus",
            "adc_champ": "Xayah",
            "support_champ": "Thresh",
            "team_2": "Invictus Gaming ",
            "top_2": "TheShy",
            "jungle_2": "Ning",
            "mid_2": "RooKie",
            "adc_2": "JackeyLove",
            "support_2": "Baolan",
            "top_champ_2": "Lucian",
            "jungle_champ_2": "Gragas",
            "mid_champ_2": "Jayce",
            "adc_champ_2": "Ezreal",
            "support_champ_2": "Alistar",
            "winner": "Funplus Phoenix",
            "kills_team1": " 20",
            "kills_team2": " 8"
        }]
    main(data)


# data2 = [
#     {
#         "league_name": "world-championship",
#         "event_date": "13.10. 19:00",
#         "home_team": "FunPlus Phoenix",
#         "away_team": "G2 Esports",
#         "xbet_home": "1.96",
#         "xbet_away": "1.93",
#         "winline_home": "1.87",
#         "winline_away": "1.83",
#         "pari_home": "1.97",
#         "pari_away": "1.77"
#     },
#     {
#         "league_name": "world-championship",
#         "event_date": "03.11. 18:00",
#         "home_team": "T1",
#         "away_team": "G2 Esports",
#         "xbet_home": "1.52",
#         "xbet_away": "2.54",
#         "winline_home": "1.48",
#         "winline_away": "2.47",
#         "pari_home": "1.50",
#         "pari_away": "2.48"
#     }]


# print(search_partial_text(data[0]['tournament_name'], data2[0]['league_name']))
# frmt_date = re.split(r' ', data2[0]['event_date'])[0] + '2019'
# print(frmt_date)
# data2[0]['event_date'] = datetime.datetime.strptime(
#     frmt_date, '%d.%m.%Y').strftime('%Y-%m-%d')
# print(data2[0]['event_date'])
# print(data[0]['game_date'])
# if data2[0]['event_date'] == data[0]['game_date'] and search_partial_text(data2[0]['league_name'], data[0]['tournament_name']) >= 50:
#     print('yay')
#     new_params = list(data2[0].items())[4:]
#     data[0].update(new_params)
#     pprint.pprint(data[0])
# else:
#     print('fuck')
