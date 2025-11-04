import streamlit as st
import pandas as pd

st.title("CoinDCX AI Mock Trading Dashboard")

logs = pd.read_csv("trades.csv") if "trades.csv" else pd.DataFrame(columns=["Time","Action","Price","Profit"])
st.dataframe(logs)

