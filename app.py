from config import api_token, api_url, api_bot_id
from bot import Bot

if __name__ == "__main__":
	bot = Bot(api_token, api_url, api_bot_id)

	bot.start()
