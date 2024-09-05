from bs4 import BeautifulSoup
import requests
import re
import nltk
from nltk.corpus import stopwords, words
import pandas as pd
from googletrans import Translator, LANGUAGES

websites = [
    "https://www.jagran.com/",
    "https://www.bhaskar.com/",
    "https://ndtv.in/",
    "https://www.amarujala.com/",
    "https://navbharattimes.indiatimes.com/",
    "https://www.patrika.com/",
    "https://www.jansatta.com/",
    "https://www.punjabkesari.in/",
    "https://www.prabhatkhabar.com/",
    "https://www.haribhoomi.com/",
    "https://www.khaskhabar.com/",
    "https://www.prabhasakshi.com/",
    "https://www.samacharjagat.com/",
    "https://www.deshbandhu.co.in/",
    "https://sanjeevnitoday.com/",
    "https://www.uttamhindu.com/",
    "https://www.loktej.com/",
    "http://www.virarjun.com/"
]


def get_subsites(url):

    # Creating empty list for the subsites
    subsites = []
    
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        
        # Get the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all the links if the given URL
        links = soup.find_all('a')

        # Looping throuh links
        for link in links:
            # Getting actual url for anchor(a) tag that is usually stored in href
            href = link.get('href')
            # verifying if the link starts with the provided url i.e. making sure if the provided url is news.com the href is news.com/<something>
            if href and href.startswith(url):
                subsites.append(href) # Adding href to subsites
        
        return subsites

    # If status code is something other than <200> i.e issue with the provided url
    else:
        return None
    

subsites_list = []
for website in websites:
    subsite = get_subsites(website)

    subsites_list.append(website)
    
    if not subsite: # Continue if the response from get_subsites() function is None
        continue

    # adding unique subsites to subsites_list
    for site in subsite:
        if not site in subsites_list:
            subsites_list.append(site)


def scrape_news_website(url):
    news = []

    # Getting data from website
    response = requests.get(url)

    if not response.status_code == 200:
        return None

    # Reading html content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Getting the data stored in heading tags of html page
    for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        tokens = tag.text
        tokens = re.sub(r"[a-zA-Z0-9]", "", tokens) # Removing english characters and numbers
        tokens = re.sub(r'[\\:;\'",<.>?/!@#$%^&*()_+\-=\[\-]{}|\\\\`‘’~]', '', tokens) # Removing special characters
        tokens = tokens.split() # Splitting sentences into array
        
        # Only considering sentences with more than 5 words
        if len(tokens) > 5:
            tokens = " ".join(tokens)
            if tokens not in news:
                news.append(tokens.strip())
    if news:
        return news
    else:
        return None
    

# Initializing instance of google translator
translator = Translator()
# Creating empty list for dataset
dataset = []
# Empty lsit to store all news headlines
news_headlines = []
# Numbering news headlines 
count = 0
# Counting total news headlines
total_headlines = 0

# Loopiing throught subsites
for url in subsites_list:
    count+=1
    try:
        # Getting news headlines for subsite
        news_list = scrape_news_website(url)
        total_headlines += len(news_list) # Adding count of the news headlines to toal count
        
        # Adding unique instance of new to news_headline
        for news in news_list:
            if not news in news_headlines:
                # Creating empty dictionary for news
                try:
                    entry = dict()
                    entry['Reference'] = url.strip() # Adding website url to dictionary
                    entry['Hindi'] = news.strip() # Adding original news to the dictionary
                    entry['English'] = translator.translate(news, dest="en").text.strip() # Adding english translated news to the dictionary
                    dataset.append(entry) # adding the dictionary to dataset list
                except Exception as err:
                    pass
            
            news_headlines.append(news)
            
    except Exception as err:
        pass


df = pd.DataFrame(dataset)
# Saving dataset as csv
df.to_csv("./language.csv", index= False)

# Saving data as excel
df.to_excel("./language.xlsx", index = False)