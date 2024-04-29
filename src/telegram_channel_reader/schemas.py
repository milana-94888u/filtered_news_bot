from pydantic import BaseModel, Field


class NewPostsRequest(BaseModel):
    channel_username: str
    last_post_id: int


class BaseNewPostData(BaseModel):
    post_id: int
    text: str
