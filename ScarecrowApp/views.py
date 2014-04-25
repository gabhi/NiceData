from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext

from ScarecrowApp.lib.Main import Scarecrow
from ScarecrowApp.models import GeneratedFigure
from datetime import date,datetime
import logging
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

        # generate a matplotlib image, (I don't know how to do that)
        '''
        sio = cStringIO.StringIO() # use io.StringIO() in Python 3x
        pyplot.savefig(sio, format="PNG")
        encoded_img = sio.getvalue().encode('Base64') # On Python 3x, use base64.b64encode(sio.getvalue())

       # return HttpResponse('<img src="data:image/png;base64,%s" />' %encoded_img)
       '''
        start_date=datetime.strptime(request.POST['start_date'],'%Y/%m/%d').date()
        end_date=datetime.strptime(request.POST['end_date'],'%Y/%m/%d').date()

        
        #start_date = date(2009,1,1)
        #end_date = date(2009,5,5)

        newScarecrow = Scarecrow(tickerIn=ticker,startIn=start_date,endIn=end_date,intervalIn='d')
        encoded_img = newScarecrow.currentSeries.plotSeriesCString()

        #return HttpResponse(ticker,req_context)
        return HttpResponse('<img src="data:image/png;base64,%s" class="img-responsive" alt="Your Generated Figure"/>' %encoded_img,req_context)

    else:
        return HttpResponse('not a post,nothing here',req_context)
