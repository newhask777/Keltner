import ccxt
import pandas as pd
import talib
import time

# Настройки
SYMBOL = 'BTC/USDT'  # Пара для торговли
TIMEFRAME = '5m'     # Таймфрейм (1 час)
EMA_PERIOD = 20      # Период для EMA
ATR_PERIOD = 10      # Период для ATR
MULTIPLIER = 2       # Множитель для канала
AMOUNT = 0.001       # Количество для торговли

# Инициализация биржи (например, Binance)
exchange = ccxt.binance({
    'apiKey': 'oNEpB3LpojdQ5xdUcGxKAJajtl2RzKnoDEsQ3rvF3YylCZCIvuNP48b4I9NbDVGc',
    'secret': '4yh5Pp4utAsBwh70VYturGjPPgkqmdjl0jTaXUFqOj4l4aSFhDlJr2NCsNy2R2Mk',
})

# Функция для получения данных
def fetch_data(symbol, timeframe, limit=100):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
   
    return df

# Функция для расчета канала Кельтнера
def calculate_keltner_channel(df, ema_period, atr_period, multiplier):
    df['ema'] = talib.EMA(df['close'], timeperiod=ema_period)
    df['atr'] = talib.ATR(df['high'], df['low'], df['close'], timeperiod=atr_period)
    df['upper'] = df['ema'] + (df['atr'] * multiplier)
    df['lower'] = df['ema'] - (df['atr'] * multiplier)
    
    return df

# Функция для проверки сигналов
def check_signals(df):
    last_row = df.iloc[-1]
    prev_row = df.iloc[-2]

    # Сигнал на покупку: цена пересекает нижнюю линию канала
    if last_row['close'] > last_row['lower'] and prev_row['close'] <= prev_row['lower']:
        return 'buy'

    # Сигнал на продажу: цена пересекает верхнюю линию канала
    elif last_row['close'] < last_row['upper'] and prev_row['close'] >= prev_row['upper']:
        return 'sell'

    return None

# Основной цикл торговли
def trade():
    print("Запуск торговой стратегии...")
    while True:
        try:
            # Получаем данные
            df = fetch_data(SYMBOL, TIMEFRAME)
            df = calculate_keltner_channel(df, EMA_PERIOD, ATR_PERIOD, MULTIPLIER)

            # Проверяем сигналы
            signal = check_signals(df)
            if signal == 'buy':
                print("Сигнал на покупку!")
                # Размещение ордера на покупку
                order = exchange.create_market_buy_order(SYMBOL, AMOUNT)
                print("Ордер на покупку размещен:", order)
            elif signal == 'sell':
                print("Сигнал на продажу!")
                # Размещение ордера на продажу
                order = exchange.create_market_sell_order(SYMBOL, AMOUNT)
                print("Ордер на продажу размещен:", order)

            # Пауза перед следующей итерацией
            time.sleep(5)  # Проверка каждый час

        except Exception as e:
            print("Ошибка:", e)
            # time.sleep(60)

# Запуск стратегии
if __name__ == "__main__":
    trade()