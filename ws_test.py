import pandas as pd
import time
import ccxt
from pybit.unified_trading import HTTP, WebSocket
from pybit import exceptions
import json
from time import sleep

# Настройки API
api_key = 'hHmv5ikDrmQrhR2i2e'
api_secret = 'vckUl1bSyBJJhhx5bmeReKL46UrPYFEAsyzq'


session = HTTP(
        # testnet=True,
        # max_retries=10,
        # recv_window=60000,
        api_key = api_key,
        api_secret = api_secret,
        # return_response_headers=True
)

# Инициализация подключения к Bybit
exchange = ccxt.bybit({
    'apiKey': api_key,
    'secret': api_secret,
})

# Параметры стратегии
__symbol = 'DOGE/USDT' #рговая пара
timeframe = '1m'  # Таймфрейм
atr_period = 14  # Период для ATR
ema_period = 20  # Период для EMA
multiplier = 1  # Множитель для ATR


# Функция для получения данных
def fetch_ohlcv(__symbol, timeframe, limit=100):
    ohlcv = exchange.fetch_ohlcv(__symbol, timeframe, limit=limit)

    # with open('azrael/json/ohlcv.json', 'w', encoding='utf-8') as f:
    #     json.dump(ohlcv, f, indent=4, ensure_ascii=False)

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


def get_assets(cl : HTTP):
    """
    Получаю остатки на аккаунте по конкретной монете
    :param cl:
    :param coin:
    :return:
    """

    balance = session.get_positions(
        category="linear",
        symbol="DOGEUSDT",
    )

    with open('azrael/json/balance.json', 'w', encoding='utf-8') as f:
        json.dump(balance, f, indent=4, ensure_ascii=False)

    
   
    return int(balance["result"]["list"][0]["size"])


def ws_start(m):
    timestamp_ = m["data"][0]["timestamp"]
    open_ = m["data"][0]["open"]
    high_ = m["data"][0]["high"]
    low_ = m["data"][0]["low"]
    close_ = m["data"][0]["close"]
    volume_ = m["data"][0]["volume"]


    data = {
        'timestamp': [timestamp_],
        'open': float(open_),
        'high': float(high_),
        'low': float(low_),
        'close': float(close_),
        'volume': float(volume_),
    }

    # with open('azrael/json/message.json', 'w', encoding='utf-8') as f:
    #     json.dump(data, f, indent=4, ensure_ascii=False)

    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    print(m) 

    return m

     

def start():

    in_position = False
    signal = None

    while True:
        try:
            # Получаем данные

            ws = WebSocket(
                testnet=False,
                channel_type="linear",
            )

            close_ws = ws.kline_stream(
                interval=1,
                symbol="DOGEUSDT",
                callback=ws_start
            )


            print(type(close_ws))

           
            
            df = fetch_ohlcv(__symbol, timeframe)
            df = calculate_keltner_channel(df, ema_period, atr_period, multiplier)

            # Проверяем сигналы
            print(df)
            signal = check_signals(df)
            print(f"Pos: {in_position}")
            print(f"Sig: {signal}")

            if signal == 'buy' and in_position == False:
                print("Сигнал на покупку")
                # Размещение ордера на покупку
                
                r = session.place_order(
                        category="linear",
                        symbol="DOGEUSDT",
                        side="Buy",
                        orderType="Market",
                        # qty=floor_price(avbl, 3),
                        qty=25,
                        marketUnit="quoteCoin", # USDT
                )
                print(r)

                get_assets(session)

                with open('azrael/json/order.json', 'w', encoding='utf-8') as f:
                    json.dump(r, f, indent=4, ensure_ascii=False)

                in_position = True
               
                print(in_position)
                print(signal)
                print("Ордер на покупку размещен:")  

            elif signal == 'buy' or signal == None and in_position == True:           
                last_row = df.iloc[-1]
   
                if last_row['close'] <= last_row['upper_band']:

                    r = session.place_order(
                        category="linear",
                        symbol="DOGEUSDT",
                        side="Sell",
                        orderType="Market",
                        # qty=floor_price(avbl, 3),
                        qty=25,
                        marketUnit="quoteCoin", # USDT
                        # timeInForce="GoodTillCancel",
                        reduceOnly=True,
                        # closeOnTrigger=False,
                    )

                    in_position = False

                    print("Close long position")           

            if signal == 'sell' and in_position == False:
                print("Сигнал на продажу")
                # # Размещение ордера на продажу
            
                r = session.place_order(
                        category="linear",
                        symbol="DOGEUSDT",
                        side="Sell",
                        orderType="Market",
                        # qty=floor_price(avbl, 3),
                        qty=25,
                        marketUnit="quoteCoin", # USDT
                )

                get_assets(session)

                with open('azrael/json/order.json', 'w', encoding='utf-8') as f:
                    json.dump(r, f, indent=4, ensure_ascii=False)

                in_position = True
                
                print(in_position)
                print(signal)
                print("Ордер на продажу размещен:")   

            elif signal == 'sell' or signal == None and in_position == True: 
                last_row = df.iloc[-1]
   
                if last_row['close'] >= last_row['lower_band']:

                    r = session.place_order(
                        category="linear",
                        symbol="DOGEUSDT",
                        side="Buy",
                        orderType="Market",
                        # qty=floor_price(avbl, 3),
                        qty=25,
                        marketUnit="quoteCoin", # USDT
                        # timeInForce="GoodTillCancel",
                        reduceOnly=True,
                        # closeOnTrigger=False,
                    )

                    in_position = False

                    print("Close short position")       

            # Пауза перед следующей итерацией
            time.sleep(5)

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            time.sleep(5)


# Основной цикл торговли
def main():
    
    # ws = WebSocket(
    #     testnet=False,
    #     channel_type="linear",
    # )

    # ws.kline_stream(
    #     interval=1,
    #     symbol="DOGEUSDT",
    #     callback=start
    # )
    
    start()


if __name__ == "__main__":
    main()