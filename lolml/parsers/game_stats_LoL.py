# Import libraries
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import os
import re
import json


def get_html_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def contain_winners(item):
    winners_list = item.find(
        'div', {'class': 'tournament__winners'}).find('ul')
    # winners_ul = winners_list.find('ul', {'class': 'winners'})
    winners_items = winners_list.find_all('li', {'class': 'winners__item'})
    if len(winners_items) == 3:
        return winners_items
    else:
        return None


# Get match type (best of 1/3/5)
def game_bo1(item):
    score = re.sub(' ', '', item.find('td', {'class': 'text-center'}).text)
    if score == '0-1' or score == '1-0':
        return 1
    else:
        amount = re.split('-', score)
        amount = int(amount[0]) + int(amount[1])
        return amount



def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    return text


def parse_user_datafile_bs(filename):
    results = []
    text = read_file(filename)

    soup = BeautifulSoup(text, features="html.parser")
    game_time = soup.find('div', {'class': ['col-6 text-center']}).find('h1').text
    t_name1 = soup.find('a', {'href': re.compile(r'/tournament/tournament-stats/')}).text
    match_date = soup.find('div', {'class': 'col-12 col-sm-5 text-right'}).text
    match_date = re.split(' ', match_date)[0]
    print(match_date)
    all_stats = soup.find_all('div', {'class': ['row rowbreak pb-4']})
    teams_stats = all_stats[1].find_all('table', {'class': ['playersInfosLine footable toggle-square-filled']})
    blue_team = teams_stats[0].find_all('tr')[1:]
    red_team = teams_stats[1].find_all('tr')[1:]

    # Blue team's players and champions
    top_blue_obj = blue_team[0].find('a')
    top_blue_champ = re.sub(' stats', '', top_blue_obj.get('title'))
    top_blue_pl = top_blue_obj.findNext('a').text

    jg_blue_obj = blue_team[6].find('a')
    jg_blue_champ = re.sub(' stats', '', jg_blue_obj.get('title'))
    jg_blue_pl = jg_blue_obj.findNext('a').text

    mid_blue_obj = blue_team[12].find('a')
    mid_blue_champ = re.sub(' stats', '', mid_blue_obj.get('title'))
    mid_blue_pl = mid_blue_obj.findNext('a').text

    adc_blue_obj = blue_team[18].find('a')
    adc_blue_champ = re.sub(' stats', '', adc_blue_obj.get('title'))
    adc_blue_pl = adc_blue_obj.findNext('a').text

    sup_blue_obj = blue_team[24].find('a')
    sup_blue_champ = re.sub(' stats', '', sup_blue_obj.get('title'))
    sup_blue_pl = sup_blue_obj.findNext('a').text


    # Red team's players and champions
    top_red_obj = red_team[0].find('a')
    top_red_champ = re.sub(' stats', '', top_red_obj.get('title'))
    top_red_pl = top_red_obj.findNext('a').text

    jg_red_obj = red_team[6].find('a')
    jg_red_champ = re.sub(' stats', '', jg_red_obj.get('title'))
    jg_red_pl = jg_red_obj.findNext('a').text

    mid_red_obj = red_team[12].find('a')
    mid_red_champ = re.sub(' stats', '', mid_red_obj.get('title'))
    mid_red_pl = mid_red_obj.findNext('a').text

    adc_red_obj = red_team[18].find('a')
    adc_red_champ = re.sub(' stats', '', adc_red_obj.get('title'))
    adc_red_pl = adc_red_obj.findNext('a').text

    sup_red_obj = red_team[24].find('a')
    sup_red_champ = re.sub(' stats', '', sup_red_obj.get('title'))
    sup_red_pl = sup_red_obj.findNext('a').text


    # Objective statistic for each team
    objective_blue = all_stats[0].find('div', {'class': ['col-12 col-sm-6']})
    objective_red = objective_blue.parent.findNext('div').findNext('div', {'class': 'col-12 col-sm-6'})

    # Total Kills each team
    kills_blue = objective_blue.find('span').text
    kills_red = objective_red.find('span').text

    # Team's placement

    blue_team_name = all_stats[0].find('div', {'class': 'blue-line-header'}).text
    red_team_name = all_stats[0].find('div', {'class': 'red-line-header'}).text
    if ('WIN' in blue_team_name):
        # blue_team_name = re.sub(r' - WIN', '', blue_team_name)
        # blue_team_name = re.sub(r'[\n]', '', blue_team_name)
        # red_team_name = re.sub(r' - LOSS','', red_team_name)
        # red_team_name = re.sub(r'[\n]', '', red_team_name)
        # winner = blue_team_name
        bResult = 1
        rResult = 0
    else:
        # red_team_name = re.sub(r' - WIN','', red_team_name)
        # red_team_name = re.sub(r'[\n]', '', red_team_name)
        # blue_team_name = re.sub(r' - LOSS', '', blue_team_name)
        # blue_team_name = re.sub(r'[\n]', '', blue_team_name)
        # winner = red_team_name
        bResult = 0
        rResult = 1

    print(red_team_name)
    print(blue_team_name)
    results.append({
        'League': t_name1,
        'gameDate': match_date,
        'gameTime': game_time,
        'blueTeam': blue_team_name,
        'bResult': bResult,
        'rResult': rResult,
        'redTeam': red_team_name,
        'blueTop': top_blue_pl,
        'blueTopChamp': top_blue_champ,
        'blueJungle': jg_blue_pl,
        'blueJungleChamp': jg_blue_champ,
        'blueMid': mid_blue_pl,
        'blueMidChamp': mid_blue_champ,
        'blueAdc': adc_blue_pl,
        'blueAdcChamp': adc_blue_champ,
        'blueSupport': sup_blue_pl,
        'blueSupportChamp': sup_blue_champ,
        'redTop': top_red_pl,
        'redTopChamp': top_red_champ,
        'redJungle': jg_red_pl,
        'redJungleChamp': jg_red_champ,
        'redMid': mid_red_pl,
        'redMidChamp': mid_red_champ,
        'redAdc': adc_red_pl,
        'redAdcChamp': adc_red_champ,
        'redSupport': sup_red_pl,
        'redSupportChamp': sup_red_champ,
        'kills_team1': kills_blue,
        'kills_team2': kills_red
    })
    print(len(results))
    return results


