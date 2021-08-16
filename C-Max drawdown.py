import pandas as pd
import numpy as np

new_data= pd.read_csv("D:\Development\Portfolio management\data\Portfolios_Formed_on_ME_monthly_EW.csv",
header=0, index_col=0, parse_dates=True, na_values=-99.99
)



print(new_data)