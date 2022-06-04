import pandas as pd
from tickers import tickers
import argparse
import logging
from datetime import datetime
from pathlib import Path
import settings
import os
import sys
pd.set_option('display.max_columns', None)

logging.basicConfig(level=logging.WARNING, format='%(asctime)s : %(message)s')

# create the arguments
parser = argparse.ArgumentParser(description='dilution tracker Scraper', 
                                    epilog='By SARRAR Mohcin',
                                    allow_abbrev=False)
parser.add_argument('-t',
                        '--tickers',
                        action='store', 
                        type=str, 
                        nargs=1,
                        required=True,
                        help='the list of tickers (Example : ["HYMC","GFAI","PROG"])')


args = parser.parse_args()

list_tickers = args.tickers[0].replace('[','').replace(']','').split(',')

def get_max_columns(ll):
    lenghts = [len(l) for l in ll]
    tmp = max(lenghts)
    index = lenghts.index(tmp)

    return ll[index]

def scraper(list_tickers):
    final_dfs = []
    list_columns = []

    for ticker in list_tickers:
        logging.warning(f'Start Scraping {ticker}...')

        tick = tickers(ticker)
        
        tick.get_historical_date()
        
        tick.get_top_info()
        tick.get_rating_warrants()
        tick.get_historical_OS()
        
        tick.get_cash_position()
        tick.get_completed_offerings()
        tick.get_all_warrants()

        tick.parse_ticker_info()
        list_columns.append(tick.init_column())

        final_dfs.append(tick.results_df)

        tick.session.close()

        logging.warning(f'End Scraping {ticker}')
    
    new_list_columns = get_max_columns(list_columns)

    results_final_dfs = pd.concat(final_dfs, ignore_index=True,sort=False)
    
    results_final_dfs = results_final_dfs.reindex(columns=new_list_columns)
    
    results_final_dfs.dropna(axis=1,how='all',inplace=True)

    # write CSV file
    for fname in os.listdir('.'):
        if fname.endswith('.csv'):
            old_df = pd.read_csv(fname)
            old_columns = old_df.columns
            new_list_columns = get_max_columns([old_columns,new_list_columns])
            
            results_final_dfs = pd.concat([results_final_dfs,old_df], ignore_index=True)
            results_final_dfs = results_final_dfs.reindex(columns=new_list_columns)
            results_final_dfs.dropna(axis=1,how='all',inplace=True)
            results_final_dfs.to_csv(fname, index=False)
            break
    else:
        filename='tickers.csv'
        results_final_dfs.to_csv(filename, index=False)


    logging.warning(f'The End, the data stored to : tickers.csv')

scraper(list_tickers)