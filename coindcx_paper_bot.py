import requests, time, random, datetime, sqlite3

# ===== Mock Trading Config =====
coins = ["BTCINR", "ETHINR", "BNBINR", "XRPINR", "SOLINR", "TRXINR"]
leverage_range = (5, 10)
profit_target = 0.03   # 3%
stop_loss = 0.05       # 5%
check_interval = 30    # seconds between price checks

# ===== Database Setup =====
conn = sqlite3.connect("coindcx_paper.db", check_same_thread=False)
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS trades(
id INTEGER PRIMARY KEY AUTOINCREMENT,
symbol TEXT,
side TEXT,
entry REAL,
exit REAL,
pnl REAL,
timestamp TEXT
)""")
conn.commit()

# ===== Helper: fetch current INR prices =====
def get_price(symbol):
    try:
        url = f"https://public.coindcx.com/market_data/trade_history?pair={symbol}"
        data = requests.get(url, timeout=10).json()
        return float(data[0]["p"]) if data else None
    except Exception as e:
        print(f"[ERROR] {symbol} price fetch failed: {e}")
        return None

# ===== Mock trading logic =====
def mock_trade():
    balance = 10000  # mock INR balance
    open_trades = []

    while True:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"\n[{now}] Checking markets...")

        for symbol in coins:
            price = get_price(symbol)
            if not price:
                continue

            if random.random() < 0.1:  # ~10% chance to enter a trade
                side = random.choice(["LONG", "SHORT"])
                lev = random.randint(*leverage_range)
                entry = price
                tp = entry * (1 + profit_target) if side == "LONG" else entry * (1 - profit_target)
                sl = entry * (1 - stop_loss) if side == "LONG" else entry * (1 + stop_loss)
                open_trades.append((symbol, side, entry, tp, sl, lev))
                print(f"OPEN {side} {symbol} | Entry ₹{entry:.2f} | TP ₹{tp:.2f} | SL ₹{sl:.2f}")

        # Check open trades for closure
        for trade in open_trades[:]:
            symbol, side, entry, tp, sl, lev = trade
            price = get_price(symbol)
            if not price:
                continue

            if side == "LONG" and (price >= tp or price <= sl):
                pnl = (price - entry) * lev
                result = "TP" if price >= tp else "SL"
            elif side == "SHORT" and (price <= tp or price >= sl):
                pnl = (entry - price) * lev
                result = "TP" if price <= tp else "SL"
            else:
                continue

            cur.execute("INSERT INTO trades (symbol, side, entry, exit, pnl, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                        (symbol, side, entry, price, pnl, datetime.datetime.now().isoformat()))
            conn.commit()
            print(f"CLOSE {symbol} | Exit ₹{price:.2f} | {result} | PnL ₹{pnl:.2f}")
            open_trades.remove(trade)

        time.sleep(check_interval)

# ===== Run bot =====
if __name__ == "__main__":
    print("Starting CoinDCX Mock Trading Bot 🚀")
    mock_trade()
