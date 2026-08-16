"""统一 LLM Provider 抽象层 / Unified LLM Provider abstraction.

读者只需在 .env 中设置 LLM_PROVIDER 与对应 key，即可在所有示例中无缝切换模型。
Readers only need to set LLM_PROVIDER and the matching key in .env to switch
models across every example.

支持的 provider / Supported providers:
  - openai   : 官方 OpenAI（默认 / default）
  - deepseek : DeepSeek（OpenAI 兼容接口 / OpenAI-compatible）
  - qwen     : 通义千问（阿里 DashScope，OpenAI 兼容接口 / OpenAI-compatible）
  - ollama   : 本地 Ollama（免 key / key-free，前几章推荐 / recommended early on）
"""
from typing import Optional

import os

from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()


def get_chat_model(temperature: float = 0.0, model: Optional[str] = None):
    """返回一个 LangChain ChatModel 实例 / Return a LangChain ChatModel."""
    if PROVIDER == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=model or os.getenv("OLLAMA_MODEL", "qwen2.5:7b"),
            temperature=temperature,
        )

    if PROVIDER == "deepseek":
        from langchain_openai import ChatOpenAI

        api_key = os.getenv("DEEPSEEK_API_KEY")
        base_url = os.getenv("DEEPSEEK_BASE_URL")
        model = model or os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        if not api_key:
            raise RuntimeError(
                "未检测到 DeepSeek API key / no DeepSeek key found. 请在 .env 中设置 "
                "DEEPSEEK_API_KEY 为真实密钥，或将 LLM_PROVIDER 设为 ollama 使用本地模型。"
            )
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=api_key,
            base_url=base_url,  # None 时走官方地址 / official endpoint when None
        )

    if PROVIDER == "qwen":
        from langchain_openai import ChatOpenAI

        api_key = os.getenv("QWEN_API_KEY")
        base_url = os.getenv("QWEN_BASE_URL")
        model = model or os.getenv("QWEN_MODEL", "qwen-plus")
        if not api_key:
            raise RuntimeError(
                "未检测到通义千问 API key / no Qwen key found. 请在 .env 中设置 "
                "QWEN_API_KEY（即 DashScope API Key），或将 LLM_PROVIDER 设为 ollama。"
            )
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=api_key,
            base_url=base_url,  # DashScope 兼容地址 / DashScope-compatible endpoint when set
        )

    if PROVIDER == "openai":
        from langchain_openai import ChatOpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        if not api_key:
            raise RuntimeError(
                "未检测到 OpenAI API key / no OpenAI key found. 请在 .env 中设置 "
                "OPENAI_API_KEY，或将 LLM_PROVIDER 设为 ollama 使用本地模型。"
            )
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=api_key,
            base_url=base_url,  # None 时走官方地址 / official endpoint when None
        )

    raise ValueError(
        f"不支持的 LLM_PROVIDER / unsupported provider: {PROVIDER}"
    )


def get_embeddings(model: Optional[str] = None):
    """返回一个嵌入模型 / Return an embeddings model (for RAG)."""
    if PROVIDER == "ollama":
        from langchain_ollama import OllamaEmbeddings

        return OllamaEmbeddings(
            model=model or os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text"),
        )

    if PROVIDER == "deepseek":
        # DeepSeek 不提供 embedding 接口，RAG 章节仍使用 OpenAI 兼容嵌入。
        # DeepSeek has no embedding API; RAG examples fall back to OpenAI embeddings.
        from langchain_openai import OpenAIEmbeddings

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "DeepSeek 无 embedding 接口 / DeepSeek has no embedding API. "
                "请在 .env 中设置 OPENAI_API_KEY 用于 RAG，或将 LLM_PROVIDER 设为 ollama。"
            )
        return OpenAIEmbeddings(
            model=model or os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small"),
            api_key=api_key,
        )

    if PROVIDER == "qwen":
        # 通义千问 embedding 走 DashScope 兼容接口（text-embedding-v3 等）。
        from langchain_openai import OpenAIEmbeddings

        api_key = os.getenv("QWEN_API_KEY")
        base_url = os.getenv("QWEN_BASE_URL")
        if not api_key:
            raise RuntimeError(
                "未检测到通义千问 API key / no Qwen key found. 请在 .env 中设置 "
                "QWEN_API_KEY 用于 embedding，或将 LLM_PROVIDER 设为 ollama。"
            )
        return OpenAIEmbeddings(
            model=model or os.getenv("QWEN_EMBED_MODEL", "text-embedding-v3"),
            api_key=api_key,
            base_url=base_url,
        )

    if PROVIDER == "openai":
        from langchain_openai import OpenAIEmbeddings

        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        if not api_key:
            raise RuntimeError(
                "未检测到 OpenAI API key / no OpenAI key found. 请在 .env 中设置 "
                "OPENAI_API_KEY，或将 LLM_PROVIDER 设为 ollama 使用本地模型。"
            )
        return OpenAIEmbeddings(
            model=model or os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small"),
            api_key=api_key,
            base_url=base_url,
        )

    raise ValueError(
        f"不支持的 LLM_PROVIDER / unsupported provider: {PROVIDER}"
    )
