from dotenv import load_dotenv
import os
import finnhub
import pandas as pd

load_dotenv()  # take environment variables from .env.

API_KEY = os.getenv("API_KEY")
print(f"using {API_KEY=} for api")

# Setup client
finnhub_client = finnhub.Client(api_key=API_KEY)

from_date = pd.to_datetime("2022-01-01")
to_date = pd.to_datetime("2022-01-04")

print(f"loading date {from_date=} {to_date=}")

# Stock candles
res = finnhub_client.stock_candles(
    "AAPL", "D", int(from_date.timestamp()), int(to_date.timestamp())
)
print(res)
