from pybit.unified_trading import WebSocket, HTTP
from pybit import exceptions
from time import sleep
import certifi
from bybit.BybitMethods import ByBitMethods

api_key='onjgaIMByB9Sk2AEnq', 
api_secret='u9QYLcd4SGoxaLqjJrCc4JybSpHjRZFVWFEU',
symbol= 'DOGEUSDT'

session = HTTP(
    api_key='onjgaIMByB9Sk2AEnq', 
    api_secret='u9QYLcd4SGoxaLqjJrCc4JybSpHjRZFVWFEU',
)


bybit = ByBitMethods()
pos = bybit.calculate_price_change_percentage(0.25577, 0.26777)



if __name__ == "__main__":
    print("Go")
    print(pos)

  