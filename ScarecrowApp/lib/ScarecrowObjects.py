from pylab import *

from matplotlib import pyplot
from matplotlib.dates import DateFormatter
import urllib
from datetime import date,datetime
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import calendar
import cStringIO
#debugging tools
import logging
logger = logging.getLogger(__name__)
from ScarecrowApp.models import Observation
import pandas
class ObservationSeries:

	def __init__(self,tempArray=[]):
		self.dataSet = tempArray
	
	#Returns an observation series of Observation data points. Essentially loads the series.
	def fetchDataSeries(self,ticker=None,startDate=date(2009,1,1),endDate=date(2009,10,1), interval="d"):
		#clear data set
		self.dataSet = [];
		#We check to see if each data is not already stored here. If not, we pull from Yahoo
		#We do not take into account holidays (we will pull if there is a holiday discrepancy)
		numBusinessDays = len(pandas.bdate_range(startDate,endDate))
		possibleDataSet = Observation.objects.filter(observationDate__gte=startDate,observationDate__lte=endDate,ticker=ticker)
		#if the number of business days = the amount of data we have, use our data
		print "POSSIBLE DATES: " + str(possibleDataSet.count())
		print "BUSINESS DAYS: " + str(numBusinessDays)
		if possibleDataSet.count() == numBusinessDays:
			print "Necessary data already exists"
			for retrievedObs in possibleDataSet:
				
				newSObs = SObservation(inDate=retrievedObs.observationDate,inTicker=retrievedObs.ticker,inOpen=retrievedObs.open,inHigh=retrievedObs.high,inLow=retrievedObs.low,inClose=retrievedObs.close,inVol=retrievedObs.vol,inAdjClose=retrievedObs.adjClose)
				self.addObservation(newSObs)
			return 

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
		logger.debug(endUrl)
		newData=urllib.urlopen(endUrl).readlines()
		newData.reverse() #Want earliest data first
		for lineNum in xrange(0,len(newData)-1):
			ds,open_,high,low,close,volume,adjclose=newData[lineNum].rstrip().split(',')
			tempDate=datetime.strptime(ds,"%Y-%m-%d").date()
			#print tempDate
			newSObs = SObservation(inDate=tempDate,inTicker=ticker,inOpen=float(open_),inHigh=float(high),inLow=float(low),inClose=float(close),inVol=float(volume),inAdjClose=float(adjclose))
			self.addObservation(newSObs)
			#Check if newObs exists, if not, create it
			if Observation.objects.filter(observationDate=newSObs.date,ticker=newSObs.ticker).exists() == False:
				#Create it
				print "Does not exist, create it"
				newObs = Observation()
				newObs.created = datetime.today()
				newObs.observationDate = newSObs.getAttributeByName("date")
				newObs.ticker = newSObs.getAttributeByName("ticker")
				newObs.open = newSObs.getAttributeByName("open")
				newObs.high = newSObs.getAttributeByName("high")
				newObs.low = newSObs.getAttributeByName("low")
				newObs.close = newSObs.getAttributeByName("close")
				newObs.vol = newSObs.getAttributeByName("volume")
				newObs.adjClose = newSObs.getAttributeByName("adjClosePrice")
				newObs.save()
			else:
				print "Item already exists, do not create"


			#We save the data in our local database here
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
		#style.use('ggplot') #using mpltools to make nice plots
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
		xRangeString = " from " + param0.capitalize() + "s " + xArray[0].strftime("%m-%Y")+" to "+ xArray[len(xArray)-1].strftime("%m-%Y")

		displayFig=pyplot.figure(figsize=(10,6.67)) #12,8
		displayFig.canvas.set_window_title(self.getObservation(0).getAttributeByName("ticker")+": "+param0.capitalize()+" vs. "+param1.capitalize())
		subPlot=displayFig.add_subplot(111,xlabel=param0.capitalize(),ylabel=param1.capitalize(),title=self.getObservation(0).getAttributeByName("ticker")+": " + param0.capitalize() + " vs. " + param1.capitalize() + xRangeString)
		subPlot.grid(False)
		#Some statistics to calculate range extension
		dateMin=date(xArray[0].year,xArray[0].month,1)
		dateMax=date(xArray[len(xArray)-1].year,xArray[len(xArray)-1].month,31)
		extensionY=(max(yArray)-min(yArray))*.1
		#print "EXTENSIONY:",extensionY
		subPlot.set_xlim(dateMin,dateMax)
		subPlot.set_ylim(float(min(yArray))-extensionY,float(max(yArray))+extensionY)
		
		if param0=="date":
			#Give the user a choice of line style in the future
			subPlot.plot_date(xArray,yArray,'-')
			subPlot.xaxis.set_major_formatter(DateFormatter("%m-%Y")) #Sets format of x axis
		#Used to show plot
		savefigure = pyplot.gcf()
		#pyplot.show() 
		# uncoment above to show plot on gui
		#Used to save plot
		#pathForChart = "charts/" + date.today().strftime("%d-%m-%y") + "/" + self.getObservation(0).getAttributeByName("ticker") + "/" + param0 + "vs" + param1 + "_" + xArray[0].strftime("%m-%Y") + "_" + xArray[len(xArray)-1].strftime("%m-%Y") + ".png"
		#We won't save the figure now
		#pathForChart = "tempImg.png"
		#savefigure.savefig(pathForChart, bbox_inches='tight')
		
		#NEW FOR DJANGO - return the canvas instead
		canvas = FigureCanvas(savefigure)
		return canvas

	#Courtesy of Bicubic of messymind.net
	def rstyle(self,ax): 
	    """Styles an axes to appear like ggplot2
	    Must be called after all plot and axis manipulation operations have been carried out (needs to know final tick spacing)
	    """
	    #set the style of the major and minor grid lines, filled blocks
	    ax.grid(True, 'major', color='w', linestyle='-', linewidth=1.4)
	    ax.grid(True, 'minor', color='0.92', linestyle='-', linewidth=0.7)
	    ax.patch.set_facecolor('0.85')
	    ax.set_axisbelow(True)
	    
	    #set minor tick spacing to 1/2 of the major ticks
	    ax.xaxis.set_minor_locator(MultipleLocator( (plt.xticks()[0][1]-plt.xticks()[0][0]) / 2.0 ))
	    ax.yaxis.set_minor_locator(MultipleLocator( (plt.yticks()[0][1]-plt.yticks()[0][0]) / 2.0 ))
	    
	    #remove axis border
	    for child in ax.get_children():
	        if isinstance(child, matplotlib.spines.Spine):
	            child.set_alpha(0)
	       
	    #restyle the tick lines
	    for line in ax.get_xticklines() + ax.get_yticklines():
	        line.set_markersize(5)
	        line.set_color("gray")
	        line.set_markeredgewidth(1.4)
	    
	    #remove the minor tick lines    
	    for line in ax.xaxis.get_ticklines(minor=True) + ax.yaxis.get_ticklines(minor=True):
	        line.set_markersize(0)
	    
	    #only show bottom left ticks, pointing out of axis
	    rcParams['xtick.direction'] = 'out'
	    rcParams['ytick.direction'] = 'out'
	    ax.xaxis.set_ticks_position('bottom')
	    ax.yaxis.set_ticks_position('left')
	    
	    
	    if ax.legend_ <> None:
	        lg = ax.legend_
	        lg.get_frame().set_linewidth(0)
	        lg.get_frame().set_alpha(0.5)
	#Returns a cstring encoded image     
	def plotSeriesCString(self,param0="date",param1="close"): #plot using pyplot
		#style.use('ggplot') #using ggplot to make nice plots
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
		xRangeString = " from " + param0.capitalize() + "s " + xArray[0].strftime("%m-%Y")+" to "+ xArray[len(xArray)-1].strftime("%m-%Y")

		displayFig=pyplot.figure(figsize=(10,6.67)) #12,8
		displayFig.canvas.set_window_title(self.getObservation(0).getAttributeByName("ticker").upper()+": "+param0.capitalize()+" vs. "+param1.capitalize())
		subPlot=displayFig.add_subplot(111,xlabel=param0.capitalize(),ylabel=param1.capitalize(),title=self.getObservation(0).getAttributeByName("ticker").upper()+": " + param0.capitalize() + " vs. " + param1.capitalize() + xRangeString)
		subPlot.grid(False)
		#Some statistics to calculate range extension
		dateMin=date(xArray[0].year,xArray[0].month,1)
		#get last day of month using calendar module
		lastDay = calendar.monthrange(xArray[len(xArray)-1].year,xArray[len(xArray)-1].month)[1]

		dateMax=date(xArray[len(xArray)-1].year,xArray[len(xArray)-1].month,lastDay)
		extensionY=(max(yArray)-min(yArray))*.1
		#print "EXTENSIONY:",extensionY
		subPlot.set_xlim(dateMin,dateMax)
		subPlot.set_ylim(float(min(yArray))-extensionY,float(max(yArray))+extensionY)
		
		if param0=="date":
			#Give the user a choice of line style in the future
			subPlot.plot_date(xArray,yArray,'-')
			subPlot.xaxis.set_major_formatter(DateFormatter("%m-%Y")) #Sets format of x axis
		#Used to show plot
		#savefigure = pyplot.gcf()
		#pyplot.show() 
		# uncoment above to show plot on gui
		#Used to save plot
		#pathForChart = "charts/" + date.today().strftime("%d-%m-%y") + "/" + self.getObservation(0).getAttributeByName("ticker") + "/" + param0 + "vs" + param1 + "_" + xArray[0].strftime("%m-%Y") + "_" + xArray[len(xArray)-1].strftime("%m-%Y") + ".png"
		#We won't save the figure now
		#pathForChart = "tempImg.png"
		#savefigure.savefig(pathForChart, bbox_inches='tight')
		#canvas = FigureCanvas(savefigure)
		self.rstyle(subPlot)
		#New for AJAX - return c string representation
		sio = cStringIO.StringIO()
		pyplot.savefig(sio,format='PNG')
		encoded_img = sio.getvalue().encode('Base64')
		return encoded_img
	        
class SObservation:
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
