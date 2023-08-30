import requests
from bs4 import BeautifulSoup

class WeatherScraper:
    def __init__(self, url, user_agent):
        self.url = url
        self.user_agent = user_agent
        self.data = []

    def fetch_section_data(self, section_container):
        section_title = section_container.find('p', class_='title').get_text()
        links = section_container.find_all('a', class_='right-rail-article right-rail-ga')
        
        for link in links:
            article_title = link.find('p', class_='right-rail-article__title').get_text()
            category = link.find('p', class_='right-rail-article__category').get_text()
            time = link.find('p', class_='right-rail-article__time').get_text()
            href = link['href']
            self.data.append({'section_title': section_title, 'category': category, 'article_title': article_title, 'time': time, 'link': href})

    def fetch_data(self):
        response = requests.get(self.url, headers={"User-Agent": self.user_agent})
        soup = BeautifulSoup(response.content, 'lxml')
        top_stories_container = soup.find('div', class_='zone-rightRail1 content-module')
        featured_stories_container = soup.find('div', class_='zone-rightRail2 content-module')
        
        if top_stories_container and featured_stories_container:
            self.fetch_section_data(top_stories_container)
            self.fetch_section_data(featured_stories_container)

    def display_data(self):
        for item in self.data:
            print("Section Title:", item['section_title'])
            print("Category:", item['category'])
            print("Article Title:", item['article_title'])
            print("Time:", item['time'])
            print("Link:", item['link'])
            print()

def main():
    url = 'https://www.accuweather.com/en/us/el-paso/79901/weather-forecast/351195'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    
    scraper = WeatherScraper(url, user_agent)
    scraper.fetch_data()
    scraper.display_data()

if __name__ == "__main__":
    main()
