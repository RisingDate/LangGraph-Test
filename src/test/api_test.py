"""
    测试API是否存活
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
from langchain_ollama.llms import OllamaLLM

load_dotenv()
model_name = [
    'gpt-3.5-turbo-0125',
    'gpt-3.5-turbo-0613',
    'gpt-3.5-turbo-instruct',
    'gpt-3.5-turbo',
    'gpt-4-0125-preview',
    'gpt-4-1106-preview',
    'gpt-4-all',
    'gpt-4-gizmo-*',
    'gpt-4-turbo-2024-04-09',
    'gpt-4-turbo-preview',
    'gpt-4-turbo',
    'gpt-4-vision-preview',
    'gpt-4.1-2025-04-14',
    'gpt-4.1-mini-2025-04-14',
    'gpt-4.1-mini',
    'gpt-4.1-nano-2025-04-14',
    'gpt-4.1-nano',
    'gpt-4.1',
    'gpt-4.5-preview-2025-02-27',
    'gpt-4',
    'gpt-4o-2024-05-13',
    'gpt-4o-2024-08-06',
    'gpt-4o-2024-11-20',
    'gpt-4o-all',
    'gpt-4o-image',
    'gpt-4o-mini-2024-07-18',
    'gpt-4o-mini',
    'gpt-4o-plus',
    'gpt-4o',
    'gpt-image-1',
    'grok-4',
    'qwen3-235b-a22b-instruct-2507',
    'qwen3-coder-480b-a35b-instruct',
    'qwen3-coder-plus',
    'glm-4.1v-thinking-flash',
    'glm-4.5-flash',
    'glm-4.5-air',
    'glm-4.5',
    'gpt-oss-120b',
    'gpt-oss-20b',
    'claude-opus-4-1-20250805',
    'claude-opus-4-1-20250805-thinking',
    'gpt-5-nano-2025-08-07',
    'gpt-5-nano',
    'gpt-5-mini-2025-08-07',
    'gpt-5-mini',
    'gpt-5-chat-latest'
]

client = OpenAI(
    base_url=os.getenv("LOCATED_API_KEY"),
    api_key=os.getenv("QWEN_BASE_URL")
)
response = None
print('test begin')
try:
    response = client.chat.completions.create(
        model="qwen3-235b-a22b:q4",
        messages=[
            {"role": "user", "content": "天津大学怎么样。"}
        ],
    )
    # print(response)
    print(response.choices[0].message.content)

except Exception as e:
    print(e)