soup = get_html_soup('https://gol.gg/tournament/list/region-ALL/league-1/')
tournaments = soup.find('table', {'class': 'table_list'})

line_count = 1
for tournament in tournaments.find_all('a'):
    print(tournament)
    if line_count == 5:
        link = tournament.get('href')
        t_name = tournament.text
        path = './user_data/' + str(t_name)
        if os.path.isdir(path):
            print('folder already exists')
        else:
            os.mkdir(path)
        print('\n' + t_name + ' in process \n')
        tournament_url = 'https://gol.gg/tournament/' + link
        soup = BeautifulSoup(requests.get(
            tournament_url).content, "html.parser")
        match_table = soup.find_all('div', {'class': 'col-12'})
        for table in match_table:
            if (table.find('h1')) and (table.find('h1').text == 'Last games'):
                match_list = table.find('tbody').find_all('tr')
                break

        # print(match_table)
        match_count = 1
        for match in match_list:
            if match.find('td', {'class': 'text_victory'}) or (match.find('td', {'class': 'text_defeat'})):
                #print(match.find('td', {'class': 'text-left'}).find('a').get('href')[2:])
                temp_str = ' '.join([x.text for x in match.find_all('td')])
                # match_date = re.search(r'\d{4}-\d{2}-\d{2}', temp_str)
                # match_date = match_date.group(0)
                if game_bo1(match) == 1:
                    download_url = 'http://gol.gg' + \
                        (match.find('td', {'class': 'text-left'}
                                    ).find('a').get('href')[2:])

                    match_name = re.sub(' ', '_',
                                        match.find('td', {'class': 'text-left'}).find('a').text)

                    urllib.request.urlretrieve(
                        download_url, './user_data/' + str(t_name) + '/' + str(match_name))
                    print('match № {0}, --> {1} downloading'.format(match_count, match_name))
                    match_count += 1
                else:
                    start_url = re.findall(r'\d+', match.find('td', {'class': 'text-left'}).find('a').get('href'))
                    print(type(start_url))
                    print(start_url[0])
                    for url_plus in range(game_bo1(match)):
                        download_url = 'http://gol.gg/game/stats/' + str(int(start_url[0]) + url_plus) + '/page-game/'

                        match_name = re.sub(' ', '_',
                                            match.find('td', {'class': 'text-left'}).find('a').text) + '_game{}'.format((url_plus+1))

                        urllib.request.urlretrieve(
                            download_url, './user_data/' + str(t_name) + '/' + str(match_name))
                        print('match № {0}, --> {1} downloading'.format(match_count, match_name))
                        match_count += 1
    line_count += 1

results = []
for directory in os.listdir('./user_data/'):
    print(directory)
    for filename in os.listdir('./user_data/' + directory + '/'):
        results.extend(parse_user_datafile_bs('./user_data/'+ directory + '/' + filename))
print(results)

with open('games_data.json', 'w') as fp:
    json.dump(results, fp, indent=4)
