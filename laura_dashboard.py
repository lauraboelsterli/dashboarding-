import panel as pn
from laura_etf_api import etf_API
# import sankey as sk
import datetime as dt

# import panel as pn
import pandas as pd
import altair as alt
import plotly.graph_objects as go
from matplotlib.figure import Figure
# import hvplot.pandas
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
# fund_name = pn.widgets.Select(name="Fund", options=api.get_funds(), value='AAA')
timeseries_filter = pn.widgets.Select(name="Market Price Data", options = api.get_options(), value='close')
date_range_slider = pn.widgets.DateRangeSlider(
    name='Select a Date Range',
    start=dt.datetime(1993, 1, 28), end=dt.datetime(2021, 11, 29),
    value=(dt.datetime(1993, 1, 28), dt.datetime(2021, 11, 29)),
    step=2,
    width=300
)
# width = pn.widgets.IntSlider(name="Width", start=250, end=2000, step=250, value=1500)
# height = pn.widgets.IntSlider(name="Height", start=200, end=2500, step=100, value=800)


# this decorator tells the function when to rerun 
@pn.depends(fund_name.param.value, watch=True)
def update_date_range(fund_name):
    '''updates the time range slider depending on the 
    minimum date and maximum date funds for each given 
    fund seleciton'''
    # selected_funds = event.new
    min_date = api.fund_df[api.fund_df['fund_symbol'].isin(fund_name)]['price_date'].min()
    max_date = api.fund_df[api.fund_df['fund_symbol'].isin(fund_name)]['price_date'].max()
    date_range_slider.start = min_date
    date_range_slider.end = max_date
    date_range_slider.value = (min_date, max_date)

# def update_date_range(event):
#     selected_funds = event.new
#     if selected_funds:
#         min_date = api.fund_df[api.fund_df['fund_name'].isin(selected_funds)]['price_date'].min()
#         max_date = api.fund_df[api.fund_df['fund_name'].isin(selected_funds)]['price_date'].max()
#         date_range_slider.start = min_date
#         date_range_slider.end = max_date
#         date_range_slider.value = (min_date, max_date)
# fund_name.param.watch(update_date_range, 'value')



# CALLBACK FUNCTIONS

# time slider 
def get_plotly(fund_name, timeseries_filter, date_range_slider):
    '''given fundname, value of itnerest (e.g. open,close prices), 
    returns a time series plot for one or more etf funds '''
    # global filtered_local 
    filtered_local = api.get_filtered_data(fund_name, timeseries_filter, date_range_slider)
    # plotting time series 
    fig = ts.make_time_series(fund_name, filtered_local, timeseries_filter)

    # fig = go.Figure()

    # for etf in fund_name:
    #     etf_data = filtered_local[filtered_local['fund_symbol'] == etf]  # filter data for each ETF
    #     fig.add_trace(go.Scatter(x=etf_data['price_date'], y=etf_data[timeseries_filter],
    #         mode='lines', name=etf, hoverinfo='x+y'))

    # # Customize the layout with titles and axis labels
    # fig.update_layout(
    #     title="ETF Price Tracker",
    #     xaxis_title="Date",
    #     yaxis_title=timeseries_filter,
    #     legend_title="ETF",
    #     hovermode="x unified"  # Shows the hover info for all traces at the same x-position
    # )

    return fig


def get_trend_indicator(fund_name, timeseries_filter, date_range_slider):
    '''get trends for each fund automatically calculated (y value (chosen value of interest) 
    most recent value percentage change is computed by first value (from chosen start date) 
    and last value (from chosen end date)) measures done by indicators widget 
    and then each fund with its metrics gets returns as column'''
    # collecting all Trend indicators
    trends = []  
    
    # Iterate over each fund symbol in the list
    for symbol in fund_name:
        # Use the API function to fetch and filter the data
        df = api.get_filtered_data([symbol], timeseries_filter, date_range_slider)
        # print(df)

        # prepping data for the trend indicator in dct format
        data = {'x': df['price_date'].values, 'y': df[timeseries_filter].values}
        
        # Create the Trend indicator for the ETF
        trend = pn.indicators.Trend(
            name=f'{symbol} Price Trend',
            data=data,
            plot_x='x',
            plot_y='y',
            plot_color='#428bca',
            plot_type='line',
            pos_color='#5cb85c',
            neg_color='#d9534f',
            width=250,
            height=200
        )
        
        # append each trend to the list
        trends.append(trend)
    
    # returning a column containing all trend indicators
    return pn.Column(*trends)



def get_total_volume_plot(fund_name, date_range_slider):
    '''make bar plots for total volume for each given fund'''
    df = api.get_filtered_data(fund_name, 'volume', date_range_slider)

    # Calculate total volume per ETF
    total_volumes = df.groupby('fund_symbol')['volume'].sum().reset_index()
    # Plot total volume
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
        barmode='group'
    )
    
    return fig



# CALLBACK BINDINGS (Connecting widgets to callback functions)


# time_slider = pn.bind(update_date_range, fund_name)
plot = pn.bind(get_plotly, fund_name, timeseries_filter, date_range_slider)
trend_indicators = pn.bind(get_trend_indicator, fund_name, timeseries_filter, date_range_slider.param.value)
total_volume_plot = pn.bind(get_total_volume_plot, fund_name, date_range_slider.param.value)
# maybe add average volume traded on the side of the volume plot (similar look to the trend indicators next to the time series plot)
# also make the width and height of the cards adjustable
# and have consistent color coding across all plots 




# DASHBOARD WIDGET CONTAINERS ("CARDS")
trend_indicators_scrollable = pn.Column(trend_indicators, scroll=True, height=400)  # Set height limit
volume_plotting = pn.Column(total_volume_plot, height=400)
# Combine into a single layout line
plot_and_trend = pn.Column(pn.Row(plot, trend_indicators_scrollable))



card_width = 320

search_card = pn.Card(
    pn.Column(fund_name, timeseries_filter, date_range_slider),
    title="Search",
    width=card_width,
    height=300,
    collapsed=False
    # css_classes=['card-padding']
)


# plot_card = pn.Card(
#     pn.Column(
#         width,
#         height
#     ),

#     title="Plot", width=card_width, collapsed=True
# )


# LAYOUT

layout = pn.template.FastListTemplate(
    title="ETF Explorer",
    sidebar=[
        search_card
        # plot_card
    ],
    theme= 'dark',
    theme_toggle=False,
    main=[
        pn.Tabs(
            ("ETF Time Series", plot_and_trend),
            ("Volume Traded", volume_plotting),  # Replace None with callback binding
            active=0  # Which tab is active by default
        )

    ],
    header_background='#a93226'

).servable()

layout.show()
