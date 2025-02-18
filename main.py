from bybit.Trader import BybitTrader
import time


bybit = BybitTrader(
    api_key='onjgaIMByB9Sk2AEnq', 
    api_secret='u9QYLcd4SGoxaLqjJrCc4JybSpHjRZFVWFEU', 
    interval=15, 
    symbol="ACHUSDT", 
    category="linear",
    qty=200,
)


bybit.ws_stream()


if __name__ == "__main__":
    while True:
        # print(http)
        time.sleep(1)