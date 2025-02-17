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

# Глобальные переменные
closes = []  # Список цен закрытия
highs = []   # Список максимальных цен
lows = []    # Список минимальных цен

# Функция для расчета EMA с использованием pandas
def calculate_ema(data, period):
    return data.ewm(span=period, adjust=False).mean()

# Функция для расчета ATR с использованием pandas
def calculate_atr(high, low, close, period):
    tr = np.maximum(high - low, np.maximum(abs(high - close), abs(low - close)))
    return tr.rolling(window=period).mean()

# Функция для расчета канала Кельтнера
def calculate_keltner_channel(high, low, close, ema_period, atr_period, multiplier):
    ema = calculate_ema(close, ema_period)
    atr = calculate_atr(high, low, close, atr_period)
    upper_channel = ema + (atr * multiplier)
    lower_channel = ema - (atr * multiplier)
    return upper_channel, lower_channel, ema

# Обработчик сообщений WebSocket
def handle_message(message):
    # print(message)
    global closes, highs, lows

    # Обрабатываем данные свечи
    candle = message['data'][0]
    close = float(candle['close'])
    high = float(candle['high'])
    low = float(candle['low'])

    # Добавляем данные в списки
    closes.append(close)
    highs.append(high)
    lows.append(low)

    # Если накоплено достаточно данных, рассчитываем канал Кельтнера
    if len(closes) >= EMA_PERIOD + ATR_PERIOD:
        # Преобразуем списки в pandas Series для удобства расчетов
        close_series = pd.Series(closes)
        high_series = pd.Series(highs)
        low_series = pd.Series(lows)

        # Рассчитываем канал Кельтнера
        upper_channel, lower_channel, ema = calculate_keltner_channel(
            high_series, low_series, close_series, EMA_PERIOD, ATR_PERIOD, MULTIPLIER
        )

        # print(f"upper {upper_channel}", f"lower {lower_channel}", f"ema {ema}")

        # Получаем последние значения
        last_close = closes[-1]
        last_upper = upper_channel.iloc[-1]
        last_lower = lower_channel.iloc[-1]

        print(f"last close {last_close}")
        print(f"last upper {last_upper}")
        print(f"last lower {last_lower}")

        # Принятие торговых решений
        if last_close > last_upper:
            print("Цена выше верхнего канала - Покупаем")
            place_order('Buy', 0.001)  # Пример размера ордера
        elif last_close < last_lower:
            print("Цена ниже нижнего канала - Продаем")
            place_order('Sell', 0.001)  # Пример размера ордера

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
            qty=str(qty),  # Количество в строковом формате
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