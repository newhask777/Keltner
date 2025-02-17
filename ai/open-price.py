from pybit import HTTP

# Инициализация клиента Bybit
session = HTTP(
    endpoint="https://api.bybit.com",  # Используйте https://api-testnet.bybit.com для тестовой сети
    api_key="ВАШ_API_KEY",
    api_secret="ВАШ_API_SECRET"
)

# Получение информации о позициях
symbol = "BTCUSDT"  # Укажите нужный символ
response = session.get_positions(
    category="linear",  # Используйте "linear" для линейных фьючерсов, "inverse" для обратных фьючерсов, "spot" для спота
    symbol=symbol
)

# Проверка наличия позиций
if response['retCode'] == 0 and len(response['result']['list']) > 0:
    position = response['result']['list'][0]  # Берем первую позицию из списка
    entry_price = float(position['avgPrice'])  # Цена входа
    print(f"Цена входа в позицию {symbol}: {entry_price}")
else:
    print(f"Позиции по символу {symbol} не найдены или произошла ошибка: {response['retMsg']}")