
import sanic
from sanic.log import logger

from . import secrets
from .slacker import Slacker

# attach additional api routes to 'routing'
routing = sanic.Blueprint('slack-bot-extras')

# To create a new app go to https://api.slack.com/apps?new_app=1
bot = Slacker(
    token=secrets.slack_api_token,
    signing_secret=secrets.slack_signing_secret,
)


# this would be called by the `/hello` slash command.
#
# To add new slash commands, go back to your app
# configuration https://api.slack.com/apps/:id
# and add new slackcommands, permissions, etc
# the url will be <openfaas_gateway>/function/<function_name>/hello
@bot.slash_cmd("hello")
async def hello(request: sanic.request.Request):
    channel = request.form.get("channel")
    # you can use the client object to send a response, this is required if
    # the command logic is too slow to respond within 3s
    response = await bot.client.chat_postMessage(
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
                    "text": "**Hello**"
                },
            },
        ]
    )

    logger.debug(response)
    return "done"
