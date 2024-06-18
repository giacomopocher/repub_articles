###############################################################################
# Author: Giacomo Opocher
# Position: 2nd Year PhD in Econ
# Institution: University of Bologna

# Course: Python for Economists
# Instructor: Dr. Anatole Cheysson 
# Object: Webscraping Repubblica

# Current Version: 15/05/2024
###############################################################################

# NOTE: I think they realized that I was screaping and they blocked me somehow.
#       I am sure the code works, but sometime I am suspended from accessing 
#       the archive.

# The code is organized as follows:
    #0. Import the necessary packages
    #1. Define my scraper function scrape()
    #2. Generate the links to scrape and scrape all the pages 
    #3. Keep only the first three articles for each year

###############################################################################

### 0. Import the necessary packages
import pandas as pd # Data management
import numpy as np 
import requests   
import random
import locale
from bs4 import BeautifulSoup
import re

###############################################################################

# 1. Define my scraper function scrape()

# Create a DataFrame to store scraped data
df = pd.DataFrame(columns=['title', 'author', 'date', 'link_art', 'subtitle', 'text'])

def scrape(link):
    try:
        pattern = r"\bdi \b"  # regex pattern to clean the author string
        pattern2 = "dal nostro inviato " # regex pattern to clean the author string
        # Request the webpage with the list of articles
        website = requests.get(link) 
        page_content = BeautifulSoup(website.content, "html.parser")
    
        # Focus on the first article of the page
        np_art = page_content.find('section', attrs={'id': 'lista-risultati'})
    
        # Extract various information from the article
        title = np_art.article.a.text.strip()
        # Clean author's name (remove the "di " article) 
        author = re.sub(pattern, "", page_content.find('em', attrs={'class': 'author'}).text)
        author = re.sub(pattern2, "", author)
        date = np_art.article.time.text
        subtitle = np_art.article.p.text.strip()
        link_art = np_art.article.a['href'] # Link to the full article

        # Access the webpage with the full content of the article
        article_pg = requests.get(link_art)
        page_content = BeautifulSoup(article_pg.content, "html.parser")
        # Extract article text
        text = page_content.find('div', attrs={'class': 'story__text'}).text.strip()  

        # Store the data in an array
        data = np.array([title, author, date, link_art, subtitle, text]) 
        
        # let the developer know that everything went well
        print('We got you, Repubblica!!')
        return data
    
    except AttributeError:
        print("AttributeError occurred :/ We lost a battle, but not the war!")
        # Split the URL to extract the year, month, and page number
        
        
###############################################################################

#2. Generate the links to scrape and scrape all the pages 

# Define a set to store all scraped URLs
links = []

# Loop through the years from 2015 to 2024
for year in range(2015, 2025):
    # Generate six random months for each year (I use 6 instead of 3 to 
    # decrease the probability of ending up with too few articles).
    for _ in range(6):
        month = random.randint(1, 12)  
        
        # Choose a random page number (from 1 to 10)
        # Only 10 because I want to be sure I find a page for each month-year
        page = "{:02d}".format(random.randint(1, 10))  
        
        # Construct the URL
        link = f"https://ricerca.repubblica.it/repubblica/archivio/repubblica/{year:04d}/{month:02d}/{page}"
        # keep track of the links: you never know
        links.append(link)
        
        # Scrape data from the generated link
        data = scrape(link)
        
        # Add scraped data to the DataFrame
        df.loc[len(df)] = data


###############################################################################

#3. Keep only the first three articles for each year

df = df.dropna() # drop missing values
locale.setlocale(locale.LC_TIME, 'it_IT.UTF-8') # set the local time in italian
df['date'] = pd.to_datetime(df['date'], format='%d %B %Y') # convert the time from strg to date format
df_first_three = df.groupby(df['date'].dt.year).head(3) # keep only the first three for each year

# Note that it might happen that, for some year we don't reach 3 articles. In
# case, just re-run the code until this condition is met. 

###############################################################################

# Flows and possible improvements

# 1. I am not handling paywalls. That's something I started doing, but unfortunately
#    the time run out. 

# 2. Take care of the missing pages/articles with a while loop and let the code
#    run authomatically until we reach three artciles per year. It is not as 
#    trivial as it might seem to implement (at least for me).

 
###############################################################################


