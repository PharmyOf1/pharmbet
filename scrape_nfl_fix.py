import requests
from bs4 import BeautifulSoup
import re

from engine_info import pd_kinect
import os
from sqlalchemy import create_engine, Table, MetaData, schema
from sqlalchemy.sql import table, column, select, update, insert


class TeamScrape(object):
    def __init__(self):
        self.url = 'http://www.pro-football-reference.com/'
        self.teams = {
        
        'crd':'Arizona Cardinals',
        'atl':'Atlanta Falcons',
        'rav':'Baltimore Ravens',
        'buf':'Buffalo Bills',
        'car':'Carolina Panthers',
        'chi':'Chicago Bears',
        'cin':'Cincinatti Bengals',
        'cle':'Cleveland Browns',
        'dal':'Dallas Cowboys',
        'den':'Denver Broncos',
        'det':'Detroit Lions',
        'gnb':'Green Bay Packers',
        'htx':'Houston Texans',
        'clt':'Indianapolis Colts',
        'jax':'Jacksonville Jaguars',
        'kan':'Kansas City Chiefs',
        'mia':'Miami Dolphins',
        'min':'Minnesota Vikings',
        'nwe':'New England Patriots',
        'nor':'New Orleans Saints',
        'nyg':'New York Giants',
        'nyj':'New York Jets',
        'rai':'Oakland Raiders',
        'phi':'Philadelphia Eagles',
        'pit':'Pittsburgh Steelers',
        'sdg':'San Diego Chargers',
        'sfo':'San Francisco 49ers',
        'sea':'Seattle Seahawks',
        'ram':'St. Louis Rams',
        'tam':'Tampa Bay Buccaneers',
        'oti':'Tennessee Titans',
        'was':'Washington Redskins',
        
        }

    def collect_links(self):
        all_links = []
        for key, val in self.teams.items():
            url= self.url + 'teams/' + str(key)
            soup = BeautifulSoup(requests.get(url).text,"html.parser")
            active_years = soup.find("table",id="team_index").findAll('tr')
            links = [x for y in [re.findall(r'href="/(.*?)">',str(row.findAll('td')[0]),re.DOTALL) for row in active_years[2:]] for x in y]
            all_links.append(links)
            print (('All links for the {} gathered.').format(val))

        return [self.url + x for y in all_links for x in y]

    
    def create_df(self, link):
        soup = BeautifulSoup(requests.get(link).text,"html.parser")
        sched_table = soup.find("table",id="team_gamelogs").findAll('tr')
        year = int((link[-8:].strip('.htm')))
        body = []

        for x in [x.findAll('td') for x in sched_table[2:]]:
            week = ([a.text for a in x][:21])
            week.insert(0,(self.teams[link[-12:-9]]))
            week.insert(0,'')
            body.append(week)

        PD.upload_record(body,year)
        return []

class connect_PD(object):
    def __init__(self,login_info):
        self.login_info = login_info
        self.engine = create_engine(login_info) 
        self.connection = self.engine.connect()
        self.meta = MetaData()
        self.meta.reflect(bind=self.engine)
        self.nfl_history = schema.Table('nfl_history', self.meta, autoload=True)
        print ('***PD Connection Established***')

    def upload_record(self, table_data, year):
            for row in table_data:
                self.connection.execute(self.nfl_history.insert(values=row))
                print ("{} | Week {} in {} uploaded").format(row[1],row[2],year)

    def close(self): 
        self.connection.close()
        print ('***PD Connection Terminated***')

if __name__ == '__main__':
    Scraper = TeamScrape()
    all_sites = (Scraper.collect_links())

    PD = connect_PD(pd_kinect)

    for link in all_sites:
        Scraper.create_df(link)

    PD.close()