from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Scarecrow.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'ScarecrowApp.views.index',name='index'),
    url(r'^admin/', include(admin.site.urls)),

    #Return the dynamically created image
    #URL FORM: server.com/seriesid/result.png
    url(r'^(?P<figure_id>\d+)/figure.png$', 'ScarecrowApp.views.getFigureImage',name='getFigureImage'),

    #URL to serve created image on same page
    url(r'^generate-image/', 'ScarecrowApp.views.generate_image',name='generateImage'),

)
	