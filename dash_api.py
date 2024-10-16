""""
Author: Laura Boelsterli

File: dash_api.py

Description: The primary API for interacting with the etf dataset.
"""
import pandas as pd

class etf_API:

    fund_df = None  # dataframe

    def __init__(self, file_path='data/ETFprices.csv'):
        '''
        initializing instance of df dataframe that will be used for the dashboard
        '''
        self.load_df(file_path)

    def load_df(self, filename):
        '''-laura
        params: filename (csv file)
        does: read the csv file into a df and convert all date columns into appropriate datetime type
        '''
        self.fund_df = pd.read_csv(filename)
        # make sure its in datetime format for usability
        self.fund_df['price_date'] = pd.to_datetime(self.fund_df['price_date'])


    def get_funds(self):
        '''-laura 
        does: fetches the list of unique ETFs within the dataset
        returns: list funds sorted in alphabetical order 
        '''
        funds = self.fund_df['fund_symbol'].unique()
        return sorted(funds)


    def get_options(self):
        '''-laura
        does: gives all market price choices shown in the search bar for plotting
        returns: all market price choices (open, close, etc.)
        '''
        df_columns = self.fund_df.columns.tolist()
        # removing price date, volume, and fund symbol from 
        # time series plotting by slicing
        df_columns = df_columns[2:-1]

        return df_columns

    def extract_local_network(self, funds, value_of_interest):
        '''-laura
        params: funds (str or list), value_of_interest (str) (market price choice (open, close, etc..))
        does: extracts all the relevant info from selected funds and selected market price value (value of interest)
        returns: df of only relevant infomraiton selected (from sleected funds and market price value)
        '''
        # filter based on choices
        fund_df = self.fund_df.loc[self.fund_df['fund_symbol'].isin(funds), ['fund_symbol', 'price_date', value_of_interest]].copy()

        return fund_df

    def get_filtered_data(self, fund_name, timeseries_filter, date_range_slider):
        '''-laura
        params: fund)name (str or list), timeseries_filter (str) (market price choice aka open, close, etc..),
        date_range_slider (tuple with start and end date)
        does: fetches and filters data for the specified funds and date range (from the date range slider)
        returns: df with only values form the specified time range'''
        # extract the data for the specified funds and columns
        local = self.extract_local_network(fund_name, timeseries_filter)
        # convert the date range to datetime format form the date slider on the dashboard
        start_date, end_date = date_range_slider
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        # filter the data based on the date range
        df = local[(local['price_date'] >= start_date) & (local['price_date'] <= end_date)]

        return df


def main():
    etf_API()

if __name__ == '__main__':
    main()