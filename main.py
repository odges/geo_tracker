from logging import Logger

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from core.events import create_start_app_handler, create_stop_app_handler
from core.setting import DEBUG
from routes.geo.route import router


def get_application() -> FastAPI:
    application = FastAPI(
        title="GEO recorder",
        debug=DEBUG,
        version="0.0.1",
    )
    logger = Logger("geo_core", "INFO")
    application.logger = logger

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.include_router(router)
    return application


app = get_application()


if __name__ == "__main__":
    from argparse import ArgumentParser

    import uvicorn

    parser = ArgumentParser()
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Enter port")
    parser.add_argument("--port", type=int, default=8001, help="Enter port")
    args = parser.parse_args()

    uvicorn.run(
        "main:app",
        host=args.host,
        loop="uvloop",
        debug=DEBUG,
        reload=DEBUG,
        port=args.port,
    )
