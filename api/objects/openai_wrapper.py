import openai
from fastapi import HTTPException, status
from loguru import logger
from openai.error import ServiceUnavailableError

from api import baseline_system_prompt_tpl, model_name, temperature


class OpenAIWrapper:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def create_completion(self, messages):
        messages = self._add_system_message(messages)
        try:
            return openai.ChatCompletion.create(
                model=model_name, messages=messages, temperature=temperature
            )
        except ServiceUnavailableError as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="OpenAI service unavailable"
            )
        except Exception as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error"
            )

    def _add_system_message(self, conversation):
        conversation.insert(0, {"role": "system", "content": baseline_system_prompt_tpl})
        return conversation
