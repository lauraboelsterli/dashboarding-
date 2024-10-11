# make time series plot to bring into the gad explorer 
from gadapi import stock_API 

# can have a trend widget as well maybe 

import panel as pn
import pandas as pd
import altair as alt
import plotly.graph_objects as go
from matplotlib.figure import Figure
import hvplot.pandas

pn.extension('plotly', 'vega', template='bootstrap')

api = stock_API()

tickers = api.get_funds()
data = api.load_df('data/ETFprices.csv')

def get_df_ts(tickers, window_size):
    df = pd.DataFrame(getattr(data, tickers))
    # df['date'] = pd.to_datetime(df.date)
    # could go back and put the date indexing her einstea dof in the load_df function
    return df.rolling(window=window_size).mean().reset_index()

# def get_altair(ticker, window_size):
#     df = get_df_ts(ticker, window_size)
#     return alt.Chart(df).mark_line().encode(x='date', y='close').properties(
#         width="container", height=400
#     )

# def get_hvplot(ticker, window_size):
#     df = get_df_ts(ticker, window_size)
#     return df.hvplot.line('date', 'close', grid=True, responsive=True, height=400)

# def get_mpl(ticker, window_size):
#     fig = Figure(figsize=(10, 6))
#     ax = fig.subplots()
#     df = get_df_ts(ticker, window_size)
#     df.plot.line('date', 'close', ax=ax)
#     return fig

# def get_plotly(ticker, window_size):
#     df = get_df_ts(ticker, window_size)
#     return go.Scatter(x=df.date, y=df.close)

# plot_fns = {
#     'altair': get_altair,
# 	'hvplot': get_hvplot,
# 	'matplotlib': get_mpl,
# 	'plotly': get_plotly
# }