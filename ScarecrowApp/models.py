from django.db import models
#We want to store generatedFigure data, but not the images
#Analytics can be run on this data in the future.
class GeneratedFigure(models.Model):
	created = models.DateTimeField(editable=False)
	modified = models.DateTimeField()
	ticker = models.CharField(max_length=10)
	x_axis_title = models.CharField(max_length=20)
	y_axis_title = models.CharField(max_length=20)
	start_date = models.DateField()
	end_date = models.DateField() #the end date
	interval = models.CharField(max_length=5)
	#Path to image
	#figure_image = models.ImageField(upload_to='images')
	#We'll just dynamically generate in a view, instead of storing images


	def __unicode__(self): #returns string representation of object
		return self.ticker + ": " + self.x_axis_title + " vs. " + self.y_axis_title

class Observation(models.Model):
	created = models.DateTimeField(editable=False)
	observationDate = models.DateField()
	ticker = models.CharField(max_length=10)
	open = models.FloatField()
	high = models.FloatField()
	low = models.FloatField()
	close = models.FloatField()
	vol = models.FloatField()
	adjClose = models.FloatField()
	def __unicode__(self):
		return self.ticker + ": " + str(self.close)