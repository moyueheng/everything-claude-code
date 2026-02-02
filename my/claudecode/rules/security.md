# 安全指南

## 强制性安全检查

任何 commit 前:
- [ ] 无硬编码 secrets (API keys, passwords, tokens)
- [ ] 所有用户输入已验证
- [ ] SQL 注入防护 (参数化查询)
- [ ] XSS 防护 (HTML 清理)
- [ ] CSRF 保护已启用
- [ ] 认证/授权已验证
- [ ] 所有 endpoints 有速率限制
- [ ] 错误消息不泄露敏感数据

## Secret 管理

```typescript
// NEVER: 硬编码 secrets
const apiKey = "sk-proj-xxxxx"

// ALWAYS: 环境变量
const apiKey = process.env.OPENAI_API_KEY

if (!apiKey) {
  throw new Error('OPENAI_API_KEY not configured')
}
```

## 安全响应协议

发现安全问题时:
1. 立即 STOP
2. 使用 **security-reviewer** Agent
3. 继续前修复 CRITICAL 问题
4. 轮换任何暴露的 secrets
5. 审查整个代码库的类似问题
