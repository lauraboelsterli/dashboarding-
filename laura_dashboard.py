import panel as pn
from laura_etf_api import etf_API
import datetime as dt
import pandas as pd
import plotly.graph_objects as go
import time_series as ts

# Loads javascript dependencies and configures Panel (required)
pn.extension()

# INITIALIZE API
api = etf_API()
api.load_df('data/ETFprices.csv')

# WIDGET DECLARATIONS
# Search Widgets
fund_name = pn.widgets.MultiSelect(name="Select All ETFs of Interest", options=api.get_funds(), value=['SPY', 'QQQ', 'GLD'], 
    height=250)
timeseries_filter = pn.widgets.Select(name="Market Price Data", options = api.get_options(), value='close')
date_range_slider = pn.widgets.DateRangeSlider(
    name='Select a Date Range',
    start=dt.datetime(1993, 1, 28), end=dt.datetime(2021, 11, 29),
    value=(dt.datetime(1993, 1, 28), dt.datetime(2021, 11, 29)),
    step=2,
    width=300
)
ts_width = pn.widgets.IntSlider(name="Width", start=250, end=800, step=50, value=600)
ts_height = pn.widgets.IntSlider(name="Height", start=200, end=800, step=50, value=400)
trend_width = pn.widgets.IntSlider(name="Width", start=50, end=600, step=50, value=300)
trend_height = pn.widgets.IntSlider(name="Height", start=50, end=600, step=50, value=100)



# this decorator tells the function when to rerun
# aka everytime fund_name chosen from the multiselect
@pn.depends(fund_name.param.value, watch=True)
def update_date_range(fund_name):
    '''-laura 
    params: fund name (lst or str)
    does: eerytime new fund_names are chosen on the dashboard this function gets triggered, to dynamically 
    change the date range slider options to only show relevant dates for those given funds (returns
    minimum date and maximum dates from given fund(s) seleciton)
    functionality and implementation found here: https://panel.holoviz.org/api/panel.depends.html
    returns: updated slider widget on the dashboard
    '''

    min_date = api.fund_df[api.fund_df['fund_symbol'].isin(fund_name)]['price_date'].min()
    max_date = api.fund_df[api.fund_df['fund_symbol'].isin(fund_name)]['price_date'].max()
    date_range_slider.start = min_date
    date_range_slider.end = max_date
    date_range_slider.value = (min_date, max_date)


# CALLBACK FUNCTIONS

def get_plotly(fund_name, timeseries_filter, date_range_slider, width, height):
    '''-laura
    params: fund_name (name of fund(s)(list or str)), timeseries_filter (market value of interest (str)), 
    date_range_slider (start and end date (tuple), width (int), height (int)
    does: given a fund name(s), a value of interest (e.g. open,close prices), and time range, a time series plot 
    is plotted on plotly 
    returns: a time series figure for one or more etf funds
    '''
    # global filtered_local 
    filtered_local = api.get_filtered_data(fund_name, timeseries_filter, date_range_slider)
    # plotting time series 
    fig = ts.make_time_series(fund_name, filtered_local, timeseries_filter, width, height)

    return fig


def get_trend_indicator(fund_name, timeseries_filter, date_range_slider, width=250, height=200):
    '''-laura
    params: fund_name (name of fund(s)(list or str)), timeseries_filter (market value of interest (str)), 
    date_range_slider (start and end date (tuple), width (int), height (int)
    does: get trends for each fund automatically calculated (y value (chosen value of interest) 
    most recent value percentage change is computed by first value (from chosen start date) 
    and last value (from chosen end date)) measures done by indicators widget 
    and then each fund with its metrics gets returns as column
    returns: trend indicator widgets '''
    # collecting all trend indicators
    trends = []  
    
    # Iterate over each fund symbol in the list
    for symbol in fund_name:
        # fetching and filter the data
        df = api.get_filtered_data([symbol], timeseries_filter, date_range_slider)
        # print(df)

        # prepping data for the trend indicator in dct format
        data = {'x': df['price_date'].values, 'y': df[timeseries_filter].values}
        
        # creating the Trend indicator for the ETF
        trend = pn.indicators.Trend(
            name=f'{symbol} Price Trend',
            data=data,
            plot_x='x',
            plot_y='y',
            plot_color='#428bca',
            plot_type='line',
            pos_color='#5cb85c',
            neg_color='#d9534f',
            width=width,
            height=height
        )
        
        # append each trend to the list
        trends.append(trend)
    
    # returning a column containing all trend indicators
    return pn.Column(*trends)



