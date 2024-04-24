from typing import Type

from sqlalchemy.orm import DeclarativeBase, declared_attr

from core.utils import convert_pascal_case_identifier_to_snake_case_plural_identifier


class BaseModel(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls: Type) -> str:
        return convert_pascal_case_identifier_to_snake_case_plural_identifier(
            cls.__name__
        )
