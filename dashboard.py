""""
Author: Laura Boelsterli and Nick

File: dashboard.py

Description: The dashbaord file interacting with api from etf dataset 
"""
import panel as pn
from dash_api import etf_API
import datetime as dt
import time_series as ts
import trend_indicator as trend_ind
import volume_indicator as vol_ind
import volatility as volatility 
import seaborn as sns

# Loads javascript dependencies and configures Panel (required)
pn.extension()

# INITIALIZE API
api = etf_API()

# WIDGET DECLARATIONS
# Search Widgets
fund_name = pn.widgets.MultiChoice(name="Select All ETFs of Interest", options=api.get_funds(),
                                   value=['SPY', 'QQQ', 'GLD'],
                                   height=150)
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
trend_width = pn.widgets.IntSlider(name="Width", start=50, end=600, step=25, value=300)
trend_height = pn.widgets.IntSlider(name="Height", start=50, end=600, step=25, value=125)
volatility_width = pn.widgets.IntSlider(name="Width", start=250, end=1000, step=50, value=800)
volatility_height = pn.widgets.IntSlider(name="Height", start=200, end=800, step=50, value=500)
# price trend display options
display_option = pn.widgets.RadioButtonGroup(
    name='Display Options',
    options=['Raw Data', 'Moving Average', 'Both'],
    value='Raw Data',
    width=300
)
# Volatility Display Options
volatility_display_option = pn.widgets.RadioButtonGroup(
    name='Volatility Display Options',
    options=['Raw Data', 'Moving Standard Dev', 'Both'],
    value='Moving Standard Dev',
    width=300
)
# rolling windnow variable connected to both the volatility and price trend graphs 
ma_window = pn.widgets.IntSlider(name="Rolling Window", start=1, end=365, step=5, value=80)




# decorator tells the function when to rerun, everytime
# a fund_name is chosen from the multiselect
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

def get_plotly(fund_name, timeseries_filter, date_range_slider, width, height, ma_window, display_option):
    '''
    -laura
    params: fund_name (name of fund(s)(list or str)), timeseries_filter (market value of interest (str)), 
    date_range_slider (start and end date (tuple), width (int), height (int), ma_window (int), display_option (str)
    does: given a fund name(s), a value of interest (e.g. open, close prices), and time range, a time series plot 
    is plotted on plotly (plotting raw data and/or moving averages depeding on user widget choice on dashboard)
    returns: a time series figure for one or more etf funds with optional moving averages
    '''
    filtered_local = api.get_filtered_data(fund_name, timeseries_filter, date_range_slider)
    colors = generate_color_palette(len(fund_name))

    # Pass display options and moving average window to the plot function
    fig = ts.make_time_series(fund_name, filtered_local, timeseries_filter, colors, width, height, ma_window, display_option)

    return fig


def get_trend_indicator(fund_name, timeseries_filter, date_range_slider, width=250, height=200):
    '''-laura
    params: fund_name (name of fund(s)(list or str)), timeseries_filter (market value of interest (str)), 
    date_range_slider (start and end date (tuple), width (int), height (int)
    does: get trends for each fund automatically calculated (y value (chosen value of interest) 
    most recent value percentage change is computed by first value (from chosen start date) 
    and last value (from chosen end date)) measures done by indicators widget 
    returns: trend indicator widgets '''

    colors = generate_color_palette(len(fund_name))
    trends = trend_ind.make_trendindicators(fund_name, timeseries_filter, date_range_slider, colors, width, height)
    return pn.Column(*trends)


def get_total_volume_indicator(fund_name, date_range_slider, width=300, height=300):
    '''-laura 
    params: fund_name (name of fund(s)(list or str)), 
    date_range_slider (start and end date (tuple), width (int), height (int)
    does: creates a summary indicator for total volume over the selected time range for 
    each ETF with numeric values formatted with suffixes to indicate if the number 
    is in billions, millions, etc., to reduce clutter and enhance readability
    returns: returns volume indicator widgets 
    '''
    indicators = vol_ind.make_volindicator(fund_name, date_range_slider, width, height)
    return pn.Row(*indicators)


