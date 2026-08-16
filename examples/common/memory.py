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
  - 检索默认走关键词（FTS5，不可用时退化为 LIKE），不强制依赖 embedding，
    因此离线 / 无 API key 也能跑通，便于把「记忆层」与「向量检索」解耦演示。
  - 若提供了 embedding，可用向量召回做语义检索（retrieve_semantic 预留接口）。

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
        # 尝试启用 FTS5（多数 Python 自带）；失败则回退到 LIKE 检索。
        self._has_fts = False
        try:
            cur.execute(
                "CREATE VIRTUAL TABLE IF NOT EXISTS semantic_fts "
                "USING fts5(fact, content='semantic', content_rowid='id')"
            )
            self._has_fts = True
        except sqlite3.OperationalError:
            self._has_fts = False
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
        sid = cur.lastrowid
        if self._has_fts:
            cur.execute(
                "INSERT INTO semantic_fts (rowid, fact) VALUES (?, ?)", (sid, fact)
            )
        self._conn.commit()
        return sid

    def get_semantic(self, semantic_id: int) -> Optional[SemanticMemory]:
        row = self._conn.execute(
            "SELECT * FROM semantic WHERE id = ?", (semantic_id,)
        ).fetchone()
        return SemanticMemory(**row) if row else None

    def retrieve_semantic(self, query: str, top_k: int = 3) -> list[SemanticMemory]:
        """按关键词召回语义记忆，并附带来源引用。"""
        if self._has_fts:
            rows = self._conn.execute(
                "SELECT s.* FROM semantic_fts f "
                "JOIN semantic s ON s.id = f.rowid "
                "WHERE semantic_fts MATCH ? ORDER BY rank LIMIT ?",
                (query, top_k),
            ).fetchall()
        else:
            like = f"%{query}%"
            rows = self._conn.execute(
                "SELECT * FROM semantic WHERE fact LIKE ? LIMIT ?", (like, top_k)
            ).fetchall()
        return [SemanticMemory(**r) for r in rows]

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
