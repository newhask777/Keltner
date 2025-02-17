from bybit import ByBitMethods
from indicators import Indicators
from pybit.unified_trading import WebSocket, HTTP
import json
import time
import pandas as pd

bybit = ByBitMethods(
    api_key='ZeV8tazdLe0VRQF2UU', 
    api_secret='bpbQwmOF7dB1N67pRGyFWb0IhLqGv1K40qb1', 
    interval=5, 
    symbol="1000RATSUSDT", 
    category="linear",
    qty=1000,
)

# ind = Indicators()

bybit.ws_stream()

# http = bybit.http_query()

if __name__ == "__main__":
    while True:
    #   print(http)
        time.sleep(1)