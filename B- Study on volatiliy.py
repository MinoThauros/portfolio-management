import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

prices_a_pandas = pd.DataFrame({
    "Blue-Stock": [8.70, 8.91, 8.71, 8.43, 8.73],
    "Orange-Stock": [10.6, 11.08, 10.71, 11.59, 12.11]
})

new_data = pd.read_csv("data\Portfolios_Formed_on_ME_monthly_EW.csv",
                       header=0, index_col=0, parse_dates=True, na_values=-99.99
                       # Header is in row 0; index_col in row 0; we wanna paser by dates
                       )


def volatility_calc(x):
    x = pd.DataFrame(x)
    # supposing that we have the prices of securities, we wanna see how much the growth fluctuates
    x = x.pct_change()
    # dataframes can be treated as normal constants/var
    # first, we demean
    deviations = x-x.mean()  # differences between the values and their mean; the spread
    squared_dev = deviations**2
    # variance=squared_dev.mean()on fait la moyenne des deviations; will not work because will do a normal math.mean(), not a statistical one
    # DataFrame.shape will return a tupple; a list whose content is immuable
    variance = squared_dev.sum()/(squared_dev.shape[0]-1)
    volatility = np.sqrt(variance)
    return volatility
    # will behave differently than the .std() because .std() computes a "sample" standard deviation thereby dividing total value by N-1 for N values


def volatility_simplified(x):
    x = pd.DataFrame(x)
    return x.std()


def time_adjust_volatility(volatility):
    n_per = float(
        input("rentrez le nombre de periodes durant le laps de temps"))
    # will be 12 if we have the monthly volatility  and we wanna have a yearly volatility
    return volatility*np.sqrt(n_per)


columns = ['Lo 10', 'Hi 10']
# based on the date structure type of DataFrames, every column has a name of type string
new_data = new_data[columns]
# will return the correpsong columns
new_data.columns = ['SmallCap', 'LargeCap']  # we modify the columns titles

# so far we've been working with % number but our formulas work best with the 1+R notation
new_data = new_data/100
# to obtain 1+R | R<=1


def adjusted_volatility(x, n_per):
    x = pd.DataFrame(x)
    volatility = x.std()
    return volatility*np.sqrt(n_per)  # monthly growth over a year => sqrt(12)


print(new_data.head())
print("volatility calc is")
print(+volatility_calc(prices_a_pandas))
print("volatility calc simplified is")
print(volatility_simplified(prices_a_pandas))
new_data.plot.line()
print(adjusted_volatility(new_data, 12))
plt.show()
# Both will be the same
