import panel as pn
from laura_etf_api import etf_API
api = etf_API()

def make_volindicator(fund_name, date_range_slider, width, height):
    '''-laura 
    params: fund_name (list of str): list of fund symbols for which the volume indicators will be generated
    date_range_slider (tuple of str): tuple containing the start and end dates to filter the data by date
    width (int): width of each volume indicator widget
    height (int): height of each volume indicator widget
    does: filters the ETF data by the specified fund names and date range, calculates the total volume traded for each fund, 
    and creates a number indicator for each one. Adjusts the display value for readability (e.g., thousands, millions)
    returns: list of pn.indicators.Number: list of Panel Number indicators, each showing the total volume for a specific fund
    '''
    df = api.get_filtered_data(fund_name, 'volume', date_range_slider)
    # calculating total volume per ETF
    total_volumes = df.groupby('fund_symbol')['volume'].sum()
    # list to hold each volume indicator
    indicators = []
    for symbol, volume in total_volumes.items():
        # determine suffix based on the value's magnitude
        if volume >= 1_000_000_000:
            display_value = volume / 1_000_000_000
            suffix = 'Billions'
        elif volume >= 1_000_000:
            display_value = volume / 1_000_000
            suffix = 'Millions'
        elif volume >= 1_000:
            display_value = volume / 1_000
            suffix = 'Thousands'
        else:
            display_value = volume
            suffix = ''

        # creating a Number indicator, using numeric value and adding the suffix in the name
        indicator = pn.indicators.Number(
            name=f'Total Volume for {symbol} ({suffix})',
            value=display_value,  
            # formatting to one decimal place
            format='{value:.1f}',  
            sizing_mode='fixed',
            width=width,
            height=height
        )
        indicators.append(indicator)

    return indicators