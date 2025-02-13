import ccxt
import pandas as pd
import time

# Настройки API
api_key = 'hHmv5ikDrmQrhR2i2e'
api_secret = 'vckUl1bSyBJJhhx5bmeReKL46UrPYFEAsyzq'

# Инициализация подключения к Bybit
exchange = ccxt.bybit({
    'apiKey': api_key,
    'secret': api_secret,
})

# Параметры стратегии
symbol = 'BTC/USDT'  # Торговая пара
timeframe = '1m'  # Таймфрейм
atr_period = 14  # Период для ATR
ema_period = 20  # Период для EMA
multiplier = 1  # Множитель для ATR

in_position = False
signal = None

# Функция для получения данных
def fetch_ohlcv(symbol, timeframe, limit=100):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Функция для расчета EMA
def calculate_ema(df, period):
    df['ema'] = df['close'].ewm(span=period, adjust=False).mean()
    return df

# Функция для расчета ATR
def calculate_atr(df, period):
    df['tr'] = df['high'] - df['low']
    df['atr'] = df['tr'].rolling(window=period).mean()
    return df

# Функция для расчета канала Кельтнера
def calculate_keltner_channel(df, ema_period, atr_period, multiplier):
    df = calculate_ema(df, ema_period)
    df = calculate_atr(df, atr_period)
    df['upper_band'] = df['ema'] + (df['atr'] * multiplier)
    df['lower_band'] = df['ema'] - (df['atr'] * multiplier)
    return df

# Функция для проверки условий входа и выхода
def check_signals(df):
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



def start(in_position):
   
    while True:
        try:
            # Получаем данные
            df = fetch_ohlcv(symbol, timeframe)
            df = calculate_keltner_channel(df, ema_period, atr_period, multiplier)

            # Проверяем сигналы
            print(df)
            signal = check_signals(df)
            print(f"Pos: {in_position}")
            print(f"Sig: {signal}")

            if signal == 'buy' and in_position == False:
                print("Сигнал на покупку")
                # Размещение ордера на покупку
                # order = exchange.create_market_buy_order(symbol, 0.001)  # Пример размера ордера
                in_position = True
                # signal = None
                print(in_position)
                print(signal)
                print("Ордер на покупку размещен:")  

            elif signal == 'buy' or signal == None and in_position == True:           
                last_row = df.iloc[-1]
   
                if last_row['close'] <= last_row['upper_band']:
                    in_position = False

                    print("Close long position")           
                # close_long_position(df, in_position)

            if signal == 'sell' and in_position == False:
                print("Сигнал на продажу")
                # # Размещение ордера на продажу
                # order = exchange.create_market_sell_order(symbol, 0.001)  # Пример размера ордера
                in_position = True
                # signal = None
                print(in_position)
                print(signal)
                print("Ордер на продажу размещен:")   

            elif signal == 'sell' or signal == None and in_position == True: 
                last_row = df.iloc[-1]
   
                if last_row['close'] >= last_row['lower_band']:
                    in_position = False

                    print("Close short position")       
                # close_short_position(df, in_position)

            # Пауза перед следующей итерацией
            time.sleep(60)

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            time.sleep(60)


# Основной цикл торговли
def main():
    start(in_position)

if __name__ == "__main__":
    main()