from django.urls import re_path

from .app import DjangoChannelsApp

live_websocket_urlpatterns = [
    re_path(r"ws/channel/(?P<channel_id>\w+)/$", DjangoChannelsApp.as_asgi()),
]
