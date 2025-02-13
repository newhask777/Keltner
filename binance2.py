import ccxt
import pandas as pd
import time

# Настройки
symbol = 'BNB/USDT'  # Торговая пара
timeframe = '1m'      # Таймфрейм
ema_period = 20       # Период для EMA
atr_period = 10       # Период для ATR
multiplier = 2        # Множитель для ATR
amount = 0.001        # Количество для торговли

# Инициализация биржи
exchange = ccxt.binance({
    'apiKey': 'oNEpB3LpojdQ5xdUcGxKAJajtl2RzKnoDEsQ3rvF3YylCZCIvuNP48b4I9NbDVGc',
    'secret': '4yh5Pp4utAsBwh70VYturGjPPgkqmdjl0jTaXUFqOj4l4aSFhDlJr2NCsNy2R2Mk',
    'enableRateLimit': True,
})

# Функция для получения данных
def fetch_data(symbol, timeframe, limit=100):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    return df

# Функция для расчета индикаторов
def calculate_indicators(df):
    df['ema'] = df['close'].ewm(span=ema_period, adjust=False).mean()
    df['atr'] = df['high'].rolling(window=atr_period).max() - df['low'].rolling(window=atr_period).min()
    df['upper_band'] = df['ema'] + (df['atr'] * multiplier)
    df['lower_band'] = df['ema'] - (df['atr'] * multiplier)
    return df

# Функция для проверки сигналов
def check_signals(df):
    
    last_row = df.iloc[-1]
    if last_row['close'] > last_row['upper_band']:
        return 'buy'
    elif last_row['close'] < last_row['lower_band']:
        return 'sell'
    else:
        return None

# Основной цикл торговли
while True:
    try:
        print("start")
        # Получаем данные
        df = fetch_data(symbol, timeframe)
        
        # Рассчитываем индикаторы
        df = calculate_indicators(df)
        
        # Проверяем сигналы
        signal = check_signals(df)
        
        # Выполняем торговые операции
        if signal == 'buy':
            print("Сигнал на покупку")
            order = exchange.create_market_buy_order(symbol, amount)
            print("Куплено:", order)
        elif signal == 'sell':
            print("Сигнал на продажу")
            order = exchange.create_market_sell_order(symbol, amount)
            print("Продано:", order)
        
        # Ждем перед следующей итерацией
        time.sleep(60)  # 5 минут
        
    except Exception as e:
        print("Ошибка:", e)
        time.sleep(60)  # Ждем перед повторной попыткой