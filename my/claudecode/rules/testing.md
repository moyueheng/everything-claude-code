# 测试要求

## 最低测试覆盖率: 80%

测试类型 (全部必需):
1. **单元测试** - 独立函数、工具、组件
2. **集成测试** - API endpoints、数据库操作
3. **E2E 测试** - 关键用户流程 (Playwright)

## 测试驱动开发

强制性工作流:
1. 先写测试 (RED)
2. 运行测试 - 应该 FAIL
3. 编写最小实现 (GREEN)
4. 运行测试 - 应该 PASS
5. 重构 (IMPROVE)
6. 验证覆盖率 (80%+)

## 测试失败排查

1. 使用 **dev-tdd-guide-ts** 或 **dev-tdd-guide-py** Agent
2. 检查测试隔离
3. 验证 mocks 是否正确
4. 修复实现，而非测试 (除非测试本身有误)

## Agent 支持

- **dev-tdd-guide-ts** / **dev-tdd-guide-py** - 主动用于新功能，强制先写测试
- **e2e-runner** - Playwright E2E 测试专家
