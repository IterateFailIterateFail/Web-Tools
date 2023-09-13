"""
User agents (for Desktop) functions

Gets user agent list from https://www.useragents.me/

Author: Darren Li
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from ast import literal_eval
from random import choices
from .config import UA_SAVE_FILE, TIMEOUT

__all__ = ['get_user_agent']


def make_from_from_json(soup):
    """Get desktop user agent dataframe from the convineint JSON"""
    common_div = soup.find('div', id='most-common-desktop-useragents-json-csv')
    json_text = common_div.find('textarea').text
    json_text = literal_eval(json_text)
    df = pd.DataFrame(json_text).rename(columns={'ua':'user_agent', 'pct': 'percentage'})
    return df


def make_from_table(soup):
    """Get desktop user agent dataframe from the table"""

    large_div = soup.find('h2', id = 'most-common-desktop-useragents').parent
    table = large_div.find('table')
    rows = table.find('tbody').find_all('tr')

    percent_list = []
    ua_list = []

    for row in rows:
        text_area = row.find('textarea')
        if not text_area:
            continue
        td = row.find_all('td')
        percent = float(td[0].text)
        ua = text_area.text
        percent_list.append(percent)
        ua_list.append(ua)

    df = pd.DataFrame({
        'user_agent': ua_list,
        'percentage': percent_list
    })
    return df


def get_user_agent(save_file=UA_SAVE_FILE):
    """Gets a user agent, weighted by percentage"""
    df = pd.read_csv(save_file)
    user_agents = df.user_agent.values
    weights = df.percentage.values / 100
    ua = choices(population=user_agents, weights=weights, k=1)[0]
    return ua

#TODO overwrite
def make_ua_df(save_file=UA_SAVE_FILE, overwrite=False):
    """Make the user_agents.csv file"""
    url = 'https://www.useragents.me/#most-common-desktop-useragents'

    # You actually do not need a user agent to access the url
    # headers = {
    #     'User-Agent':''
    # }

    resp = requests.get(url,
                        #headers=headers, 
                        timeout=TIMEOUT)
    
    soup = BeautifulSoup(resp.text, features="lxml")

    #ua_df = make_from_from_json(soup)
    ua_df = make_from_table(soup)

    if not save_file.exists() or overwrite:
        ua_df.to_csv(save_file, index=False)
    else: 
        print('Not overriding user agent file.')

if __name__ == "__main__":

    make_ua_df()
