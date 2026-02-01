---
name: dev-tdd-py
description: 强制执行 Python 测试驱动开发工作流程。先搭建接口，先生成测试，然后实现最小代码以通过测试。确保 80%+ 覆盖率。
---

# Python TDD 命令

此命令调用 **tdd-guide-py** agent 来强制执行 Python 测试驱动开发方法论。

## 命令作用

1. **搭建接口** - 首先定义类型/接口
2. **先生成测试** - 编写失败的测试（RED）
3. **实现最小代码** - 编写刚好足够的代码以通过（GREEN）
4. **重构** - 在保持测试绿色的同时改进代码（REFACTOR）
5. **验证覆盖率** - 确保 80%+ 测试覆盖率

## 使用时机

在以下情况使用 `/dev-tdd-py`：
- 实现新功能
- 添加新函数/组件
- 修复 bug（首先编写重现 bug 的测试）
- 重构现有代码
- 构建关键业务逻辑

## 工作原理

tdd-guide agent 将：

1. **定义接口** 用于输入/输出
2. **编写将失败的测试**（因为代码还不存在）
3. **运行测试** 并验证它们因正确的原因而失败
4. **编写最小实现** 使测试通过
5. **运行测试** 并验证它们通过
6. **重构** 代码同时保持测试绿色
7. **检查覆盖率** 如果低于 80% 则添加更多测试

## TDD 循环

```
RED → GREEN → REFACTOR → REPEAT

RED:      编写失败的测试
GREEN:    编写最小代码以通过
REFACTOR: 改进代码，保持测试通过
REPEAT:   下一个功能/场景
```

## 使用示例

```
用户: /dev-tdd-py 我需要一个计算市场流动性分数的函数

Agent (tdd-guide):
# TDD 会话：市场流动性分数计算器

## 第 1 步：定义接口（搭建脚手架）

```python
# lib/liquidity.py
from dataclasses import dataclass
from datetime import datetime
from typing import Union

@dataclass
class MarketData:
    total_volume: float
    bid_ask_spread: float
    active_traders: int
    last_trade_time: datetime

def calculate_liquidity_score(market: MarketData) -> float:
    """计算市场流动性分数"""
    # TODO：实现
    raise NotImplementedError('Not implemented')
```

## 第 2 步：编写失败的测试（RED）

```python
# tests/test_liquidity.py
import pytest
from datetime import datetime
from lib.liquidity import calculate_liquidity_score, MarketData

def test_high_liquidity_market_returns_high_score():
    market = MarketData(
        total_volume=100000,
        bid_ask_spread=0.01,
        active_traders=500,
        last_trade_time=datetime.now()
    )

    score = calculate_liquidity_score(market)

    assert score > 80
    assert score <= 100

def test_low_liquidity_market_returns_low_score():
    market = MarketData(
        total_volume=100,
        bid_ask_spread=0.5,
        active_traders=2,
        last_trade_time=datetime.now()
    )

    score = calculate_liquidity_score(market)

    assert score < 30
    assert score >= 0

def test_edge_case_zero_volume():
    market = MarketData(
        total_volume=0,
        bid_ask_spread=0,
        active_traders=0,
        last_trade_time=datetime.now()
    )

    score = calculate_liquidity_score(market)

    assert score == 0
```

## 第 3 步：运行测试 - 验证失败

```bash
pytest tests/test_liquidity.py -v

FAIL tests/test_liquidity.py::test_high_liquidity_market_returns_high_score
  - NotImplementedError: Not implemented

1 测试失败，0 通过
```

✅ 测试按预期失败。准备好实现。

## 第 4 步：实现最小代码（GREEN）

```python
# lib/liquidity.py
def calculate_liquidity_score(market: MarketData) -> float:
    # 处理零交易量边缘情况
    if market.total_volume == 0:
        return 0

    # 计算各组件分数（0-100 范围）
    volume_score = min(market.total_volume / 1000, 100)
    spread_score = max(100 - (market.bid_ask_spread * 1000), 0)
    trader_score = min(market.active_traders / 10, 100)

    # 最近活动奖励
    hours_since_last_trade = (datetime.now() - market.last_trade_time).total_seconds() / 3600
    recency_score = max(100 - (hours_since_last_trade * 10), 0)

    # 加权平均
    score = (
        volume_score * 0.4 +
        spread_score * 0.3 +
        trader_score * 0.2 +
        recency_score * 0.1
    )

    return max(0, min(score, 100))  # 限制在 0-100
```

## 第 5 步：运行测试 - 验证通过

```bash
pytest tests/test_liquidity.py -v

PASS tests/test_liquidity.py::test_high_liquidity_market_returns_high_score
PASS tests/test_liquidity.py::test_low_liquidity_market_returns_low_score
PASS tests/test_liquidity.py::test_edge_case_zero_volume

3 测试通过
```

✅ 所有测试通过！

## 第 6 步：重构（改进）

```python
# lib/liquidity.py - 使用常量和更好的可读性进行重构
from dataclasses import dataclass
from datetime import datetime
from typing import Final

WEIGHTS: Final[dict[str, float]] = {
    'VOLUME': 0.4,
    'SPREAD': 0.3,
    'TRADERS': 0.2,
    'RECENCY': 0.1,
}

