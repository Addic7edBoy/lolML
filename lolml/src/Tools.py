import pathlib
import json
import re
import csv
import pandas as pd
import os
import requests
import urllib.request
from bs4 import BeautifulSoup


class myTools(object):
    def __init__(self, *args):
        self.initialValues = {'matchupFoe': '../Data/matchups/foe', 'matchupAlly': '../Data/matchups/ally', 'gameStats': '../user_data/', 'test': './'}
        self.targets = self.initialValues.keys()
        self.paths = list(self.initialValues.values())
        self.types = ['csv', 'json', 'txt']

    def __repr__(self):
        self.temp = []
        for k, v in self.initialValues.items():
            self.temp.append("'{}': {}".format(k, v))
        return self.temp

    def get_soup(url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def check_paths(self):
        for path in self.paths:
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    def json2csv(self, inFile, outFile):
        df = pd.read_json(inFile)
        export_csv = df.to_csv (outFile, index = None, header=True)
        return export_csv


    def write_file(self, target, filename, df):
        # Tools.check_paths(self)
        if target in self.targets:
            path = self.initialValues[target] + filename
            doc_type = re.split(r'\.', filename)[1]
            print(filename)
            print(path)
            print(doc_type, ' type')
            if doc_type in self.types:
                if doc_type == 'csv':
                    df = pd.DataFrame(df)
                    df.to_csv(path, index=False, header=True)

                elif doc_type == 'json':
                    with open(path, 'w') as fp:
                        json.dump(df, fp, indent=4)

                elif doc_type == 'txt':
                    with open(path, 'w') as fp:
                        fp.write(str(df))

            else:
                raise self.BadInputException('type')
        else:
            raise self.BadInputException('target')

    def load_file(self, target, filename):
        if target in self.targets:
            path = self.initialValues[target] + filename
            doc_type = re.split(r'\.', filename)[1]
            print(path)
            print(doc_type)
            if doc_type in self.types:
                if doc_type == 'csv':
                    df = pd.read_csv(path, index_col=None)
                    return df

                elif doc_type == 'json':
                    with open(path, 'r') as fp:
                        data = json.load(fp)
                    return data

                elif doc_type == 'txt':
                    with open(path, 'r') as fp:
                        data = fp.read()
                    return data
            else:
                raise self.BadInputException('type')
        else:
            raise self.BadInputException('target')

    class BadInputException(Exception):
        def __init__(self, x):
            Exception.__init__(self, "Non existing atrributes chosen. \n Here's a list of available variables:\n 'type': ['csv', 'json', 'txt']\n 'target' and its path: {0}".format(myTools.__repr__()))
