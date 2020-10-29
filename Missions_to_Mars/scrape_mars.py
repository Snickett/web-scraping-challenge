# dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    listings = []
    
    # scrape latest title
    title1 = soup.find('div', class_="content_title").text
    
    # scrape latest article description
    desc1 = soup.find('div', class_="rollover_description_inner").text
    
    #page visit
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    html_img = browser.html
    soup_img = BeautifulSoup(html_img, 'html.parser')
    
    #pulling out img id
    img_id = str(soup_img.find(id="full_image"))
    img_id=img_id.split("ze/")
    img_id=img_id[1].split("_ip")
    img_id=img_id[0]
    
    #inserting img id to build correct img url
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages/images/largesize/"+img_id+ "_hires.jpg"
    browser.quit()
    
    # Pandas scraping

    url3 ="https://space-facts.com/mars/"

    tables = pd.read_html(url3)
    html_table = tables[1].to_html()
    
    # creating image url dictionary
    hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg"},
    {"title": "Cerberus Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg"},
    {"title": "Schiaparelli Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg"},
    {"title": "Syrtis Major Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg"},
]

    #for item in results:
    scraped_info = {}
    scraped_info["Title"] = title1
    scraped_info["Desc"] = desc1
    scraped_info["featured_img"] = featured_image_url
    scraped_info["table"] = html_table
    scraped_info["imageurl"] = hemisphere_image_urls

    listings.append(scraped_info)
    return listings