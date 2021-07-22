import sys
from importlib import reload

import pytest
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.test import override_settings
from django.utils.timezone import now

from wagtail_live.adapters.channels import routing
from wagtail_live.adapters.channels.app import DjangoChannelsApp
from wagtail_live.blocks import construct_live_post_block


@pytest.mark.django_db
@override_settings(
    CHANNEL_LAYERS={"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}},
    WAGTAIL_LIVE_PUBLISHER="wagtail_live.adapters.channels.publisher.DjangoChannelsPublisher",
)
@pytest.mark.asyncio
async def test_django_channels_publisher(blog_page_factory, mocker):
    for module in ["wagtail_live.utils", "wagtail_live.signals", "wagtail_live.models"]:
        if module in sys.modules:
            reload(sys.modules[module])
    application = URLRouter(routing.live_websocket_urlpatterns)
    communicator = WebsocketCommunicator(application, "ws/channel/test_channel/")
    connected, subprotocol = await communicator.connect()
    assert connected

    channel_layer = get_channel_layer()
    groups = channel_layer.groups
    assert len(groups) == 1
    assert "liveblog_test_channel" in groups
    assert len(groups["liveblog_test_channel"]) == 1

    mocker.patch.object(DjangoChannelsApp, "send_json", return_value=None)
    page = await sync_to_async(blog_page_factory)(channel_id="test_channel")
    live_post = construct_live_post_block(message_id="some-id", created=now())

    # ADD
    await sync_to_async(page.add_live_post)(live_post=live_post)
    live_post = await sync_to_async(page.get_live_post_by_message_id)(
        message_id="some-id"
    )
    live_post_id = live_post.id
    mocked = DjangoChannelsApp.send_json

    mocked.assert_called_with(
        {
            "renders": {
                live_post_id: live_post.render(context={"block_id": live_post_id})
            },
            "removals": [],
        }
    )
    assert mocked.call_count == 1

    # EDIT
    await sync_to_async(page.update_live_post)(live_post=live_post)
    mocked.assert_called_with(
        {
            "renders": {
                live_post_id: live_post.render(context={"block_id": live_post_id})
            },
            "removals": [],
        }
    )
    assert mocked.call_count == 2

    # DELETE
    await sync_to_async(page.delete_live_post)(message_id="some-id")
    mocked.assert_called_with(
        {
            "renders": {},
            "removals": [live_post_id],
        }
    )
    assert mocked.call_count == 3

    # Close
    await communicator.disconnect()
