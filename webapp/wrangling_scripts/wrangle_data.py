import pandas as pd
import plotly.graph_objs as go
from datetime import date, timedelta
import requests

today = date.today()
two_weeks_ago = today - timedelta(14)
url = "https://api.covid19tracking.narrativa.com/api/country/spain/region/canarias/sub_region/fuerteventura?date_from="+two_weeks_ago.strftime("%Y-%m-%d")+"&date_to="+today.strftime("%Y-%m-%d")
payload = {}
headers= {}
response = requests.request("GET", url, headers=headers, data = payload)

new_cases_t2wk = []
for date in response.json()['dates']:
    new_cases = response.json()['dates'][date]['countries']['Spain']['regions'][0]['sub_regions'][0]['today_new_confirmed']
    new_cases_t2wk.append({'date': date, 'new_cases': new_cases})

df_new_cases = pd.DataFrame(new_cases_t2wk)

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    # first chart plots arable land from 1990 to 2015 in top 10 economies 
    # as a line chart
    
    graph_one = []    
    graph_one.append(
      go.Scatter(
      x = [0, 1, 2, 3, 4, 5],
      y = [0, 2, 4, 6, 8, 10],
      mode = 'lines'
      )
    )

    layout_one = dict(title = 'Chart One',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label'),
                )

# second chart plots ararble land for 2015 as a bar chart    
    graph_two = []

    graph_two.append(
      go.Bar(
      x = df_new_cases['date'].values,
      y = df_new_cases['new_cases'].values
      )
    )

    layout_two = dict(title = 'New daily covid cases in Fuerteventura',
                xaxis = dict(title = 'date',),
                yaxis = dict(title = 'count of new cases'),
                )


# third chart plots percent of population that is rural from 1990 to 2015
    graph_three = []
    graph_three.append(
      go.Scatter(
      x = [5, 4, 3, 2, 1, 0],
      y = [0, 2, 4, 6, 8, 10],
      mode = 'lines'
      )
    )

    layout_three = dict(title = 'Chart Three',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label')
                       )
    
# fourth chart shows rural population vs arable land
    graph_four = []
    
    graph_four.append(
      go.Scatter(
      x = [20, 40, 60, 80],
      y = [10, 20, 30, 40],
      mode = 'markers'
      )
    )

    layout_four = dict(title = 'Chart Four',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label'),
                )
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures