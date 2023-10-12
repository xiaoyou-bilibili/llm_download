from pydantic import BaseModel, Field
from typing import List


class GoogleSpiderInput(BaseModel):
    keyword: str = Field(description="搜索关键词")


class GoogleLinkInfo(BaseModel):
    """链接信息"""
    title: str = Field(description="标题")
    url: str = Field(description="链接")


class GoogleSpiderOutput(BaseModel):
    """谷歌搜索引擎输出"""
    links: List[GoogleLinkInfo] = Field(description="链接列表")
    name: str = Field(description="资源名字")


class WebSpiderInput(BaseModel):
    url: str = Field(description="资源链接")


class WebLinkInfo(BaseModel):
    """链接信息,资源的描述信息会在资源链接的上面或者下面，你需要自己判断，如果有提取码啥的也需要加到描述里面去"""
    desc: str = Field(description="资源描述")
    url: str = Field(description="下载链接")


class WebSpiderOutput(BaseModel):
    """链接列表"""
    links: List[WebLinkInfo] = Field(description="链接列表")


class SourceOutput(BaseModel):
    """资源的输出"""
    links: List[str] = Field(description="链接列表")
