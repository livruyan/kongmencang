import { defineConfig } from 'vitepress'

// 中文侧边栏 / Chinese sidebar
const zhSidebar = [
  {
    text: '开始 / Getting Started',
    items: [
      { text: '项目简介', link: '/' },
      { text: 'Phase 1 · Python/环境速补（可跳过）', link: '/primer' },
      { text: 'Phase 1 · 第一个 Chain', link: '/p1-hello-chain' },
      { text: '扩展示例 · 流式输出', link: '/p1-hello-chain#extra-p1' },
    ],
  },
  {
    text: 'Phase 2 · Chains / Memory / RAG',
    items: [
      { text: 'Phase 2 · 组合链、记忆与 RAG', link: '/p2-chains-memory-rag' },
      { text: '扩展示例 · 带记忆的 RAG', link: '/p2-chains-memory-rag#extra-p2' },
    ],
  },
  {
    text: 'Phase 3 · Agent 原理',
    items: [
      { text: 'Phase 3 · 从 ReAct 到自主循环', link: '/p3-agent-principles' },
      { text: '扩展示例 · Plan-and-Execute', link: '/p3-agent-principles#extra-p3' },
    ],
  },
  {
    text: 'Phase 4 · Tools',
    items: [
      { text: 'Phase 4 · 工具：Agent 的能力来源', link: '/p4-tools' },
      { text: '扩展示例 · 结构化输出', link: '/p4-tools#extra-p4' },
    ],
  },
  {
    text: 'Phase 5 · 多 Agent 对比',
    items: [
      { text: 'Phase 5 · 多 Agent 工作流对比', link: '/p5-multi-agent' },
      { text: '扩展示例 · 双 Agent 辩论', link: '/p5-multi-agent#extra-p5' },
    ],
  },
  {
    text: 'Phase 6 · LangGraph 图编排',
    items: [
      { text: 'Phase 6 · 状态图、节点与条件边', link: '/p6-langgraph' },
      { text: '扩展示例 · 条件分支图', link: '/p6-langgraph#extra-p6' },
    ],
  },
  {
    text: 'Phase 7 · 工程化基石',
    items: [
      { text: 'Phase 7 · 人工介入与状态持久化', link: '/p7-hitl-persistence' },
      { text: '扩展示例 · 时间旅行', link: '/p7-hitl-persistence#extra-p7' },
    ],
  },
  {
    text: 'Phase 8 · 生产部署',
    items: [
      { text: 'Phase 8 · 从图到服务', link: '/p8-deployment' },
      { text: 'Docker 实战（容器化）', link: '/p8-deployment#docker' },
      { text: '云部署（CloudBase）', link: '/p8-deployment#cloud-deploy' },
      { text: '扩展示例 · 流式 API', link: '/p8-deployment#extra-p8' },
    ],
  },
  {
    text: 'Phase 9 · Capstone 与复盘',
    items: [
      { text: 'Phase 9 · 端到端系统与全景复盘', link: '/p9-capstone' },
      { text: '扩展示例 · 简易评测', link: '/p9-capstone#extra-p9' },
    ],
  },
]

