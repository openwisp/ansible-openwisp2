from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView

try:
    from django.urls import reverse_lazy
except ImportError:
    from django.core.urlresolvers import reverse_lazy

redirect_view = RedirectView.as_view(url=reverse_lazy('admin:index'))

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    {% if openwisp2_controller_urls %}
    url(r'', include('openwisp_controller.urls')),
    {% endif %}
    url(r'^api/v1/', include('openwisp_utils.api.urls')),
    url(r'^api/v1/', include('openwisp_users.api.urls')),
    {% if openwisp2_network_topology %}
    url(r'^', include('openwisp_network_topology.urls')),
    {% endif %}
    {% if openwisp2_firmware_upgrader %}
    url(r'^', include('openwisp_firmware_upgrader.urls')),
    {% endif %}
    {% if openwisp2_radius %}
    url(r'^', include('openwisp_radius.urls')),
    url(r'^api/v1/', include('openwisp_users.api.urls')),
    url(r'^api/v1/', include('openwisp_utils.api.urls')),
    {% endif %}
    {% for extra_url in openwisp2_extra_urls %}
    {{ extra_url }},
    {% endfor %}
    url(r'^$', redirect_view, name='index'),
]

urlpatterns += staticfiles_urlpatterns()
