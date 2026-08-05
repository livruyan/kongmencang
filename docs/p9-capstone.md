# Phase 9 · Capstone 多 Agent 系统与 9 Phase 全景复盘

> 目标：用一个**端到端可运行**的多 Agent 系统把所有知识点串起来，并对整个课程做一次性复盘，给出进阶路线。

## Capstone：端到端研究系统

示例 `examples/p9/capstone.py` 把前面所有概念收进**一张 LangGraph 图**：

```
START -> coordinator
coordinator --(route)--> research / math
research -> writer -> reviewer -> approval
approval --(yes)--> publish
approval --(no)--> revise -> reviewer  (回环)
publish/revise -> END
```

它同时用到了：
- **Phase 4 工具**：research 节点调用 `search` 检索工具；
- **Phase 5 路由**：coordinator 按问题类型分流；
- **Phase 6 图**：StateGraph 显式建模节点/边/条件边；
- **Phase 7 HITL**：approval 节点用 `interrupt` 暂停等人类审批；
- **Phase 3 循环**：每个节点内部都是「思考→行动」的微观循环。

```bash
python -m examples.p9.capstone
```

这就是「范式统一论」的终极证明：**一个生产级多 Agent 系统，本质就是一张带工具、带条件边、可暂停的图。**

## 9 Phase 全景复盘

| Phase | 核心收获 | 对应的「图」概念 |
|-------|----------|------------------|
| 1 | LangChain 核心、第一个 Chain | Chain = 节点链 |
| 2 | 组合链、记忆、RAG | 节点链 + 状态（记忆/检索） |
| 3 | Agent 原理（ReAct 循环） | 思考/工具/观察节点 + 条件边 |
| 4 | Tools | 工具 = 节点；调用 = 条件边 |
| 5 | 多 Agent 对比 | CrewAI=线性图，AutoGen=条件边图 |
| 6 | LangGraph 图编排 | 通用「状态+节点+边」语言 |
| 7 | HITL + 持久化 | 人类决策边 + State 外置 |
| 8 | 生产部署 | 图 → 服务 → 容器 → 可观测 |
| 9 | Capstone + 复盘 | 全部整合为一张图 |

**一句话主线**：你从「调一个模型」出发，逐步认识到「所有 Agent 编排，最终都能用状态图统一表达」。这，就是本项目的核心主张。

## 进阶路线（学完之后去哪）

1. **子图与模块化**：把 Capstone 每个角色拆成子图，组合进更大系统（LangGraph subgraph）。
2. **持久化落地**：把 MemorySaver 换成 PostgresSaver / Redis，支撑真实多用户。
3. **可观测深化**：接 Langfuse，做成本/延迟/质量看板。
4. **评估体系**：用 LangSmith 数据集做回归评估，量化「改一处提示词，整体质量变化多少」。
5. **横向对比实战**：用 CrewAI / AutoGen 各写一遍 Capstone，真切体会「图范式」带来的可控性优势。

## 验收清单（毕业标准）

- [ ] 能独立从零搭建一个 LangGraph 多 Agent 系统（含工具、路由、HITL）
- [ ] 能把任意 Agent 框架的编排「翻译」成图
- [ ] 能说出本课程核心主张并举例证明
- [ ] 跑通过 Capstone 示例

---

🎓 **恭喜走完 9 个 Phase。** 你已具备「从底层范式理解 Agent」的能力，足以构建复杂、可控、可上线的 Agent 应用。

## 扩展示例 / Extra Example {#extra-p9}

### 简易评测（examples/p9/eval_pipeline.py）
上线前的兜底：用一组断言用例检查输出是否包含必要关键字，算出通过率。

```bash
python -m examples.p9.eval_pipeline
```