def get_volatility_chart(fund_name, timeseries_filter, date_range_slider, ma_window, volatility_display_option, width=800, height=500 ):
    '''-laura 
    params:fund_name (str or list), timeseries_filter (str), date_range_slider (tuple), width (int), height (int), 
    ma_window (int) (this is the selected rolling window), 
    volatility_display_option (str) (chosen by suer (to show raw data, rolling sd ot both))
    does: Plots volatility as either raw daily percentage changes, rolling volatility, or both
    returns:fig: a Plotly figure object showing the volatility plot
    '''
    filtered_local = api.get_filtered_data(fund_name, timeseries_filter, date_range_slider)
    colors = generate_color_palette(len(fund_name))
    fig = volatility.make_volatility_chart(fund_name, filtered_local, timeseries_filter, colors, ma_window, volatility_display_option, width, height)
    return fig

def generate_color_palette(n):
    '''nick'''
    return sns.color_palette("husl", n).as_hex()



# CALLBACK BINDINGS (Connecting widgets to callback functions)

# plot = pn.bind(get_plotly, fund_name, timeseries_filter, date_range_slider, ts_width, ts_height)
plot = pn.bind(get_plotly, fund_name, timeseries_filter, date_range_slider, ts_width, ts_height, ma_window, display_option)
trend_indicators = pn.bind(get_trend_indicator, fund_name, timeseries_filter, date_range_slider.param.value, trend_width, trend_height)
volume_indicators = pn.bind(get_total_volume_indicator, fund_name, date_range_slider.param.value)
volatility_chart = pn.bind(get_volatility_chart, fund_name, timeseries_filter, date_range_slider, ma_window, volatility_display_option, volatility_width, volatility_height)

# DASHBOARD WIDGET CONTAINERS ("CARDS")
trend_indicators_scrollable = pn.Column(trend_indicators, scroll=True, height=400)  # Set height limit
scrollable_row = pn.Column(pn.Row(volume_indicators),scroll=True)
# scrollable_row = pn.Column(pn.Row(volume_indicators),scroll=True,width=600)
# volume_plot = pn.Row(total_volume_plot, scroll=True)
volume_plot = pn.Row(scrollable_row, scroll=True, width=900, height = 200 )
# Combine into a single layout line
plot_and_trend = pn.Column(pn.Row(plot, trend_indicators_scrollable ), volume_plot)



card_width = 320


options_card = pn.Card(
    pn.Column(
        pn.pane.Markdown("### Price Tracker Display Options"),  # Title for Price Trend Options
        display_option,
        pn.pane.Markdown("### Volatility Analysis Display Options"),  # Title for Volatility Options
        volatility_display_option,
        pn.pane.Markdown("### Rolling Window"),  # Title for Moving Average
        ma_window
    ),
    title="Rolling Window Graph Options",
    width=card_width,
    sizing_mode='stretch_width',
    collapsed=True 
)

search_card = pn.Card(
    pn.Column(fund_name, timeseries_filter, date_range_slider),
    title="Search",
    width=card_width,
    sizing_mode='stretch_width',  
    collapsed=False
)


plotandtrend_card = pn.Card(
    pn.Column(
        pn.pane.Markdown("### ETF Price Tracker Time Series"),  # Title for Price Trend Options
        pn.Column(ts_width, ts_height),
        pn.pane.Markdown("### ETF Price Trend Indicator"),  # Title for Volatility Options
        pn.Column(trend_width, trend_height)
    ),
    title="ETF Price Trend Tab Dimensions",
    width=card_width,
    sizing_mode='stretch_width',
    collapsed=True 
)

volatility_card = pn.Card(
    pn.Column(volatility_width, volatility_height),
    title="ETF Volatility Tab Dimensions",
    width=card_width,
    sizing_mode='stretch_width',  
    collapsed=True
)

stacked_cards = pn.Column(
    search_card,
    options_card,  
    plotandtrend_card,
    volatility_card,
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
                pn.Tabs(
        ("Price Trends", plot_and_trend),
        ("Volatility Analysis", volatility_chart)
        )
    ],
    header_background='#333333',
    accent_base_color='#1C1C1C'

).servable()

layout.show()



