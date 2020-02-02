
import sanic
import slack
from sanic.log import logger
from sanic.response import json, text

from . import secrets

# To create a new app go to https://api.slack.com/apps?new_app=1
routing = sanic.Blueprint('slack-bot')
client = slack.WebClient(token=secrets.slack_api_token, run_async=True)

# To add new slash commands, go back to your app
# configuration https://api.slack.com/apps/:id
# and add new slackcommands, permissions, etc
@routing.route("/slash", methods=["POST"])
async def slash(request: sanic.request.Request):
    data = request.body
    logger.debug(data)

    valid = client.validate_slack_signature(
        signing_secret=secrets.slack_signing_secret,
        # make sure to decode the bytes to a string!
        data=data.decode("utf-8"),
        timestamp=request.headers.get("X-Slack-Request-Timestamp"),
        signature=request.headers.get("X-Slack-Signature"),
    )

    if not valid:
        logger.warn("invalid request")
        return json({"response_type": "ephemeral", "text": "invalid request"})

    # slash commands are form encoded data, not json
    # you will generally want to extract the channel name and the command
    # you can also access user_id, user_name, channel_id, team_id, team_domain
    channel = request.form.get("channel_name")

    cmd_text = request.form.get("text")
    logger.debug(cmd_text)

    command = request.form.get("command")
    logger.debug(command)

    # you can use the client object to send a response, this is required if
    # the command logic is too slow to respond within 3s
    response = await client.chat_postMessage(
        channel=f"#{channel}",
        # use Block Kit https://api.slack.com/block-kit
        # and the Block Builder to create rich responses
        # https://api.slack.com/tools/block-kit-builder
        # this example is a stripped down version of the Search
        # Results template available in the Block Builder
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "We found *205 Hotels* in New Orleans, LA from *12/14 to 12/17*"
                },
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*<fakeLink.toHotelPage.com|Windsor Court Hotel>*\n★★★★★\n$340 per night\nRated: 9.4 - Excellent"
                }
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*<fakeLink.toHotelPage.com|The Ritz-Carlton New Orleans>*\n★★★★★\n$340 per night\nRated: 9.1 - Excellent"
                }
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*<fakeLink.toHotelPage.com|Omni Royal Orleans Hotel>*\n★★★★★\n$419 per night\nRated: 8.8 - Excellent"
                }
            }
        ]
    )

    logger.debug(response)

    # if the command is fast enough,you can also respond directly to
    # the request
    return text("", status=200)
