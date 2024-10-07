import random
from uuid import UUID

import requests
import requests.status_codes as status
from loguru import logger

from market_router import config

_LOGIN_VARIABLES = ["username", "password"]


def deposit(deposit_data: dict, api_key: str):
    try:
        headers = {"X-API-KEY": api_key}

        response = requests.post(
            f"{config['market_router_url']}/v1/payment/deposit",
            headers=headers,
            json=deposit_data,
        )
        response.raise_for_status()

        response_data = response.json()
        if response.status_code == status.codes.ok:
            logger.info(
                f"Please complete the payment process in the following link: {response_data['url']}"
            )
        return response_data

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP request failed: {e.response.text}")
        raise e
    except Exception as e:
        logger.error(f"Error: {e}")
        raise e


def submit_instance(instance: dict, api_key: str) -> dict:
    headers = {"X-API-KEY": api_key}

    url = f"{config['market_router_url']}/v1/instances"

    try:
        response = requests.post(url, json=instance, headers=headers)
        response.raise_for_status()

        response_data = response.json()
        logger.info(f"Request submitted successfully")
        return response_data

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP request failed: {e.response.text}")
        raise e
    except Exception as e:
        logger.error(f"Error: {e}")
        raise e


def register_user(user_data: dict):
    try:
        response = requests.post(f"{config['market_router_url']}/v1/auth/register", json=user_data)
        response.raise_for_status()

        response_data = response.json()
        if response.status_code == status.codes.created:
            logger.info(f"User {user_data['username']} created successfully")

        return response_data

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP request failed: {e.response.text}")
        raise e
    except Exception as e:
        logger.error(f"Error: {e}")
        raise e


def login_user(user_data: dict):
    try:
        login_data = {k: user_data[k] for k in _LOGIN_VARIABLES}

        response = requests.post(f"{config['market_router_url']}/v1/auth/login", data=login_data)
        response.raise_for_status()

        response_data = response.json()

        if response.status_code == status.codes.ok:
            logger.info(f"User {user_data['username']} logged in successfully")

        return response_data

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP request failed: {e.response.text}")
        raise e
    except Exception as e:
        logger.error(f"Error: {e}")
        raise e


def create_api_key(login_info):
    try:
        headers = {"Authorization": f"Bearer {login_info['access_token']}"}

        response = requests.post(
            f"{config['market_router_url']}/v1/auth/create-api-key?"
            f"name=neutral-portfolio_provider_{random.randint(1, 10000)}",
            headers=headers,
        )
        response.raise_for_status()

        response_data = response.json()
        if response.status_code == status.codes.created:
            logger.info("API key created successfully")

        return response_data

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP request failed: {e.response.text}")
        raise e
    except Exception as e:
        logger.error(f"Error: {e}")
        raise e


def submit_proposal(instance_id: UUID, proposal: dict, api_key: str):
    headers = {"X-API-KEY": api_key}

    try:
        response = requests.post(
            f"{config['market_router_url']}/v1/proposals/create/for-instance/{instance_id}",
            json=proposal,
            headers=headers,
        )
        response_data = response.json()
        response.raise_for_status()
        if response.status_code == 201:
            logger.info(f"Request submitted successfully")
        return response_data
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP request failed: {e.response.text}")
        raise e
    except Exception as e:
        logger.error(f"Error: {e}")
        raise e


def get_instances(api_key: str):
    headers = {"X-API-KEY": api_key}
    url = f"{config['market_router_url']}/v1/instances/?instance_status=0"
    try:
        response = requests.get(url, headers=headers)
        response_data = response.json()
        response.raise_for_status()
        if response.status_code == 200:
            logger.info(f"Instances retrieved successfully")
        return response_data
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP request failed: {e.response.text}")
        raise e
    except Exception as e:
        logger.error(f"Error: {e}")
        raise e


def submit_proposal(instance_id: UUID, proposal: dict, api_key: str):
    headers = {"X-API-KEY": api_key}

    try:
        response = requests.post(
            f"{config['market_router_url']}/v1/proposals/create/for-instance/{instance_id}",
            json=proposal,
            headers=headers,
        )
        response.raise_for_status()
        if response.status_code == 201:
            logger.info(f"Proposal submitted successfully")
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP request failed: {e.response.text}")
        raise e
    except Exception as e:
        logger.error(f"Error: {e}")
        raise e


def get_instance_proposals(api_key: str):
    headers = {"X-API-KEY": api_key}
    url = f"{config['market_router_url']}/v1/proposals"
    try:
        response = requests.get(url, headers=headers)
        response_data = response.json()
        response.raise_for_status()
        if response.status_code == 200:
            logger.info(f"Proposals retrieved successfully")
        return response_data
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP request failed: {e.response.text}")
        raise e
    except Exception as e:
        logger.error(f"Error: {e}")
        raise e
