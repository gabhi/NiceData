import csv, urllib
from datetime import datetime
from ScarecrowObjects import Observation,ObservationSeries
#Contains
class Scarecrow:
	def __init__(self):
		self.currentSeries = None
		
	def initialize(self):
		self.currentSeries=self.fetchDataSeries(ticker="GOOG")
		print "Loaded data"

	#Returns an observation series of Observation data points
	def fetchDataSeries(self,ticker=None,startDate=datetime(2009,1,1),endDate=datetime(2009,10,1), interval="d"):
		#We check to see if data is not already stored here. If not, we pull from Yahoo
		if(ticker == None):
			print "ERROR: NO TICKER SPECIFIED"
			return None
		#Construct URL
		base="http://ichart.yahoo.com/table.csv?s="
		fromDateString="&a="+str(startDate.month-1)+"&b="+str(startDate.day)+"&c="+str(startDate.year)
		toDateString="&d="+str(endDate.month-1)+"&e="+str(endDate.day)+"&f="+str(endDate.year)
		intervalString="&g="+interval
		staticString="&ignore=.csv"
		endUrl=base+ticker+fromDateString+toDateString+intervalString+staticString

		newData=urllib.urlopen(endUrl).readlines()
		newData.reverse() #Want earliest data first
		newSeries = ObservationSeries()
		for lineNum in xrange(0,len(newData)-1):
			ds,open_,high,low,close,volume,adjclose=newData[lineNum].rstrip().split(',')
			tempDateTimeObject=datetime.strptime(ds,"%Y-%m-%d")
			newSeries.addObservation(Observation(inDate=tempDateTimeObject,inTicker=ticker,inOpen=float(open_),inHigh=float(high),inLow=float(low),inClose=float(close),inVol=float(volume),inAdjClose=float(adjclose)))
		return newSeries
	def saveCurrentDataSet(self):
		print "TODO"
	def getCurrentDataSet(self):
		return self.currentSeries
if __name__ == "__main__":

	newAlgo = Scarecrow()
	newAlgo.initialize()
	print "Successfully grabbed "+str(newAlgo.getCurrentDataSet().getSize())+" observations."
	print "Observation 1:" + str(newAlgo.getCurrentDataSet().getObservation(0).highPrice)
	print "MOVING AVG: "+str(newAlgo.getCurrentDataSet().getMovingAvg(startDate=datetime(2009,5,1)))
	print "ROC for current to day before: "+str(newAlgo.getCurrentDataSet().getROC(n=1,startDate=datetime.today()))
	newAlgo.getCurrentDataSet().plotSeries()