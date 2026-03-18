from langchain_openai import ChatOpenAI


class BaseLLM:
    def __init__(self, model_name='qwen'):
        self.model_name = model_name

    def generate_response(self, prompt):
        raise NotImplementedError("Subclasses must implement this method")

    def get_llm(self, model_name=None):
        # 这里可以根据 model_name 返回不同的 LLM 实例
        if model_name is None:
            model_name = self.model_name
        if model_name == 'qwen':
            llm = ChatOpenAI(
                api_key="eihei_23333",
                base_url="http://127.0.0.1:8600/v1",
                model="qwen3.5-122b-a10b:q8",
                temperature=0.7,
                top_p=0.8,
                presence_penalty=1.5,
                model_kwargs={
                    "extra_body": {
                        "top_k": 20,
                        "chat_template_kwargs": {"enable_thinking": False}
                    }
                }
            )
        else:
            llm = None

        return llm