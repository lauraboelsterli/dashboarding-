'''
Author: Laura Boelsterli

File: time_series.py

Description: function to create etf time series
'''

import plotly.graph_objects as go

def make_time_series(fund_name, filtered_local, timeseries_filter, colors, width=800, height=400, ma_window=20, display_option='Both'):
    '''-laura
    params: fund_name (str or list),filtered_local (df), timeseries_filter (str), colors (list), 
    width (int), height (int), ma_window (int), display_option (str)
    does: plots the raw data for each fund if 'Raw Data' or 'Both' is selected in display_option and overlays 
    a moving average with the specified window size if 'Moving Average' or 'Both' is selected, then 
    updates plot layout to a dark theme with unified hover mode, customized axis titles, and grid transparency
    returns: fig: Plotly figure object showing the time series plot with raw data, moving average, or both, 
    depending on the selected option
    '''
    fig = go.Figure()
    
    for i, etf in enumerate(fund_name):
        etf_data = filtered_local[filtered_local['fund_symbol'] == etf].copy()
        
        # plot raw data if selected or if 'Both' is chosen
        if display_option in ['Raw Data', 'Both']:
            fig.add_trace(go.Scatter(
                x=etf_data['price_date'],
                y=etf_data[timeseries_filter],
                mode='lines',
                name=f"{etf} Raw Data",
                line=dict(color=colors[i])
            ))

        # plot moving average if selected or if 'Both' is chosen
        if display_option in ['Moving Average', 'Both'] and ma_window > 1:
            etf_data['MA'] = etf_data[timeseries_filter].rolling(window=ma_window).mean()
            fig.add_trace(go.Scatter(
                x=etf_data['price_date'],
                y=etf_data['MA'],
                mode='lines',
                name=f"{etf} {ma_window}-Day MA",
                line=dict(color=colors[i], dash='dash')
            ))

    fig.update_layout(
        title=dict(
            text="ETF Price Tracker",
            x=0.5, 
            xanchor='center'
        ),
        xaxis_title="Date",
        yaxis_title= f"{timeseries_filter.capitalize()} Price",
        legend_title="ETF",
        plot_bgcolor="#1C1C1C",
        paper_bgcolor="#1C1C1C",
        font=dict(color="#F0F0F0"),
        hovermode="x unified",
        xaxis=dict(
            showgrid=True, 
            gridcolor='rgba(255, 255, 255, 0.1)' 
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='rgba(255, 255, 255, 0.1)'  
        ),
        width=width,
        height=height
    )

    fig.update_xaxes(zeroline=False)
    fig.update_yaxes(zeroline=False)


    return fig
