"""
Phase 5 · 示例 2：协调者路由到不同专家（模拟 AutoGen group-chat 的条件边）
============================================================================
目的：演示 AutoGen 那类「群聊」的核心机制——一个协调者（coordinator）
根据对话决定「下一个该谁说话」，这就是**条件边**：下一个节点不是固定的，
而是由模型在运行时决策。

专家（节点）：
  - math_agent：数学
  - language_agent：语言/翻译
  - code_agent：代码

协调者（条件判断）：读取用户请求，输出要派给哪个专家。
如果把「协调者」和「专家」都看作节点，那么「派给谁」就是条件边。
"""

from langchain_core.messages import SystemMessage, HumanMessage

from examples.common.llm import get_chat_model

EXPERT_SYS = {
    "math": "你是数学专家，只回答数学计算/推理问题，简洁给出答案。",
    "language": "你是语言专家，只回答翻译/语法/用词问题，简洁给出答案。",
    "code": "你是编程专家，只回答代码相关问题，给出简明示例或解释。",
}

COORDINATOR_SYS = (
    "你是协调者。给定用户请求，判断它属于哪一类，"
    "只回复一个词：math / language / code。不要解释。"
)


def coordinate(question: str) -> str:
    model = get_chat_model()
    msg = model.invoke([
        SystemMessage(content=COORDINATOR_SYS),
        HumanMessage(content=question),
    ])
    choice = msg.content.strip().lower()
    return choice if choice in EXPERT_SYS else "code"


def run_router(question: str):
    print(f"# 用户请求：{question}\n")

    # 条件边：协调者决定下一个节点
    routed = coordinate(question)
    print(f"【Coordinator 路由】-> {routed}_agent\n")

    # 执行被路由到的专家节点
    model = get_chat_model()
    answer = model.invoke([
        SystemMessage(content=EXPERT_SYS[routed]),
        HumanMessage(content=question),
    ])
    print(f"【{routed}_agent 回答】\n" + answer.content.strip())
    return answer.content.strip()


if __name__ == "__main__":
    run_router("请把 'state graph' 翻译成中文。")
    print("\n" + "=" * 40 + "\n")
    run_router("求 1 到 100 的和。")
