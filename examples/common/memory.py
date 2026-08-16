"""记忆独立层 / Independent Memory Layer.
=========================================================================
把「记忆」从 RAG 的附庸中解放出来，做成可溯源的独立层。这是生产级多智能体
系统相对「教程版快照记忆」的关键升级，也是防幻觉（hallucination）的核心机制。

本模块提供三层结构 / Three layers:

  1. Episodic（情节记忆）
     一次会话 / 任务中发生的「事件」：谁说了什么、工具返回了什么、何时发生。
     带 session_id、role、时间戳，可回放。

  2. Semantic（语义记忆）
     从对话 / 文档中提炼出的「事实 / 知识」，长期沉淀、跨会话复用。
     例如：用户偏好、已确认的项目决策、外部实体属性。

  3. Traceability（溯源）
     每条 semantic 记忆都记录 source_ref（来自哪条 episode），以及 session / turn。
     回答时**必须引用来源**；查询不到来源时，系统不应断言 —— 这就是防幻觉开关。

设计取舍 / Design notes:
  - 默认后端为 SQLite（Python 标准库，零额外依赖，可持久化到磁盘）。
  - 检索采用**字符级 n-gram 重合**的朴素词法召回（对中文鲁棒、零依赖、无需
    embedding），因此离线 / 无 API key 也能跑通，便于把「记忆层」与「向量检索」
    解耦演示。若接入 embedding，可替换为向量召回（retrieve_semantic 接口不变）。

典型用法见 examples/p10/hello_chain.py。
"""

from __future__ import annotations

import os
import sqlite3
import time
from dataclasses import dataclass
from typing import Optional


# ---------------------------------------------------------------------------
# 数据模型 / Records
# ---------------------------------------------------------------------------
@dataclass
class Episode:
    id: int
    session_id: str
    role: str
    content: str
    created_at: float


@dataclass
class SemanticMemory:
    id: int
    fact: str
    source_ref: str          # 例如 "episode:12" 或 "doc:readme.md#line30"
    session_id: str
    created_at: float


# ---------------------------------------------------------------------------
# 记忆独立层 / MemoryStore
# ---------------------------------------------------------------------------
class MemoryStore:
    """可溯源的记忆存储。支持内存模式与 SQLite 持久化模式。"""

    def __init__(self, db_path: str = ":memory:"):
        # db_path=":memory:" 为纯演示；传入文件路径则落盘持久化。
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    # -- schema ----------------------------------------------------------
    def _init_schema(self) -> None:
        cur = self._conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS episodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at REAL NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS semantic (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fact TEXT NOT NULL,
                source_ref TEXT NOT NULL,
                session_id TEXT NOT NULL,
                created_at REAL NOT NULL
            )
            """
        )
        self._conn.commit()

    # -- episodic --------------------------------------------------------
    def add_episode(self, session_id: str, role: str, content: str) -> int:
        cur = self._conn.cursor()
        cur.execute(
            "INSERT INTO episodes (session_id, role, content, created_at) "
            "VALUES (?, ?, ?, ?)",
            (session_id, role, content, time.time()),
        )
        self._conn.commit()
        return cur.lastrowid

    def get_episode(self, episode_id: int) -> Optional[Episode]:
        row = self._conn.execute(
            "SELECT * FROM episodes WHERE id = ?", (episode_id,)
        ).fetchone()
        return Episode(**row) if row else None

    def retrieve_episodes(self, session_id: str, limit: int = 20) -> list[Episode]:
        rows = self._conn.execute(
            "SELECT * FROM episodes WHERE session_id = ? "
            "ORDER BY created_at DESC LIMIT ?",
            (session_id, limit),
        ).fetchall()
        return [Episode(**r) for r in rows]

    # -- semantic --------------------------------------------------------
    def add_semantic(self, fact: str, source_ref: str, session_id: str = "global") -> int:
        cur = self._conn.cursor()
        cur.execute(
            "INSERT INTO semantic (fact, source_ref, session_id, created_at) "
            "VALUES (?, ?, ?, ?)",
            (fact, source_ref, session_id, time.time()),
        )
        self._conn.commit()
        return cur.lastrowid

    def get_semantic(self, semantic_id: int) -> Optional[SemanticMemory]:
        row = self._conn.execute(
            "SELECT * FROM semantic WHERE id = ?", (semantic_id,)
        ).fetchone()
        return SemanticMemory(**row) if row else None

    def list_semantic(self) -> list[SemanticMemory]:
        """返回全部语义记忆（用于演示「溯源全貌」）。"""
        rows = self._conn.execute(
            "SELECT * FROM semantic ORDER BY id"
        ).fetchall()
        return [SemanticMemory(**r) for r in rows]

    @staticmethod
    def _char_ngrams(text: str, n: int = 2) -> set[str]:
        """把文本转成字符级 n-gram 集合（去标点、统一小写）。

        对中文按字切、英文按词根也能覆盖，是零依赖的跨语言相似度基线。
        """
        cleaned = "".join(ch for ch in text if ch.isalnum())
        cleaned = cleaned.lower()
        if len(cleaned) == 0:
            return set()
        if len(cleaned) < n:
            return {cleaned}
        return {cleaned[i : i + n] for i in range(len(cleaned) - n + 1)}

    def _overlap_score(self, a: str, b: str) -> int:
        """字符级 n-gram 重合度，作为朴素词法相似度分数。"""
        return len(self._char_ngrams(a) & self._char_ngrams(b))

    def retrieve_semantic(self, query: str, top_k: int = 3) -> list[SemanticMemory]:
        """按词法重合度召回语义记忆，并附带来源引用。

        采用字符级 n-gram 重合（对中文鲁棒、无需 embedding）。返回与查询
        有重合的语义记忆，按重合度降序；无任何重合则返回空列表。
        """
        rows = self._conn.execute("SELECT * FROM semantic").fetchall()
        scored = []
        for r in rows:
            score = self._overlap_score(query, r["fact"])
            # 阈值过滤：要求至少 2 个 n-gram 重合，避免 "gr" 这类偶然单字重合误召回
            if score >= 2:
                scored.append((score, r))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [SemanticMemory(**r) for _, r in scored[:top_k]]

    # -- 防幻觉：把记忆拼成带引用的上下文 --------------------------------
    def build_citation_context(self, query: str, top_k: int = 3) -> str:
        """返回带 [来源] 标注的上下文；无来源时返回空串。

        调用方应把该字符串注入 prompt；若为空，则**不应让模型凭空断言**，
        而应让它明确说「记忆中没有相关信息」。
        """
        hits = self.retrieve_semantic(query, top_k=top_k)
        if not hits:
            return ""
        lines = []
        for h in hits:
            src = f"episode:{h.source_ref.split(':')[-1]}" if h.source_ref.startswith("episode:") \
                else h.source_ref
            lines.append(f"- [{src}] {h.fact}")
        return "\n".join(lines)

    def close(self) -> None:
        self._conn.close()
