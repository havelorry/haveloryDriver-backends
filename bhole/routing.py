from django.urls import path, re_path
from channels.routing import ProtocolTypeRouter
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from driver.consumers import NotificationConsumer
from driver.routing import websocket_urlpatterns
application = ProtocolTypeRouter({
    "http": URLRouter([
        # Our async news fetcher
        path("/notifications$", NotificationConsumer),

        # AsgiHandler is "the rest of Django" - send things here to have Django
        # views handle them.
        re_path("^", AsgiHandler),
    ]),

    "websocket":URLRouter(
       websocket_urlpatterns
    )
})