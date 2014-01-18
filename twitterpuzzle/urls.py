from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'twitterpuzzle.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$','twitter.views.index'),
  #  url(r'^index/(?P<uid>).JPG/$','twitter.views.result'),
    url(r'^index/(?P<uid>\d+)$','twitter.views.result'),
)
