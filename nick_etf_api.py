""""
File: gadapi.py

Description: The primary API for interacting with the gad dataset.
"""

import pandas as pd
# import sankey as sk
from collections import Counter


class etf_API:
    fund_df = None  # dataframe

    def load_df(self, filename):
        '''laura'''
        self.fund_df = pd.read_csv(filename)
        # make sure its in datetime format for usability 
        self.fund_df['price_date'] = pd.to_datetime(self.fund_df['price_date'])

    def get_funds(self):
        '''laura'''
        """ Fetch the list of unique ETFs within the dataset"""

        funds = self.fund_df['fund_symbol'].unique()
        # print(funds, 'unique')
        return sorted(funds)

    def get_options(self):
        '''laura'''
        df_columns = self.fund_df.columns.tolist()
        # to remove price date, volume, and fund symbol from time series plotting
        df_columns = df_columns[2:-1]

        return df_columns

    def extract_local_network(self, funds, value_of_interest):
        '''laura'''
        # filter based on choices
        fund_df = self.fund_df.loc[
            self.fund_df['fund_symbol'].isin(funds), ['fund_symbol', 'price_date', value_of_interest]].copy()

        return fund_df

    def get_filtered_data(self, fund_name, timeseries_filter, date_range_slider):
        """Fetch and filter data for the specified funds and date range"""
        # Extract the data for the specified funds and columns
        local = self.extract_local_network(fund_name, timeseries_filter)
        # Convert the date range to datetime format
        start_date, end_date = date_range_slider
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        # Filter the data based on the date range
        df = local[(local['price_date'] >= start_date) & (local['price_date'] <= end_date)]

        return df


def main():
    stockapi = etf_API()
    stockapi.load_df('data/ETFprices.csv')
    df = stockapi.fund_df
    # print(df)
    funds = stockapi.get_funds()
    # print(funds)

    # local = stockapi.extract_local_network(["AAA"], 'open')
    # print(local)

    options = stockapi.get_options()
    # print(options)


if __name__ == '__main__':
    main()