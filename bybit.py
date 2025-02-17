from pybit.unified_trading import WebSocket, HTTP
from pybit import exceptions
import ccxt
import pandas as pd
import time
import json
from datetime import datetime
from indicators import Indicators

class ByBitMethods(Indicators):

    def __init__(self, api_key=None, api_secret=None, interval=5, symbol='BTCUSDT', category='linear', qty=None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.interval = interval
        self.symbol = symbol
        self.category = category
        self.stream_type = ''
        self.qty = qty

        # Параметры стратегии
        # self.timeframe = '5m'  # Таймфрейм
        self.atr_period = 14  # Период для ATR
        self.ema_period = 20  # Период для EMA
        self.multiplier = 1  # Множитель для ATR

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

        self.in_position = False
        self.signal = None

    # WebSocket method
    def ws_stream(self):
        self.stream_type = 'websocket'

        def save_to_db(message):
            # print(message)

            # with open('json/message.json', 'w', encoding='utf-8') as f:
            #     json.dump(message, f, indent=4, ensure_ascii=False)

            df = self.http_query(self.session)
            # df = df.iloc[:, :-1]
            df = self.calculate_keltner_channel(df, self.ema_period, self.atr_period, self.multiplier)

            # print(df)

            # self.signal = self.check_signals_by_message(df, message)
            last_row = df.iloc[-1]
            prev_row = df.iloc[-2]
            print(f"Pos: {self.in_position}")
            print(f"Sig: {self.signal}")

            # if self.signal == 'Buy'  and self.in_position == False:
            if float(message["data"][0]["close"]) > last_row['upper_band']  and self.in_position == False:
                
                # print(self.signal)
                print("Сигнал на покупку")
                # Размещение ордера на покупку
                
                r = self.session.place_order(
                        category=self.category,
                        symbol=self.symbol,
                        side="Buy",
                        orderType="Market",
                        # qty=floor_price(avbl, 3),
                        qty=self.qty,
                )

                self.in_position = True
                self.signal = 'Buy'
               
                print(self.in_position)
                print(self.signal)
                print("Ордер на покупку размещен:")  

            elif self.signal == 'Buy' or self.signal == None and self.in_position == True:           
                last_row = df.iloc[-1]
   
                if float(message["data"][0]["close"]) < last_row['upper_band']:
                # if last_row['close'] < last_row['upper_band']:

                    r = self.session.place_order(
                        category=self.category,
                        symbol=self.symbol,
                        side="Sell",
                        orderType="Market",
                        # qty=floor_price(avbl, 3),
                        qty=self.qty,
                        # timeInForce="GoodTillCancel",
                        reduceOnly=True,
                        # closeOnTrigger=True,
                    )

                    self.in_position = False
                    self.signal = None

                    print("Close long position")           

            if float(message["data"][0]["close"]) < last_row['lower_band']  and self.in_position == False:
            # if self.signal == 'Sell' < last_row['lower_band']  and self.in_position == False:
                
                print("Сигнал на продажу")
                # # Размещение ордера на продажу
            
                r = self.session.place_order(
                        category=self.category,
                        symbol=self.symbol,
                        side="Sell",
                        orderType="Market",
                        # qty=floor_price(avbl, 3),
                        qty=self.qty,
                )

                self.in_position = True
                self.signal = 'Sell'
                
                print(self.in_position)
                print(self.signal)
                print("Ордер на продажу размещен:")   

            elif self.signal == 'Sell' or self.signal == None and self.in_position == True: 
                last_row = df.iloc[-1]
   
                if float(message["data"][0]["close"]) > last_row['lower_band']:
                # if last_row['close'] > last_row['lower_band']:

                    r = self.session.place_order(
                        category=self.category,
                        symbol=self.symbol,
                        side="Buy",
                        orderType="Market",
                        # qty=floor_price(avbl, 3),
                        qty=self.qty,
                        # timeInForce="GoodTillCancel",
                        reduceOnly=True,
                        # closeOnTrigger=True,
                    )

                    self.in_position = False
                    self.signal = None

                    print("Close short position")  
     

        try:
            ws = WebSocket(
                testnet=False,
                channel_type=self.category,
            )

            stream = ws.kline_stream(
                symbol=self.symbol,
                interval=self.interval,
                callback=save_to_db
            )
   
        except exceptions.InvalidRequestError as e:
            print("Bybit Request Error", e.status_code, e.message, sep=' | ')
        except exceptions.FailedRequestError as e:
                print("Bybit Request Failed", e.status_code, e.message, sep=' | ')
        except Exception as e:
            print(e)



    # HTTP method   
    def http_query(self, session):
        self.stream_type = 'http'

        if self.save_http:
            print('save http')
 
        # klines = self.session.get_kline(category=self.category, symbol=self.symbol, interval=self.interval,)
        # df = self.create_df(klines["result"]["list"])
        df = self.ccxt_ohlcv(self.symbol, self.interval, limit=100)

        return df


        