from typing import List, Optional

from pydantic import BaseModel, Extra


class Message(BaseModel):
    role: str
    content: str


class CompletionRequest(BaseModel):
    messages: List[dict]

    class Config:
        extra = Extra.allow


class Choice(BaseModel):
    index: int
    message: Message
    logprobs: Optional[dict]
    finish_reason: str


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[Choice]
    usage: Usage

    class Config:
        extra = Extra.allow
