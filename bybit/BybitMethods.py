from pybit.unified_trading import WebSocket, HTTP
from pybit import exceptions
import ccxt
import pandas as pd
import json

'''
Реализовать:
- метод для получения по текущей позиции
- метод для установки тэйк профита в процентах
- вынести основной метод в класс Трэйдер
- создать скринер
'''

class ByBitMethods:

    # Функция для получения цены открытия
    def get_open_price(self):
        try:
            response = self.session.get_positions(
                category="linear",  # Используйте "linear" для линейных фьючерсов, "inverse" для обратных фьючерсов, "spot" для спота
                symbol=self.symbol
            )

            print(response['result']['list'][0]['avgPrice'])
            return float(response['result']['list'][0]['avgPrice'])
        except:
            print('No open positions')
            return None
        

    # Функция для расчета изменения цены в процентах  
    def calculate_price_change_percentage(self, current_price, open_price):
        try:
            if open_price > 0:
                percantage = round(((current_price - open_price) / open_price) * 100, 2)
                # percantage = round(percantage, 2)
                print(percantage)
            return percantage
        except:
            return print('no open price')


    # Функция для проверки условий входа и выхода Канал Кельтнера
    def check_signals(self, df):
        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]

        # Условие для покупки
        # if last_row['close'] > last_row['upper_band'] and prev_row['close'] <= prev_row['upper_band']:
        if last_row['close'] > last_row['upper_band'] and prev_row['close'] > prev_row['upper_band']:
            return 'Buy'

        # Условие для продажи
        # elif last_row['close'] < last_row['lower_band'] and prev_row['close'] >= prev_row['lower_band']:
        elif last_row['close'] < last_row['lower_band'] and prev_row['close'] < prev_row['lower_band']:
            return 'Sell'

        return None
    

    # Функция для проверки условий входа и выхода
    def check_signals_by_message(self, df, message):
        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]

       

        # Условие для покупки
        # if message["data"][0]["close"] > last_row['upper_band'] and prev_row['close'] <= prev_row['upper_band']:
        if float(message["data"][0]["close"]) > last_row['upper_band']:
            return 'Buy'

        # Условие для продажи
        # elif message["data"][0]["close"] < last_row['lower_band'] and prev_row['close'] >= prev_row['lower_band']:
        elif float(message["data"][0]["close"]) < last_row['lower_band']:
            return 'Sell'
        
        # print(message["data"][0]["close"])
        # print("last row", last_row['upper_band'])

        return None


    # Функция для проверки доступных средств
    def get_assets(self, cl : HTTP):
        """
        Получаю остатки на аккаунте по конкретной монете
        :param cl:
        :param coin:
        :return:
        """

        balance = self.session.get_positions(
            category="linear",
            symbol="DOGEUSDT",
        )

        with open('azrael/json/balance.json', 'w', encoding='utf-8') as f:
            json.dump(balance, f, indent=4, ensure_ascii=False)

        
    
        return int(balance["result"]["list"][0]["size"])
        