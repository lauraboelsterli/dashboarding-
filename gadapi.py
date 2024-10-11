""""
File: gadapi.py

Description: The primary API for interacting with the gad dataset.
"""

import pandas as pd
import sankey as sk
from collections import Counter



class stock_API:

    fund_df = None  # dataframe

    def load_df(self, filename):
        '''laura'''
        self.fund_df = pd.read_csv(filename)
        # make sure its in datetime format for usability 
        self.fund_df['price_date'] = pd.to_datetime(self.fund_df['price_date'])




        # print(self.fund_df)

    # def get_df_ts(self, df, window_size):
    #     # df['date'] = pd.to_datetime(df.date)
    #     # Select only numeric columns for the rolling mean
    #     numeric_df = df.select_dtypes(include='number')
    #     # Apply the rolling mean on numeric columns only
    #     rolling_mean_df = numeric_df.rolling(window=window_size).mean()
    #     # Adding back the non-numeric column so we have the fund name wiht the rolling mean
    #     rolling_mean_df['fund_symbol'] = df['fund_symbol']
    #     # could go back and put the date indexing her einstea dof in the load_df function
    #     return rolling_mean_df.reset_index()
    

# work on this one if anything 
    # def get_df_ts(self, fund_name, time_series_filter, window):
    #     # df['date'] = pd.to_datetime(df.date)
    #     # set date as index for better pandas time series functionality 
    #     self.fund_df.set_index('price_date', inplace=True)
    #     # Select only numeric columns for the rolling mean
    #     numeric_df = df.select_dtypes(include='number')
    #     # Apply the rolling mean on numeric columns only
    #     rolling_mean_df = numeric_df.rolling(window=window_size).mean()
    #     # Adding back the non-numeric column so we have the fund name wiht the rolling mean
    #     rolling_mean_df['fund_symbol'] = df['fund_symbol']
    #     # could go back and put the date indexing her einstea dof in the load_df function
        
    #     return rolling_mean_df.reset_index()


        


    def get_funds(self):
        '''laura'''
        """ Fetch the list of unique phenotypes (diseases)
        with at least one positive association in the gad dataset """

        funds = self.fund_df['fund_symbol'].unique()
        # print(funds, 'unique')
        return sorted(funds)


    def get_options(self):
        '''laura'''
        df_columns = self.fund_df.columns.tolist()
        df_columns = df_columns[1:]
        print(df_columns)
        return df_columns

    def extract_local_network(self, fund, value_of_interest):
        '''laura'''
        # filter based on choices 
        # fund_df = self.fund_df[self.fund_df['fund_symbol']== fund]
        # fund_df = self.fund_df[[value_of_interest]]
        # fund_df['price_date']= self.fund_df['price_date']

        # fund_df = self.fund_df[self.fund_df['fund_symbol'] == fund].copy()
        # fund_df = self.fund_df[[value_of_interest]]
        # fund_df['price_date'] = self.fund_df['price_date'].values
        fund_df = self.fund_df.loc[self.fund_df['fund_symbol'] == fund, ['price_date', value_of_interest]].copy()


        return fund_df


def main():

    stockapi = stock_API()
    stockapi.load_df('data/ETFprices.csv')
    df= stockapi.fund_df
    # print(df)
    funds = stockapi.get_funds()

    # get_df_ts(self, df, funds, window_size=5)
    # timeseriesdf= stockapi.get_df_ts(df, window_size=5)
    # print(timeseriesdf)


    local = stockapi.extract_local_network("AAA", 'open')

    print(local)
    # funds = get_funds(self.fund_df)
    
    # print(funds)
    options = stockapi.get_options()

    # print(options)





if __name__ == '__main__':
    main()