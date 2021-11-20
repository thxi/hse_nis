import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

from Market import Market


np.random.seed(228)

N = 100
start_price = 100.0
market = Market(N=N, start_price=start_price)
NUM_SIMULATIONS = 10000
market.run(NUM_SIMULATIONS)

prices = np.array(market.prices)
# returns = (prices[1:] / prices[:-1]) - 1
returns = np.log(prices[1:]) - np.log(prices[:-1])

plt.plot(returns)
plt.title("Stock price returns")
plt.ylabel("Ret")
plt.xlabel("time step h")
plt.show()


log_returns = [np.log(prices[i] / prices[i - 1]) for i in range(1, len(prices))]
log_returns = (log_returns - np.mean(log_returns)) / np.std(log_returns)
normq, realq = stats.probplot(log_returns, dist="norm")[0]
normq = normq[::-1]
realq = realq[::-1]


r = list(range(len(normq)))
print(len(r))
print(len(normq))
print(len(realq))
plt.plot(r, normq, label="N(0, 1)", color="black", lw=0.1)
plt.scatter(r, realq, label="Ret", color="black", s=0.1)
plt.yscale("log")
plt.ylim((10 ** (-3), 10))
plt.ylabel("P > Ret(|Ret|)")
plt.xlabel("|Ret|")
plt.xlim((-0.05, 5100))
labels = ["$10^{-1}$", "0", "$10^1$"]
plt.xticks([0, 2500, 5000], labels)
labels = ["$10^{-4}$", "$10^{-3}$", "$10^{-2}$", "$10^{-1}$", "$10^{0}$"]
plt.yticks([1e-3, 10 ** (-2), 10 ** (-1.1), 10 ** (-0.1), 5], labels)
plt.legend()
plt.title("Normal Q-Q plot")
plt.show()
