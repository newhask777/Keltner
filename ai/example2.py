from pybit.unified_trading import WebSocket, HTTP
import pandas as pd
import numpy as np
import time

# Конфигурация
API_KEY = 'hHmv5ikDrmQrhR2i2e'
API_SECRET = 'vckUl1bSyBJJhhx5bmeReKL46UrPYFEAsyzq'
SYMBOL = 'DOGEUSDT'  # Используем USDT-пары в API v5
TIMEFRAME = 1  # 1 минута

# Параметры канала Кельтнера
EMA_PERIOD = 20
ATR_PERIOD = 10
MULTIPLIER = 1

# Глобальный DataFrame для хранения данных
df = pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close'])

# Функция для расчета EMA с использованием pandas
def calculate_ema(data, period):
    return data['close'].ewm(span=period, adjust=False).mean()

# Функция для расчета ATR с использованием pandas
def calculate_atr(data, period):
    high = data['high']
    low = data['low']
    close = data['close']
    tr = np.maximum(high - low, np.maximum(abs(high - close), abs(low - close)))
    return tr.rolling(window=period).mean()

# Функция для расчета канала Кельтнера
def calculate_keltner_channel(data, ema_period, atr_period, multiplier):
    ema = calculate_ema(data, ema_period)
    atr = calculate_atr(data, atr_period)
    upper_channel = ema + (atr * multiplier)
    lower_channel = ema - (atr * multiplier)
    return upper_channel, lower_channel, ema

# Обработчик сообщений WebSocket
def handle_message(message):
    global df

    # Обрабатываем данные свечи
    candle = message['data'][0]
    timestamp = pd.to_datetime(candle['start'], unit='ms')
    open_price = float(candle['open'])
    high_price = float(candle['high'])
    low_price = float(candle['low'])
    close_price = float(candle['close'])

    # Добавляем новую строку в DataFrame
    new_row = pd.DataFrame({
        'timestamp': [timestamp],
        'open': [open_price],
        'high': [high_price],
        'low': [low_price],
        'close': [close_price]
    })
    df = pd.concat([df, new_row], ignore_index=True)

    print(df)

    # Если накоплено достаточно данных, рассчитываем канал Кельтнера
    if len(df) >= EMA_PERIOD + ATR_PERIOD:
        upper_channel, lower_channel, ema = calculate_keltner_channel(
            df, EMA_PERIOD, ATR_PERIOD, MULTIPLIER
        )

        # Получаем последние значения
        last_close = df['close'].iloc[-1]
        last_upper = upper_channel.iloc[-1]
        last_lower = lower_channel.iloc[-1]

        # Принятие торговых решений
        if last_close > last_upper:
            print("Цена выше верхнего канала - Покупаем")
            place_order('Buy', 20)  # Пример размера ордера
        elif last_close < last_lower:
            print("Цена ниже нижнего канала - Продаем")
            place_order('Sell', 20)  # Пример размера ордера

# Функция для отправки ордера
def place_order(side, qty):
    session = HTTP(
        api_key=API_KEY,
        api_secret=API_SECRET
    )
    try:
        order = session.place_order(
            category="linear",  # Используем линейные контракты (USDT)
            symbol=SYMBOL,
            side=side,
            orderType="Market",
            qty=qty,  # Количество в строковом формате
            timeInForce="GTC"
        )
        print(f"Ордер {side} размещен: {order}")
    except Exception as e:
        print(f"Ошибка при размещении ордера: {e}")

# Запуск WebSocket
ws = WebSocket(
    testnet=False,
    api_key=API_KEY,
    api_secret=API_SECRET,
    channel_type="linear"  # Используем линейные контракты (USDT)
)

# Подписка на поток данных свечей
ws.kline_stream(
    interval=TIMEFRAME,
    symbol=SYMBOL,
    callback=handle_message
)

# Запуск бесконечного цикла для поддержания соединения
while True:
    time.sleep(1)