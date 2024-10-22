'''
Author: Laura Boelsterli

File: volatility.py

Description: function to create etf price volatility time series 
'''
import plotly.graph_objects as go

def make_volatility_chart(fund_name, filtered_local, timeseries_filter, colors, ma_window=20, display_option='Both', width=800, height=550):
    '''-laura 
    params:fund_name (str or list), timeseries_filter (str), date_range_slider (tuple), width (int), height (int), 
    ma_window (int) (this is the selected rolling window), 
    volatility_display_option (str) (chosen by user (to show raw data, rolling sd ot both))
    does: Calculates and plots volatility as either raw daily percentage change, a rolling standard deviation, or shows both.
    returns:
    fig: Plotly figure object showing the volatility plot
    '''
    fig = go.Figure()

    for i, etf in enumerate(fund_name):
        etf_data = filtered_local[filtered_local['fund_symbol'] == etf].copy()

        # # calculate raw daily percentage change
        # etf_data['Volatility_Raw'] = etf_data[timeseries_filter].pct_change() * 100

        # # calculate rolling standard deviation for volatility
        # # automatically calculates the mean of the rolling window and then finds the stdard deviation
        # etf_data['Volatility_Rolling'] = etf_data[timeseries_filter].rolling(window=ma_window).std()

        # calc daily percentage change (returns)
        etf_data['Volatility_daily'] = etf_data[timeseries_filter].pct_change() * 100
        # claculating rolling standard deviation of daily returns (volatility)
        etf_data['Volatility_Rolling'] = etf_data['Volatility_daily'].rolling(window=ma_window).std()


        # plot raw volatility if selected or if 'Both' is chosen
        if display_option in ['Raw Data', 'Both']:
            fig.add_trace(go.Scatter(
                x=etf_data['price_date'],
                y=etf_data['Volatility_daily'],
                mode='lines',
                name=f"{etf} Daily % Change",
                line=dict(color=colors[i], dash='solid')
            ))

        # plot rolling volatility if selected or if 'Both' is chosen
        if display_option in ['Moving Standard Dev', 'Both'] and ma_window > 1:
            fig.add_trace(go.Scatter(
                x=etf_data['price_date'],
                y=etf_data['Volatility_Rolling'],
                mode='lines',
                name=f"{etf} {ma_window}-Day Rolling Volatility",
                line=dict(color=colors[i], dash='dot')
            ))

    fig.update_layout(
        title=dict(
            text="ETF Volatility Analysis",
            x=0.5, 
            xanchor='center'
        ),
        xaxis_title="Date",
        yaxis_title="Volatility (%)",
        plot_bgcolor="#1C1C1C",
        paper_bgcolor="#1C1C1C",
        font=dict(color="#F0F0F0"),
        hovermode="x unified",
        xaxis=dict(
            showgrid=True, 
            gridcolor='rgba(255, 255, 255, 0.1)',
            zeroline=False
        ),
        yaxis=dict(
            showgrid=True, 
            gridcolor='rgba(255, 255, 255, 0.1)',
            zeroline=False
        ),
        width=width,
        height=height
    )

    return fig
