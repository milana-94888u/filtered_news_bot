from typing import Literal, Union

from pydantic import BaseModel, Field, ConfigDict


class UserData(BaseModel):
    telegram_id: int
