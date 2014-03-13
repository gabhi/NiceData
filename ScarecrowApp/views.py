from django.shortcuts import render
from django.http import HttpResponse

from ScarecrowApp.lib.ScarecrowObjects import ObservationSeries
from ScarecrowApp.lib.Main import Scarecrow
from ScarecrowApp.models import GeneratedFigure
# Create your views here.
def index(request):
	context = ({'Context': 'Hi!'})
	return render(request,'index.html',context)

def getFigureImage(request,figure_id): #figure id after creating a generatedfigure object
	fig = GeneratedFigure.objects.get(id=figure_id)

	newScarecrow = Scarecrow(tickerIn=fig.ticker,startIn=fig.start_date,endIn=fig.end_date,intervalIn=fig.interval)
	canvas = newScarecrow.currentSeries.plotSeries()
	response = HttpResponse(content_type='image/png')

	canvas.print_png(response)
	return response