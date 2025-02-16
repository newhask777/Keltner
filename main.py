from bybit import ByBitMethods
from indicators import Indicators
from pybit.unified_trading import WebSocket, HTTP
import json
import time
import pandas as pd

bybit = ByBitMethods(
    api_key='hHmv5ikDrmQrhR2i2e', 
    api_secret='vckUl1bSyBJJhhx5bmeReKL46UrPYFEAsyzq', 
    interval=1, symbol="DOGEUSDT", 
    category="linear"
)

ind = Indicators()

# ws = bybit.ws_stream()

# http = bybit.http_query()

if __name__ == "__main__":
    while True:
    #   print(http)
        ws = bybit.ws_stream()
        time.sleep(10)