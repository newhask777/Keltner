from pybit.unified_trading import WebSocket, HTTP
from pybit import exceptions
import ccxt
import pandas as pd
import time
import json
from datetime import datetime
from indicators import Indicators

class ByBitMethods(Indicators):

    def __init__(self, api_key=None, api_secret=None, interval=5, symbol='BTCUSDT', category='linear', save_ws=False, save_http=False, db=None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.interval = interval
        self.symbol = symbol
        self.category = category
        self.stream_type = ''
        self.save_ws = save_ws
        self.save_http = save_http
        self.db = db

        # Параметры стратегии
        self.timeframe = '1m'  # Таймфрейм
        self.atr_period = 14  # Период для ATR
        self.ema_period = 20  # Период для EMA
        self.multiplier = 1  # Множитель для ATR

         # Инициализация подключения к Bybit
        self.exchange = ccxt.bybit({
            'apiKey': self.api_key,
            'secret': self.api_secret,
        })

        self.session = HTTP()

        self.in_position = False
        self.signal = None

    # WebSocket method
    def ws_stream(self):
        self.stream_type = 'websocket'

        def save_to_db(message):
            # print(message)

            df = self.http_query(self.session)
            # df = df.iloc[:, :-1]
            df = self.calculate_keltner_channel(df, self.ema_period, self.atr_period, self.multiplier)

            # print(df)

            # print(self.signal)
            # print(self.in_position)

            self.signal = self.check_signals(df)
            print(f"Pos: {self.in_position}")
            print(f"Sig: {self.signal}")

            # print(self.signal)
            # time.sleep(10)

            if self.signal == 'buy' and self.in_position == False:
                print("Сигнал на покупку")
                # Размещение ордера на покупку
                
                # r = self.session.place_order(
                #         category="linear",
                #         symbol="DOGEUSDT",
                #         side="Buy",
                #         orderType="Market",
                #         # qty=floor_price(avbl, 3),
                #         qty=25,
                #         marketUnit="quoteCoin", # USDT
                # )
                # print(r)

                self.in_position = True
               
                print(self.in_position)
                print(self.signal)
                print("Ордер на покупку размещен:")  

            elif self.signal == 'buy' or self.signal == None and self.in_position == True:           
                last_row = df.iloc[-1]
   
                if last_row['close'] <= last_row['upper_band']:

                    # r = self.session.place_order(
                    #     category="linear",
                    #     symbol="DOGEUSDT",
                    #     side="Sell",
                    #     orderType="Market",
                    #     # qty=floor_price(avbl, 3),
                    #     qty=25,
                    #     marketUnit="quoteCoin", # USDT
                    #     # timeInForce="GoodTillCancel",
                    #     reduceOnly=True,
                    #     # closeOnTrigger=False,
                    # )

                    self.in_position = False

                    print("Close long position")           

            if self.signal == 'sell' and self.in_position == False:
                print("Сигнал на продажу")
                # # Размещение ордера на продажу
            
                # r = self.session.place_order(
                #         category="linear",
                #         symbol="DOGEUSDT",
                #         side="Sell",
                #         orderType="Market",
                #         # qty=floor_price(avbl, 3),
                #         qty=25,
                #         marketUnit="quoteCoin", # USDT
                # )

                self.in_position = True
                
                print(self.in_position)
                print(self.signal)
                print("Ордер на продажу размещен:")   

            elif self.signal == 'sell' or self.signal == None and self.in_position == True: 
                last_row = df.iloc[-1]
   
                if last_row['close'] >= last_row['lower_band']:

                    # r = self.session.place_order(
                    #     category="linear",
                    #     symbol="DOGEUSDT",
                    #     side="Buy",
                    #     orderType="Market",
                    #     # qty=floor_price(avbl, 3),
                    #     qty=25,
                    #     marketUnit="quoteCoin", # USDT
                    #     # timeInForce="GoodTillCancel",
                    #     reduceOnly=True,
                    #     # closeOnTrigger=False,
                    # )

                    self.in_position = False

                    print("Close short position")  

            time.sleep(10)     


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
        df = self.ccxt_ohlcv("DOGEUSDT", 1, limit=100)

        return df


        