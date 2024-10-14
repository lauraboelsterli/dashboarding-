import panel as pn
from nick_etf_api import etf_API
# import sankey as sk
import datetime as dt

# import panel as pn
import pandas as pd
import altair as alt
import plotly.graph_objects as go
from matplotlib.figure import Figure
import hvplot.pandas

# Loads javascript dependencies and configures Panel (required)
pn.extension()

# clean the code 
# fix sizing 
# fix colors to be consistenly color coded 

# INITIALIZE API
api = etf_API()
api.load_df('data/ETFprices.csv')


# WIDGET DECLARATIONS
# Search Widgets
fund_name = pn.widgets.MultiSelect(name="ETFs", options=api.get_funds(), value=['SPY', 'QQQ', 'GLD'])
# fund_name = pn.widgets.Select(name="Fund", options=api.get_funds(), value='AAA')
timeseries_filter = pn.widgets.Select(name="Value of Interest", options = api.get_options(), value='close')
date_range_slider = pn.widgets.DateRangeSlider(
    name='Date Range Slider',
    start=dt.datetime(1993, 1, 28), end=dt.datetime(2021, 11, 29),
    value=(dt.datetime(1993, 1, 28), dt.datetime(2021, 11, 29)),
    step=2
)
width = pn.widgets.IntSlider(name="Width", start=250, end=2000, step=250, value=1500)
height = pn.widgets.IntSlider(name="Height", start=200, end=2500, step=100, value=800)


# this decorator tells the function when to rerun 
@pn.depends(fund_name.param.value, watch=True)
def update_date_range(fund_name):
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

def get_volume(fund_name, date_range_slider):
    '''volume returned for each day in the time range'''
    # global local
    df = api.volume(fund_name, date_range_slider)  # calling the api
    # print(local)
    # table = pn.widgets.Tabulator(df, selectable=False)
    table = pn.pane.DataFrame(df, width=500, height=300)
    return table



# time slider 
def get_plotly(fund_name, timeseries_filter, date_range_slider):
    # add in time range after
    # global local 
    local = api.extract_local_network(fund_name, timeseries_filter)
    start_date, end_date = date_range_slider
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    # plot only the date for the given dates
    filtered_local = local[(local['price_date'] >= start_date) & (local['price_date'] <= end_date)]
    # plotting time series 
    fig = go.Figure()

    for etf in fund_name:
        etf_data = filtered_local[filtered_local['fund_symbol'] == etf]  # filter data for each ETF
        fig.add_trace(go.Scatter(x=etf_data['price_date'], y=etf_data[timeseries_filter],
            mode='lines', name=etf, hoverinfo='x+y'))

    # Customize the layout with titles and axis labels
    fig.update_layout(
        title="ETF Price Tracker",
        xaxis_title="Date",
        yaxis_title=timeseries_filter,
        legend_title="ETF",
        hovermode="x unified"  # Shows the hover info for all traces at the same x-position
    )

    return fig



def get_trend_indicator(fund_name, timeseries_filter, date_range_slider):
    # found on trend holoviz web 
    start_date, end_date = date_range_slider
    trends = []  # Collect each Trend indicator here
    
    for symbol in fund_name:
        # Get the data for each selected ETF
        local = api.extract_local_network([symbol], timeseries_filter)
        start_date, end_date = date_range_slider
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        # Filter the data based on date range
        df = local[(local['price_date'] >= start_date) & (local['price_date'] <= end_date)]
        
        # Store x and y data in a dictionary format for the trend
        data = {'x': df['price_date'].values, 'y': df[timeseries_filter].values}
        
        # Create the Trend indicator for the ETF
        trend = pn.indicators.Trend(
            name=f'{symbol} Price Trend',
            data=data,
            plot_x='x',
            plot_y='y',
            # way to conenct eh color from graph to the color in the trend widget????
            plot_color='#428bca',
            plot_type='line',
            pos_color='#5cb85c',
            neg_color='#d9534f',
            width=250,
            height=200
        )
        
        # Append each trend to the list
        trends.append(trend)
    
    # Return a Column containing all trend indicators
    return pn.Column(*trends)


def get_total_volume_plot(fund_name, date_range_slider):
    start_date, end_date = date_range_slider
    local = api.extract_local_network(fund_name, 'volume')
    start_date, end_date = pd.to_datetime(start_date), pd.to_datetime(end_date)
    
    # Filter data
    df = local[(local['price_date'] >= start_date) & (local['price_date'] <= end_date)]
    
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

# catalog = pn.bind(get_catalog, fund_name, timeseries_filter)

# returns volume for given day — can make it avg value per fund selected (and make it a pie chart???)
catalog = pn.bind(get_volume, fund_name, date_range_slider)
# time_slider = pn.bind(update_date_range, fund_name)
plot = pn.bind(get_plotly, fund_name, timeseries_filter, date_range_slider)
trend_indicators = pn.bind(get_trend_indicator, fund_name, timeseries_filter, date_range_slider.param.value)
# plot = pn.bind(get_plotly, fund_name, timeseries_filter, time_slider)
# Bind this function to the layout if you want an aggregated volume view
total_volume_plot = pn.bind(get_total_volume_plot, fund_name, date_range_slider.param.value)




# DASHBOARD WIDGET CONTAINERS ("CARDS")
# plot_and_trend = pn.Row(plot, trend_indicators)
# plot_and_trend_and_volume = pn.Column(plot_and_trend, total_volume_plot)

# Wrap `trend_indicators` in a scrollable Column
trend_indicators_scrollable = pn.Column(trend_indicators, scroll=True, height=400)  # Set height limit
# Combine into a single layout line
plot_and_trend_and_volume = pn.Column(pn.Row(plot, trend_indicators_scrollable), total_volume_plot)



card_width = 320

search_card = pn.Card(
    pn.Column(
        fund_name,
        timeseries_filter, date_range_slider
    ),
    title="Search", width=card_width,height=300, collapsed=False
)


plot_card = pn.Card(
    pn.Column(
        width,
        height
    ),

    title="Plot", width=card_width, collapsed=True
)


# LAYOUT

layout = pn.template.FastListTemplate(
    title="ETF Explorer",
    sidebar=[
        search_card,
        plot_card
    ],
    theme_toggle=False,
    main=[
        pn.Tabs(
            # ("Volume Traded", catalog),  # Replace None with callback binding
            ("ETF Time Series", plot_and_trend_and_volume)  # Replace None with callback binding

            # active=1  # Which tab is active by default
        )

    ],
    header_background='#a93226'

).servable()

layout.show()
