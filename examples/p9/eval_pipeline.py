"""Phase 9 · 简易评测 / Minimal eval harness.

Agent 上线前需要评测。这里给出一个基于「断言」的最小评测框架雏形：用一组用例
检查输出是否包含必要关键字，算出通过率。
Before shipping an Agent you need evals. Here's a minimal assertion-based eval
harness skeleton: a set of cases checks whether outputs contain required
keywords, then we compute a pass rate.
"""
from examples.common.llm import get_chat_model


def ask(question: str) -> str:
    return get_chat_model().invoke(question).content


def run_cases(cases: list[dict]) -> float:
    passed = 0
    for c in cases:
        out = ask(c["question"]).lower()
        ok = all(k in out for k in c["must_contain"])
        passed += ok
        print(f"[{'PASS' if ok else 'FAIL'}] {c['question']} -> {out[:40]}...")
    return passed / len(cases)


def main():
    cases = [
        {"question": "1+1 等于几？", "must_contain": ["2"]},
        {"question": "中国的首都是哪里？", "must_contain": ["北京"]},
    ]
    score = run_cases(cases)
    print(f"\n通过率 / Pass rate: {score:.0%}")


if __name__ == "__main__":
    main()
