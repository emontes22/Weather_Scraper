import asyncio
from scraper import WeatherScraper
from telegram import Bot

async def send_data_to_telegram():
    # Initialize bot with API Token
    bot = Bot(token='Your_TOKEN_API')

    #Specify the chat ID
    chat_id = 'Your_ID'

    # Instance of WeatherScraper and fetch data
    scraper = WeatherScraper(url='https://www.accuweather.com/en/us/el-paso/79901/weather-forecast/351195', user_agent='Your_user_agent')
    scraper.fetch_data()

    # Prepare the message
    message = "Weather and News Updates:\n\n"

    # Append weather data
    message += "Weather Data:\n"
    for key, value in scraper.weather_data.items():
        message += f'{key}: {value.strip()}\n'
    message += "\n"

    # Append news data
    message += "News Data:\n"
    for item in scraper.news_data:
        message += f'Section Title: {item["section_title"]}\n'
        message += f'Category: {item["category"]}\n'
        message += f'Article Title: {item["article_title"]}\n'
        message += f'Time: {item["time"].strip()}\n'
        message += f'Link: {item["link"]}\n\n'

    # Send the message to Telegram
    await bot.send_message(chat_id=chat_id, text=message)

if __name__ == '__main__':
    # Create an event loop and run the asynchronous function
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_data_to_telegram())