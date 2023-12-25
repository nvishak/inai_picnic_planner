from typing import Union

from pydantic import BaseModel

# Generic message
class Msg(BaseModel):
    msg: str
