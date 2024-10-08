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
        self.fund_df = pd.read_csv(filename)
        # make sure its in datetime format for usability 
        self.fund_df['price_date'] = pd.to_datetime(self.fund_df['price_date'])
        # set date as index for better pandas time series functionality 
        self.fund_df.set_index('price_date', inplace=True)

        # print(self.fund_df)

    def get_funds(self):
        """ Fetch the list of unique phenotypes (diseases)
        with at least one positive association in the gad dataset """

        funds = self.fund_df['fund_symbol'].unique()
        # print(funds, 'unique')
        return sorted(funds)


    def get_options(self):
        df_columns = self.fund_df.columns.tolist()
        # print(df_columns)
        return df_columns

    def extract_local_network(self, fund, value_of_interest):
        # filter based on choices 
        fund_df = self.fund_df[self.fund_df['fund_symbol']== fund]
        fund_df = self.fund_df[[value_of_interest]]

        return fund_df


def main():

    stockapi = stock_API()
    stockapi.load_df('data/ETFprices.csv')

    local = stockapi.extract_local_network("AAA", 'open')
    # print(local)
    # funds = get_funds(self.fund_df)
    funds = stockapi.get_funds()
    # print(funds)
    options = stockapi.get_options()
    # print(options)


if __name__ == '__main__':
    main()