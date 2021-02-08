# Import libraries
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import glob
import datetime
import xlrd
import openpyxl as xl
import re


class ScrapeInGame(object):
    def __init__(self, year='2019', d_split_arr=['spring', 'summer', 'worlds', 'complete'], path='../temp/inGame/'):
        self.year = year
        self.d_split_arr = d_split_arr
        self.path = path

    def save_xlsx(self):
        for split in self.d_split_arr:
            resp = self.get_xlsx_request('https://oracleselixir.com/gamedata/' +
                                    self.year + '-' + split + '/', self.year, split)
            if str(resp) == '<Response [404]>':
                print('url not found')
                pass
            else:
                with open(self.path + self.year + '_' + self.split + '.xlsx', 'wb') as output:
                    output.write(resp.content)

    def get_xlsx_request(self, url, year, split):

        url = url
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'ga=GA1.2.241321163.1584212733; kola.128265=F35EF6A8-B1C7-4242-A989-2DB6A5687A65; kola.128265.session=F060AD5B-797E-4FC2-80C3-0506652403E8; _gid=GA1.2.510345096.1585323676,',
            'Host': 'oracleselixir.com',
            'Referer': 'https://oracleselixir.com/match-data/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/80.0.3987.87 Chrome/80.0.3987.87 Safari/537.36',
        }

        resp = requests.get(url, headers=headers)
        return resp

    def concat_tables(self):

        # filenames
        excel_names = glob.glob(self.path + "20*.xlsx")
        print(excel_names)

        # read them in
        frames = [pd.read_excel(name) for name in excel_names]


        # drop all rows except team info ones
        frames = [self.teamOnly(df) for df in frames]

        # drop unnecessary columns
        frames = [self.drop(df) for df in frames]
        print(frames[0].head(10))

        # delete the first row for all frames except the first
        # i.e. remove the header row -- assumes it's the first
        frames[1:] = [df[1:] for df in frames[1:]]

        # concatenate them..
        combined = pd.concat(frames)

        # write it out
        combined.to_csv(self.path + "combined.csv",
                        header=True, index=True)

    def teamOnly(dataObj):
        # table_raw = pd.read_csv(path)
        table_raw = dataObj
        print(type(table_raw))
        team_rows = table_raw[table_raw['playerid'].isin([100, 200])]
        return team_rows

    def drop(dataObj):
        df = dataObj
        df1 = df[['league', 'split', 'week', 'game', 'date', 'patchno', 'side', 'team',
                  'teamdragkills', 'elders', 'herald', 'teambaronkills', 'totalgold', 'earnedgpm', 'cspm']]
        df1 = df1[~(df1.league == 'LPL')]
        df1 = df1[~(df1.date == ' ')]
        return df1

    def format_date(path):
        df = pd.read_csv(path)
        print(df.date)
        df.date = (pd.to_datetime('1899-12-30') +
                   pd.to_timedelta(df.date, 'D'))
        print(df.date)
        df.to_csv('../temp/inGame/result.csv', header=True, index=False)

    def main(self):
        self.save_xlsx()
        self.concat_tables()
        self.format_date(self.path + 'combined.csv')
