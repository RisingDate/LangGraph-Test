"""
    测试API是否存活
"""
import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

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
    api_key=os.getenv("LOCAL_API_KEY"),
    base_url=os.getenv("QWEN_BASE_URL")
)

print('test begin', flush=True)
messages = [
    {"role": "user", "content": "天津大学怎么样。"}
]
print("Stream Output:", flush=True)

try:
    response = client.chat.completions.create(
        model="qwen3.5-122b-a10b:q8",
        messages=messages,
        temperature=0.7,
        stream=True,
        top_p=0.8,
        presence_penalty=1.5,
        extra_body={
            "top_k": 20,
            "chat_template_kwargs": {"enable_thinking": True}
        }
    )

    for chunk in response:
        if chunk.choices and len(chunk.choices) > 0:
            content = chunk.choices[0].delta.content
            if content:
                print(content, end="", flush=True)
    print(flush=True)

except Exception as e:
    print(f"\nRequest Error: {e}", flush=True)

