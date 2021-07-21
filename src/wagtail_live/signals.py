import django.dispatch

from .utils import get_live_publisher

live_page_update = django.dispatch.Signal()

live_publisher = get_live_publisher()

# Connect a listener to the live_page_update signal
# if the publisher defined uses the websockets technique
if hasattr(live_publisher, "publish"):
    live_page_update.connect(live_publisher().publish)
