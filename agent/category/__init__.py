from typing import Callable, Any
from agent.common import return_parse
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import tool, AgentExecutor
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.tools.render import format_tool_to_openai_function, convert_pydantic_to_openai_function
from agent.category.model import CategoryEnum, SourceInput, CategoryOutput
from base import Base
import requests
from langchain.output_parsers.enum import EnumOutputParser


class Category:
    def __init__(self, base: Base, llm: ChatOpenAI):
        self.__base = base
        self.__llm = llm
        self.__prompt = ChatPromptTemplate.from_messages([
            ("system",
             "你是一个判断资源类型的助手，你需要自己根据资源的描述或者自身的知识来进行推断，只返回资源类型"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        self.__tools = [self.__wiki()]
        self.__functions = [format_tool_to_openai_function(t) for t in self.__tools]
        self.__functions.append(convert_pydantic_to_openai_function(CategoryOutput))
        self.__agent = {
                           "input": lambda x: x["input"],
                           "agent_scratchpad": lambda x: format_to_openai_functions(x['intermediate_steps'])
                       } | self.__prompt | self.__llm.bind(functions=self.__functions) | return_parse("CategoryOutput",
                                                                                                      {
                                                                                                          "category": "其他"})
        self.__agent_execute = AgentExecutor(agent=self.__agent, tools=self.__tools, verbose=True)
        self.__parse = EnumOutputParser(enum=CategoryEnum)

    def __wiki(self) -> Callable[[str], Any]:
        @tool("wiki", args_schema=SourceInput)
        def spider(name: str) -> str:
            """查询wiki，返回资源的描述信息"""
            response = requests.get(
                "https://zh.wikipedia.org/api/rest_v1/page/summary/{}".format(name),
                proxies=self.__base.proxy,
                headers=self.__base.http_header,
            )
            data = response.json()
            if "extract" in data:
                return response.json()["extract"]
            else:
                return ""

        return spider

    def category(self, content: str) -> CategoryEnum:
        # 判断资源的类型
        response = self.__agent_execute.invoke({"input": content}, return_only_outputs=True)
        # 把资源类型解析为枚举
        return self.__parse.parse(response["category"])
