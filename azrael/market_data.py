from pybit.unified_trading import HTTP
from pybit import exceptions
from env  import *
import json
import logging

log = logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

# with open('logs/market_data.txt', 'w') as f:
#     f.write(str(log))

session = HTTP(
    testnet=True,
    max_retries=10,
    recv_window=60000,
    api_key=api_key,
    api_secret=api_secret,
    # return_response_headers=True
)

try:
    market_data = session.get_orderbook(category="linear", symbol="BTCUSDT")
    print(market_data)

    with open('json/market_data.json', 'w', encoding='utf-8') as f:
        json.dump(market_data, f, indent=4, ensure_ascii=False)
        
except exceptions.InvalidRequestError as e:
    print(e.status_code, e.message, sep=" | ")




