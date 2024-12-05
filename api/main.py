"""
Main module for the FastAPI application.

This module sets up the FastAPI application, configures middleware, and starts a background scheduler
for periodic tasks. It also includes the main entry point for running the application with Uvicorn.
"""

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
    """
    Start the background scheduler for periodic tasks.

    This function adds a job to the scheduler to create proposals at regular intervals
    defined in the configuration and starts the scheduler.
    """
    scheduler.add_job(
        proposal.create_proposal,
        "interval",
        seconds=config["proposal_interval"],
    )
    scheduler.start()


app = FastAPI(version=APP_VERSION, debug=True)


@app.on_event("startup")
def on_startup():
    """
    Event handler for the startup event.

    This function is called when the FastAPI application starts and is responsible for
    starting the background scheduler.
    """
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
    # Run the FastAPI application using Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.WEB_PORT)
