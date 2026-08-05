"""
Phase 5 · 示例 1：手写一个「多 Agent 小队」（模拟 CrewAI 的 crew）
===================================================================
目的：不装 CrewAI，用最朴素的方式演示「多 Agent 协作」的本质——
所谓 crew，不过是把几个角色串成一条流水线：前一个 Agent 的输出，
是后一个 Agent 的输入。这不就是一张「线性图」吗？

角色（每个角色 = 一个节点 / 一个 prompt 模板）：
  - Researcher（研究员）：针对主题产出要点
  - Writer（写手）：把要点扩写成一段文字
  - Reviewer（审校）：审视文字，给出改进建议

流水线（边）：
  topic --> Researcher --> Writer --> Reviewer
"""

from langchain_core.messages import SystemMessage, HumanMessage

from examples.common.llm import get_chat_model


RESEARCHER_SYS = "你是一名严谨的研究员。给定主题，只输出 3 条关键要点，每条一行，不要解释。"
WRITER_SYS = "你是一名技术写手。基于给定的要点，写一段连贯、通俗的中文介绍（不超过 120 字）。"
REVIEWER_SYS = "你是一名审校。基于写手草稿，给出 2 条具体、可执行的改进建议，每条一行。"


def run_node(system: str, user: str) -> str:
    """一个通用「节点」：拿 system + user 输入，产出文本。"""
    model = get_chat_model()
    msg = model.invoke([SystemMessage(content=system), HumanMessage(content=user)])
    return msg.content.strip()


def run_crew(topic: str):
    print(f"# 主题：{topic}\n")

    # 节点 1：研究员
    research = run_node(RESEARCHER_SYS, f"主题：{topic}")
    print("【Researcher 要点】\n" + research + "\n")

    # 节点 2：写手（输入 = 研究员输出）
    draft = run_node(WRITER_SYS, f"要点：\n{research}")
    print("【Writer 草稿】\n" + draft + "\n")

    # 节点 3：审校（输入 = 写手输出）
    review = run_node(REVIEWER_SYS, f"草稿：\n{draft}")
    print("【Reviewer 建议】\n" + review + "\n")

    return {"research": research, "draft": draft, "review": review}


if __name__ == "__main__":
    run_crew("为什么大多数 Agent 框架都能映射到状态图？")
