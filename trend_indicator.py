import panel as pn
from dash_api import etf_API
api = etf_API()

def make_trendindicators(fund_name, timeseries_filter, date_range_slider, colors, width, height):
    '''-laura
    params: fund_name (list of str): list of user selected fund symbols for which trend indicators will be generated
    timeseries_filter (str): a column name representing the value of interest (e.g., 'open', 'close') 
    date_range_slider (tuple of str): tuple containing the start and end dates to filter the data
    colors (list of str): list of colors in hex format, one for each fund symbol
    width (int): width of each trend indicator widget
    height (int): height of each trend indicator widget
    does:Creates a list of Trend indicator widgets for each fund symbol, visualizing the specified 
    timeseries data over the date range, retunring th emost recent price value and percent chnage over given time range
    returns: list of pn.indicators.Trend: A list of Panel Trend indicator widgets, one for each fund symbol
    '''
    # collecting all trend indicators
    trends = []
    for i, symbol in enumerate(fund_name):

        df = api.get_filtered_data([symbol], timeseries_filter, date_range_slider)

        data = {'x': df['price_date'].values, 'y': df[timeseries_filter].values}
        trend = pn.indicators.Trend(
            name=f'{symbol} Price Trend',
            data=data,
            plot_x='x',
            plot_y='y',
            plot_color=colors[i],  
            plot_type='line',
            pos_color='#00FF00',  
            neg_color='#FF3333',  
            width=width,
            height=height
        )
        trends.append(trend)

    return trends 