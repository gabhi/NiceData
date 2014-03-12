from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import loader, Context

# Create your views here.
def index(request):
	template = loader.get_template('index.html')
	context = ({'Context': 'Hi!'})
	return render(request,'index.html',context)