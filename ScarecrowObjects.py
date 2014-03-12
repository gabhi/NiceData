from matplotlib import pyplot
from matplotlib.dates import DateFormatter
import csv, urllib
from datetime import date,datetime, timedelta
class ObservationSeries:

	def __init__(self,tempArray=[]):
		self.dataSet = tempArray
	
	#Returns an observation series of Observation data points. Essentially loads the series.
	def fetchDataSeries(self,ticker=None,startDate=date(2009,1,1),endDate=date(2009,10,1), interval="d"):
		#clear data set
		self.dataSet = [];
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
		for lineNum in xrange(0,len(newData)-1):
			ds,open_,high,low,close,volume,adjclose=newData[lineNum].rstrip().split(',')
			tempDate=datetime.strptime(ds,"%Y-%m-%d").date()
			#print tempDate
			self.addObservation(Observation(inDate=tempDate,inTicker=ticker,inOpen=float(open_),inHigh=float(high),inLow=float(low),inClose=float(close),inVol=float(volume),inAdjClose=float(adjclose)))

	def addObservation(self,inObservation):
		self.dataSet.append(inObservation)

	def getObservation(self,indice):
		return self.dataSet[indice]
	def getObservations(self,startIndex,endIndex):
		return self.dataSet[startIndex:endIndex]
	def getMinimumDateInSet(self):
		return self.dataSet[0].date
	#returns the index value of the date object inDate.
	#Since we have ordered data, this will be replaced with an O(1) function in the future
	def getIndiceOfDate(self,inDate):
		returnIndice = -1
		count = 0
		for observation in self.dataSet:
			if observation.date == inDate:
				returnIndice = count
			count = count + 1
		return returnIndice
	def getMaximumDateInSet(self):
		return self.dataSet[len(self.dataSet)-1].date
	def isDateRangeInSet(self,beginDateRange,endDateRange):
		return (self.getMinimumDateInSet() < beginDateRange) and (self.getMaximumDateInSet() > endDateRange)
	def getSize(self):
		return len(self.dataSet)

	def getSeriesByAttribute(self,nameOfAttr):
		returnList=[observation.getAttributeByName(nameOfAttr) for observation in self.dataSet]
		return returnList
	def plotSeries(self,param0="date",param1="close"): #plot using pyplot
		if len(self.dataSet)==0 and param1!="date": #Check to see if there is anything to plot and that y axis is NOT date
			return -1
		#otherwise plot the chosen parameter against time
		xArray=[]
		yArray=[]
		xArray = self.getSeriesByAttribute(param0)
		yArray = self.getSeriesByAttribute(param1)
		#convert to all floats
		yArray = map(float,yArray)
		#print yArray
		xRangeString = " from "+param0+"s "+xArray[0].strftime("%m-%Y")+" to "+ xArray[len(xArray)-1].strftime("%m-%Y")

		displayFig=pyplot.figure(figsize=(12,8))
		displayFig.canvas.set_window_title(self.getObservation(0).getAttributeByName("ticker")+": "+param0+" vs. "+param1)
		subPlot=displayFig.add_subplot(111,xlabel=param0,ylabel=param1,title=self.getObservation(0).getAttributeByName("ticker")+": "+param0+" vs. "+param1+xRangeString)
		subPlot.grid(True)
		#Some statistics to calculate range extension
		dateMin=date(xArray[0].year,xArray[0].month,1)
		dateMax=date(xArray[len(xArray)-1].year,xArray[len(xArray)-1].month,31)
		extensionY=(max(yArray)-min(yArray))*.1
		#print "EXTENSIONY:",extensionY
		subPlot.set_xlim(dateMin,dateMax)
		subPlot.set_ylim(float(min(yArray))-extensionY,float(max(yArray))+extensionY)
		if param0=="date":
			subPlot.plot_date(xArray,yArray)
			subPlot.xaxis.set_major_formatter(DateFormatter("%m-%Y")) #Sets format of x axis

		pyplot.show()



class Observation:
	def __init__(self,inDate="N/A",inTicker="N/A",inOpen=-1,inHigh=-1,inLow=-1,inClose=-1,inVol=-1,inAdjClose=-1):
		self.date=inDate #a date object
		self.ticker = inTicker
		self.openPrice=inOpen
		self.highPrice=inHigh
		self.lowPrice=inLow
		self.closePrice=inClose
		self.volume=inVol
		self.adjClosePrice=inAdjClose
	def getAttributeByName(self,attrName):
		if attrName=="date":
			return self.date

		elif attrName=="ticker":
			return self.ticker
		elif attrName=="open":
			return self.openPrice
		elif attrName=="high":
			return self.highPrice
		elif attrName=="low":
			return self.lowPrice
		elif attrName=="close":
			return self.closePrice
		elif attrName=="volume":
			return self.volume
		elif attrName=="adjClosePrice":
			return self.adjClosePrice
		else:
			return -1
