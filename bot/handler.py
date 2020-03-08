import sanic
from sanic.log import logger
from sanic.response import json, text

from . import secrets
from .slacker import Slacker

# attach additional api routes to 'routing'
routing = sanic.Blueprint('slack-bot-extras')

# To create a new app go to https://api.slack.com/apps?new_app=1
# Manager your apps:
#     https://api.slack.com/apps
# Manage slash commands in an app:
#     https://api.slack.com/apps/:id/slash-commands
bot = Slacker(
    token=secrets.slack_api_token,
    signing_secret=secrets.slack_signing_secret,
)

# this would be called by the `/hello` slash command.
#
# the url will be <openfaas_gateway>/function/<function_name>/hello
@bot.slash_cmd("hello")
async def hello(request: sanic.request.Request):
    logger.debug(f"handling request: {request}")
    # sample form payload
    # {
    #     'token': ['...'],
    #     'team_id': ['...'],
    #     'team_domain': ['...'],
    #     'channel_id': ['...'],
    #     'channel_name': ['general'],
    #     'user_id': ['...'],
    #     'user_name': ['roesler.lucas'],
    #     'command': ['/hello'],
    #     'response_url': ['https://hooks.slack.com/c...'],
    #     'trigger_id': ['...']
    # }
    channel = request.form.get("channel_name")
    input_txt: str = request.form.get("text", "")

    if input_txt.strip() in ["help", ""]:
        # just respond with json to answer the slash command
        return json({
            #  or"in_channel" or show to everyone in the channel
            "response_type": "ephemeral",
            "text": 'How to use /hello',
            "attachments": [
                {
                    "type": "mrkdwn",
                    "text": 'Submit some text and see it said back using `/hello test it out`.',
                },
            ],
        })

    # _or_ you can use the client object to send a response, this is required
    # if the command logic is too slow to respond within 3s
    #
    # NOTE: you will need to add your bot to the channel,
    #       just say `@<bot_name>` to inite them.
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
                    "text": "*Hello*"
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"_You Said:_ \"{input_txt}\"",
                },
            },
        ]
    )
    logger.debug(response)

    # ireturning plain text is equivalent to
    # return json({
    #         #  or"in_channel" or show to everyone in the channel
    #         "response_type": "ephemeral",
    #         "text": "*hi there*",
    #     })
    return text("*hi there*")
