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

    name_change = "https://www1.nseindia.com/content/equities/namechange.csv"
    symbol_change = "https://www1.nseindia.com/content/equities/symbolchange.csv"

    #bse_new_listing = "https://www.bseindia.com/markets/PublicIssues/AcqIssueDetail.aspx"
    #nse_new_listing = "https://www.nseindia.com/market-data/new-stock-exchange-listings-forthcoming"
    nse_listing = pd.read_html("https://www.nseindia.com/market-data/new-stock-exchange-listings-forthcoming")
    #dfs = pd.read_html('http://en.wikipedia.org/wiki/World_population')
    print(nse_listing[-1])
    # corp_base_path data
    corp_base_path = "https://www1.nseindia.com/corporates/datafiles/"

    corp_announcements = "AN_LATEST_ANNOUNCED.csv"
    corp_actions = "CA_TODAY.csv"
    preference_shares = "pref_shares.csv"
    daily_buyback = "AN_NAV_LATEST_ANNOUNCED.csv"
    shareholding_patterns = "LatestShareholdings.csv"
    # new set of data
    acquisition = "AN_LATEST_ANNOUNCED_ACQUISITION.csv"
    #amalgamation_merger = "AN_LATEST_ANNOUNCED_AMALGAMATION_MERGER.csv"
    demerger = "AN_LATEST_ANNOUNCED_DEMERGER.csv"
    #merger_acquisition = "AN_LATEST_ANNOUNCED_MERGER_ACQUISITION"
    open_offer = "AN_LATEST_ANNOUNCED_OPEN_OFFER.csv"
    scheme_of_arrangement = "AN_LATEST_ANNOUNCED_SCHEME_OF_ARRANGEMENT.csv"

    corp_data = [corp_announcements, corp_actions, daily_buyback, shareholding_patterns, preference_shares]
    other_data = [name_change, symbol_change]
    # new data list
    new_data = [acquisition, demerger, open_offer, scheme_of_arrangement]

    b = pd.DataFrame()
    a = pd.DataFrame()
    for i in new_data:
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
        b = pd.read_csv(dest)
        a = a.append(b, ignore_index=True, sort=False)
    return a

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
    #nse_equities_content('bulk')
    #nse_equities_content('block')
    #nse_equities_content('ShortSelling')
