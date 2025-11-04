import requests, time

CAPITAL = 1000
POSITION = None
ENTRY_PRICE = 0
PROFIT = 0

def get_price(symbol="BTCUSDT"):
    data = requests.get("https://api.coindcx.com/exchange/ticker").json()
    for d in data:
        if d['market'] == symbol:
            return float(d['last_price'])
    return None

def trade_logic():
    global POSITION, ENTRY_PRICE, PROFIT
    price = get_price()
    if not POSITION:
        POSITION = "BUY"
        ENTRY_PRICE = price
        print(f"Opened BUY at {price}")
    elif POSITION == "BUY" and price >= ENTRY_PRICE * 1.03:
        PROFIT += (price - ENTRY_PRICE)
        POSITION = None
        print(f"Booked profit at {price}")
    elif POSITION == "BUY" and price <= ENTRY_PRICE * 0.95:
        PROFIT -= (ENTRY_PRICE - price)
        POSITION = None
        print(f"Stopped out at {price}")
    print(f"Total Profit: {PROFIT:.2f}")

while True:
    trade_logic()
    time.sleep(10)

