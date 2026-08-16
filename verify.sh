#!/usr/bin/env bash
# ============================================================================
# verify.sh — 一键验证 Phase 10-13 能否跑通
# ----------------------------------------------------------------------------
# 前置（需你本地先做好）:
#   1) make setup                         # 建 .venv + 装 Python/Node 依赖 + 复制 .env
#   2) 编辑 .env 选好 LLM_PROVIDER        # openai / deepseek / qwen / ollama
#      - 用 ollama: 先 `ollama serve` 并确保已 pull 模型
#      - 用云端: 填好对应 API key
#
# 用法:
#   ./verify.sh            # 依次验证 Phase 10 -> 13
#   ./verify.sh 11         # 只验证单个 Phase（如 11）
#   ./verify.sh 10 13      # 只验证指定的几个 Phase
#
# 说明: 每个 Phase 会真正调用 LLM，耗时取决于模型响应速度（默认超时 360s）。
#       判分依据是该示例打印出的「关键标记」，而非具体回答内容（回答是非确定的）。
# ============================================================================
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'; BLUE='\033[0;34m'; NC='\033[0m'

PASS=0
FAIL=0

# ---- 前置检查 ---------------------------------------------------------------
echo -e "${BLUE}=== 前置检查 ===${NC}"
if [ ! -d .venv ]; then
  echo -e "${RED}✗ 未找到 .venv，请先运行: make setup${NC}"
  exit 1
fi
echo -e "${GREEN}✓ 找到 .venv${NC}"

if [ ! -f .env ]; then
  echo -e "${YELLOW}⚠ 未找到 .env，请先运行 make setup 生成并配置 LLM_PROVIDER / API key${NC}"
else
  PROVIDER="$(grep -E '^LLM_PROVIDER=' .env 2>/dev/null | tail -1 | cut -d= -f2- | tr -d '[:space:]')"
  if [ -z "$PROVIDER" ]; then
    echo -e "${YELLOW}⚠ 未检测到 LLM_PROVIDER，请确认 .env 已正确配置${NC}"
  else
    echo -e "${GREEN}✓ LLM_PROVIDER=$PROVIDER${NC}"
  fi
fi

# ---- 每个 Phase 的预期关键标记（用于判分）----------------------------------
check_markers() {
  local p="$1" log="$2"
  local -a marks=()
  case "$p" in
    10) marks=(
      "用例 1：有来源的问题（应带引用回答）"
      "用例 2：无来源的问题（防幻觉护栏应拦下）"
      "溯源 episode#"
      );;
    11) marks=(
      "已从 MCP 服务器加载"
      "web_search"
      "最终答案"
      );;
    12) marks=(
      "[supervisor] 路由决策"
      "[worker] 调研员产出"
      "[worker] 写作者产出"
      "最终对话轨迹（messages）"
      );;
    13) marks=(
      "发现 Agent Card"
      "智能体回答"
      );;
    *) echo -e "${RED}  未知 Phase: $p${NC}"; return;;
  esac

  local ok=1
  for m in "${marks[@]}"; do
    if grep -qF "$m" "$log"; then
      echo -e "${GREEN}  ✓ 标记命中: $m${NC}"
    else
      echo -e "${RED}  ✗ 缺失标记: $m${NC}"
      ok=0
    fi
  done
  if [ "$ok" -eq 1 ]; then
    echo -e "${GREEN}→ Phase $p 通过${NC}"
    PASS=$((PASS + 1))
  else
    echo -e "${RED}→ Phase $p 未通过（详见上方输出尾部）${NC}"
    FAIL=$((FAIL + 1))
  fi
}

run_phase() {
  local p="$1"
  echo -e "\n${BLUE}=== Phase $p ===${NC}"
  local log="/tmp/verify_p${p}.log"
  # macOS 没有 GNU `timeout`，用「后台进程 + sleep 后 kill」实现可移植超时。
  # 注意：直接调用 .venv 里的 python，并用 nohup 让进程组忽略 SIGHUP——
  # 原先走 `make run` 时，后台子 shell 里的 make 会收到 Hangup(1) 提前退出，
  # 导致 Phase 11（会拉起 MCP server 子进程）等带子进程的 Phase 偶发失败。
  local timeout_sec=360
  ( nohup ./.venv/bin/python -m "examples.p${p}.hello_chain" > "$log" 2>&1 ) &
  local pid=$!
  ( sleep "$timeout_sec"; kill -9 "$pid" 2>/dev/null ) &
  local watcher=$!
  wait "$pid"
  local rc=0
  rc=$?
  kill "$watcher" 2>/dev/null
  if [ "$rc" -eq 0 ]; then
    echo -e "${GREEN}✓ 进程正常退出（rc=0）${NC}"
  elif [ "$rc" -eq 137 ]; then
    echo -e "${RED}✗ 超时（${timeout_sec}s）：模型响应慢或卡住，可改大脚本里的超时时间${NC}"
  else
    echo -e "${RED}✗ 进程非零退出（rc=$rc）${NC}"
  fi
  echo "----- 输出尾部 (tail -n 25) -----"
  tail -n 25 "$log"
  echo "---------------------------------"
  check_markers "$p" "$log"
}

# ---- 决定要跑哪些 Phase -----------------------------------------------------
if [ "$#" -gt 0 ]; then
  PHASES=("$@")
else
  PHASES=(10 11 12 13)
fi

for p in "${PHASES[@]}"; do
  run_phase "$p"
done

# ---- 总结 -------------------------------------------------------------------
echo -e "\n${BLUE}=== 验证总结 ===${NC}"
echo -e "通过: ${GREEN}$PASS${NC}  未通过: ${RED}$FAIL${NC}"
if [ "$FAIL" -eq 0 ]; then
  echo -e "${GREEN}全部通过 🎉${NC}"
  exit 0
else
  echo -e "${RED}有未通过项，请查看上方日志定位问题${NC}"
  exit 1
fi
