#!/usr/bin/env python
# coding: utf-8

# ## Question 1

# In[11]:


import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_header_tags(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    header_tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

    header_texts = [tag.get_text().strip() for tag in header_tags]

    return header_texts

def create_dataframe(url):
    header_tags = get_header_tags(url)

    df = pd.DataFrame({'Header Tags': header_tags})

    return df

#Example:

url = 'https://en.wikipedia.org/wiki/Python_(programming_language)'
df = create_dataframe(url)
print(df)


# ## Question 2

# In[14]:


import requests
import pandas as pd
from bs4 import BeautifulSoup

# Function to scrape the list of former presidents
def scrape_former_presidents(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    div = soup.find('div', class_='presidentListing')

    names = []
    terms = []

    for row in div.children:
        if row.name == 'div':
            name = row.strong.text.strip()
            term = row.span.text.strip()

            names.append(name)
            terms.append(term)

    df = pd.DataFrame({
        'Name': names,
        'Term of Office': terms
    })
    return df

# Scrape the list of former presidents of India
url = 'https://presidentofindia.nic.in/former-presidents.htm'
df_presidents = scrape_former_presidents(url)

# Print the dataframe
print("List of Former Presidents of India:")
print(df_presidents)


# ## Question 3

# In[25]:


import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_icc_cricket_rankings(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    teams_table = soup.find('table', class_='table rankings-table')
    teams_rows = teams_table.find_all('tr')
    teams_data = []
    for row in teams_rows[1:11]:
        cols = row.find_all('td')
        team = cols[1].text.strip()
        matches = cols[2].text.strip()
        points = cols[3].text.strip()
        rating = cols[4].text.strip()
        teams_data.append([team, matches, points, rating])
    teams_df = pd.DataFrame(teams_data, columns=['Team', 'Matches', 'Points', 'Rating'])

    batsmen_table = soup.find('table', class_='table rankings-table batsmen')
    batsmen_rows = batsmen_table.find_all('tr')
    batsmen_data = []
    for row in batsmen_rows[1:11]:
        cols = row.find_all('td')
        batsman = cols[1].text.strip()
        team = cols[2].text.strip()
        rating = cols[3].text.strip()
        batsmen_data.append([batsman, team, rating])
    batsmen_df = pd.DataFrame(batsmen_data, columns=['Batsman', 'Team', 'Rating'])

    bowlers_table = soup.find('table', class_='table rankings-table bowlers')
    bowlers_rows = bowlers_table.find_all('tr')
    bowlers_data = []
    for row in bowlers_rows[1:11]:
        cols = row.find_all('td')
        bowler = cols[1].text.strip()
        team = cols[2].text.strip()
        rating = cols[3].text.strip()
        bowlers_data.append([bowler, team, rating])
    bowlers_df = pd.DataFrame(bowlers_data, columns=['Bowler', 'Team', 'Rating'])

    return teams_df, batsmen_df, bowlers_df


# In[26]:


url = 'https://www.icc-cricket.com/rankings/mens/team-rankings/odi'
teams, batsmen, bowlers = scrape_icc_cricket_rankings(url)

print("Top 10 ODI Teams:")
print(teams)

print("\nTop 10 ODI Batsmen:")
print(batsmen)

print("\nTop 10 ODI Bowlers:")
print(bowlers)


# ## Question 4

# In[ ]:


import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_icc_cricket_rankings(url):

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    teams_table = soup.find('table', class_='table')
    teams_rows = teams_table.find_all('tr')
    teams_data = []
    for row in teams_rows[1:11]:
        cols = row.find_all('td')
        team = cols[0].text.strip()
        matches = cols[1].text.strip()
        points = cols[2].text.strip()
        rating = cols[3].text.strip()
        teams_data.append([team, matches, points, rating])
    teams_df = pd.DataFrame(teams_data, columns=['Team', 'Matches', 'Points', 'Rating'])

    # Scrape top 10 women's ODI batting players
    batting_table = soup.find('table', class_='table rankings-table batsmen')
    batting_rows = batting_table.find_all('tr')
    batting_data = []
    for row in batting_rows[1:11]:
        cols = row.find_all('td')
        player = cols[0].text.strip()
        team = cols[1].text.strip()
        rating = cols[2].text.strip()
        batting_data.append([player, team, rating])
    batting_df = pd.DataFrame(batting_data, columns=['Player', 'Team', 'Rating'])

    # Scrape top 10 women's ODI all-rounders
    all_rounder_table = soup.find('table', class_='table rankings-table all-rounder')
    all_rounder_rows = all_rounder_table.find_all('tr')
    all_rounder_data = []
    for row in all_rounder_rows[1:11]:
        cols = row.find_all('td')
        player = cols[0].text.strip()
        team = cols[1].text.strip()
        rating = cols[2].text.strip()
        all_rounder_data.append([player, team, rating])
    all_rounder_df = pd.DataFrame(all_rounder_data, columns=['Player', 'Team', 'Rating'])

    return teams_df, batting_df, all_rounder_df

url = 'https://www.icc-cricket.com/rankings/womens/team-rankings/odi'
teams, batting_players, all_rounders = scrape_icc_cricket_rankings(url)

print("Top 10 ODI Women's Teams:")
print(teams)

print("\nTop 10 Women's ODI Batting Players:")
print(batting_players)

print("\nTop 10 Women's ODI All-rounders:")
print(all_rounders)


# ## Question 5

# In[31]:


def scrape_news(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = soup.find_all('article')
    headlines = [article.h2.text.strip() for article in articles]
    times = [article.time['datetime'] for article in articles]
    links = [article.a['href'] for article in articles]

    df = pd.DataFrame({'Headline': headlines, 'Time': times, 'News Link': links})
    return df

url = 'https://www.cnbc.com/world/?region=world'
df = scrape_news(url)

print(df)


# ## Question 6

# In[33]:


import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_articles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('li', class_='js-article-list-item')

    paper_titles = []
    authors_list = []
    published_dates = []
    paper_urls = []

    for article in articles:
        title_element = article.find('h3', class_='js-article-title')
        author_element = article.find('ul', class_='authors-list')
        date_element = article.find('span', class_='article-info-line')
        url_element = article.find('a', class_='js-article-title-link')

        if title_element and author_element and date_element and url_element:
            paper_titles.append(title_element.text.strip())
            authors = [author.text.strip() for author in author_element.find_all('a')]
            authors_list.append(", ".join(authors))
            published_dates.append(date_element.text.strip())
            paper_urls.append(url_element['href'])

    df = pd.DataFrame({
        'Paper Title': paper_titles,
        'Authors': authors_list,
        'Published Date': published_dates,
        'Paper URL': paper_urls
    })
    return df

url = 'https://www.journals.elsevier.com/artificial-intelligence/most-downloaded-articles'
df_articles = scrape_articles(url)

print("Most Downloaded Articles:")
print(df_articles)


# ## Question 7

# In[1]:


import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_restaurants(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    restaurants = soup.find_all('div', class_='restnt-info')

    restaurant_names = []
    cuisines = []
    locations = []
    ratings = []
    image_urls = []

    for restaurant in restaurants:
        name_element = restaurant.find('div', class_='restnt-name ellipsis')
        cuisine_element = restaurant.find('div', class_='restnt-cuisine ellipsis')
        location_element = restaurant.find('div', class_='restnt-loc ellipsis')
        rating_element = restaurant.find('div', class_='rating')
        image_element = restaurant.find('div', class_='restnt-image')
        
        if name_element and cuisine_element and location_element and rating_element and image_element:
            restaurant_names.append(name_element.text.strip())
            cuisines.append(cuisine_element.text.strip())
            locations.append(location_element.text.strip())
            ratings.append(rating_element.text.strip())
            image_urls.append(image_element.find('img')['src'])

    df = pd.DataFrame({
        'Restaurant Name': restaurant_names,
        'Cuisine': cuisines,
        'Location': locations,
        'Ratings': ratings,
        'Image URL': image_urls
    })
    return df

# Scrape restaurant details from dineout.co.in
url = 'https://www.dineout.co.in/delhi-restaurants'
df_restaurants = scrape_restaurants(url)

print("Restaurant Details:")
print(df_restaurants)


# In[ ]:




