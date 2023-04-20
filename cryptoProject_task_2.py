import threading
import time
from binance.client import Client

# Подставьте свои ключи API сюда
API_KEY = 'put here your API key' # ключ для доступа к API Binance
API_SECRET = 'and here API secret'# секретный ключ

client = Client(API_KEY, API_SECRET)

# Получаем актуальную цену фьючерса ETHUSDT
def get_eth_price():
    price = client.futures_symbol_ticker(symbol='ETHUSDT')
    return float(price['price'])

# Определяем собственные движения цены ETH за последние 60 минут
def get_eth_movement():
    klines = client.futures_klines(symbol='ETHUSDT', interval=Client.KLINE_INTERVAL_1HOUR, limit=60)
    prices = [float(kline[4]) for kline in klines]
    result = (prices[-1] - prices[0]) / prices[0]
    for price in prices[1:]:
        result -= (price - prices[0]) / prices[0]
    return result

# Мониторим изменения цены и выводим сообщения в консоль
def monitor_eth_price():
    last_price = get_eth_price()
    while True:
        current_price = get_eth_price()
        percent_change = abs(current_price - last_price) / last_price * 100
        if percent_change >= 1:
            eth_returns = get_eth_movement()
            print(f'ETH price has changed by {percent_change:.2f}% in the last 60 minutes, with own returns of {eth_returns:.2f}%')
            last_price = current_price
        # Ожидание 10 секунд перед повторным чтением цены
        time.sleep(10)

# Запускаем отдельный поток для мониторинга изменений цены и вывода сообщений в консоль
price_thread = threading.Thread(target=monitor_eth_price)
price_thread.start()
