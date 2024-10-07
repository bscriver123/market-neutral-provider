import os

import openai
from loguru import logger

from api import APP_API_KEY
from market_router import config, market_neutral_background_prompt, model_name
from market_router import utils as api_calls

_PROPOSAL_VARIABLES = ["endpoint", "max_bid"]


def submit_proposal():
    agma_api_key = os.getenv("MARKET_ROUTER_API_KEY")

    proposal_details = _load_proposal_details()

    instances = api_calls.get_instances(agma_api_key)

    if not instances:
        logger.info("No instances found.")
        return

    for instance in instances:
        if _is_market_neutral_instance(instance):
            proposals = api_calls.get_instance_proposals(agma_api_key)
            if not _check_if_proposal_exists(proposals, instance["id"]):
                api_calls.submit_proposal(instance["id"], proposal_details, agma_api_key)


def _check_if_proposal_exists(proposals, instance_id):
    return any(proposal["instance_id"] == instance_id for proposal in proposals)


def _load_proposal_details():
    proposal_details = {variable: config[variable] for variable in _PROPOSAL_VARIABLES}
    proposal_details["endpoint_api_key"] = APP_API_KEY
    return proposal_details


def _is_market_neutral_instance(instance):
    messages = [{"role": "system", "content": market_neutral_background_prompt}]
    messages.append({"role": "user", "content": instance["background"]})

    response = openai.ChatCompletion.create(model=model_name, messages=messages, temperature=1)
    content = response.choices[0].message.content

    return True if "YES" in content else False
