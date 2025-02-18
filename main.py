from bybit.Trader import BybitTrader
import time


bybit = BybitTrader(
    # Live
    api_key='onjgaIMByB9Sk2AEnq', 
    api_secret='u9QYLcd4SGoxaLqjJrCc4JybSpHjRZFVWFEU', 
    # Testnet
    # api_key = '1jSxOb8XOKS1QD2w3x',
    # api_secret = 'wsIJ6gHBOdYLWY21K0RzoFdV9PO0f49M3VLu',

    interval=15, 
    symbol="DOGEUSDT", 
    category="linear",
    qty=30,
)


bybit.ws_stream()


if __name__ == "__main__":
    while True:
        time.sleep(1)