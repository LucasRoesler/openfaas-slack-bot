from typing import Callable

import sanic
import slack
from sanic.log import logger
from sanic.response import json, text

Handler = Callable[[sanic.request.Request], sanic.response.HTTPResponse]


# To create a new app go to https://api.slack.com/apps?new_app=1
class Slacker:
    router: sanic.Blueprint
    client: slack.WebClient
    signing_secret: str

    def __init__(self, token: str, signing_secret: str):
        self.client = slack.WebClient(token=token, run_async=True)
        self.router = sanic.Blueprint('slack-bot-slash')
        self.signing_secret = signing_secret

    def slash_cmd(self, name: str):

        def decorator(handler: Handler):

            @self.router.route(f"/{name}", methods=["POST"])
            async def handler_wrapper(request: sanic.request.Request):
                try:
                    valid = self.client.validate_slack_signature(
                        signing_secret=self.signing_secret,
                        # make sure to decode the bytes to a string!
                        data=request.body.decode("utf-8"),
                        timestamp=request.headers.get("X-Slack-Request-Timestamp"),
                        signature=request.headers.get("X-Slack-Signature"),
                    )
                except Exception as e:
                    logger.error("validation failed", exc_info=e)
                    return text("server error", 500)

                if not valid:
                    logger.warn("invalid request")
                    return json({
                        "response_type": "ephemeral",
                        "text": "invalid request",
                    })
                try:
                    return await handler(request)
                except Exception as e:
                    logger.error("validation failed", exc_info=e)
                    return text("server error", 500)

            return handler_wrapper

        return decorator
