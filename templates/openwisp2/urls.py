from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()
admin.site.site_url = None


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('django_netjsonconfig.controller.urls', namespace='controller')),
]

urlpatterns += staticfiles_urlpatterns()
