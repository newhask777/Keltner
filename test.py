from pybit.unified_trading import WebSocket
from pybit import exceptions
from time import sleep
import certifi



def main():

    print(certifi.where())

    try:
        ws = WebSocket(
            testnet=False,
            channel_type="linear",
            api_key="hHmv5ikDrmQrhR2i2e",
            api_secret="vckUl1bSyBJJhhx5bmeReKL46UrPYFEAsyzq",
        )


        def handle_message(message):
            print(message)
    
        stream = ws.kline_stream(
                symbol="DOGEUSDT",
                interval=5,
                callback=handle_message
            )

    except exceptions.InvalidRequestError as e:
        print("Bybit Request Error", e.status_code, e.message, sep=' | ')
    except exceptions.FailedRequestError as e:
        print("Bybit Request Failed", e.status_code, e.message, sep=' | ')
    except Exception as e:
        print(e)

    while True:
        sleep(1)

if __name__ == "__main__":
    print("Go")
    main()