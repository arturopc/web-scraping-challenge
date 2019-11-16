from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def scrape():
    #Dictionary of all data
    marsDictionary = {}

    #Initialize browser
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    #--------------MARS NEWS--------------------------
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    #Create soup object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #Save the most recent news title and text
    newsArticle = soup.find('div', class_ = 'list_text')
    title = soup.find('div', class_ = 'content_title').text
    text = soup.find('div', class_ = 'article_teaser_body').text
    date = soup.find('div', class_ = 'list_date').text

    #Add news data to dictionary
    marsDictionary["newsTitle"] = title
    marsDictionary["newsDate"] = date
    marsDictionary["newsText"] = text

    #--------------JPL--------------------------
    #JPL url
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #Soup object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Get featured image of mars
    image = soup.find('img', class_ = 'thumb')
    #Complete url of image
    featuredImageUrl = "https://www.jpl.nasa.gov" + image['src']

    #Add featured image to dictionary
    marsDictionary["featuredImage"] = featuredImageUrl

    #--------------Twitter--------------------------
    #Twitter url
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    #Soup object
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #Get latest mars weather tweet
    tweet = soup.find('p', class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    #Add tweet to dictionary
    marsDictionary["weather"] = tweet

    #--------------Facts--------------------------
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    #Use pandas to scrape site and create a dataframe
    table = pd.read_html(url)
    marsDf = pd.DataFrame(table[0])

    #Change column names and create html
    marsDf.columns = ["Mars", "Facts"]
    marsHtml = marsDf.to_html()
    marsFacts = marsHtml.replace('\n', '')

    #Add facts to dictionary
    marsDictionary["factsTable"] = marsFacts

    #--------------Astrogeology--------------------------
    #New astrogeology site
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    #Go to each of the four links and get images
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    marsHemispheres = []
    for i in range(4):
        #Find link to next page
        im = browser.find_by_tag('h3')
        im[i].click()
        #In new page look for image source and title
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        imUrl = soup.find('img', class_ = 'wide-image')['src']
        imTitle = soup.find('h2', class_ = 'title').text
        hDict = {
            "title": imTitle,
            "imgUrl": "https://astrogeology.usgs.gov" + imUrl
        }
        marsHemispheres.append(hDict)
        browser.back()

    #Add facts to dictionary
    marsDictionary["hemispheres"] = marsHemispheres


    return marsDictionary

    

