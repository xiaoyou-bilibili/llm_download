from langchain.chat_models import ChatOpenAI
from agent.source.google import GoogleSpider
from base import Base, GOOGLE_SPIDER
from web import app

if __name__ == '__main__':
    base = Base()
    llm = ChatOpenAI(
        openai_api_key=base.openapi_key,
        openai_api_base=base.openapi_base,
        model_name="gpt-3.5-turbo",
        temperature=0,
    )
    # 配置相关服务
    app.config[GOOGLE_SPIDER] = GoogleSpider(base, llm)
    # 运行flask
    app.run(host='0.0.0.0', port=7001)

