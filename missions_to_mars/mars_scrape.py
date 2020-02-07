
# Import dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import requests


# Create Mars Data Dictionary
mars_data = {}

# Enable chromedriver
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# These are the various URls we'll be using
news_url = 'https://mars.nasa.gov/news/'
jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
weather_url = 'https://twitter.com/marswxreport?lang=en'
facts_url = 'https://space-facts.com/mars/'
astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


# ### NASA Mars News

def mars_news_collection():
    # Open URL
    browser.visit(news_url)

    # Create HTML Object
    html = browser.html

    # Create Beautiful Soup Object
    soup = BeautifulSoup(html, 'html.parser')

    # Find the most recent title and description
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text

    mars_data['news_title'] = news_title
    mars_data['news_p'] = news_p

    return mars_data

# ### JPL Mars Space Images - Featured Image

def mars_image_collection():
    # Open URL
    browser.visit(jpl_url)

    # Create HTML Object
    html = browser.html

    # Create Beautiful Soup Object
    soup = BeautifulSoup(html, 'html.parser')

    # Find the most recent mars image
    image_url  = soup.find('article')['style']
    image_url = image_url.split("'")
    featured_image_url = 'https://www.jpl.nasa.gov' + image_url[1]

    mars_data['featured_image_url'] = featured_image_url

    return mars_data

# ### Mars Weather

def mars_weather_collection():
    # Open URL  
    browser.visit(weather_url)

    # Create HTML Object
    html = browser.html

    # Create Beautiful Soup Object
    soup = BeautifulSoup(html, 'html.parser')

    # Find the most recent Mars weather
    mars_weather = soup.find('span', class_='css-901oao').text

    mars_data['weather'] = mars_weather

    return mars_data


### Mars Facts

def mars_facts_collection():
    # Open URL
    browser.visit(facts_url)

    # Create HTML Object
    html = browser.html

    # Read table as dataframe
    facts_tables = pd.read_html(facts_url)
    facts_table = facts_tables[0]

    # Convert to HTML
    html_table = facts_table.to_html()
    html_table_clean = html_table.replace('\n', '')

    mars_data['mars_facts'] = html_table_clean

    return mars_data


### Mars Hemispheres

def mars_hemi_collection():

    # Open URL
    browser.visit(astro_url)

    # Create HTML Object
    html = browser.html

    # Create Beautiful Soup Object
    soup = BeautifulSoup(html, 'html.parser')

    # Create list for urls 
    hemisphere_urls = []

    # Find class 'item' and child URLs.  visit child URLs, scrape and append to the list
    images = soup.find_all('div', class_='item')
    for i in images:
        browser.visit('https://astrogeology.usgs.gov' + i.find('a')['href'])
        browser_image = browser.html
        soup = BeautifulSoup(browser_image, 'html.parser')
        title = soup.find('title').text
        img_url = soup.find('img', class_='wide-image')['src']
        hemisphere_urls.append({"title" : title, "img_url" : img_url})

    mars_data['mars_hemi'] = hemisphere_urls

    return mars_data

