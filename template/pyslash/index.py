import logging
import os

import sanic

from function import handler

app = sanic.Sanic(__name__)
app.blueprint(handler.bot.router)
app.blueprint(handler.routing)


def get_int(name: str, default: int) -> int:
    value = os.environ.get(name, default)
    try:
        return int(value)
    except Exception as e:
        logging.warn(e)
        return default


if __name__ == "__main__":
    workers = get_int("WORKERS", 1)
    app.run(host='0.0.0.0', port=5000, debug=True, workers=workers)
