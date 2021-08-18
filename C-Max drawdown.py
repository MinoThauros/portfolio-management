import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('display.float_format', str)

new_data = pd.read_csv("data\Portfolios_Formed_on_ME_monthly_EW.csv",
                       header=0, index_col=0, parse_dates=True, na_values=-99.99
                       )

rets = new_data[['Lo 10', 'Hi 10']]
rets.columns = [['SmallCap', 'LargeCap']]
rets = rets/100  # so that we dont have %
# Year-month format;will however return the first day of the month; returns '2018-09-01', '2018-10-01',...
rets.index = pd.to_datetime(rets.index, format="%Y%m")

# let's convert the dates to period; will return '1926-08', '1926-09', '1926-10' instead
# => In this format, we can fetch return for each year doing rets[2018] for 2018
# => fetches the indexes that matches portions of the indexes for research purposes
rets.index = rets.index.to_period('M')
# rets.plot.line()
# plt.show()


# print(rets.loc["2018"])  # old way is deprecated
# rets.loc["2018"].plot.line()
# plt.show()

# let us now compute drawdown
# 1) wealth index


def wealthIndex():
    # will compute the growth of a certain amount (here, 1000$) at the rate of the fund
    temp = 1000*(1+rets["LargeCap"]).cumprod()
    # the % of growth is relatively to the precedent period
    # so to  know how much the money has grown, it's the product of all preceding periods for the period
    # including the period
    rounded_temp = temp.round(4)
    return rounded_temp

    # 2) previous peaks


def findPreviousPeaks():
    return wealthIndex().cummax()
    # keeps rising; computes only peaks


# 3) compute drawdown => wealth value as a percentage of previous peak
def drawDown():
    return (wealthIndex()-findPreviousPeaks())/findPreviousPeaks()
    # drop in value relatively to the peak itself


def maxdrawDown():
    return drawDown().min()

# let's now compute the max drawdown of recent times


def recent_maxdrawDown():
    print(drawDown()["1975":].idxmin())  # returns the index for the drawndown
    return drawDown()["1975":].min()


# II- lets optimize the workflow for small cap


def drawdownz(series: pd.Series):
    """Takes a time series of asset price.
       returns a DataFrame with columns for 
       the previous peaks, and 
       the percentage drawdown
    """
    # series contains the year-on-year growth factor

    wealth = 1000*(1+series).cumprod()
    previous_peaks = wealth.cummax()  # we keep rising
    # as a percentage of the previous peak
    drawdowns = (wealth - previous_peaks)/previous_peaks
    reslts = pd.concat([wealth, previous_peaks, drawdowns],
                       axis=1, join='inner')
    reslts.columns = [['Wealth', 'Peaks', 'Drawdowns']]
    print('maxDrawDown is: ')
    print(drawdowns.min())
    print('in year: ')
    print(drawdowns.idxmin())
    return reslts.round(4)


# print(drawdownz(rets["LargeCap"]).head())
print(drawdownz(rets["SmallCap"])[['Wealth', "Peaks"]].head())
drawdownz(rets[:'1950']["SmallCap"])[['Wealth', "Peaks"]].plot()
drawdownz(rets[:'1950']["LargeCap"])[['Wealth', "Peaks"]].plot()
plt.show()
