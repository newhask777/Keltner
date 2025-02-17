from pybit import HTTP
import time

# Инициализация клиента Bybit API v5
session = HTTP(
    endpoint="https://api.bybit.com",  # Эндпоинт для основной торговли
    api_key="ВАШ_API_KEY",  # Ваш API ключ
    api_secret="ВАШ_API_SECRET"  # Ваш API секрет
)

# Параметры для запроса
symbol = "BTCUSDT"  # Торговая пара
base_price = 30000  # Базовая цена, относительно которой считаем процент

def get_current_price(symbol):
    # Получаем текущую цену
    ticker = session.get_tickers(category="linear", symbol=symbol)
    if ticker['retCode'] == 0 and ticker['result']['list']:
        return float(ticker['result']['list'][0]['lastPrice'])
    else:
        raise Exception("Не удалось получить текущую цену")

def calculate_price_change_percentage(current_price, base_price):
    # Рассчитываем изменение цены в процентах
    return ((current_price - base_price) / base_price) * 100

try:
    current_price = get_current_price(symbol)
    percentage_change = calculate_price_change_percentage(current_price, base_price)
    print(f"Текущая цена: {current_price}")
    print(f"Изменение цены относительно базовой: {percentage_change:.2f}%")
except Exception as e:
    print(f"Ошибка: {e}")