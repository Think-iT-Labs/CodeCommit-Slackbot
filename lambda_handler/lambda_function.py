from event_factory import EventFactory
import urllib
import json
from os import environ


webhook_url = environ['SLACK_WEBHOOK_URL']


def lambda_handler(event, context):
    factory = EventFactory(event)
    event_instance = factory.get_instance()
    slack_payload = event_instance.get_slack_payload()
    headers = {
        'Content-Type': 'application/json'
    }
    data = json.dumps(slack_payload)
    data = data.encode('ascii')
    request = urllib.request.Request(url=webhook_url, data=data, headers=headers)
    urllib.request.urlopen(request)
