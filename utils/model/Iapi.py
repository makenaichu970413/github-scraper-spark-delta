# Library
from pydantic import BaseModel
from typing import Optional


class IHeaders(BaseModel):
    Authorization: Optional[str] = None
