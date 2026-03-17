# LangGraph-Test
LangGraph测试

在使用 LangGraph 构建生产级后端系统时，代码结构通常遵循**“关注点分离”**的原则。由于 LangGraph 的核心是**状态（State）**、**节点（Nodes）**和**边（Edges）**，文件夹结构通常会围绕这些概念展开。

以下是一个典型的 LangGraph 后端项目目录结构及其详细作用：

------

### 📂 典型的项目目录结构

Plaintext

```
├── src/
│   ├── agents/             # 图的入口与组合 (Graphs)
│   ├── nodes/              # 节点逻辑 (具体的函数)
│   ├── chains/             # 封装好的 LangChain 链
│   ├── state/              # 状态定义 (State Schema)
│   ├── tools/              # 外部工具 (API 调用, 数据库查询)
│   ├── prompts/            # 提示词模板
│   ├── schema/             # 输入输出的 Pydantic 模型
│   ├── persistence/        # 持久化层 (Checkpointers)
│   └── utils/              # 通用工具函数
├── langgraph.json          # LangGraph Cloud 配置文件
├── main.py                 # FastAPI 启动入口
└── .env                    # 环境配置
```

------

### 🔍 各文件夹详细作用

#### 1. `state/` (记忆中枢)

- **作用**：定义整个图共享的 `TypedDict` 或 `Dataclass`。

- **内容**：规定了哪些数据会在节点之间传递。

  > **Tip**: 建议将 `State` 单独抽离，因为 `nodes` 和 `agents` 都会频繁引用它。

#### 2. `nodes/` (打工人)

- **作用**：存放图中每一个节点的业务逻辑。
- **内容**：每个文件通常是一个接收 `State` 并返回 `Partial State` 的异步函数。
  - 例如：`llm_node.py` (调用模型), `search_node.py` (搜索信息), `format_node.py` (格式化输出)。

#### 3. `agents/` (图的蓝图)

- **作用**：使用 `StateGraph` 将节点和边连接起来的地方。
- **内容**：这里定义了 `workflow.add_node` 和 `workflow.add_edge` 的逻辑，并最终执行 `workflow.compile()`。它是整个逻辑的“大脑”入口。

#### 4. `tools/` (工具箱)

- **作用**：存放 LLM 可以调用的外部工具。
- **内容**：使用 `@tool` 装饰器的函数。比如数据库 CRUD 操作、调用第三方天气 API 或执行 Python 代码。

#### 5. `prompts/` (剧本)

- **作用**：集中管理所有的 Prompt。
- **内容**：将复杂的 System Message 或提示词模板从逻辑代码中分离出来，方便后期调优和多语言管理。

#### 6. `schema/` (契约)

- **作用**：定义 API 的 Request 和 Response 格式。
- **内容**：通常使用 **Pydantic**。虽然 `state` 定义了内部流转，但 `schema` 定义了外部用户看到的接口样子。

#### 7. `persistence/` (存档点)

- **作用**：管理图的状态持久化。
- **内容**：配置 `MemorySaver`、`PostgresSaver` 或 `RedisSaver`。这能让你的 Agent 具备“长时记忆”，即便服务器重启也能恢复之前的对话进度。

