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
