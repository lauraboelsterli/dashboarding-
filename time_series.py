import plotly.graph_objects as go

def make_time_series(fund_name, filtered_local, timeseries_filter,colors, width=800, height=400):
    '''-laura 
    params: fund_name (name of fund(s)(list or str)), 
    filtered_local (df) of values from only the selected time range,
    timeseries_filter (market value of interest (str)), width (int), height (int)
    does: plots a time series with given df for one or more etfs of given market price value
    of interest (like for example, closing price)
    returns: time series plotly figure 
    '''
    fig = go.Figure()
    for i, etf in enumerate(fund_name):
        etf_data = filtered_local[filtered_local['fund_symbol'] == etf]
        fig.add_trace(go.Scatter(
            x=etf_data['price_date'],
            y=etf_data[timeseries_filter],
            mode='lines',
            name=etf,
            line=dict(color=colors[i])
        ))

    fig.update_layout(
        # centering the title
        title=dict(
        text="ETF Price Tracker",
        x=0.5, 
        xanchor='center'
        ),
        xaxis_title="Date",
        yaxis_title=timeseries_filter,
        legend_title="ETF",
        plot_bgcolor="#1C1C1C",
         paper_bgcolor="#1C1C1C",
         font=dict(color="#F0F0F0"),
         hovermode="x unified",
        xaxis=dict(
        showgrid=True, 
        # making semi-transparent grid color
        gridcolor='rgba(255, 255, 255, 0.1)'  
        ),
        yaxis=dict(
        showgrid=True, 
        # making semi-transparent grid color
        gridcolor='rgba(255, 255, 255, 0.1)'  
        )
     )

    return fig