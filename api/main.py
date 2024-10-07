from typing import Final

import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.endpoints.market_neutral.router import router
from market_router import config
from market_router.scripts import proposal

scheduler = BackgroundScheduler()

APP_VERSION: Final[str] = "0.0.2"


def start_scheduler():
    scheduler.add_job(
        proposal.create_proposal,
        "interval",
        seconds=config["proposal_interval"],
    )
    scheduler.start()


app = FastAPI(version=APP_VERSION, debug=True)


@app.on_event("startup")
def on_startup():
    start_scheduler()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.WEB_PORT)
