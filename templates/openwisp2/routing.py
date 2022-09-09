from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

{% for import in openwisp2_websocket_extra_imports %}
{{ import }}
{% endfor %}

routes = []

{% if openwisp2_controller_urls %}
from openwisp_controller.routing import get_routes as get_controller_routes
routes.extend(get_controller_routes())
{% endif %}

{% for extra_routes in openwisp2_websocket_extra_routes %}
routes.extend({{ extra_routes }})
{% endfor %}

application = ProtocolTypeRouter(
    {
        'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(routes))
        )
    }
)
