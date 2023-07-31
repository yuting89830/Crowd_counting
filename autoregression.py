# -*- coding: utf-8 -*-
"""ARModelTimeSeries.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1glpkeoau5LgLnFjYM6A4H9yHHtk5yGM_
"""

from pandas import read_csv
from datetime import datetime
from pandas import DataFrame
from pandas import concat
from matplotlib import pyplot
from sklearn.metrics import mean_squared_error
url = 'crowd_change1.csv'
#df1 = pd.read_csv(url)
# series = read_csv(url, header=0, index_col=0, parse_dates=True, squeeze=True)
series = read_csv(url, header=0, index_col=0, parse_dates=True)
series.head()
print(series)

from pandas import read_csv
from matplotlib import pyplot
from pandas.plotting import lag_plot
series = read_csv(url, header=0, index_col=0)
lag_plot(series)
pyplot.show()

from pandas import read_csv
from pandas import DataFrame
from pandas import concat
from matplotlib import pyplot
series = read_csv(url, header=0, index_col=0)
values = DataFrame(series.values)
dataframe = concat([values.shift(1), values], axis=1)
dataframe.columns = ['t-1', 't+1']
result = dataframe.corr()
print(result)

from pandas import read_csv
from matplotlib import pyplot
from pandas.plotting import autocorrelation_plot
series = read_csv(url, header=0, index_col=0)
autocorrelation_plot(series)
pyplot.show()

from pandas import read_csv
from matplotlib import pyplot
from statsmodels.graphics.tsaplots import plot_acf
series = read_csv(url, header=0, index_col=0)
plot_acf(series, lags=1900)
pyplot.show()

# split dataset
X = series.values
train, test = X[1:len(X)-48], X[len(X)-48:]

from statsmodels.tsa.ar_model import AutoReg

from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import mean_squared_error
from math import sqrt
# train autoregression
model = AutoReg(train, lags=1500)
model_fit = model.fit()
print('Coefficients: %s' % model_fit.params)

# make predictions
predictions = model_fit.predict(start=len(train), end=len(train)+len(test)-1, dynamic=False)
for i in range(len(predictions)):
	print('predicted=%f, expected=%f' % (predictions[i], test[i]))
rmse = sqrt(mean_squared_error(test, predictions))
print('Test RMSE: %.3f' % rmse)

# plot results
pyplot.plot(test)
pyplot.plot(predictions, color='red')
pyplot.show()