from typing import Literal, Union

from pydantic import BaseModel, Field, ConfigDict


class PublicTelegramChannelState(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    source_type: Literal["PublicTelegramChannel"] = "PublicTelegramChannel"
    last_post_id: int


NewsSourceState = Union[PublicTelegramChannelState]


class NewsSourceData(BaseModel):
    unique_name: str
    state_data: NewsSourceState = Field(..., discriminator="source_type")
