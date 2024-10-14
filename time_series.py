import plotly.graph_objects as go

def make_time_series(fund_name, filtered_local, timeseries_filter):
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