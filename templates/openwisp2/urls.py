from django.urls import include, path, reverse_lazy
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView

redirect_view = RedirectView.as_view(url=reverse_lazy('admin:index'))

urlpatterns = [
    path('admin/', admin.site.urls),
{% if openwisp2_controller_urls %}
    path('', include('openwisp_controller.urls')),
{% endif %}
    path('api/v1/', include('openwisp_utils.api.urls')),
    path('api/v1/', include('openwisp_users.api.urls')),
{% if openwisp2_network_topology %}
    path('', include('openwisp_network_topology.urls')),
{% endif %}
{% if openwisp2_firmware_upgrader %}
    path('', include('openwisp_firmware_upgrader.urls')),
{% endif %}
{% if openwisp2_monitoring %}
    path('', include('openwisp_monitoring.urls')),
{% endif %}
{% if openwisp2_radius and openwisp2_radius_urls %}
    path('', include('openwisp_radius.urls')),
{% endif %}
{% for extra_url in openwisp2_extra_urls %}
    {{ extra_url }},
{% endfor %}
    path('$', redirect_view, name='index'),
]

urlpatterns += staticfiles_urlpatterns()
