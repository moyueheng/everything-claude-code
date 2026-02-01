---
name: dev-tdd-py
description: Python 测试驱动开发工作流。强制执行 TDD 原则，确保 80%+ 覆盖率，包含单元测试、集成测试和 E2E 测试。
---

# Python 测试驱动开发工作流

此 skill 确保所有 Python 代码开发遵循 TDD 原则，具有全面的测试覆盖率。

## 何时激活

- 编写新功能或功能
- 修复 bug 或问题
- 重构现有代码
- 添加 API 端点
- 创建新模块/类

## 核心原则

### 1. 测试先于代码
**始终**先编写测试，然后实现代码使测试通过。

### 2. 覆盖率要求
- 最低 80% 覆盖率（单元 + 集成 + E2E）
- 覆盖所有边界情况
- 测试错误场景
- 验证边界条件

### 3. 测试类型

#### 单元测试
- 单个函数和工具
- 类方法
- 纯函数
- 辅助函数和工具

#### 集成测试
- API 端点
- 数据库操作
- 服务交互
- 外部 API 调用

#### E2E 测试
- 关键用户流程
- 完整工作流
- 端到端场景

## TDD 工作流步骤

### 第 1 步：编写用户旅程
```
作为 [角色], 我想要 [动作], 以便 [收益]

示例：
作为用户，我想要语义化搜索市场，
以便即使没有精确关键词也能找到相关市场。
```

### 第 2 步：生成测试用例
为每个用户旅程创建全面的测试用例：

```python
import pytest

class TestSemanticSearch:
    def test_returns_relevant_markets_for_query(self):
        # 测试实现
        pass

    def test_handles_empty_query_gracefully(self):
        # 测试边界情况
        pass

    def test_fallback_to_substring_when_redis_unavailable(self):
        # 测试回退行为
        pass

    def test_sorts_results_by_similarity_score(self):
        # 测试排序逻辑
        pass
```

### 第 3 步：运行测试（应该失败）
```bash
pytest
# 测试应该失败 - 我们还没有实现
```

### 第 4 步：实现代码
编写最简代码使测试通过：

```python
# 由测试指导的实现
async def search_markets(query: str) -> list[Market]:
    # 在这里实现
    pass
```

### 第 5 步：再次运行测试
```bash
pytest
# 测试现在应该通过
```

### 第 6 步：重构
在保持测试通过的同时提高代码质量：
- 消除重复
- 改进命名
- 优化性能
- 增强可读性

### 第 7 步：验证覆盖率
```bash
pytest --cov=src --cov-report=term-missing
# 验证达到 80%+ 覆盖率
```

## 测试模式

### 单元测试模式 (pytest)
```python
import pytest
from datetime import datetime
from myapp.market import Market, calculate_liquidity_score

class TestCalculateLiquidityScore:
    """测试流动性分数计算"""

    def test_high_liquidity_returns_high_score(self):
        market = Market(
            total_volume=100000,
            bid_ask_spread=0.01,
            active_traders=500,
            last_trade_time=datetime.now()
        )

        score = calculate_liquidity_score(market)

        assert score > 80
        assert score <= 100

    def test_low_liquidity_returns_low_score(self):
        market = Market(
            total_volume=100,
            bid_ask_spread=0.5,
            active_traders=2,
            last_trade_time=datetime.now()
        )

        score = calculate_liquidity_score(market)

        assert score < 30
        assert score >= 0

    def test_zero_volume_returns_zero(self):
        market = Market(
            total_volume=0,
            bid_ask_spread=0,
            active_traders=0,
            last_trade_time=datetime.now()
        )

        score = calculate_liquidity_score(market)

        assert score == 0
```

### API 集成测试模式 (FastAPI)
```python
import pytest
from httpx import AsyncClient
from myapp.main import app

@pytest.mark.asyncio
class TestMarketsAPI:
    """测试市场 API 端点"""

    async def test_get_markets_success(self):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/markets")

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert isinstance(data["data"], list)

    async def test_get_markets_validates_query_params(self):
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/markets?limit=invalid")

        assert response.status_code == 400

    async def test_get_markets_handles_db_errors(self):
        # Mock 数据库失败
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/api/markets")

        assert response.status_code == 500
```

