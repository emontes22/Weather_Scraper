import requests
from bs4 import BeautifulSoup
import re

# Class for web scraping weather and news data from accuweather.com
class WeatherScraper:
    def __init__(self, url, user_agent):
        # Initialize URL scraper and user agent
        self.url = url
        self.user_agent = user_agent
        self.news_data = [] # Store news data as a list of dictionaries
        self.weather_data = {}  # Store weather data as a dictionary

    # Function to fetch and process news section data
    def fetch_section_data(self, section_container):
        # Extract section title
        section_title = section_container.find('p', class_='title').get_text()
        # Get all links to news articles inside each section
        links = section_container.find_all('a', class_='right-rail-article right-rail-ga')
        
        # Go through the links and extract relevant information
        for link in links:
            article_title = link.find('p', class_='right-rail-article__title').get_text()
            category = link.find('p', class_='right-rail-article__category').get_text()
            time = link.find('p', class_='right-rail-article__time').get_text()
            href = link['href']
            # Store the extracted data as dictionary and append to the news_data list
            self.news_data.append({'section_title': section_title, 'category': category, 'article_title': article_title, 'time': time, 'link': href})

    # Function to extract weather data
    def extract_weather_data(self, soup):
        # Extract weather temperature
        self.weather_data['Current Weather'] = soup.find('div', class_='temp').get_text()
        # Extract current time
        self.weather_data['Current Time'] = soup.find('p', class_='cur-con-weather-card__subtitle').get_text()
        # Get the 'RealFeel' element
        real_feel_element = soup.find('div', class_='real-feel')
        if real_feel_element:
            # Extract only text from 'RealFeel' element
            real_feel_text = real_feel_element.get_text()
            # Regular expressions to extract only the temperature
            temperature_match = re.search(r'\d+°', real_feel_text)
            if temperature_match:
                # Store the 'RealFeel' temperature
                temperature = temperature_match.group()
                self.weather_data['RealFeel Weather'] = temperature.strip()
        # Extract the weather type information
        self.weather_data['Weather Type'] = soup.find('span', class_='phrase').get_text()

    # Function to fetch and process weather and news data
    def fetch_data(self):
        # Send HTTP Get request to the url with the given user-agent
        response = requests.get(self.url, headers={"User-Agent": self.user_agent})
        # Parse the HTML content of the response
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Extract and process news articles from "Top Stories" and "Featured Stories"
        top_stories_container = soup.find('div', class_='zone-rightRail1 content-module')
        featured_stories_container = soup.find('div', class_='zone-rightRail2 content-module')
        
        # Fetch and process data from both news sections
        if top_stories_container and featured_stories_container:
            self.fetch_section_data(top_stories_container)
            self.fetch_section_data(featured_stories_container)

        # Extract current weather information
        self.extract_weather_data(soup)