import pandas as pd
import talib as ta

# Пример данных (замените на реальные данные)
data = pd.read_csv('your_data.csv')
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Параметры канала Кельтнера
period = 20
multiplier = 1

# Расчет скользящей средней (EMA)
data['EMA'] = ta.EMA(data['Close'], timeperiod=period)

# Расчет ATR (Average True Range) для волатильности
data['ATR'] = ta.ATR(data['High'], data['Low'], data['Close'], timeperiod=period)

# Расчет верхней и нижней границ канала Кельтнера
data['Upper_KC'] = data['EMA'] + (data['ATR'] * multiplier)
data['Lower_KC'] = data['EMA'] - (data['ATR'] * multiplier)

# Инициализация переменных для отслеживания позиции
position = None  # 'long', 'short' или None
entry_price = 0
exit_price = 0

# Логика торговли
for i in range(1, len(data)):
    # Проверка на вход в длинную позицию (пробой верхней границы)
    if data['Close'][i] > data['Upper_KC'][i-1] and position != 'long':
        if position == 'short':
            # Выход из короткой позиции
            exit_price = data['Close'][i]
            print(f"Exit Short at {exit_price}")
        # Вход в длинную позицию
        position = 'long'
        entry_price = data['Close'][i]
        print(f"Enter Long at {entry_price}")

    # Проверка на вход в короткую позицию (пробой нижней границы)
    elif data['Close'][i] < data['Lower_KC'][i-1] and position != 'short':
        if position == 'long':
            # Выход из длинной позиции
            exit_price = data['Close'][i]
            print(f"Exit Long at {exit_price}")
        # Вход в короткую позицию
        position = 'short'
        entry_price = data['Close'][i]
        print(f"Enter Short at {entry_price}")

    # Выход из позиции при достижении противоположной границы
    elif position == 'long' and data['Close'][i] < data['EMA'][i]:
        exit_price = data['Close'][i]
        print(f"Exit Long at {exit_price}")
        position = None
    elif position == 'short' and data['Close'][i] > data['EMA'][i]:
        exit_price = data['Close'][i]
        print(f"Exit Short at {exit_price}")
        position = None