### 使用 Fixture 的测试
```python
import pytest
from datetime import datetime
from myapp.market import Market

@pytest.fixture
def high_liquidity_market():
    """创建高流动性市场 fixture"""
    return Market(
        total_volume=100000,
        bid_ask_spread=0.01,
        active_traders=500,
        last_trade_time=datetime.now()
    )

@pytest.fixture
def low_liquidity_market():
    """创建低流动性市场 fixture"""
    return Market(
        total_volume=100,
        bid_ask_spread=0.5,
        active_traders=2,
        last_trade_time=datetime.now()
    )

class TestMarketLiquidity:
    def test_high_liquidity(self, high_liquidity_market):
        score = calculate_liquidity_score(high_liquidity_market)
        assert score > 80

    def test_low_liquidity(self, low_liquidity_market):
        score = calculate_liquidity_score(low_liquidity_market)
        assert score < 30
```

### 参数化测试
```python
import pytest

@pytest.mark.parametrize("email,expected_valid", [
    ("user@example.com", True),
    ("user@", False),
    ("@example.com", False),
    ("", False),
    ("user.name@example.co.uk", True),
    ("user@example", False),
])
def test_validate_email(email, expected_valid):
    assert validate_email(email) == expected_valid

@pytest.mark.parametrize("volume,spread,traders,expected_range", [
    (100000, 0.01, 500, (80, 100)),
    (100, 0.5, 2, (0, 30)),
    (0, 0, 0, (0, 0)),
])
def test_liquidity_score_ranges(volume, spread, traders, expected_range):
    market = create_market(volume, spread, traders)
    score = calculate_liquidity_score(market)
    min_val, max_val = expected_range
    assert min_val <= score <= max_val
```

## 测试文件组织

```
project/
├── src/
│   └── myapp/
│       ├── __init__.py
│       ├── market.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # 共享 fixture
│   ├── unit/                    # 单元测试
│   │   ├── __init__.py
│   │   ├── test_market.py
│   │   └── test_utils.py
│   ├── integration/             # 集成测试
│   │   ├── __init__.py
│   │   ├── test_api.py
│   │   └── test_database.py
│   └── e2e/                     # E2E 测试
│       ├── __init__.py
│       └── test_user_flows.py
├── pyproject.toml
└── pytest.ini
```

## 模拟外部服务

### 数据库 Mock (pytest-asyncio)
```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_db():
    """Mock 数据库连接"""
    with patch("myapp.db.get_connection") as mock:
        mock_conn = AsyncMock()
        mock_conn.fetch.return_value = [
            {"id": 1, "name": "Test Market"}
        ]
        mock.return_value = mock_conn
        yield mock

async def test_get_markets(mock_db):
    markets = await get_markets()
    assert len(markets) == 1
    assert markets[0]["name"] == "Test Market"
```

### Redis Mock
```python
import pytest
from unittest.mock import patch

@pytest.fixture
def mock_redis():
    """Mock Redis 客户端"""
    with patch("myapp.cache.redis_client") as mock:
        mock.get.return_value = None
        mock.set.return_value = True
        mock.search_by_vector.return_value = [
            {"slug": "test-market", "similarity_score": 0.95}
        ]
        yield mock

def test_search_with_redis(mock_redis):
    results = search_markets("test")
    assert len(results) > 0
```

### OpenAI Mock
```python
import pytest
from unittest.mock import patch

@pytest.fixture
def mock_openai():
    """Mock OpenAI API"""
    with patch("myapp.ai.generate_embedding") as mock:
        mock.return_value = [0.1] * 1536  # Mock 1536维 embedding
        yield mock

def test_generate_embedding(mock_openai):
    embedding = generate_embedding("test text")
    assert len(embedding) == 1536
```

