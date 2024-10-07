"""Top level package."""
from pathlib import Path

import yaml
from dotenv import load_dotenv

BASEPATH = Path(__file__).parent.absolute()
WORKDIR = Path(__file__).parent.parent.absolute()

load_dotenv(dotenv_path=WORKDIR / ".env")
CONFIG_DIR = WORKDIR / "config"


# Load config
with open(CONFIG_DIR / "config.yaml", "r") as f:
    config = yaml.safe_load(f)

model_name = "gpt-4o-mini"
market_neutral_background_prompt = """
Evaluate the following description and respond YES if it includes any information related to investments decisions. Otherwise, respond NO.
"""  # noqa E501
