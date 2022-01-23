import numpy as np

m = 100
delta = 1 / m


class Agent:
    def __init__(self, b, alpha, a_1, inventory=0, cash=0):
        # strategy S(b)
        self.b = b  # spread
        self.alpha = alpha  # liquidity density
        self.inventory = inventory
        self.cash = cash

        self.a_t = a_1

    def value(self, p_current):
        return self.cash + p_current * self.inventory

    def limit_order(self, p_current, p_next):
        # current_price = p_t
        if p_current < self.a_t:
            old = self.a_t
            self.a_t = p_current
            # print(f"{self.b=} updating {old=} {self.a_t=}")
        elif p_current > self.a_t + self.b:
            old = self.a_t
            self.a_t = p_current - self.b
            # print(f"{self.b=} updating {old=} {self.a_t=}")
        else:
            # print(f"{self.b=} not updating {self.a_t=}")
            self.a_t = self.a_t

        # submit limit order
        # should go through discretization range
        if p_next > self.a_t + self.b:
            price_start = self.a_t + self.b
            # print(price_start, self.a_t, self.b)
            price_end = p_next
            prices = np.arange(price_start, price_end + delta, delta)
            # print(f"{self.b=} selling", prices)
            for p in prices:
                self.inventory -= self.alpha
                self.cash += p * self.alpha
        elif p_next < self.a_t:
            price_start = p_next
            price_end = self.a_t
            prices = np.arange(price_start, price_end + delta, delta)
            # print(f"{self.b=} buying", prices)
            for p in prices:
                self.inventory += self.alpha
                self.cash -= p * self.alpha
