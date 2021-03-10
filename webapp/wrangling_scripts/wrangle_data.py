import pandas as pd
import plotly.graph_objs as go
from datetime import date, timedelta
import requests
import pdb

today = date.today()
two_weeks_ago = today - timedelta(14)
url = "https://api.covid19tracking.narrativa.com/api/country/spain/region/canarias/sub_region/fuerteventura?date_from="+two_weeks_ago.strftime("%Y-%m-%d")+"&date_to="+today.strftime("%Y-%m-%d")
payload = {}
headers= {}
response = requests.request("GET", url, headers=headers, data = payload)

today = date.today()
last_60_days = today - timedelta(60)
url_60_days = "https://api.covid19tracking.narrativa.com/api/country/spain/region/canarias/sub_region/fuerteventura?date_from="+last_60_days.strftime("%Y-%m-%d")+"&date_to="+today.strftime("%Y-%m-%d")
payload = {}
headers= {}
response_60_days = requests.request("GET", url_60_days, headers=headers, data = payload)
#pdb.set_trace()

new_cases_t2wk = []
for date in response.json()['dates']:
    new_cases = response.json()['dates'][date]['countries']['Spain']['regions'][0]['sub_regions'][0]['today_new_confirmed']
    new_cases_t2wk.append({'country': 'Fuerteventura', 'date': date, 'new_cases': new_cases})
for date in response.json()['dates']:
    new_cases = response.json()['dates'][date]['countries']['Spain']['regions'][0]['today_new_confirmed']
    new_cases_t2wk.append({'country': 'Canary Islands', 'date': date, 'new_cases': new_cases})
df_new_cases = pd.DataFrame(new_cases_t2wk)
#pdb.set_trace()

cumulative_cases_t2wk = []
for day in response_60_days.json()['dates']:
    today_confirmed = response_60_days.json()['dates'][day]['countries']['Spain']['regions'][0]['sub_regions'][0]['today_confirmed']
    cumulative_cases_t2wk.append({'country': 'Fuerteventura', 'date': day, 'confirmed_cases': today_confirmed})
for day in response_60_days.json()['dates']:
    today_confirmed = response_60_days.json()['dates'][day]['countries']['Spain']['regions'][0]['today_confirmed']
    cumulative_cases_t2wk.append({'country': 'Canary Islands', 'date': day, 'confirmed_cases': today_confirmed})
df_cumulative_cases = pd.DataFrame(cumulative_cases_t2wk)
#pdb.set_trace()

new_deaths_t2wk = []
for day in response.json()['dates']:
    today_deaths = response.json()['dates'][day]['countries']['Spain']['regions'][0]['sub_regions'][0]['today_new_deaths']
    new_deaths_t2wk.append({'country': 'Fuerteventura', 'date': day, 'new_deaths': today_deaths})
for day in response.json()['dates']:
    today_deaths = response.json()['dates'][day]['countries']['Spain']['regions'][0]['today_new_deaths']
    new_deaths_t2wk.append({'country': 'Canary Islands', 'date': day, 'new_deaths': today_deaths})
df_new_deaths = pd.DataFrame(new_deaths_t2wk)
#pdb.set_trace()

cumulative_deaths_t2wk = []
for day in response_60_days.json()['dates']:
    total_deaths = response_60_days.json()['dates'][day]['countries']['Spain']['regions'][0]['sub_regions'][0]['today_deaths']
    cumulative_deaths_t2wk.append({'country': 'Fuerteventura', 'date': day, 'total_deaths': total_deaths})
for day in response_60_days.json()['dates']:
    total_deaths = response_60_days.json()['dates'][day]['countries']['Spain']['regions'][0]['today_deaths']
    cumulative_deaths_t2wk.append({'country': 'Canary Islands', 'date': day, 'total_deaths': total_deaths})
df_cumulative_deaths = pd.DataFrame(cumulative_deaths_t2wk)
#pdb.set_trace()

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
    graph_one_pop = []    
    graph_one_pop.append(
      go.Scatter(
      x = df_new_cases['date'][df_new_cases['country'] == 'Fuerteventura'].values,
      y = (df_new_cases['new_cases'][df_new_cases['country'] == 'Fuerteventura'].values)*1000/116000,
      name = 'Fuerteventura',
      mode = 'lines + markers'
      )
    )

    graph_one_pop.append(
      go.Scatter(
      x = df_new_cases['date'][df_new_cases['country'] == 'Canary Islands'].values,
      y = (df_new_cases['new_cases'][df_new_cases['country'] == 'Canary Islands'].values)*1000/2207000,
      name = 'Canary Islands',
      mode = 'lines + markers',
      line = dict(width=4, dash='dash')
      )
    )

    layout_one_pop = dict(title = 'New COVID cases per 1000 people',
                xaxis = dict(title = 'date'),
                yaxis = dict(title = 'new cases per 1000 people'),
                )

    graph_one = []    
    graph_one.append(
      go.Scatter(
      x = df_new_cases['date'][df_new_cases['country'] == 'Fuerteventura'].values,
      y = df_new_cases['new_cases'][df_new_cases['country'] == 'Fuerteventura'].values,
      name = 'Fuerteventura',
      mode = 'lines + markers'
      )
    )

    graph_one.append(
      go.Scatter(
      x = df_new_cases['date'][df_new_cases['country'] == 'Canary Islands'].values,
      y = df_new_cases['new_cases'][df_new_cases['country'] == 'Canary Islands'].values,
      name = 'Canary Islands',
      mode = 'lines + markers',
      line = dict(width=4, dash='dash')
      )
    )

    layout_one = dict(title = 'New daily COVID cases in absolute count',
                xaxis = dict(title = 'date'),
                yaxis = dict(title = 'new cases'),
                )

