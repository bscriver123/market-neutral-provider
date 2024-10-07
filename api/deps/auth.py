from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from loguru import logger

from api import APP_API_KEY


class OAuth2PasswordBearerWithHeader(OAuth2PasswordBearer):
    def init(self, tokenUrl: str, header_name: str = "Authorization"):
        logger.info(f"Token URL: {tokenUrl}, Header Name: {header_name}")
        super().init(tokenUrl=tokenUrl)
        self.header_name = header_name

    async def call(self, request: Request):
        logger.info(f"Headers: {request.headers}")
        authorization: str = request.headers.get(self.header_name)
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token = authorization[len("Bearer ") :]
        return token


oauth2_scheme = OAuth2PasswordBearerWithHeader(tokenUrl="token")


def authenticate_user(token: str = Depends(oauth2_scheme)) -> bool:
    if token != APP_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True
