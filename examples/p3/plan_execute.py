"""Phase 3 · Plan-and-Execute 模式 / Plan-and-Execute.

把一个大任务先拆成有序步骤（规划），再逐步执行（执行）。这是自主 Agent 的常见变体，
也揭示了「Agent 循环」可以是「规划节点 → 多轮执行节点」的组合。
Plan a task into ordered steps, then execute them one by one. A common Agent
variant; it shows the "agent loop" can be "planner node -> repeated executor
nodes".
"""
from langchain_core.prompts import ChatPromptTemplate
from examples.common.llm import get_chat_model

PLANNER = ChatPromptTemplate.from_messages([
    ("system", "把用户目标拆成 3 个有序步骤，每行一个，不要编号以外的解释。"),
    ("human", "{goal}"),
])

EXECUTOR = ChatPromptTemplate.from_messages([
    ("system", "你是执行者，请只完成下面这一步，给出简短结果。"),
    ("human", "步骤：{step}"),
])


def main():
    llm = get_chat_model()
    goal = "向完全不懂编程的人解释 Agent 是什么"
    plan = llm.invoke(PLANNER.format_prompt(goal=goal)).content
    steps = [s.strip() for s in plan.splitlines() if s.strip()]

    print("=== 计划 / Plan ===")
    for s in steps:
        print("-", s)

    print("\n=== 执行 / Execute ===")
    for step in steps:
        result = llm.invoke(EXECUTOR.format_prompt(step=step)).content
        print(f"[{step}]\n{result}\n")


if __name__ == "__main__":
    main()
