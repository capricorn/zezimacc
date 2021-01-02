from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter

import chatbox.routing
import chatbox.consumers

application = ProtocolTypeRouter({
    'websocket': URLRouter(chatbox.routing.websocket_urlpatterns)
})
