"""Phase 5 · 双 Agent 辩论 / Two-agent debate.

模拟 AutoGen group-chat 的一种形态：两个角色交替发言、互相挑战，由一个简单的
「轮次循环」驱动。你会发现它仍是「节点 + 顺序/条件边」。
One shape of an AutoGen group-chat: two roles take turns challenging each other,
driven by a simple turn loop. Still "nodes + edges" underneath.
"""
from langchain_core.prompts import ChatPromptTemplate
from examples.common.llm import get_chat_model

PRO = ChatPromptTemplate.from_messages([
    ("system", "你是正方，支持观点：{topic}。回应反方上一轮。"),
    ("human", "反方说：{counter}"),
])
CON = ChatPromptTemplate.from_messages([
    ("system", "你是反方，质疑观点：{topic}。回应正方上一轮。"),
    ("human", "正方说：{statement}"),
])


def main():
    llm = get_chat_model(temperature=0.8)
    topic = "AI 会提升而非取代程序员"
    statement = "AI 能自动完成大量重复编码工作。"
    for _ in range(2):
        counter = llm.invoke(
            CON.format_prompt(topic=topic, statement=statement)
        ).content
        print("反方：", counter)
        statement = llm.invoke(
            PRO.format_prompt(topic=topic, counter=counter)
        ).content
        print("正方：", statement)


if __name__ == "__main__":
    main()