### HTTP 请求 Mock (responses/httpx)
```python
import pytest
import responses

@pytest.fixture
def mock_api():
    """Mock 外部 API 调用"""
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            "https://api.example.com/data",
            json={"result": "success"},
            status=200
        )
        yield rsps

def test_fetch_external_data(mock_api):
    data = fetch_external_data()
    assert data["result"] == "success"
```

## 测试覆盖率验证

### 运行覆盖率报告
```bash
# 基本覆盖率
pytest --cov=src --cov-report=term

# 详细报告（显示缺失行）
pytest --cov=src --cov-report=term-missing

# HTML 报告
pytest --cov=src --cov-report=html

# XML 报告（用于 CI）
pytest --cov=src --cov-report=xml
```

### 覆盖率阈值 (pyproject.toml)
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src --cov-report=term-missing"

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/test_*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
]
fail_under = 80
```

## 应避免的常见测试错误

### ❌ 错误：测试实现细节
```python
# 不要测试内部状态
assert obj._internal_counter == 5
```

### ✅ 正确：测试公共行为
```python
# 测试公共接口
assert obj.get_count() == 5
```

### ❌ 错误：测试没有隔离
```python
# 测试相互依赖
class TestUser:
    def test_create_user(self):
        self.user_id = create_user()

    def test_update_user(self):
        # 依赖于前一个测试 - 错误！
        update_user(self.user_id)
```

### ✅ 正确：独立的测试
```python
class TestUser:
    def test_create_user(self):
        user_id = create_user()
        assert user_exists(user_id)

    def test_update_user(self):
        user_id = create_user()  # 每个测试自己创建数据
        update_user(user_id)
        assert get_user(user_id).updated
```

### ❌ 错误：过于宽松的断言
```python
# 不够具体
assert result is not None
```

### ✅ 正确：精确的断言
```python
# 验证具体值
assert result["id"] == 123
assert result["name"] == "Test Market"
assert len(result["items"]) == 3
```

## 持续测试

### 开发时 watch 模式
```bash
# 文件更改时自动运行测试
pytest -f

# 或安装 pytest-watch
ptw
```

### 只运行失败的测试
```bash
# 重新运行上次失败的测试
pytest --lf

# 先运行失败的，然后其他的
pytest --ff
```

### 预提交钩子 (.pre-commit-config.yaml)
```yaml
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        types: [python]
        pass_filenames: false
        always_run: true
```

### CI/CD 集成 (GitHub Actions)
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: pytest --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

## 最佳实践

1. **先写测试** - 始终 TDD
2. **每个测试一个概念** - 专注于单一行为
3. **描述性的测试名称** - 解释测试的内容
4. **Arrange-Act-Assert** - 清晰的测试结构
   ```python
   def test_something():
       # Arrange
       data = setup_data()

       # Act
       result = do_something(data)

       # Assert
       assert result == expected
   ```
5. **使用 fixture 共享设置** - 避免重复
6. **测试边界情况** - None、空值、最大值
7. **测试错误路径** - 不只是快乐路径
8. **保持测试快速** - 单元测试 < 50ms 每个
9. **清理副作用** - 使用 fixture 清理
10. **审查覆盖率报告** - 识别覆盖缺口

## 异步测试

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result == "expected"

@pytest.fixture
async def async_client():
    async with AsyncClient() as client:
        yield client
        # 清理在 yield 之后

@pytest.mark.asyncio
async def test_with_async_fixture(async_client):
    response = await async_client.get("/api/test")
    assert response.status_code == 200
```

## 成功指标

- 达到 80%+ 代码覆盖率
- 所有测试通过（绿色）
- 没有跳过或禁用的测试
- 快速测试执行（单元测试 < 30s）
- E2E 测试覆盖关键用户流程
- 测试在投入生产前捕获 bug

---

**记住**：测试不是可选的。它们是支持自信重构、快速开发和生产可靠性的安全网。
