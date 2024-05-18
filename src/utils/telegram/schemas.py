from pydantic import BaseModel


class NewPostsRequest(BaseModel):
    channel_username: str
    last_post_id: int = 0


class BasePostData(BaseModel):
    post_id: int
    text: str
