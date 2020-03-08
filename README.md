# pyslash OpenFaaS Slack Slash Command Template

## Usage

1. `faas-cli new bot --lang=pyslash`
2. Wite your command logic in `./bot/handler.py`

The abosolute smallest example slash command looks like this

```py
import sanic
from sanic.response import json

from . import secrets
from .slacker import Slacker

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
    return json({
            "response_type": "in_channel",
            "text": "*hi there*",
        })
```

You must also set the secrets for your Slack API token an dsigning secret in your stack file:

```yaml
functions:
  bot:
    lang: pyslash
    handler: ./bot
    image: theaxer/test-bot:latest
    secrets:
      - slack-api-token
      - slack-signing-secret
```

## Deployment
Configure your Slack bot.  Create or manage your app at https://api.slack.com/apps

Get your bot's API token from the`https://api.slack.com/apps/<app_id>/install-on-team` and your
signing key from `https://api.slack.com/apps/<app_id>/general`
```sh
faas-cli secret create slack-api-token --from-literal=xoxb-921547957923-933041549141-J0i1Nt9ZLBoL6BCEpXoGEQrK
faas-cli secret create slack-signing-secret --from-literal=7bd05b1bca10d191f69de20866c4c890
faas-cli up
```

Each Slash command that you register in your handler must also be registered in the Slack UI,
`https://api.slack.com/apps/<app_id>/slash-commands`

The URL for each slash command will be `http://<openfaas_gateway>/function/<function_name>/<handler_method>`
