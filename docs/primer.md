# Phase 1 · Python / 环境速补（可跳过）

> 如果你已经熟悉 Python 与 LLM API 基础，可以跳过本章；需要时在目录里回看即可。

## 1. Python 速补 / Python Crash Course

### 变量与函数
```python
name = "LangGraph"          # 字符串 / string
count = 3                   # 整数 / int
items = [1, 2, 3]           # 列表 / list

def greet(concept: str) -> str:
    return f"Hello, {concept}!"

print(greet("StateGraph"))
```

### 类与导入
```python
from dataclasses import dataclass

@dataclass
class Node:
    name: str
    next: str | None = None
```

### 包与模块
- 一个目录里有 `__init__.py` 就是一个**包（package）**，可以被 `import`。
- 本项目示例都放在 `examples/` 包下，统一通过 `examples.common.llm` 引入模型。

## 2. 环境搭建 / Environment Setup

```bash
# 1. 创建并激活虚拟环境
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env             # 然后编辑 .env 选择 LLM_PROVIDER
```

## 3. LLM API 速览 / LLM API Primer

- **Token**：模型处理文本的最小单位（大致等于「词」或「字」的片段）。调用按 token 计费。
- **Chat Completion**：给模型一组「消息」（`system` 设定角色，`user` 是用户输入），模型返回回复。
- **API Key 安全**：key 永远不要写进代码或提交到 Git；把它放进 `.env`（已被 `.gitignore` 忽略），运行时读取。

```python
# LangChain 中最常见的调用形态：prompt | model
chain = prompt | model
result = chain.invoke({"concept": "状态图"})
```

下一步：[写你的第一个 Chain →](/p1-hello-chain)
