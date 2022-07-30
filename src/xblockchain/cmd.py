import argparse

import uvicorn

from xblockchain.api import app


def start_server():
    parser = argparse.ArgumentParser(description='Start a xBlockchain server')
    parser.add_argument('--host', type=str, help='server host', default="localhost")
    parser.add_argument('--port', type=int, help='server port', default=5000)

    args = parser.parse_args()

    uvicorn.run(app, host=args.host, port=args.port)
