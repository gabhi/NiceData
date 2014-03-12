from datetime import timedelta, date
from ScarecrowObjects import Observation,ObservationSeries
#Contains
class Scarecrow:
	def __init__(self,tickerIn=None,startIn=None,endIn=None,intervalIn=None):
		self.currentSeries = ObservationSeries()
		if (tickerIn and startIn and endIn):
			if intervalIn:
				self.currentSeries.fetchDataSeries(ticker=tickerIn,startDate=startIn,endDate=endIn,interval=intervalIn)
			else:
				self.currentSeries.fetchDataSeries(ticker=tickerIn,startDate=startIn,endDate=endIn)
		else:
			print "WARNING: You still need to load this instance with a data series"


	#Dynamically instantiate a trading strategy and backtest with settings from settingsDict
	def backtestOnCurrentSeries(self,algoName,settingsDict):
		#TODO
		return
	def saveCurrentDataSet(self):
		#TODO
		return
	def getCurrentDataSet(self):
		return self.currentSeries

	#Calculates the moving average of a range in the current dataset
	def getMovingAvg(self,startDate,timeRange): #range is currently only implemented in # of observaitons
		endIndice=self.currentSeries.getIndiceOfDate(startDate)
		startIndice = endIndice-int(timeRange)

		if startIndice<0:
			print "Date range is not in set"
			print startIndice
			return -1
		avg = 0
		for observation in self.currentSeries.getObservations(endIndice-int(timeRange),endIndice):
			avg = avg + observation.closePrice
		avg = avg/timeRange
		return avg

	#Gets the ratio of the price at startDate to that of the price n observations earlier
	def getROC(self,n,startDate):
		endIndice=self.currentSeries.getIndiceOfDate(startDate)
		startIndice=endIndice-int(n)
		if startIndice < 0:
			return -1
		endClosePrice = self.currentSeries.getObservation(endIndice).closePrice
		startClosePrice = self.currentSeries.getObservation(startIndice).closePrice
		return float(endClosePrice/startClosePrice)

if __name__ == "__main__":
	yesterday = date.today() - timedelta(days=1)
	newAlgo = Scarecrow("GOOG",date(2009,1,1),yesterday)
	print "Created a Scarecrow"
	print "SIZE: "+str(newAlgo.getCurrentDataSet().getSize())+" observations."
	print "MOVING AVG: "+str(newAlgo.getMovingAvg(startDate=date(2014,2,5),timeRange=50.0))
	print "ROC(Yesterday,Yesterday-1):"+str(newAlgo.getROC(n=1,startDate=yesterday))
	newAlgo.getCurrentDataSet().plotSeries()