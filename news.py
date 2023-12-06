import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Replace 'YOUR_BOT_TOKEN' with the token you obtained from the BotFather
TOKEN = '6855616059:AAHEAYW0fDebHL7U9ycuIWWh2ShlLEU0yXk'

# Replace 'YOUR_NEWS_API_KEY' with your News API key
NEWS_API_KEY = '322a7405703449fe895cf6f683f1b4a7'

# Define a function to send the top 10 crypto news to users
def send_top_crypto_news(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id

    # Fetch top crypto news from News API
    news_url = f'https://newsapi.org/v2/top-headlines?q=latest&apiKey={NEWS_API_KEY}'
    response = requests.get(news_url)
    news_data = response.json()

    if news_data['status'] == 'ok':
        # Extract the top 10 news articles
        articles = news_data['articles'][:10]
        
        # Send each article as a separate message
        for index, article in enumerate(articles, start=1):
            news_message = f"📰 *Crypto News #{index}* 📰\n\n" \
                            f"*Title*: {article['title']}\n" \
                            f"*Source*: {article['source']['name']}\n" \
                            f"*Description*: {article['description']}\n" \
                            f"*URL*: {article['url']}"
            
            # Send news to the user
            context.bot.send_message(chat_id=user_id, text=news_message, parse_mode='Markdown')
    else:
        context.bot.send_message(chat_id=user_id, text="Sorry, unable to fetch crypto news at the moment. Please try again later.")

# Define a function to handle the /start command
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    context.bot.send_message(chat_id=user_id, text="Welcome to Crypto News Bot! Type /topnews to get news.")

# Set up the updater with the bot token
updater = Updater(token=TOKEN, use_context=True)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Register the start and topnews command handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("topnews", send_top_crypto_news))

# Start the Bot
updater.start_polling()

# Run the bot until you send a signal to stop it
updater.idle()
