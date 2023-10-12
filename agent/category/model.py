import enum
from pydantic import BaseModel, Field


class SourceInput(BaseModel):
    name: str = Field(description="资源名字")


class CategoryOutput(BaseModel):
    """资源类型"""
    category: str = Field(description="动漫、图书、音乐、电影、其他")


class CategoryEnum(enum.Enum):
    Animation = "动漫"
    Book = "图书"
    Music = "音乐"
    Movie = "电影"
    Other = "其他"
