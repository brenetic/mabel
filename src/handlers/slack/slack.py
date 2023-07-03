import logging
import time

from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler


app = App(process_before_response=True)


def acknowledge_anyway(ack):
    ack()


def respond_to_slack_within_3_seconds(body, ack):
    try:
        title = body["text"]
        ack(f"Accepted! (task: {title})")
    except Exception as err:
        ack(f"Something went wrong with error {err}")


def handle_app_mentions(body, say, logger):
    logger.info(body)
    say("What's up?")


def process_request(context, respond, say, body):
    time.sleep(5)
    title = body["text"]
    say(f"<@{context.user_id}> called command in channel {context.channel_id}")
    respond(f"Completed! (task: {title})")


app.event("app_mention")(ack=acknowledge_anyway, lazy=[handle_app_mentions])


SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)


def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)
