import numpy as np
from Exchange import Exchange
from tqdm import tqdm


class Agent:
    def __init__(self, c, s):
        self.cash = c
        self.shares = s


class Market:
    def __init__(self, N, start_price):
        self.N = N
        self.start_price = start_price
        self.participants = []
        for _ in range(self.N):
            a = Agent(
                np.abs(np.random.normal(1000000.0, 10000.0)),
                np.abs(int(np.random.normal(10000, 100))),
            )
            self.participants += [a]
        self.prices = [self.start_price]
        self.order_to_agent = {}

    def run_trading_session(self):
        exchange = Exchange(self.prices[-1])
        last_price = self.prices[-1]
        self.order_to_agent = {}
        for n in range(self.N):
            if np.random.random() > 0.1:
                continue
            limit_price = np.abs(np.random.normal(1, 0.02) * last_price)
            limit_price = int(100 * limit_price) / 100.0
            side, size = "N", 0
            if np.random.random() < 0.5:
                side = "S"
                size = int(np.random.random() * self.participants[n].shares)
            else:
                side = "B"
                size = int(np.random.random() * self.participants[n].cash / limit_price)
            order_id = exchange.add_order(side, limit_price, size)
            self.order_to_agent[order_id] = n
            exchange.prepare_orders_match()
            exchange.match_orders()
            exchange.save_prices()
            buys_filled = exchange.buys_filled
            sells_filled = exchange.sells_filled
            for b_id, b_info in list(buys_filled.items()):
                agent = self.order_to_agent[b_id]
                for F in b_info:
                    size, price = F[0], F[1]
                    self.participants[agent].shares += size
                    self.participants[agent].cash -= price * size
            for s_id, s_info in list(sells_filled.items()):
                agent = self.order_to_agent[s_id]
                for F in s_info:
                    size, price = F[0], F[1]
                    self.participants[agent].shares -= size
                    self.participants[agent].cash += price * size
        price = (exchange.bids[-1] + exchange.asks[-1]) / 2.0
        return price

    def run_simulations(self, T):
        for _ in tqdm(range(T)):
            price = self.run_trading_session()
            self.prices += [price]
