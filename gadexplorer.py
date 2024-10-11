import panel as pn
from gadapi import stock_API
import sankey as sk


import panel as pn
import pandas as pd
import altair as alt
import plotly.graph_objects as go
from matplotlib.figure import Figure
import hvplot.pandas

# Loads javascript dependencies and configures Panel (required)
pn.extension()
pn.extension("plotly")


# INITIALIZE API
api = stock_API()
api.load_df('data/ETFprices.csv')


# WIDGET DECLARATIONS
# Search Widgets
fund_name = pn.widgets.Select(name="Fund", options=api.get_funds(), value='AAA')
timeseries_filter = pn.widgets.Select(name="Value of Interest", options = api.get_options(), value='close')
# singular = pn.widgets.Checkbox(name="Singular Associations?", value=True)
# window_size = pn.widgets.IntSlider(name="Window Size", start=1, end=50, step=1, value=10)


# Plotting widgets
width = pn.widgets.IntSlider(name="Width", start=250, end=2000, step=250, value=1500)
height = pn.widgets.IntSlider(name="Height", start=200, end=2500, step=100, value=800)


# CALLBACK FUNCTIONS
def get_catalog(fund_name, timeseries_filter):
    global local
    local = api.extract_local_network(fund_name, timeseries_filter)  # calling the api
    # print(local)
    table = pn.widgets.Tabulator(local, selectable=False)
    return table



# def get_plotly(api.fund_df, window_size):
#     df = api.get_df_ts(api.fund_df, window_size)
#     fig = go.Figure(data=go.Scatter(x=df['date'], y=df['close'], mode='lines'))
#     return fig

def get_plotly(fund_name, timeseries_filter):
    # add in time range after
    # global local 
    local = api.extract_local_network(fund_name, timeseries_filter)
    # want the df to retun value of itnerest akak (close, open,etc for time series filter, and chosen fund name)
    # df = api.get_df_ts(api.fund_df, window_size)
    # plotting time series 
    fig = go.Figure(data=go.Scatter(x=local['price_date'], y=local[timeseries_filter], mode='lines'))
    return fig





# CALLBACK BINDINGS (Connecting widgets to callback functions)
catalog = pn.bind(get_catalog, fund_name, timeseries_filter)
# plot = pn.bind(get_plot, phenotype, min_pub, singular, width, height)
# df = api.fund_df
# plot = pn.bind(get_plotly, timeseries_filter)
plot = pn.bind(get_plotly, fund_name, timeseries_filter)


# pn.panel(plot).servable()


# DASHBOARD WIDGET CONTAINERS ("CARDS")

card_width = 320

search_card = pn.Card(
    pn.Column(
        fund_name,
        timeseries_filter

    ),
    title="Search", width=card_width, collapsed=False
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
    title="Stock Explorer",
    sidebar=[
        search_card,
        plot_card,
    ],
    theme_toggle=False,
    main=[
        pn.Tabs(
            ("Associations", catalog),  # Replace None with callback binding
            ("Network", plot),  # Replace None with callback binding

            active=1  # Which tab is active by default?
        )

    ],
    header_background='#a93226'

).servable()

layout.show()
