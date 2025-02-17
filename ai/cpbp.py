from pybit.unified_trading import WebSocket, HTTP
import time

# Настройки API
api_key='ZeV8tazdLe0VRQF2UU', 
api_secret='bpbQwmOF7dB1N67pRGyFWb0IhLqGv1K40qb1',
symbol = '1000RATSUSDT'  # Торговая пара
position_size = 0.001  # Размер позиции (в BTC)
target_percent = 2  # Процент изменения цены для закрытия позиции

# Подключение к API Bybit
session = HTTP(
    testnet=False,
    api_key='ZeV8tazdLe0VRQF2UU', 
    api_secret='bpbQwmOF7dB1N67pRGyFWb0IhLqGv1K40qb1',
)

def get_current_price():
    """Получить текущую цену"""
    ticker = session.get_tickers(category="linear", symbol=symbol)
    # return float(ticker['result']['list'][0]['lastPrice'])
    return ticker

def get_position_info():
    """Получить информацию о текущей позиции"""
    position = session.get_positions(category="linear", symbol=symbol)
    if position:
        # return float(position['result']['list'][0]['size']), float(position['result']['list'][0]['avgPrice'])
        return position
    return None

def close_position():
    """Закрыть позицию"""
    session.place_order(
        category="linear",
        symbol=symbol,
        side="Sell" if position_size > 0 else "Buy",
        orderType="Market",
        qty=abs(position_size),
        timeInForce="GTC"
    )
    print("Позиция закрыта.")

def monitor_price():
    """Мониторинг цены и закрытие позиции при достижении цели"""
    entry_price = None
    while True:
        current_price = get_current_price()
        position_size, entry_price = get_position_info()

        if entry_price is None:
            print("Позиция не найдена.")
            break

        # Рассчитываем целевые уровни
        if position_size > 0:  # Длинная позиция
            target_price = entry_price * (1 + target_percent / 100)
            if current_price >= target_price:
                print(f"Цена достигла целевого уровня: {target_price}")
                close_position()
                break
        elif position_size < 0:  # Короткая позиция
            target_price = entry_price * (1 - target_percent / 100)
            if current_price <= target_price:
                print(f"Цена достигла целевого уровня: {target_price}")
                close_position()
                break

        print(f"Текущая цена: {current_price}, Целевая цена: {target_price}")
        time.sleep(5)  # Проверяем каждые 5 секунд

if __name__ == "__main__":
    get_position_info()