SCALE_FACTORS: Final[dict[str, float]] = {
    'VOLUME': 1000,
    'SPREAD': 1000,
    'TRADERS': 10,
    'RECENCY_PENALTY': 10,
}

def _clamp(value: float, min_val: float, max_val: float) -> float:
    return max(min_val, min(value, max_val))

def calculate_liquidity_score(market: MarketData) -> float:
    if market.total_volume == 0:
        return 0

    volume_score = min(market.total_volume / SCALE_FACTORS['VOLUME'], 100)
    spread_score = _clamp(100 - (market.bid_ask_spread * SCALE_FACTORS['SPREAD']), 0, 100)
    trader_score = min(market.active_traders / SCALE_FACTORS['TRADERS'], 100)

    hours_since_last_trade = (datetime.now() - market.last_trade_time).total_seconds() / 3600
    recency_score = _clamp(100 - (hours_since_last_trade * SCALE_FACTORS['RECENCY_PENALTY']), 0, 100)

    weighted_score = (
        volume_score * WEIGHTS['VOLUME'] +
        spread_score * WEIGHTS['SPREAD'] +
        trader_score * WEIGHTS['TRADERS'] +
        recency_score * WEIGHTS['RECENCY']
    )

    return _clamp(weighted_score, 0, 100)
```

## 第 7 步：验证测试仍然通过

```bash
pytest tests/test_liquidity.py -v

PASS tests/test_liquidity.py::test_high_liquidity_market_returns_high_score
PASS tests/test_liquidity.py::test_low_liquidity_market_returns_low_score
PASS tests/test_liquidity.py::test_edge_case_zero_volume

3 测试通过
```

✅ 重构完成，测试仍然通过！

## 第 8 步：检查覆盖率

```bash
pytest tests/test_liquidity.py --cov=lib/liquidity --cov-report=term-missing

File            Stmts   Miss  Cover   Missing
---------------  -----  ----  ------  --------
lib/liquidity.py    25     0   100%

覆盖率: 100% ✅ (目标: 80%)
```

✅ TDD 会话完成！


## Python TDD 最佳实践

**要这样做：**
- ✅ 在任何实现之前先编写测试
- ✅ 在实现之前运行测试并验证它们失败
- ✅ 编写最小代码以使测试通过
- ✅ 只有在测试通过后才重构
- ✅ 添加边缘情况和错误场景
- ✅ 目标是 80%+ 覆盖率（关键代码 100%）

**不要这样做：**
- ❌ 在测试之前编写实现
- ❌ 跳过每次更改后运行测试
- ❌ 一次编写太多代码
- ❌ 忽略失败的测试
- ❌ 测试实现细节（测试行为）
- ❌ 模拟所有内容（首选集成测试）

## Python 测试工具

**pytest** (推荐):
```bash
# 基本测试
pytest tests/ -v

# 带覆盖率
pytest tests/ --cov=src --cov-report=term-missing

# 特定测试
pytest tests/test_module.py::test_function -v

# 重新运行上次失败的
pytest --lf

# 并行运行
pytest -n auto
```

**项目结构**:
```
project/
├── src/
│   └── mymodule/
│       └── __init__.py
│       └── liquidity.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # 共享 fixture
│   └── test_liquidity.py
├── pyproject.toml
└── requirements.txt
```

**fixture 示例**:
```python
# conftest.py
import pytest

@pytest.fixture
def mock_service():
    class MockService:
        def __init__(self):
            self.calls = []
        def call(self, *args):
            self.calls.append(args)
            return 'ok'
    return MockService()

# test_module.py
def test_with_fixture(mock_service):
    result = mock_service.call('arg1')
    assert result == 'ok'
    assert len(mock_service.calls) == 1
```

**参数化测试**:
```python
import pytest

@pytest.mark.parametrize('input_value,expected', [
    ('user@example.com', True),
    ('user@', False),
    ('@example.com', False),
    ('', False),
])
def test_validate_email(input_value, expected):
    assert validate_email(input_value) == expected
```

## 要包含的测试类型

**单元测试**（函数级）：
- 快乐路径场景
- 边缘情况（空、None、最大值）
- 错误条件
- 边界值

**集成测试**（组件级）：
- API 端点
- 数据库操作
- 外部服务调用

**E2E 测试**（完整流程）：
- 关键用户流程
- 多步骤过程
- 全栈集成

## 覆盖率要求

- **所有代码最低 80%**
- **以下要求 100%**：
  - 金融计算
  - 认证逻辑
  - 安全关键代码
  - 核心业务逻辑

## 重要说明

**强制要求**：必须在实现之前编写测试。TDD 循环是：

1. **RED** - 编写失败的测试
2. **GREEN** - 实现以通过测试
3. **REFACTOR** - 改进代码

永远不要跳过 RED 阶段。永远不要在测试之前编写代码。

## 与其他命令的集成

- 首先使用 `/plan` 了解要构建什么
- 使用 `/dev-tdd-py` 通过测试进行实现
- 如果发生构建错误，使用 `/build-and-fix`
- 使用 `/code-review` 审查实现
- 使用 `/test-coverage` 验证覆盖率

## 相关 Agent

此命令调用位于以下位置的 `tdd-guide` agent：
`~.claude/agents/tdd-guide-py.md`
