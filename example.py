#!/usr/bin/python3
import logging

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn

import logman

ALLOWED_HOSTS = [
    'localhost',
]
ALLOWED_CORS = [
    'http://localhost',
    'https://localhost',
]
ENFORCE_HTTPS = False
DEV_DEBUG = True
LOG_TO_CLI = True

logman.init('example', log_to_cli=LOG_TO_CLI)


def tame_uvicorn_logger():
    '''
    neutralize uvicorn logger handlers, then setup our own
    '''
    # below two lines successful in getting rid of that one pesky streamhandler
    uvicorn.config.LOGGING_CONFIG['loggers'] = {}
    logging.getLogger('').handlers = []  # wat
    # below logger handlers violence seems to be unnecessary, the silly one above is sufficient
    # logging.getLogger('uvicorn').handlers = []
    # logging.getLogger('uvicorn.access').handlers = []
    # logging.getLogger('uvicorn.asgi').handlers = []
    # logging.getLogger('uvicorn.error').handlers = []
    # set our own handlers
    logman.configure_logger('uvicorn', 'api', logman.Log_Config, log_to_cli=LOG_TO_CLI)
    # interested in access logs, either from uvicorn.access or create middleware for more details?
    # or maybe both?
    logman.configure_logger('uvicorn.access', 'api', logman.Log_Config, log_to_cli=LOG_TO_CLI)
    # Hmm? configuring uvicorn.access causes uvicorn.error log .. incorrect logger setup somewhere?
    # [2020-01-03..] [INFO] Started server process [27260] (uvicorn.error - main.py:389)
    # [2020-01-03..] [INFO] 127.0.0.1:65364 - "GET / HTTP/1.1" 200 (uvicorn.error - h11_impl.py:454)
    # yeah, pretty sure these logs should be logged into uvicorn.access, not uvicorn.error ..
    # ---
    # haven't looked at what exactly is logged to uvicorn.asgi and uvicorn.error .. maybe want?
    # logman.configure_logger('uvicorn.asgi', 'api', logman.Log_Config, log_to_cli=True)
    # logman.configure_logger('uvicorn.error', 'api', logman.Log_Config, log_to_cli=True)


async def homepage(request):
    logman.info('hello, this is homepage')
    return JSONResponse({'hello': 'world'})

routes = [
    Route('/', endpoint=homepage),
]

# TODO: figure out if we want both TrustedHostMiddleware and CORSMiddleware or just the latter?
middleware = [  # https://www.starlette.io/middleware/
    Middleware(TrustedHostMiddleware, allowed_hosts=ALLOWED_HOSTS),
    Middleware(CORSMiddleware, allow_origins=ALLOWED_CORS),
]
if ENFORCE_HTTPS:
    middleware.append(Middleware(HTTPSRedirectMiddleware))  # strictly enforce https-only access

app = Starlette(debug=DEV_DEBUG, routes=routes, middleware=middleware)

# uvicorn configuration
uvicorn.Config(app)
tame_uvicorn_logger()


if __name__ == '__main__':
    logman.info('Starting Starlette server!')
    # inform in logger that we're running uvicorn from this script
    uvicorn_logger = logging.getLogger('uvicorn')
    uvicorn_logger.info('Running uvicorn from example.py:__main__')
    uvicorn.run(app, port=8000)
