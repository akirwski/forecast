import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class HoltWinterForecast:

    def __init__(self, file, period, column_num):
        self.df =  pd.read_csv(file)
        self.df = self.df.replace(',','', regex=True)
        self.df.iloc[:, column_num] = pd.to_numeric(self.df.iloc[:, column_num])
        self.dfForecast = pd.DataFrame()
        self.period = period
        self.column_num = column_num
        self.df.head()

    def calcForecast(self, alpha, beta, gamma):
        numTotal = len(self.df.index)
        seasonalSeries = []
        baseSeries = []
        trendSeries = [0]
        forecastSeries = [0]

        ##calculate Average
        total = 0;
        for i in range(self.period):
            total = total + int(self.df.iloc[i, self.column_num])

        average = total / self.period

        ##get Seasonality for the first weekly, montly, or seasonaly period
        for i in range(self.period):
            seasonalSeries.append(int(self.df.iloc[i, self.column_num]) - average)

        ##calculate last base and trend
        last_base = int(self.df.iloc[self.period-1, self.column_num]) - seasonalSeries[self.period-1]
        baseSeries.append(last_base)

        #keep actual sales in list
        actualSales = self.df.iloc[self.period-1:, self.column_num]

        #calculate seasonality
        for n in range(numTotal-self.period):
              firstBase = alpha*(float(actualSales[self.period + n]) - seasonalSeries[n])+(1-alpha)*(baseSeries[n]+trendSeries[n])
              baseSeries.append(firstBase)
              firstTrend = beta*(baseSeries[n+1] - baseSeries[n]) + (1-beta)*(trendSeries[n])
              trendSeries.append(firstTrend)
              firstSeasonal = gamma*(float(actualSales[self.period + n]) - firstBase) +(1-gamma)*seasonalSeries[n]
              seasonalSeries.append(firstSeasonal)

        #forecast from actual sales
        for n in range(numTotal-self.period):
            value = baseSeries[n] + trendSeries[n] + seasonalSeries[n]
            forecastSeries.append(value)

        #insert results in the new dataframe which will be used for predicting future values
        data = {'Sales': self.df.iloc[self.period-1 :, self.column_num], 'Base' : baseSeries, 'Trend' : trendSeries, 'Seasonal' : seasonalSeries[self.period-1:], 'Forecast': forecastSeries}
        self.dfForecast = pd.DataFrame(data)


    def predict(self, x):
        #Formula to predict future values: Y(t+n) = Et + nTt + S(t+n-p)
        numTotal = len(self.df.index)
        finalBase = self.dfForecast.iloc[numTotal-self.period, 1]
        finalTrend = self.dfForecast.iloc[numTotal-self.period, 2]
        times = numTotal / self.period
        forecastAnswer = finalBase + finalTrend*(x-numTotal)+ self.dfForecast.iloc[int((self.period * (times- 1)) + 1 - self.period), 3]
        return forecastAnswer


    def ME_MAD(self):
        #calculate Mean Error and Mean Absolute Deviation (which shows the quality of forecasting)
        num = len(self.dfForecast.index)
        sum = 0
        abssum = 0
        for i in range(1,num):
            a = float(self.dfForecast.iloc[i, 0])
            b = float(self.dfForecast.iloc[i, 4])
            sum += (a-b)
            abssum += abs(a-b)

        me = sum / num
        mad = abssum / num
        return (me, mad)

    def showGraph(self, label1, label2):
      #label1 should indicate actual sales or somthing
      #label2 shoule indicate the values that you predicted
      ax = plt.subplots()
      ax = holt.df.iloc[:, 3].plot(label=label1)
      ax = holt.dfForecast.iloc[:, 4].plot(label=label2)
      plt.legend(loc='best')
      plt.xlabel('Time Series')
      if self.period == 52: t = "Weekly Report"
      elif self.period == 12: t = "Monthly Report"
      elif self.period == 4: t = "Seasonaly Report"
      else: t = "Report"
      plt.title(t)
      plt.show()

"""
##Test Code
#initilize the class with your data file, a number of period, a index of the column(where actual sales are stored)
holt = HoltWinterForecast('holtwinter.csv', 52, 3)

#input alpha, beta, gamma
holt.calcForecast(0.4, 0.4, 0.4)

#show original data and data with forecast
holt.df.head()
holt.dfForecast.head()

#predict with a specific time values  157 = (52 * 3) + 1  = three years and one week
print(holt.predict(157))

#quality of forecast
quality = holt.ME_MAD()
print("ME: {}, MAD: {}".format(quality[0], quality[1]))

#make a graph
holt.showGraph("Actual Sales", "Forecast")

"""
