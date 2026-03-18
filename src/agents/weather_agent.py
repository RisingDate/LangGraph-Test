import os
import sys

# 将项目根目录添加到 python path，确保可以使用 src.tools
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import render_text_description
from src.tools.weather_getter import get_weather
from src.agents.baseLLM import BaseLLM
from langgraph.prebuilt import create_react_agent
import re

load_dotenv()
basellm = BaseLLM(model_name='qwen')

# 配置 LLM
llm = basellm.get_llm('qwen')

agent = create_react_agent(
    model=llm, # 目前没有豆包的，但是使用openai的格式是可以调通的
    tools=[get_weather],
    prompt="You are a helpful assistant",
)

res = agent.invoke(
    {"messages": [{"role": "user", "content": "北京的天气如何？"}]}
)
print(res)
sys.exit(0)


# 定义 ReAct Prompt
template = '''你是一个智能助手。请回答用户的问题。
你可以使用以下工具：

{tools}

请使用以下格式：

Question: 用户的问题
Thought: 你应该思考该做什么
Action: 采取的行动，必须是 [{tool_names}] 之一
Action Input: 行动的输入
Observation: 行动的结果
... (Thought/Action/Action Input/Observation 可以重复此步骤)
Thought: 我现在知道最终答案了
Final Answer: 最终答案

开始！

Question: {input}
Thought:{agent_scratchpad}'''

prompt = PromptTemplate.from_template(template)
tools = [get_weather]
prompt = prompt.partial(
    tools=render_text_description(tools),
    tool_names=", ".join([t.name for t in tools]),
)


def simple_agent(user_input):
    scratchpad = ""
    print(f"Question: {user_input}\n", flush=True)

    # 简单的循环执行
    for step in range(5):
        # 1. 生成 Prompt 并调用 LLM
        formatted_prompt = prompt.format(input=user_input, agent_scratchpad=scratchpad)
        response = llm.bind(stop=["\nObservation"]).invoke(formatted_prompt)
        result_text = response.content

        # 打印模型生成的内容（Thought + Action）
        print(result_text, flush=True)

        scratchpad += result_text

        # 2. 检查是否有 Final Answer
        if "Final Answer:" in result_text:
            return

        # 3. 解析 Action
        regex = r"Action:\s*(.*?)\nAction Input:\s*(.*)"
        match = re.search(regex, result_text, re.DOTALL)

        if match:
            tool_name = match.group(1).strip()
            tool_input = match.group(2).strip().strip('"\'')

            # 4. 执行工具
            observation = "Tool not found"
            for tool in tools:
                if tool.name == tool_name:
                    try:
                        observation = tool.invoke(tool_input)
                    except Exception as e:
                        observation = f"Error: {e}"
                    break

            # 打印并追加观察结果
            obs_str = f"\nObservation: {observation}\n"
            print(obs_str, flush=True)
            scratchpad += obs_str
        else:
            # 如果没有 Action 也没 Final Answer，可能模型在瞎聊，结束
            if "Action:" not in result_text:
                print("\n[Finished without Final Answer]", flush=True)
                return


if __name__ == "__main__":
    simple_agent("tj的天气如何？")
