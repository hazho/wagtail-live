""" How to use it?
To create an app, register your URL to slack, get a token plus all additional infrastucture, see:
https://github.com/slackapi/bolt-python/tree/main/examples/django
Then do something like this in your url_patterns:
from wagtail_live.slack.views import slack_events_handler
url_patterns += [
    path("slack/events", slack_events_handler, name="slack_events_handler"),
]
Add the following to your settings.py file:
LIVE_PAGE_MODEL = "model name"
LIVE_APP = "app name"
SLACK_BOT_TOKEN = "your slack bot token"
SLACK_SIGNING_SECRET = "your slack signing secret"
And you are good to go! (Soon hopefully!)
"""

from wagtail_live.receivers import BaseMessageReceiver


class SlackEventsAPIReceiver(BaseMessageReceiver):
    def dispatch(self, event):
        message = event
        if "subtype" in message and message["subtype"] == "message_changed":
            self.change_message(message)
            return

        elif "subtype" in message and message["subtype"] == "message_deleted":
            self.delete_message(message)
            return

        else:
            self.add_message(message)

    def get_channel_name_from_message(self, message):
        return message["channel"]

    def get_message_id_from_message(self, message):
        return message["ts"]

    def get_message_text(self, message):
        return message["text"]

    def get_message_files(self, message):
        if "files" in message:
            return message["files"]
        return []

    def get_message_id_from_edited_message(self, message):
        return self.get_message_id_from_message(message["previous_message"])

    def get_message_text_from_edited_message(self, message):
        return self.get_message_text(message["message"])

    def get_message_files_from_edited_message(self, message):
        return self.get_message_files(message["message"])
