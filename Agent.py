import numpy as np

# can send
#  market order
#  limit order
# the class should have
# why do we need this?
# why not only create the market?

m = 10
delta = 1 / m

# algorithm 1: spread based strategy
class Agent:
    def __init__(self, b, a, a_1, inventory=0, cash=0):
        self.b = b
        self.a = a
        self.inventory = inventory
        self.cash = cash

        self.a_t = a_1

    def make_action(self, p_t, p_next):
        # current_price = p_t
        if p_t < self.a_t:
            old = self.a_t
            self.a_t = p_t
            print(f"updating {old=} {self.a_t=}")
        elif p_t > self.a_t + self.b:
            old = self.a_t
            self.a_t = p_t - self.b
            print(f"updating {old=} {self.a_t=}")
        else:
            print(f"not updating {self.a_t=}")
            self.a_t = self.a_t

        # submit 2 limit orders
        # should go through discretization range
        if p_next > self.a_t + self.b:
            price_start = self.a_t + self.b
            print(price_start, self.a_t, self.b)
            price_end = p_next
            prices = np.arange(price_start, price_end + delta, delta)
            print("selling", prices)
            for p in prices:
                self.inventory -= self.a
                self.cash += p * self.a
        elif p_next < self.a_t:
            price_start = p_next
            price_end = self.a_t
            prices = np.arange(price_start, price_end + delta, delta)
            print("buying", prices)
            for p in prices:
                self.inventory += self.a
                self.cash -= p * self.a
