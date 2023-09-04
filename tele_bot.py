import asyncio
from scraper import WeatherScraper
from telegram import Bot

# Asynchronous function to send scraped data to a Telegram bot
async def send_data_to_telegram():
    # Initialize telegram bot with API Token
    bot = Bot(token='Your_TOKEN_API') # Replace with your TOKEN API

    # Specify the chat ID 
    chat_id = 'Your_ID' # Replace with your chat ID

    # Instance of WeatherScraper and fetch data
    scraper = WeatherScraper(url='https://www.accuweather.com/en/us/el-paso/79901/weather-forecast/351195', user_agent='Your_user_agent') # Replace with your user agent
    scraper.fetch_data()

    # Prepare the message to send
    message = "Weather and News Updates:\n\n"

    # Append weather data to the message
    message += "Weather Data:\n"
    for key, value in scraper.weather_data.items():
        message += f'{key}: {value.strip()}\n'
    message += "\n"

    # Append news data to the message
    message += "News Data:\n"
    for item in scraper.news_data:
        message += f'Section Title: {item["section_title"]}\n'
        message += f'Category: {item["category"]}\n'
        message += f'Article Title: {item["article_title"]}\n'
        message += f'Time: {item["time"].strip()}\n'
        message += f'Link: {item["link"]}\n\n'

    # Send the message to the specified chat ID
    await bot.send_message(chat_id=chat_id, text=message)

if __name__ == '__main__':
    # Create an event loop and run the asynchronous function
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_data_to_telegram())