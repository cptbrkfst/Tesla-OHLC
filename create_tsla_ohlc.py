import datetime as dt
import matplotlib.dates as mdates
from matplotlib.finance import candlestick_ohlc
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader as web

style.use('ggplot')  # Define style ggplot


def to_csv():
    """Store Tesla ticker as csv file"""
    start = dt.datetime(2000, 1, 1)  # Define start/end dates
    end = dt.datetime(2016, 12, 31)

    df_tsla = web.DataReader('TSLA', 'yahoo', start, end)
    df_tsla.to_csv('tsla.csv')  # Store Tesla values as csv

to_csv()

# Set data frame
df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)
df['100ma'] = df['Adj Close'].rolling(window=100, min_periods=0).mean()  # Define 100 Moving Average

df_ohlc = df['Adj Close'].resample('10D').ohlc()  # Resample ohcl data for 10 day averages
df_volume = df['Volume'].resample('10D').sum()  # Resample volume data for df_ohlc to remove granularity

df_ohlc.reset_index(inplace=True)  # reset index w/o creating new object
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)  # Set df dates to mdates

ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)  # Map subplots for graph
ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
ax1.xaxis_date()  # Treat x-axis as dates

candlestick_ohlc(ax1, df_ohlc.values, width=5, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
plt.show()
