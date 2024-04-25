from typing import Annotated

from sqlalchemy import String, Uuid
from sqlalchemy.orm import mapped_column


int_primary_key = Annotated[int, mapped_column(primary_key=True)]
uuid_primary_key = Annotated[Uuid, mapped_column(primary_key=True)]


def str_with_length(length: int) -> type[Annotated]:
    return Annotated[str, mapped_column(String(length))]
