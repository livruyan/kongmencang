"""
Phase 10 · 记忆独立层：episodic + semantic + 溯源（防幻觉）
=========================================================================
目的：把「记忆」从 RAG 的附庸里解放出来，做成可溯源的独立层，并演示它如何
从机制上抑制幻觉。对应改进报告 P0「记忆独立层」。

要点：
  1. Episodic（情节记忆）：一次会话里发生的事件，可回放；
  2. Semantic（语义记忆）：从对话中提炼的「事实」，长期沉淀、跨会话复用；
  3. Traceability（溯源）：每条语义记忆都带 source_ref，回答必须引用来源；
  4. 防幻觉开关：检索不到来源时，模型不应断言，而是明确说「记忆里没有」。

运行 / Run:
    python -m examples.p10.hello_chain
    # 或 make run p=10
"""
from langchain_core.messages import HumanMessage

from examples.common.llm import get_chat_model
from examples.common.memory import MemoryStore


def seed_memory(ms: MemoryStore) -> None:
    """模拟一段对话：把发生的事件写进 episodic，再把提炼出的事实写进 semantic。"""
    # --- 情节记忆：发生了什么 ---
    e1 = ms.add_episode("session-user", "user", "我们决定用 LangGraph 做多智能体编排。")
    e2 = ms.add_episode("session-user", "user", "部署目标环境是 Kubernetes，不用裸 Docker。")
    e3 = ms.add_episode("session-user", "assistant", "好的，那我把部署章节改成 K8s。")

    # --- 语义记忆：从上面提炼事实，并带来源（指向 episode id）---
    ms.add_semantic("编排框架选型为 LangGraph", f"episode:{e1}", "session-user")
    ms.add_semantic("部署目标环境为 Kubernetes", f"episode:{e2}", "session-user")
    print(f"已写入 3 条 episode（id={e1},{e2},{e3}），2 条 semantic 事实（带溯源）。")


def answer_guarded(ms: MemoryStore, question: str) -> str:
    """带防幻觉护栏的回答：先检索带引用的记忆，再决定是否允许模型断言。"""
    ctx = ms.build_citation_context(question)
    if not ctx:
        # 关键防幻觉逻辑：没有来源，绝不让模型凭空编
        return "（记忆中无相关来源，按防幻觉策略拒答）我无法从已知记忆中找到依据，请补充信息。"

    model = get_chat_model()
    prompt = (
        "你是一个严谨的助手。下面是你「可溯源」的记忆（每条都带 [来源]）。\n"
        "只能依据这些记忆回答，并在答案末尾标注引用；不要编造记忆之外的信息。\n\n"
        f"【记忆】\n{ctx}\n\n"
        f"【问题】{question}"
    )
    return model.invoke([HumanMessage(content=prompt)]).content.strip()


def main() -> None:
    ms = MemoryStore()  # :memory: 演示；生产可传文件路径做持久化
    seed_memory(ms)

    print("\n===== 用例 1：有来源的问题（应带引用回答）=====")
    q1 = "我们选了什么编排框架？部署环境是什么？"
    print("Q:", q1)
    print("A:", answer_guarded(ms, q1))

    print("\n===== 用例 2：无来源的问题（防幻觉护栏应拦下）=====")
    q2 = "我们的数据库用的是 MySQL 还是 Postgres？"
    print("Q:", q2)
    print("A:", answer_guarded(ms, q2))

    print("\n===== 记忆检索明细（验证溯源）=====")
    for hit in ms.retrieve_semantic("部署"):
        print(f"  semantic#{hit.id} fact='{hit.fact}' source={hit.source_ref}")
        ep = ms.get_episode(int(hit.source_ref.split(":")[-1]))
        if ep:
            print(f"    -> 溯源 episode#{ep.id} [{ep.role}]: {ep.content}")

    ms.close()


if __name__ == "__main__":
    main()
