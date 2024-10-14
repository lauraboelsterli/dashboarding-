import plotly.graph_objects as go

def make_time_series(fund_name, filtered_local, timeseries_filter, width=800, height=400):
    '''-laura and nick
    params: fund_name (name of fund(s)(list or str)), 
    filtered_local (df) of values from only the selected time range,
    timeseries_filter (market value of interest (str)), width (int), height (int)
    does: plots a time series with given df for one or more etfs of given market price value
    of interest (like for example, closing price)
    returns: time series plotly figure 
    '''
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
        hovermode="x unified",  # Shows the hover info for all traces at the same x-position
        width=width,
        height=height
    )

    return fig