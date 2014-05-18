from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.template import RequestContext

from ScarecrowApp.lib.Main import Scarecrow
from ScarecrowApp.models import GeneratedFigure
from datetime import date,datetime
import logging
import json, urllib2
logger = logging.getLogger(__name__)


from django.views.generic import FormView
from ScarecrowApp.forms import ControlPanel

def index(request):
	context = ({'Context': 'Hi!'})
        logger.debug("index rendered.")

	return render(request,'index.html',{'form': ControlPanel()})

def getFigureImage(request,figure_id): #figure id after creating a generatedfigure object
	fig = GeneratedFigure.objects.get(id=figure_id)

	newScarecrow = Scarecrow(tickerIn=fig.ticker,startIn=fig.start_date,endIn=fig.end_date,intervalIn=fig.interval)
	canvas = newScarecrow.currentSeries.plotSeries()
	response = HttpResponse(content_type='image/png')

	canvas.print_png(response)
	return response

def generate_image(request):

    req_context = RequestContext(request,{'test':'lol',})

    if request.method == 'POST':
        ticker = request.POST['ticker']

        start_date=datetime.strptime(request.POST['start_date'],'%Y/%m/%d').date()
        end_date=datetime.strptime(request.POST['end_date'],'%Y/%m/%d').date()

        newScarecrow = Scarecrow(tickerIn=ticker,startIn=start_date,endIn=end_date,intervalIn='d')
        encoded_img = newScarecrow.currentSeries.plotSeriesCString()
        print encoded_img
        if(encoded_img == -1):
            print "Django returning 427"
            return HttpResponseServerError(status=427)

        #return HttpResponse(ticker,req_context)
        return HttpResponse('<img src="data:image/png;base64,%s" class="img-responsive" alt="Your Generated Figure"/>' %encoded_img,req_context)

    else:
        return HttpResponse('not a post,nothing here',req_context)

def generate_jsondata(request,inTicker):
    startDate = request.GET['start'] #in the form of yyyy-mm-dd
    endDate = request.GET['end']

    #URL request construction
    quandl_url="http://www.quandl.com/api/v1/datasets/WIKI/"+inTicker.upper()
    quandl_url += ".json?sort_order=asc&trim_start="+startDate
    quandl_url += "&trim_end="+endDate+"&column=4&exclude_headers=true"
    quandl_url += "&auth_token=fDgiy3MbwDyWNYSpXwun"
    print quandl_url
    data = json.load(urllib2.urlopen(quandl_url))
    data = data['data'] #now a list of stock data
    count = 1
    rows = []
    for row in data:
        rows.append({"id":count,"cell":row})    
        count+=1 
    returnDict = {
        "total":len(data),
        "page":1,
        "records":len(data),
        "rows":rows
    }

    req_context = RequestContext(request,{'test':'lol'})
    return HttpResponse(json.dumps(returnDict),req_context)
