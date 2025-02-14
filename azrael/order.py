from pybit.unified_trading import HTTP
from pybit import exceptions
from env  import *
import json
import logging


def get_assets(cl : HTTP, coin: str):
    """
    Получаю остатки на аккаунте по конкретной монете
    :param cl:
    :param coin:
    :return:
    """

    balance = cl.get_wallet_balance(
            accountType="UNIFIED",
            coin=coin,
    )
   
    return balance


def main():

    # log = logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

    # with open('logs/market_data.txt', 'w') as f:
    #     f.write(str(log))

    session = HTTP(
        # testnet=True,
        # max_retries=10,
        # recv_window=60000,
        api_key = '63dU6UYGJqyKgKRlxE',
        api_secret = 'V2d9acJjYeGWVaXUp5kcM9P3PlQQiSyR2kFx',
        # return_response_headers=True
    )

    try:
        # r = cl.get_instruments_info(category="spot", symbol="SOLUSDT")
        # print(r)

        avbl = get_assets(session, "USDT")
        print(avbl)

        # print(session.get_wallet_balance(
        #     accountType="UNIFIED",
        #     coin="USDT",
        # ))

      

        with open('json/balance.json', 'w', encoding='utf-8') as f:
            json.dump(avbl, f, indent=4, ensure_ascii=False)



        # r = session.place_order(
        #     category="linear",
        #     symbol="TONUSDT",
        #     side="Sell",
        #     orderType="Market",
        #     # qty=floor_price(avbl, 3),
        #     qty=avbl,
        #     marketUnit="quoteCoin", # USDT
        # )

        # with open('json/order.json', 'w', encoding='utf-8') as f:
        #     json.dump(r, f, indent=4, ensure_ascii=False)

        # print(r)

    except exceptions.InvalidRequestError as e:
        print("ByBit API Request Error", e.status_code, e.message, sep=" | ")
    except exceptions.FailedRequestError as e:
        print("HTTP Request Failed", e.status_code, e.message, sep=" | ")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    print("start")
    main()


