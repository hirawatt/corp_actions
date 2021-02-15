import requests
import pandas as pd
from IPython.display import display
from tabulate import tabulate
import io
import os
from dotenv import load_dotenv
from datetime import datetime, date

load_dotenv()
discord_webhook_url = os.getenv('discord_webhook_url')
discord_webhook_url_nse = os.getenv('discord_webhook_url_nse')
discord_webhook_url_bse = os.getenv('discord_webhook_url_bse')

def corporates():
    pwd = os.getcwd()

    today = date.today()
    year = today.year
    mnth = today.strftime('%b').upper()
    dt = today.strftime('%d')

    corp_base_path = "https://www1.nseindia.com/corporates/datafiles/"

    corp_announcements = "AN_LATEST_ANNOUNCED.csv"
    corp_actions = "CA_TODAY.csv"
    name_change = "https://www1.nseindia.com/content/equities/namechange.csv"
    symbol_change = "https://www1.nseindia.com/content/equities/symbolchange.csv"
    preference_shares = "pref_shares.csv"
    daily_buyback = "AN_NAV_LATEST_ANNOUNCED.csv"
    shareholding_patterns = "LatestShareholdings.csv"

    corp_data = [corp_announcements, corp_actions, daily_buyback, shareholding_patterns, preference_shares]
    other_data = [name_change, symbol_change]

    for i in corp_data:
        dest = pwd +'/data/'+ i
        dest_url = corp_base_path + i
        print(dest, dest_url, sep='\n')
        r = requests.get(dest_url)
        print(r.status_code)
        if r.status_code == 200:
            r = r.text
        else:
            raise ValueError("Error Downloadning File", i)
        with open(dest, 'w') as f:
            f.write(r)
        data = pd.read_csv(io.StringIO(r))
        tabular_data = tabulate(data, tablefmt="grid")
        msg = {
            "Content-Type": "multipart/form-data",
            "content": tabular_data
            }
        requests.post(discord_webhook_url_nse, data=msg)

def nse_equities_content(i):
    pwd = os.getcwd()
    dest = pwd + '/data/' + i + '.csv'
    dest_url = "https://archives.nseindia.com/content/equities/{}.csv"
    r = requests.get(dest_url.format(i))
    print(dest, dest_url.format(i))
    print(r.status_code)
    if r.status_code == 200:
        r = r.text
    else:
        raise ValueError("Error Downloadning File", i)
    with open(dest, 'w') as f:
        f.write(r)
    data = pd.read_csv(io.StringIO(r))
    tabular_data = tabulate(data, tablefmt="grid")
    msg = {
        "Content-Type": "multipart/form-data",
        "content": tabular_data
        }
    requests.post(discord_webhook_url_nse, data=msg)

if __name__ == '__main__':
    corporates()
    nse_equities_content('bulk')
    nse_equities_content('block')
    nse_equities_content('ShortSelling')
