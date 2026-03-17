"""
存档点 (Checkpoints)

作用：
管理图的状态持久化。

内容：
配置 `MemorySaver`、`PostgresSaver` 或 `RedisSaver`。
这能让你的 Agent 具备“长时记忆”，即便服务器重启也能恢复之前的对话进度。
"""

