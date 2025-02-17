from pybit.unified_trading import WebSocket
import time

# Параметры
symbol = "BTCUSDT"  # Торговая пара
base_price = 30000  # Цена входа

# Функция для расчета изменения цены в процентах
def calculate_price_change_percentage(current_price, base_price):
    return ((current_price - base_price) / base_price) * 100

# Обработчик сообщений от WebSocket
def handle_message(message):
    try:
        # Извлекаем текущую цену из сообщения
        current_price = float(message['data']['lastPrice'])
        # Рассчитываем изменение цены в процентах
        percentage_change = calculate_price_change_percentage(current_price, base_price)
        print(f"Текущая цена: {current_price}")
        print(f"Изменение цены относительно базовой: {percentage_change:.2f}%")
    except KeyError as e:
        print(f"Ошибка при обработке сообщения: {e}")

# Инициализация WebSocket
ws = WebSocket(
    testnet=False,  # Используйте True, если хотите подключиться к тестовой сети
    channel_type="linear"  # Тип канала (linear для фьючерсов USDT)
)

# Подписка на канал с тикерами
ws.ticker_stream(symbol=symbol, callback=handle_message)

# Бесконечный цикл для поддержания соединения
while True:
    time.sleep(1)