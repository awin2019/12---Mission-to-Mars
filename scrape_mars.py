from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    #visit mars website
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    #scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #get the first article title and paragraph
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # get the image url
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)

    # scrape image url
    html_image = browser.html
    soup = BeautifulSoup(html_image, 'html.parser')

    image_url  = soup.find('article')['style']
    image_url = image_url.replace("background-image: url", "", 1)
    image_url = image_url.replace("('", "", 1)
    image_url = image_url.replace(");'", "")[0:-3]

    main_url = 'https://www.jpl.nasa.gov'
    full_image_url = f'{main_url}{image_url}'

    # get the weather url
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    # scrape weather url
    html_weather = browser.html
    soup = BeautifulSoup(html_weather, 'html.parser')

    tweets = soup.find_all('div', class_='js-tweet-text-container')

    for tweet in tweets: 
        weather_tweet = tweet.find('p').text
        if 'Sol' and 'pressure' in weather_tweet:
            print(weather_tweet)
            break
        else: 
            pass

    # get the url facts table
    url_facts = "https://space-facts.com/mars/"
    table = pd.read_html(url_facts)
    facts_df = table[1]
    facts_df.columns = ["Parameter", "Values"]
    facts_df.set_index(["Parameter"])

    html_table = facts_df.to_html()
    html_table = html_table.replace('\n','')

    # get moon images
    cerberus = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'

    browser.visit(cerberus)
    cerberus_image = browser.html
    soup = BeautifulSoup(cerberus_image, 'html.parser')
    cerberus  = soup.find('img')['src']
    cerberus

    #
    schiaparelli = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'

    browser.visit(schiaparelli)
    schiaparelli_image = browser.html
    soup = BeautifulSoup(schiaparelli_image, 'html.parser')
    schiaparelli = soup.find('img')['src']
    schiaparelli

    #
    syrtis = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'

    browser.visit(syrtis)
    syrtis_image = browser.html
    soup = BeautifulSoup(syrtis_image, 'html.parser')
    syrtis = soup.find('img')['src']
    syrtis

    #
    valles = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'

    browser.visit(valles)
    valles_image = browser.html
    soup = BeautifulSoup(valles_image, 'html.parser')
    valles = soup.find('img')['src']
    valles

    #
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "full_image_url": full_image_url,
        "weather_tweet": weather_tweet,
        "html_table": html_table,
        "cerberus": cerberus,
        "schiaparelli": schiaparelli,
        "syrtis": syrtis,
        "valles": valles
    }

    # Quite the browser after scraping
    browser.quit()

    # Return results
    return mars_data
