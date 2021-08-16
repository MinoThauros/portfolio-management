import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

prices_a = np.array([8.70, 8.91, 8.71])  # 3 prices over 3 days


def dailyreturn():
    # gains=[]
    # i=0
    # while i <= len(prices_a)-2: #usiung the 1+R format
    # gain=(prices_a[i+1]/prices_a[i])-1
    # gains.append(gain*100)
    # i=i+1
    # return gains

    # laternative 2: would slicinng the arrays improve runtime complexity: no

    prices_UpShift = prices_a[1:]  # slices from 1 to the end
    # slices from the begining to ]-1 (the last one not included )
    prices_DownShift = prices_a[:-1]
    # will automatically treat the array as a vector
    return (prices_UpShift/prices_DownShift-1)


prices_a_pandas = pd.DataFrame({
    "Blue": [8.70, 8.91, 8.71, 8.43, 8.73],
    "Orange": [10.6, 11.08, 10.71, 11.59, 12.11]
})  # creates indexes for each row (ligne)
# takes in a dictionary: key:value pairs; let's slice it to manipulate the dataset
print(prices_a_pandas)


def dailyreturnPanda():
    # issue: index here will start at one
    prices_UpShift = prices_a_pandas.iloc[1:]
    # And here index will finish at 3
    prices_DownShift = prices_a_pandas.iloc[:-1]
    # return (prices_UpShift/prices_DownShift-1)=> it's either gonna return one or indeterminate (the matrix)

    # the <pandas>.values returns a purely numpy array/object; rendring the indexing issue void
    return (prices_UpShift.values/prices_DownShift-1)


def growth():
    return prices_a_pandas/prices_a_pandas.shift(1) - 1
    # this will  shift downwards; making the values "delayed"; of yesterday


def grwoth_improved():
    # data structure will remain an object with the same number of indexes
    return prices_a_pandas.pct_change().shift(-1)
    # use this one; .pct_changes() sequencially checks variation btw every row of the data set
    # Shift done in order to delete the NaN but NaN's appeared at the end instead; dataframe will keep the same number of indexes


def dataframe_cleanup(x):
    x = pd.DataFrame(x)
    return x.dropna()
    # will delete the NaN rows


returns = grwoth_improved()
returns.plot.bar()
plt.show()  # we need to tell plt  to show it
deviation = returns.std()
correct_format = returns+1
# it's the 1+R format that we need to use in order to be able to get total portfolio return
print(correct_format)
print("after cleanup")
print(dataframe_cleanup(correct_format))
# returns a product of every element; we caln also write (returns+1).prod-1
compoundedReturn = np.prod(correct_format)
# np.prod multiplies every element in the dataframe in format r+1 to get compounded returns
print(compoundedReturn)