def get_total_volume_plot(fund_name, date_range_slider, width=600, height=400):
    '''-laura 
    params: fund_name (name of fund(s)(list or str)), 
    date_range_slider (start and end date (tuple), width (int), height (int)
    does: makes bar plots for total volume for each given fund
    returns: figure of bar plot made on plotly 
    '''
    df = api.get_filtered_data(fund_name, 'volume', date_range_slider)

    # calculate total volume per ETF
    total_volumes = df.groupby('fund_symbol')['volume'].sum().reset_index()
    # plotting the total volume:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=total_volumes['fund_symbol'], 
        y=total_volumes['volume'],
        name="Total Volume",
        opacity=1
    ))
    
    fig.update_layout(
        title="Total Volume Traded Over Selected Date Range",
        xaxis_title="ETF",
        yaxis_title="Total Volume",
        barmode='group',
        width = width,
        height=height
    )
    
    return fig

def get_total_volume_indicator(fund_name, date_range_slider, width=300, height=300):
    '''-laura 
    params: fund_name (name of fund(s)(list or str)), 
    date_range_slider (start and end date (tuple), width (int), height (int)
    does: creates a summary indicator for total volume over the selected time range for 
    each ETF with numeric values formatted with suffixes to indicate if the number 
    is in billions, millions, etc., to reduce clutter and enhance readability
    returns: returns volume indicator widgets 
    '''
    df = api.get_filtered_data(fund_name, 'volume', date_range_slider)

    # Calculate total volume per ETF
    total_volumes = df.groupby('fund_symbol')['volume'].sum()
    
    # List to hold each volume indicator
    indicators = []
    
    for symbol, volume in total_volumes.items():
        # Determine suffix based on the value's magnitude
        if volume >= 1_000_000_000:
            display_value = volume / 1_000_000_000
            suffix = 'Billions'
        elif volume >= 1_000_000:
            display_value = volume / 1_000_000
            suffix = 'Millions'
        elif volume >= 1_000:
            display_value = volume / 1_000
            suffix = 'Thousands'
        else:
            display_value = volume
            suffix = ''

        # Create a Number indicator, using numeric value and adding the suffix in the name
        indicator = pn.indicators.Number(
            name=f'Total Volume for {symbol} ({suffix})',
            value=display_value,  # This remains a numeric value
            format='{value:.1f}',  # Use formatting for one decimal place
            sizing_mode='fixed',
            width=width,
            height=height
        )
        indicators.append(indicator)

    return pn.Row(*indicators)




# CALLBACK BINDINGS (Connecting widgets to callback functions)
plot = pn.bind(get_plotly, fund_name, timeseries_filter, date_range_slider, ts_width, ts_height)
trend_indicators = pn.bind(get_trend_indicator, fund_name, timeseries_filter, date_range_slider.param.value, trend_width, trend_height)
volume_indicators = pn.bind(get_total_volume_indicator, fund_name, date_range_slider.param.value)


# DASHBOARD WIDGET CONTAINERS ("CARDS")
trend_indicators_scrollable = pn.Column(trend_indicators, scroll=True, height=400)  # Set height limit
scrollable_row = pn.Column(pn.Row(volume_indicators),scroll=True,width=1000)
# volume_plot = pn.Row(total_volume_plot, scroll=True)
volume_plot = pn.Row(scrollable_row, scroll=True)
# Combine into a single layout line
plot_and_trend = pn.Column(pn.Row(plot, trend_indicators_scrollable ), volume_plot)



card_width = 320

search_card = pn.Card(
    pn.Column(fund_name, timeseries_filter, date_range_slider),
    title="Search",
    width=card_width,
    sizing_mode='stretch_width',  
    collapsed=False
)

plot_card = pn.Card(
    pn.Column(ts_width, ts_height),
    title="Time Series Dimensions",
    width=card_width,
    sizing_mode='stretch_width',  
    collapsed=True
)

trend_card = pn.Card(
    pn.Column(trend_width, trend_height),
    title="Price Trend Dimensions",
    width=card_width,
    sizing_mode='stretch_width',  
    collapsed=True
)

stacked_cards = pn.Column(
    search_card,
    plot_card,
    trend_card,
    sizing_mode='stretch_width'
    )


# LAYOUT
layout = pn.template.FastListTemplate(
    title="ETF Explorer",
    sidebar=[
        stacked_cards
    ],
    theme= 'dark',
    theme_toggle=False,
    main=[
        plot_and_trend
    ],
    header_background='#a93226'

).servable()

layout.show()
