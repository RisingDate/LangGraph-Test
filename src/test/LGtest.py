import os
import sys

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.tools.weather_getter import get_weather
from src.agents.baseLLM import BaseLLM
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AnyMessage
from pydantic import BaseModel


class WeatherResponse(BaseModel):
    conditions: str


def get_prompt(state: AgentState, config: RunnableConfig) -> list[AnyMessage]:
    user_name = config["configurable"].get("user_name")
    vip_level = config["configurable"].get("vip_level")
    if vip_level >= 3:
        system_msg = f"你是一位专业的高级顾问。请以最尊敬和详细的方式为尊贵的{user_name}提供服务，提供深度分析和建议。"
    elif vip_level >= 1:
        system_msg = f"你是一位友好的助手。请为{user_name}提供周到的服务和详细的信息。"
    else:
        system_msg = f"你是一个智能助手。请简洁地回答{user_name}的问题。"
    return [{"role": "system", "content": system_msg}] + state["messages"]


basellm = BaseLLM(model_name='qwen')

# 配置 LLM
llm = basellm.get_llm('qwen')
checkpointer = InMemorySaver()  # 内存节点

agent = create_react_agent(
    model=llm,
    tools=[get_weather],
    prompt=get_prompt,
    checkpointer=checkpointer,
    response_format=WeatherResponse
)

res1 = agent.invoke(
    {"messages": [{"role": "user", "content": "bj的天气如何？"}]},
    config={"configurable": {"user_name": "小田老板", "vip_level": 2, "thread_id": 0}}
)
res2 = agent.invoke(
    {"messages": [{"role": "user", "content": "我前面的问题是啥"}]},
    config={"configurable": {"user_name": "小田老板", "vip_level": 2, "thread_id": 0}}
)
print(res1["structured_response"])
print(res1["messages"][-1].content)
print(res2["messages"][-1].content)
# res2 = agent.invoke(
#     {"messages": [{"role": "user", "content": "bj的天气如何？"}]},
#     config={"configurable": {"user_name": "小田老板", "vip_level": 2, "thread_id": 1}}
# )
# res3 = agent.invoke(
#     {"messages": [{"role": "user", "content": "bj的天气如何？"}]},
#     config={"configurable": {"user_name": "小田同学", "vip_level": 0, "thread_id": 2}}
# )
# print("=== 普通用户 (VIP 0) ===")
# print(res3["messages"][-1].content)
#
# print("=== 普通会员 (VIP 2) ===")
# print(res2["messages"][-1].content)
#
# print("=== 尊贵会员 (VIP 5) ===")
# print(res1["messages"][-1].content)
# rich.print(res1)
