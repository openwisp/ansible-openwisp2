from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

{% for import in openwisp2_websocket_extra_imports %}
{{ import }}
{% endfor %}

routes = []

{% if openwisp2_controller_urls %}
from openwisp_controller.routing import get_routes as get_controller_routes

routes.extend(get_controller_routes())
{% endif %}

{% if openwisp2_network_topology %}
from openwisp_network_topology.routing import (
    websocket_urlpatterns as network_topology_routes
)

routes.extend(network_topology_routes)
{% endif %}

{% if openwisp2_radius %}
from openwisp_radius.routing import (
    websocket_urlpatterns as radius_routes
)

routes.extend(radius_routes)
{% endif %}

{% for extra_routes in openwisp2_websocket_extra_routes %}
routes.extend({{extra_routes}})
{% endfor %}

application = ProtocolTypeRouter(
    {
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(routes))
        ),
        "http": get_asgi_application(),
    }
)
