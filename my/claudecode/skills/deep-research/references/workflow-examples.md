# 研究工作流示例

本文档提供各种研究场景的具体工作流示例。

## 示例 1：技术趋势调研

### 场景
用户想了解 "2024 年大语言模型在代码生成领域的最新进展"。

### 执行计划

```yaml
plan_id: "llm_code_gen_2024"
title: "2024年大语言模型代码生成技术调研"
steps:
  1. 搜索 LLM 代码生成的最新论文和综述
  2. 分析主流模型的技术架构和特点
  3. 对比不同模型的性能指标和适用场景
  4. 总结技术发展趋势和未来方向
```

### 详细执行流程

**Step 1: 文献搜索**
```
子任务: 搜索最新论文
智能体: Deep Researcher
查询: "large language model code generation 2024 survey paper"
深度: 2
时间限制: 120s

预期输出:
- 最新发表的综述论文
- 主流模型的技术报告
- 基准测试结果
```

**Step 2: 技术分析**
```
子任务: 分析技术架构
智能体: Deep Analyzer
输入: Step 1 收集的论文内容
分析维度:
  - 模型架构 (Transformer, MoE, etc.)
  - 训练方法 (Pre-training, Fine-tuning, RLHF)
  - 代码表示 (AST, Token, Graph)
  - 评估指标 (Pass@k, HumanEval, etc.)

预期输出:
- 各模型的技术特点对比表
- 架构演进趋势分析
```

**Step 3: 性能对比**
```
子任务: 性能指标对比
智能体: Python Interpreter
任务:
  1. 从搜索结果中提取性能数据
  2. 创建对比表格
  3. 可视化关键指标

代码示例:
```python
import pandas as pd

# 从搜索结果中提取的数据
models = ['GPT-4', 'Claude-3', 'CodeLlama', 'StarCoder2']
metrics = {
    'HumanEval': [67.0, 72.7, 48.8, 46.2],
    'MBPP': [52.0, 58.0, 41.0, 45.0],
    'Parameters': [1.8T, 'Unknown', 70B, 15B]
}

df = pd.DataFrame(metrics, index=models)
print(df)
```
```

**Step 4: 趋势总结**
```
子任务: 生成趋势报告
智能体: Deep Analyzer
输入: 前三个步骤的结果
输出要求:
  - 技术发展趋势 (3-5条)
  - 关键突破点
  - 未来研究方向
  - 应用前景
```

### 最终报告结构

```markdown
# 2024年大语言模型代码生成技术调研报告

## 执行摘要
- 核心发现 1: ...
- 核心发现 2: ...
- 核心发现 3: ...

## 技术现状
### 主流模型对比
| 模型 | HumanEval | MBPP | 特点 |
|------|-----------|------|------|
| ...  | ...       | ...  | ...  |

### 技术架构演进
...

## 性能分析
...

## 发展趋势
1. ...
2. ...
3. ...

## 信息来源
- [1] ...
- [2] ...
```

---

## 示例 2：竞品分析

### 场景
用户想对比 "OpenAI、Claude、Gemini 三个大模型的能力差异"。

### 执行计划

```yaml
plan_id: "llm_comparison_2024"
title: "主流大语言模型能力对比分析"
steps:
  1. 搜索三个模型的官方能力说明和基准测试
  2. 查找第三方评测和用户反馈
  3. 分析各自的技术特点和适用场景
  4. 生成对比表格和选择建议
```

### 详细执行流程

**Step 1: 官方信息收集**
```
子任务: 收集官方资料
智能体: Deep Researcher
并行查询:
  - "OpenAI GPT-4 capabilities official benchmark"
  - "Claude 3 model capabilities Anthropic"
  - "Google Gemini capabilities benchmark"
深度: 2

关键信息:
  - 官方发布的能力指标
  - 支持的上下文长度
  - 定价信息
  - API 特性
```

**Step 2: 第三方评测**
```
子任务: 查找独立评测
智能体: Deep Researcher
查询: "GPT-4 vs Claude vs Gemini comparison independent test 2024"

关注来源:
  - LMSYS Chatbot Arena
  - 学术论文对比研究
  - 技术博客评测
  - 开发者社区反馈
```

**Step 3: 场景分析**
```
子任务: 分析适用场景
智能体: Deep Analyzer
分析维度:
  代码生成:
    - OpenAI: ...
    - Claude: ...
    - Gemini: ...

  长文本处理:
    - OpenAI: ...
    - Claude: ...
    - Gemini: ...

  推理能力:
    - OpenAI: ...
    - Claude: ...
    - Gemini: ...

  多模态:
    - OpenAI: ...
    - Claude: ...
    - Gemini: ...
```

**Step 4: 建议生成**
```
子任务: 生成选择建议
智能体: Planning Agent (综合)
输出:
  选择矩阵:
    - 代码开发: 推荐 ...
    - 内容创作: 推荐 ...
    - 数据分析: 推荐 ...
    - 多语言: 推荐 ...

  成本效益分析:
    - 各场景下的性价比
```

---

## 示例 3：问题诊断

### 场景
用户报告 "Python 异步代码性能不佳，需要诊断和优化"。

### 执行计划

```yaml
plan_id: "python_async_perf"
title: "Python异步代码性能诊断与优化"
steps:
  1. 分析用户提供的代码，识别潜在问题
  2. 搜索 Python 异步最佳实践和常见陷阱
  3. 使用工具执行性能分析
  4. 提供优化建议和修改方案
```

### 详细执行流程

