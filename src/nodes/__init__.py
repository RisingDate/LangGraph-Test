"""
打工人 (Workers)

作用：
存放图中每一个节点的业务逻辑。

内容：
每个文件通常是一个接收 `State` 并返回 `Partial State` 的异步函数。
例如：`llm_node.py` (调用模型), `search_node.py` (搜索信息), `format_node.py` (格式化输出)。
"""

