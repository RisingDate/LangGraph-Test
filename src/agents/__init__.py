"""
图的蓝图 (Graph Blueprint)

作用：
使用 `StateGraph` 将节点和边连接起来的地方。

内容：
这里定义了 `workflow.add_node` 和 `workflow.add_edge` 的逻辑，并最终执行 `workflow.compile()`。
它是整个逻辑的“大脑”入口。
"""

