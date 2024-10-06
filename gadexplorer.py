import panel as pn
from gadapi import GADAPI
import sankey as sk

# Loads javascript dependencies and configures Panel (required)
pn.extension()

# INITIALIZE API
api = GADAPI()
api.load_gad("gad.csv")


# WIDGET DECLARATIONS

# Search Widgets

phenotype = pn.widgets.Select(name="Phenotype", options=api.get_phenotypes(), value='asthma')
min_pub = pn.widgets.IntSlider(name="Min Publications", start=1, end=10, step=1, value=3)
singular = pn.widgets.Checkbox(name="Singular Associations?", value=True)


# Plotting widgets

width = pn.widgets.IntSlider(name="Width", start=250, end=2000, step=250, value=1500)
height = pn.widgets.IntSlider(name="Height", start=200, end=2500, step=100, value=800)


# CALLBACK FUNCTIONS

def get_catalog(phenotype, min_pub, singular):
    global local
    local = api.extract_local_network(phenotype, min_pub, singular)  # calling the api
    table = pn.widgets.Tabulator(local, selectable=False)
    return table


def get_plot(phenotype, min_pub, singular, width, height):
    global local
    fig = sk.make_sankey(local, "phenotype", "gene", vals="npubs", width=width, height=height)
    return fig


# CALLBACK BINDINGS (Connecting widgets to callback functions)
catalog = pn.bind(get_catalog, phenotype, min_pub, singular)
plot = pn.bind(get_plot, phenotype, min_pub, singular, width, height)




# DASHBOARD WIDGET CONTAINERS ("CARDS")

card_width = 320

search_card = pn.Card(
    pn.Column(
        phenotype,
        min_pub,
        singular

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
    title="GAD Explorer",
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
