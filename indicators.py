import os
import pandas as pd
from pybit.unified_trading import WebSocket, HTTP
import ccxt

from datetime import datetime
import time
import json



class Indicators:
        
    def __init__(self):
        self.api_key='hHmv5ikDrmQrhR2i2e', 
        self.api_secret='vckUl1bSyBJJhhx5bmeReKL46UrPYFEAsyzq', 


    # def __init__(self, bybit_method: str, bybit_methods: dict=None, *args, **kwargs):
    #     super(Indicators, self).__init__(*args, **kwargs)
    #     self.bybit_method = bybit_method

    
        # Инициализация подключения к Bybit
        self.exchange = ccxt.bybit({
            'apiKey': self.api_key,
            'secret': self.api_secret,
        })

        self.session = HTTP(
                # testnet=True,
                # max_retries=10,
                # recv_window=60000,
                api_key = self.api_key,
                api_secret = self.api_secret,
                # return_response_headers=True
        )

        # Параметры стратегии
        self.timeframe = '1m'  # Таймфрейм
        self.atr_period = 14  # Период для ATR
        self.ema_period = 20  # Период для EMA
        self.multiplier = 1  # Множитель для ATR


    # Функция для получения данных с CCXT
    def ccxt_ohlcv(self, __symbol, timeframe, limit=100):
        ohlcv = self.exchange.fetch_ohlcv(__symbol, timeframe, limit=limit)

        # with open('azrael/json/ohlcv.json', 'w', encoding='utf-8') as f:
        #     json.dump(ohlcv, f, indent=4, ensure_ascii=False)

        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    

    # Создание датафрэйма
    def create_df(self, ohlcv):
    
        # with open('azrael/json/ohlcv.json', 'w', encoding='utf-8') as f:
        #     json.dump(ohlcv, f, indent=4, ensure_ascii=False)

        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'some'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df


    # Функция для расчета EMA
    def calculate_ema(self, df, period):
        df['ema'] = df['close'].ewm(span=period, adjust=False).mean()
        return df


    # Функция для расчета ATR
    def calculate_atr(self, df, period):
        df['tr'] = df['high'] - df['low']
        df['atr'] = df['tr'].rolling(window=period).mean()
        return df


    # Функция для расчета канала Кельтнера
    def calculate_keltner_channel(self, df, ema_period, atr_period, multiplier):
        df = self.calculate_ema(df, self.ema_period)
        df = self.calculate_atr(df, self.atr_period)
        df['upper_band'] = df['ema'] + (df['atr'] * self.multiplier)
        df['lower_band'] = df['ema'] - (df['atr'] * self.multiplier)
        return df


    # Функция для проверки условий входа и выхода
    def check_signals(self, df):
        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]

        # Условие для покупки
        # if last_row['close'] > last_row['upper_band'] and prev_row['close'] <= prev_row['upper_band']:
        if last_row['close'] > last_row['upper_band'] and prev_row['close'] > prev_row['upper_band']:
            return 'buy'

        # Условие для продажи
        # elif last_row['close'] < last_row['lower_band'] and prev_row['close'] >= prev_row['lower_band']:
        elif last_row['close'] < last_row['lower_band'] and prev_row['close'] < prev_row['lower_band']:
            return 'sell'

        return None


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
        