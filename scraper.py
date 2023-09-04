import requests
from bs4 import BeautifulSoup
import re

class WeatherScraper:
    def __init__(self, url, user_agent):
        self.url = url
        self.user_agent = user_agent
        self.news_data = []
        self.weather_data = {}  # Store weather data as a dictionary

    def fetch_section_data(self, section_container):
        section_title = section_container.find('p', class_='title').get_text()
        links = section_container.find_all('a', class_='right-rail-article right-rail-ga')
        
        for link in links:
            article_title = link.find('p', class_='right-rail-article__title').get_text()
            category = link.find('p', class_='right-rail-article__category').get_text()
            time = link.find('p', class_='right-rail-article__time').get_text()
            href = link['href']
            self.news_data.append({'section_title': section_title, 'category': category, 'article_title': article_title, 'time': time, 'link': href})

    def extract_weather_data(self, soup):
        self.weather_data['Current Weather'] = soup.find('div', class_='temp').get_text()
        self.weather_data['Current Time'] = soup.find('p', class_='cur-con-weather-card__subtitle').get_text()
        real_feel_element = soup.find('div', class_='real-feel')
        if real_feel_element:
            real_feel_text = real_feel_element.get_text()
            temperature_match = re.search(r'\d+°', real_feel_text)
            if temperature_match:
                temperature = temperature_match.group()
                self.weather_data['RealFeel Weather'] = temperature.strip()
        self.weather_data['Weather Type'] = soup.find('span', class_='phrase').get_text()


    def fetch_data(self):
        response = requests.get(self.url, headers={"User-Agent": self.user_agent})
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Extract and process news articles from "Top Stories" and "Featured Stories"
        top_stories_container = soup.find('div', class_='zone-rightRail1 content-module')
        featured_stories_container = soup.find('div', class_='zone-rightRail2 content-module')
        
        if top_stories_container and featured_stories_container:
            self.fetch_section_data(top_stories_container)
            self.fetch_section_data(featured_stories_container)

        # Extract current weather information
        self.extract_weather_data(soup)

def main():
    url = 'https://www.accuweather.com/en/us/el-paso/79901/weather-forecast/351195'
    user_agent = 'Your_user_agent'
    
    scraper = WeatherScraper(url, user_agent)
    scraper.fetch_data()
