from pybit.unified_trading import HTTP
from pybit import exceptions
from env  import *
import json
import logging

def main():

    log = logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

    # with open('logs/market_data.txt', 'w') as f:
    #     f.write(str(log))

    session = HTTP(
        # testnet=True,
        # max_retries=10,
        recv_window=60000,
        api_key=api_key,
        api_secret=api_secret,
        return_response_headers=True
    )

    try:
        executions, e, h = session.get_executions(category="linear", limit=10)
        print(h.get('X-Bapi-Limit-Status'), h.get('X-Bapi-Limit'), sep='/') # get rate limit

        with open('json/auth.json', 'w', encoding='utf-8') as f:
            json.dump(str(executions[2]), f, indent=4, ensure_ascii=False)
            
    except exceptions.InvalidRequestError as e:
        print("ByBit Request Error", e.status_code, e.message, sep=" | ")
    except exceptions.FailedRequestError as e:
        print("ByBit Requewst Failed", e.status_code, e.message, sep=" | ")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    print("start")
    main()


