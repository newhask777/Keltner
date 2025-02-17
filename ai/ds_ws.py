import websocket
import json
import time
import numpy as np
import hmac
import hashlib
import requests

# Конфигурация
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'
SYMBOL = 'BTCUSD'
TIMEFRAME = '1'  # 1 минута
WS_URL = f'wss://stream.bybit.com/realtime_{SYMBOL}'
API_URL = 'https://api.bybit.com'

# Параметры канала Кельтнера
EMA_PERIOD = 20
ATR_PERIOD = 10
MULTIPLIER = 1

# Глобальные переменные
closes = []
highs = []
lows = []

# Функция для подписи запросов
def generate_signature(secret, params):
    return hmac.new(secret.encode('utf-8'), params.encode('utf-8'), hashlib.sha256).hexdigest()

# Функция для отправки ордера
def place_order(side, qty):
    timestamp = str(int(time.time() * 1000))
    params = {
        'api_key': API_KEY,
        'side': side,
        'symbol': SYMBOL,
        'order_type': 'Market',
        'qty': qty,
        'time_in_force': 'GoodTillCancel',
        'timestamp': timestamp
    }
    params['sign'] = generate_signature(API_SECRET, '&'.join([f"{k}={v}" for k, v in sorted(params.items())]))
    response = requests.post(f'{API_URL}/v2/private/order/create', data=params)
    return response.json()

# Функция для расчета EMA
def calculate_ema(data, period):
    return data.ewm(span=period, adjust=False).mean()

# Функция для расчета ATR
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
def on_message(ws, message):
    global closes, highs, lows

    data = json.loads(message)
    if 'data' not in data:
        return

    candle = data['data'][0]
    close = float(candle['close'])
    high = float(candle['high'])
    low = float(candle['low'])

    closes.append(close)
    highs.append(high)
    lows.append(low)

    if len(closes) >= EMA_PERIOD + ATR_PERIOD:
        upper_channel, lower_channel, ema = calculate_keltner_channel(
            np.array(highs), np.array(lows), np.array(closes), EMA_PERIOD, ATR_PERIOD, MULTIPLIER)
        last_close = closes[-1]
        last_upper = upper_channel[-1]
        last_lower = lower_channel[-1]

        if last_close > last_upper:
            print("Цена выше верхнего канала - Покупаем")
            place_order('Buy', 0.001)  # Пример размера ордера
        elif last_close < last_lower:
            print("Цена ниже нижнего канала - Продаем")
            place_order('Sell', 0.001)  # Пример размера ордера

# Обработчик ошибок WebSocket
def on_error(ws, error):
    print(error)

# Обработчик закрытия WebSocket
def on_close(ws):
    print("WebSocket закрыт")

# Обработчик открытия WebSocket
def on_open(ws):
    print("WebSocket открыт")
    ws.send(json.dumps({
        "op": "subscribe",
        "args": [f"kline.{TIMEFRAME}.{SYMBOL}"]
    }))

# Запуск WebSocket
ws = websocket.WebSocketApp(WS_URL, on_message=on_message, on_error=on_error, on_close=on_close)

ws.on_open = on_open

ws.run_forever()