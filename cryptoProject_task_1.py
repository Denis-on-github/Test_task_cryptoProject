'''
Для определения собственных движений цены фьючерса ETHUSDT без влияния цены BTCUSDT можно использовать
метод множественной регрессии с фиксированными эффектами.

Для этого необходимо собрать данные о цене ETHUSDT и BTCUSDT за определенный период времени
(например, год). Затем провести регрессионный анализ, где зависимой переменной будет цена ETHUSDT,
а независимыми переменными - цена BTCUSDT и фиктивная переменная, которая будет равна 1, если
наблюдение соответствует периоду, когда цена BTCUSDT не оказывала значительного влияния на цену
ETHUSDT (например, это может быть период снижения волатильности на рынке криптовалют).

В результате анализа можно получить уравнение регрессии, в котором коэффициент при фиктивной переменной
покажет собственные движения цены ETHUSDT без влияния цены BTCUSDT.

Для подбора параметров можно использовать метод наименьших квадратов и оценить качество модели на
основе коэффициента детерминации (R-квадрат).

Выбор метода множественной регрессии с фиксированными эффектами обусловлен тем, что этот метод
позволяет учесть влияние факторов, которые не меняются во времени, на цену ETHUSDT, а также
контролировать влияние BTCUSDT на эту цену.
'''

import requests
import pandas as pd
import matplotlib.pyplot as plt

# Используем Binance API, получаем ссылки для каждой валюты за определенное кол-во дней
limit = 365
eth_url = f'https://api.binance.com/api/v3/klines?symbol=ETHUSDT&interval=1d&limit={limit}'
btc_url = f'https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit={limit}'

# Получаем данные с сайта
eth_response = requests.get(eth_url)
eth_data = eth_response.json()

btc_responce = requests.get(btc_url)
btc_data = btc_responce.json()

# Преобразовываем данные в таблицу с помощью pandas
eth_df = pd.DataFrame(eth_data, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
                                 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',
                                 'Taker buy quote asset volume', 'Ignore'])

btc_df = pd.DataFrame(btc_data, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time',
                                 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume',
                                 'Taker buy quote asset volume', 'Ignore'])

# Удаляем ненужные столбцы и переименовываем нужные
eth_df = eth_df[['Open time', 'Close']].rename(columns={'Close': 'ETHUSDT'})
btc_df = btc_df[['Open time', 'Close']].rename(columns={'Close': 'BTCUSDT'})

# Преобразовываем данные в нужный формат
eth_df['Open time'] = pd.to_datetime(eth_df['Open time'], unit='ms')
eth_df['ETHUSDT'] = eth_df['ETHUSDT'].astype(float)

btc_df['Open time'] = pd.to_datetime(btc_df['Open time'], unit='ms')
btc_df['BTCUSDT'] = btc_df['BTCUSDT'].astype(float)

# Объединяем таблицы
df = pd.merge(eth_df, btc_df, on='Open time')

# Вычисляем изменения цены Ethereum без учета изменений цены Bitcoin
eth_returns_excl_btc = df['ETHUSDT'].pct_change() - df['BTCUSDT'].pct_change()

# Строим график
plt.figure(figsize=(12, 6))
plt.plot(df['Open time'], eth_returns_excl_btc)
plt.title(f'Changes in Ethereum price (excluding Bitcoin influence) over the last {limit} days')
plt.xlabel('Date')
plt.ylabel('Returns (%)')
plt.show()
