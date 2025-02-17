import pandas as pd
from pybit.unified_trading import WebSocket, HTTP
import ccxt


class KeltnerChannel:
        
    def __init__(self):
        pass


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