**Step 1: 代码分析**
```
子任务: 静态代码分析
智能体: Deep Analyzer
输入: 用户代码

分析要点:
  - 是否正确使用 async/await
  - 是否存在阻塞调用
  - 并发控制是否合理
  - 资源管理是否得当

常见问题:
  - 在 async 函数中使用同步 I/O
  - 过度创建 Task
  - 缺少适当的并发限制
  - 异常处理不完善
```

**Step 2: 最佳实践研究**
```
子任务: 搜索优化方案
智能体: Deep Researcher
查询: "Python asyncio performance optimization best practices 2024"

关注内容:
  - 官方文档推荐模式
  - 性能优化技巧
  - 常见反模式
  - 调试工具推荐
```

**Step 3: 性能测试**
```
子任务: 执行性能分析
智能体: Python Interpreter

代码示例:
```python
import asyncio
import time
import cProfile
import pstats

# 用户的原始代码
async def original_code():
    ...

# 性能分析
profiler = cProfile.Profile()
profiler.enable()

start = time.time()
asyncio.run(original_code())
elapsed = time.time() - start

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)

print(f"总耗时: {elapsed:.2f}s")
```
```

**Step 4: 优化方案**
```
子任务: 生成优化代码
智能体: Python Interpreter

输出:
  1. 优化后的代码
  2. 性能对比数据
  3. 优化说明文档
```

---

## 示例 4：概念学习

### 场景
用户想 "系统学习 RAG (检索增强生成) 技术"。

### 执行计划

```yaml
plan_id: "rag_learning_path"
title: "RAG 技术系统学习路径"
steps:
  1. 搜索 RAG 技术的基础概念和原理
  2. 研究主流 RAG 框架和实现
  3. 分析实际应用案例
  4. 整理学习资源和路径
```

### 详细执行流程

**Step 1: 基础概念**
```
子任务: 概念梳理
智能体: Deep Researcher
查询: "RAG retrieval augmented generation tutorial concept"

输出结构:
  - 什么是 RAG
  - 为什么需要 RAG
  - 基本架构组成
  - 核心挑战
```

**Step 2: 技术实现**
```
子任务: 实现方案研究
智能体: Deep Researcher
查询: "RAG implementation LangChain LlamaIndex vector database"

覆盖内容:
  - 文档加载和分割
  - 嵌入模型选择
  - 向量数据库对比
  - 检索策略
  - 重排序方法
  - 生成优化
```

**Step 3: 案例分析**
```
子任务: 实际案例分析
智能体: Deep Researcher + Analyzer

案例类型:
  - 企业知识库问答
  - 客服机器人
  - 代码助手
  - 研究助手

分析维度:
  - 架构设计
  - 技术选型
  - 性能指标
  - 经验教训
```

**Step 4: 学习路径**
```
子任务: 生成学习路径
智能体: Planning Agent

输出:
  阶段1: 基础 (1-2周)
    - 学习资源
    - 实践项目
    - 考核标准

  阶段2: 进阶 (2-3周)
    - 学习资源
    - 实践项目
    - 考核标准

  阶段3: 实战 (持续)
    - 开源项目贡献
    - 个人项目
    - 社区参与
```

---

## 示例 5：决策支持

### 场景
用户需要 "为团队选择合适的数据库方案"。

### 执行计划

```yaml
plan_id: "db_selection_2024"
title: "数据库选型决策支持"
steps:
  1. 分析团队需求和使用场景
  2. 研究主流数据库方案
  3. 对比各方案的优缺点
  4. 提供选型建议和迁移方案
```

### 详细执行流程

**Step 1: 需求分析**
```
子任务: 需求梳理
智能体: Deep Analyzer

分析维度:
  数据特征:
    - 数据类型 (结构化/半结构化/非结构化)
    - 数据规模 (当前/预期)
    - 增长速度

  访问模式:
    - 读/写比例
    - 查询复杂度
    - 响应时间要求

  运维要求:
    - 团队技术栈
    - 运维能力
    - 预算限制
```

**Step 2: 方案研究**
```
子任务: 数据库研究
智能体: Deep Researcher

研究对象:
  关系型: PostgreSQL, MySQL
  文档型: MongoDB, Elasticsearch
  向量型: Pinecone, Weaviate, Milvus
  时序型: InfluxDB, TimescaleDB
  图数据库: Neo4j

评估维度:
  - 功能特性
  - 性能表现
  - 扩展性
  - 社区生态
  - 成本
```

**Step 3: 对比分析**
```
子任务: 生成对比矩阵
智能体: Python Interpreter

输出:
  对比表格:
    | 数据库 | 适用场景 | 优点 | 缺点 | 成本 |
    |--------|----------|------|------|------|
    | ...    | ...      | ...  | ...  | ...  |

  决策树:
    if 事务要求高:
      推荐 PostgreSQL
    elif 文档存储:
      推荐 MongoDB
    elif 向量检索:
      推荐 ...
```

**Step 4: 决策建议**
```
子任务: 生成建议报告
智能体: Planning Agent

报告内容:
  推荐方案:
    - 首选方案及理由
    - 备选方案

  实施路径:
    - 迁移步骤
    - 风险评估
    - 回滚方案

  成本估算:
    - 基础设施成本
    - 开发成本
    - 运维成本
```

---

## 工作流选择指南

| 场景类型 | 推荐模式 | 关键智能体 |
|---------|---------|-----------|
| 技术调研 | 广度优先 | Deep Researcher |
| 竞品分析 | 对比分析 | Deep Researcher + Analyzer |
| 问题诊断 | 根因分析 | Deep Analyzer + Python |
| 概念学习 | 渐进深入 | Deep Researcher |
| 决策支持 | 评估矩阵 | Planning Agent |
| 代码开发 | 迭代实现 | Python + Analyzer |
| 数据分析 | 管道处理 | Python + Researcher |
