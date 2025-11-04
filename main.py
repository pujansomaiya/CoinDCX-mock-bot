import requests, random, time, pandas as pd

# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------
COINS = ["BTCINR", "ETHINR", "BNBINR", "XRPINR", "DOGEINR", "SOLINR"]
ENGINES = ["GPT5","Claude","Gemini","DeepSeek","Perplexity","MetaAI",
           "Mistral","Falcon","TrendAI","SentimentAI","RSI","MACD",
           "VolumeFlow","PriceAction","ChainAI"]

TRADE_AMOUNT = 100  # ₹100 per trade (mock)
TP = 0.03  # 3% take profit
SL = 0.05  # 5% stop loss
LEVERAGE = random.randint(5,10)
BALANCE = 15000  # starting mock balance in INR

# ------------------------------------------------------------
# FUNCTIONS
# ------------------------------------------------------------

def get_price(symbol):
    url = f"https://api.coindcx.com/exchange/ticker"
    try:
        data = requests.get(url, timeout=10).json()
        for coin in data:
            if coin['market'] == symbol:
                return float(coin['last_price'])
    except Exception as e:
        print("Error fetching price:", e)
    return None

def ai_votes():
    votes = []
    for e in ENGINES:
        votes.append(random.choices(["BUY","SELL","HOLD"], [0.4, 0.4, 0.2])[0])
    result = pd.Series(votes).value_counts()
    decision = result.idxmax()
    return decision, result.to_dict()

# ------------------------------------------------------------
# MAIN TRADING LOOP
# ------------------------------------------------------------
print("🔹 AI Mock Trading Bot Started 🔹")
print(f"Leverage: {LEVERAGE}x | TP: {TP*100}% | SL: {SL*100}%\n")

portfolio = []
profit_total = 0

for i in range(12):  # 12 cycles = roughly 1 hour (every 5 minutes)
    print(f"⏱️ Cycle {i+1}/12 ----------------------")

    for coin in COINS:
        price = get_price(coin)
        if not price:
            continue

        decision, votes = ai_votes()
        print(f"{coin} | Price ₹{price:.2f} | Decision: {decision} | Votes: {votes}")

        entry = price
        target = entry * (1 + TP)
        stop = entry * (1 - SL)
        result = random.choice(["TP Hit", "SL Hit", "Open"])
        pnl = 0

        if result == "TP Hit":
            pnl = TRADE_AMOUNT * TP * LEVERAGE
        elif result == "SL Hit":
            pnl = -TRADE_AMOUNT * SL * LEVERAGE

        profit_total += pnl
        BALANCE += pnl

        print(f"Result: {result} | PnL: {pnl:.2f} | Balance: ₹{BALANCE:.2f}\n")

    time.sleep(5)  # wait 5 seconds per cycle (you can change)

print("🔹 TRADING SESSION COMPLETE 🔹")
print(f"Final Balance: ₹{BALANCE:.2f}")
print(f"Total Profit/Loss: ₹{profit_total:.2f}")

