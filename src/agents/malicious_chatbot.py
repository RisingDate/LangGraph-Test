import sys
from typing import Annotated

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict

from src.agents.baseLLM import BaseLLM


# 定义状态机
class State(TypedDict):
    # 消息的类型为list, add_messages函数
    # 每次请求都是将消息附加到列表中，而不是覆盖它们
    messages: Annotated[list, add_messages]


# 初始化 图 容器
graph_builder = StateGraph(State)
# 初始化模型
# llm = BaseLLM(model_name='qwen').get_llm('qwen')
llm = init_chat_model(model=f"openai:gpt-4o")


def chatbot(state: State):
    return {'messages': [llm.invoke(state['messages'])]}


graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot") # 等同于graph_builder.set_entry_point("chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()
from IPython.display import Image, display

display(Image(graph.get_graph().draw_mermaid_png()))

sys.exit(0)
for event in graph.stream({"messages": [{"role": "user", "content": "你是谁"}]}):
    for value in event.values():
        print("Assistant:", value["messages"][-1].content)