# second chart plots ararble land for 2015 as a bar chart    
    graph_two = []

    graph_two.append(
      go.Bar(
      x = df_cumulative_cases['date'][df_cumulative_cases['country'] == 'Fuerteventura'].values,
      y = df_cumulative_cases['confirmed_cases'][df_cumulative_cases['country'] == 'Fuerteventura'].values,
      name = 'Fuerteventura'
      )
    )

    graph_two.append(
      go.Bar(
      x = df_cumulative_cases['date'][df_cumulative_cases['country'] == 'Canary Islands'].values,
      y = df_cumulative_cases['confirmed_cases'][df_cumulative_cases['country'] == 'Canary Islands'].values,
      name = 'Canary Islands',
      opacity=0.6,
      marker_line_width=1.5
      )
    )

    layout_two = dict(title = 'Total COVID cases',
                xaxis = dict(title = 'date',),
                yaxis = dict(title = 'total cases')
                )

# third chart plots percent of population that is rural from 1990 to 2015
    graph_three_pop = []
    graph_three_pop.append(
      go.Scatter(
      x = df_new_deaths['date'][df_new_deaths['country'] == 'Fuerteventura'].values,
      y = (df_new_deaths['new_deaths'][df_new_deaths['country'] == 'Fuerteventura'].values)*(1000/116000),
      name = 'Fuerteventura',
      mode = 'lines + markers'
      )
    )

    graph_three_pop.append(
      go.Scatter(
      x = df_new_deaths['date'][df_new_deaths['country'] == 'Canary Islands'].values,
      y = (df_new_deaths['new_deaths'][df_new_deaths['country'] == 'Canary Islands'].values)*(1000/2207000),
      name = 'Canary Islands',
      mode = 'lines + markers',
      line = dict(width=4, dash='dash')
      )
    )

    layout_three_pop = dict(title = 'Deaths from COVID daily per 1000 people',
                xaxis = dict(title = 'date'),
                yaxis = dict(title = 'deaths')
                       )

    graph_three = []
    graph_three.append(
      go.Scatter(
      x = df_new_deaths['date'][df_new_deaths['country'] == 'Fuerteventura'].values,
      y = df_new_deaths['new_deaths'][df_new_deaths['country'] == 'Fuerteventura'].values,
      name = 'Fuerteventura',
      mode = 'lines + markers'
      )
    )

    graph_three.append(
      go.Scatter(
      x = df_new_deaths['date'][df_new_deaths['country'] == 'Canary Islands'].values,
      y = df_new_deaths['new_deaths'][df_new_deaths['country'] == 'Canary Islands'].values,
      name = 'Canary Islands',
      mode = 'lines + markers',
      line = dict(width=4, dash='dash')
      )
    )

    layout_three = dict(title = 'Deaths from COVID daily',
                xaxis = dict(title = 'date'),
                yaxis = dict(title = 'deaths')
                       )
    
# fourth chart shows rural population vs arable land
    graph_four = []

    graph_four.append(
      go.Bar(
      x = df_cumulative_deaths['date'][df_cumulative_deaths['country'] == 'Fuerteventura'].values,
      y = df_cumulative_deaths['total_deaths'][df_cumulative_deaths['country'] == 'Fuerteventura'].values,
      name = 'Fuerteventura'
      )
    )

    graph_four.append(
      go.Bar(
      x = df_cumulative_deaths['date'][df_cumulative_deaths['country'] == 'Canary Islands'].values,
      y = df_cumulative_deaths['total_deaths'][df_cumulative_deaths['country'] == 'Canary Islands'].values,
      name = 'Canary Islands',
      opacity=0.6,
      marker_line_width=1.5
      )
    )

    layout_four = dict(title = 'Deaths from COVID total',
                xaxis = dict(title = 'date',),
                yaxis = dict(title = 'total deaths'),
                )
    
    # append all charts to the figures list

    config = {'responsive': True}

    figures = []
    figures.append(dict(data=graph_one_pop, layout=layout_one_pop, config=config))
    figures.append(dict(data=graph_one, layout=layout_one, config=config))
    figures.append(dict(data=graph_two, layout=layout_two, config=config))
    figures.append(dict(data=graph_three_pop, layout=layout_three_pop, config=config))
    #figures.append(dict(data=graph_three, layout=layout_three, config=config))
    figures.append(dict(data=graph_four, layout=layout_four, config=config))

    return figures