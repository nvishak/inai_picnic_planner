from typing import Union

from pydantic import BaseModel


# JSON payload containing access token
class Token(BaseModel):
    access_token: str
    token_type: str


# Contents of JWT token
class TokenPayload(BaseModel):
    sub: Union[int, None] = None