// 英文侧边栏 / English sidebar
const enSidebar = [
  {
    text: 'Getting Started',
    items: [
      { text: 'Introduction', link: '/en/' },
      { text: 'Phase 1 · Python/Env Primer (skippable)', link: '/en/primer' },
      { text: 'Phase 1 · The First Chain', link: '/en/p1-hello-chain' },
      { text: 'Extra · Streaming', link: '/en/p1-hello-chain#extra-p1' },
    ],
  },
  {
    text: 'Phase 2 · Chains / Memory / RAG',
    items: [
      { text: 'Phase 2 · Composition, Memory & RAG', link: '/en/p2-chains-memory-rag' },
      { text: 'Extra · Conversational RAG', link: '/en/p2-chains-memory-rag#extra-p2' },
    ],
  },
  {
    text: 'Phase 3 · Agent Principles',
    items: [
      { text: 'Phase 3 · From ReAct to the Loop', link: '/en/p3-agent-principles' },
      { text: 'Extra · Plan-and-Execute', link: '/en/p3-agent-principles#extra-p3' },
    ],
  },
  {
    text: 'Phase 4 · Tools',
    items: [
      { text: 'Phase 4 · Tools: Agent Capability', link: '/en/p4-tools' },
      { text: 'Extra · Structured output', link: '/en/p4-tools#extra-p4' },
    ],
  },
  {
    text: 'Phase 5 · Multi-Agent',
    items: [
      { text: 'Phase 5 · Multi-Agent Compared', link: '/en/p5-multi-agent' },
      { text: 'Extra · Two-agent debate', link: '/en/p5-multi-agent#extra-p5' },
    ],
  },
  {
    text: 'Phase 6 · LangGraph',
    items: [
      { text: 'Phase 6 · State Graph & Edges', link: '/en/p6-langgraph' },
      { text: 'Extra · Branching graph', link: '/en/p6-langgraph#extra-p6' },
    ],
  },
  {
    text: 'Phase 7 · Production Basics',
    items: [
      { text: 'Phase 7 · HITL & Persistence', link: '/en/p7-hitl-persistence' },
      { text: 'Extra · Time travel', link: '/en/p7-hitl-persistence#extra-p7' },
    ],
  },
  {
    text: 'Phase 8 · Deployment',
    items: [
      { text: 'Phase 8 · Graph to Service', link: '/en/p8-deployment' },
      { text: 'Docker in practice', link: '/en/p8-deployment#docker' },
      { text: 'Cloud deploy (CloudBase)', link: '/en/p8-deployment#cloud-deploy' },
      { text: 'Extra · Streaming API', link: '/en/p8-deployment#extra-p8' },
    ],
  },
  {
    text: 'Phase 9 · Capstone & Retro',
    items: [
      { text: 'Phase 9 · System & Retrospective', link: '/en/p9-capstone' },
      { text: 'Extra · Minimal eval', link: '/en/p9-capstone#extra-p9' },
    ],
  },
]

export default defineConfig({
  title: 'LangChain & LangGraph 系统化学习',
  description: '从底层范式理解 Agent 编排：状态图 + 节点 + 条件边',
  locales: {
    root: {
      label: '简体中文',
      lang: 'zh-CN',
      themeConfig: {
        nav: [
          { text: '简介', link: '/' },
          { text: 'Phase 1', link: '/p1-hello-chain' },
          { text: 'Phase 2', link: '/p2-chains-memory-rag' },
          { text: 'Phase 3', link: '/p3-agent-principles' },
          { text: 'Phase 4', link: '/p4-tools' },
          { text: 'Phase 5', link: '/p5-multi-agent' },
          { text: 'Phase 6', link: '/p6-langgraph' },
          { text: 'Phase 7', link: '/p7-hitl-persistence' },
          { text: 'Phase 8', link: '/p8-deployment' },
          { text: 'Phase 9', link: '/p9-capstone' },
        ],
        sidebar: zhSidebar,
      },
    },
    en: {
      label: 'English',
      lang: 'en',
      link: '/en/',
      themeConfig: {
        nav: [
          { text: 'Intro', link: '/en/' },
          { text: 'Phase 1', link: '/en/p1-hello-chain' },
          { text: 'Phase 2', link: '/en/p2-chains-memory-rag' },
          { text: 'Phase 3', link: '/en/p3-agent-principles' },
          { text: 'Phase 4', link: '/en/p4-tools' },
          { text: 'Phase 5', link: '/en/p5-multi-agent' },
          { text: 'Phase 6', link: '/en/p6-langgraph' },
          { text: 'Phase 7', link: '/en/p7-hitl-persistence' },
          { text: 'Phase 8', link: '/en/p8-deployment' },
          { text: 'Phase 9', link: '/en/p9-capstone' },
        ],
        sidebar: enSidebar,
      },
    },
  },
  themeConfig: {
    socialLinks: [{ icon: 'github', link: 'https://github.com/' }],
    search: {
      provider: 'local',
    },
  },
})
