from matplotlib import pyplot
from matplotlib.dates import DateFormatter
from datetime import datetime, timedelta
class ObservationSeries:
	def __init__(self,tempArray=[]):
		print "Initialized a Set"
		self.dataSet = tempArray
	def addObservation(self,inObservation):
		self.dataSet.append(inObservation)
	def getObservation(self,indice):
		return self.dataSet[indice]
	def getMinimumDateInSet(self):
		return self.dataSet[0].date

	#returns the index value of the dateTime object inDate
	def getIndiceOfDate(self,inDate):
		returnIndice = -1
		count = 0
		for observation in self.dataSet:
			if observation.date == inDate:
				print "DATE MATCH"
				returnIndice = count
			count = count + 1
		return returnIndice
	def getMaximumDateInSet(self):
		return self.dataSet[len(self.dataSet)-1].date
	def isDateRangeInSet(self,beginDateRange,endDateRange):
		return (self.getMinimumDateInSet() < beginDateRange) and (self.getMaximumDateInSet() > endDateRange)
	def getSize(self):
		return len(self.dataSet)

	#Gets the ratio of the price at startDate to that of the price n observations earlier
	def getROC(self,n,startDate):
		endIndice=self.getIndiceOfDate(startDate)
		startIndice=endIndice-int(n)
		if startIndice < 0:
			return -1
		return float(self.dataSet[endIndice].closePrice)/self.dataSet[startIndice].closePrice

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
		print yArray
		xRangeString = " from "+param0+"s "+xArray[0].strftime("%m-%Y")+" to "+ xArray[len(xArray)-1].strftime("%m-%Y")

		displayFig=pyplot.figure(figsize=(12,8))
		displayFig.canvas.set_window_title(self.getObservation(0).getAttributeByName("ticker")+": "+param0+" vs. "+param1)
		subPlot=displayFig.add_subplot(111,xlabel=param0,ylabel=param1,title=self.getObservation(0).getAttributeByName("ticker")+": "+param0+" vs. "+param1+xRangeString)
		subPlot.grid(True)
		#Some statistics to calculate range extension
		dateMin=datetime(xArray[0].year,xArray[0].month,1)
		dateMax=datetime(xArray[len(xArray)-1].year,xArray[len(xArray)-1].month,31)
		extensionY=(max(yArray)-min(yArray))*.1
		print "EXTENSIONY:",extensionY
		subPlot.set_xlim(dateMin,dateMax)
		subPlot.set_ylim(float(min(yArray))-extensionY,float(max(yArray))+extensionY)
		if param0=="date":
			subPlot.plot_date(xArray,yArray)
			subPlot.xaxis.set_major_formatter(DateFormatter("%m-%Y")) #Sets format of x axis

		pyplot.show()
	def getMovingAvg(self,startDate,timeRange=50.0): #range is currently only implemented in # of observaitons
		endIndice=self.getIndiceOfDate(startDate)
		print "END INDICE: "+str(endIndice)
		print "START DATE FROM END INDICE: "+str(self.dataSet[endIndice].date)
		startIndice = endIndice-int(timeRange)
		print "START INDICE: "+str(startIndice)
		if startIndice<0:
			print "Date range is not in set"
			return -1
		print "Date and range valid - calculating moving avg"
		avg = 0
		for observation in self.dataSet[endIndice-int(timeRange):endIndice]:
			avg = avg + observation.closePrice
			#print "SUM NOW: "+str(avg)
		avg = avg/timeRange
		return avg
		#for closePrice in self.dataSet[len(,:]


class Observation:
	def __init__(self,inDate="N/A",inTicker="N/A",inOpen=-1,inHigh=-1,inLow=-1,inClose=-1,inVol=-1,inAdjClose=-1):
		self.date=inDate #a datetime object
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
