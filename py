import os
import requests
import pandas as pd
import telebot
from io import BytesIO

# 
bot = telebot.TeleBot("7122748860:AAEvuPFW3XjXvNEU6gkUCmn14t-MdHbfXG4")

def fetch_binance_data(symbol, interval, limit):
    # URL 
    url = f"https://api.binance.com/api/v1/klines?symbol={symbol}&interval={interval}&limit={limit}"
    response = requests.get(url)
    data = response.json()

    # DataFrame
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)

    return df

def save_to_csv(df, file_path):
    # حفظ البيانات في ملف CSV
    df.to_csv(file_path)
    return file_path

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome to Binance Data Bot! Click below to download historical data:", reply_markup=generate_markup())

def generate_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    btn_ada = telebot.types.InlineKeyboardButton('ADA Data', callback_data='ada')
    btn_btc = telebot.types.InlineKeyboardButton('BTC Data', callback_data='btc')
    btn_eth = telebot.types.InlineKeyboardButton('ETH Data', callback_data='eth')
    markup.add(btn_ada, btn_btc, btn_eth)
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'ada':
        symbol = "ADAUSDT"
        interval = "1d"
        limit = 1000
        df = fetch_binance_data(symbol, interval, limit)
        file_path = save_to_csv(df, 'ada_data.csv')
        with open(file_path, 'rb') as file:
            bot.send_document(call.message.chat.id, file)
        os.remove(file_path)
    elif call.data == 'btc':
        symbol = "BTCUSDT"
        interval = "1d"
        limit = 1000
        df = fetch_binance_data(symbol, interval, limit)
        file_path = save_to_csv(df, 'btc_data.csv')
        with open(file_path, 'rb') as file:
            bot.send_document(call.message.chat.id, file)
        os.remove(file_path)
    elif call.data == 'eth':
        symbol = "ETHUSDT"
        interval = "1d"
        limit = 1000
        df = fetch_binance_data(symbol, interval, limit)
        file_path = save_to_csv(df, 'eth_data.csv')
        with open(file_path, 'rb') as file:
            bot.send_document(call.message.chat.id, file)
        os.remove(file_path)
bot.polling()
