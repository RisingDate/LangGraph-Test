"""
"""
建议将 `State` 单独抽离，因为 `nodes` 和 `agents` 都会频繁引用它。
规定了哪些数据会在节点之间传递。
内容：

定义整个图共享的 `TypedDict` 或 `Dataclass`。
作用：

记忆中枢 (Memory Center)

