# 编码风格

## 不可变性 (CRITICAL)

ALWAYS 创建新对象，NEVER 修改原对象：

### TypeScript/JavaScript

```typescript
// WRONG: 修改原对象
function updateUser(user: User, name: string): User {
  user.name = name  // MUTATION!
  return user
}

// CORRECT: 不可变性
function updateUser(user: User, name: string): User {
  return { ...user, name }
}
```

### Python

```python
from dataclasses import replace
from typing import TypedDict

# WRONG: 修改原对象
def update_user(user: dict, name: str) -> dict:
    user["name"] = name  # MUTATION!
    return user

# CORRECT: 不可变性
def update_user(user: dict, name: str) -> dict:
    return {**user, "name": name}

# 使用 dataclasses (Python 3.7+)
@dataclass
class User:
    name: str
    email: str

# CORRECT: 使用 replace 创建新实例
user = User(name="Alice", email="alice@example.com")
updated_user = replace(user, name="Bob")
```

## 文件组织

多小文件 > 少大文件：
- 高内聚低耦合
- 典型 200-400 行，最多 800 行
- 从大型组件/模块中提取工具函数
- 按功能/领域组织，而非按类型

## 错误处理

ALWAYS 全面处理错误：

### TypeScript

```typescript
try {
  const result = await riskyOperation()
  return result
} catch (error) {
  console.error('Operation failed:', error)
  throw new Error('Detailed user-friendly message')
}
```

### Python

```python
import logging

logger = logging.getLogger(__name__)

try:
    result = await risky_operation()
    return result
except Exception as e:
    logger.error("Operation failed", exc_info=e)
    raise RuntimeError("Detailed user-friendly message") from e
```

## 输入验证

ALWAYS 验证用户输入：

### TypeScript (Zod)

```typescript
import { z } from 'zod'

const schema = z.object({
  email: z.string().email(),
  age: z.number().int().min(0).max(150)
})

const validated = schema.parse(input)
```

### Python (Pydantic)

```python
from pydantic import BaseModel, EmailStr, Field, ValidationError

class UserInput(BaseModel):
    email: EmailStr
    age: int = Field(ge=0, le=150)

try:
    validated = UserInput(**input)
except ValidationError as e:
    raise ValueError(f"Invalid input: {e}")
```

## 类型注解

ALWAYS 使用类型注解提高代码可维护性：

### TypeScript

```typescript
interface User {
  id: string
  name: string
  email: string
}

function getUser(id: string): Promise<User> {
  // ...
}
```

### Python

```python
from typing import Protocol

class User(Protocol):
    id: str
    name: str
    email: str

async def get_user(user_id: str) -> User:
    # ...
```

## 代码质量检查清单

标记工作完成前：
- [ ] 代码可读且命名良好
- [ ] 函数小巧 (<50 行)
- [ ] 文件专注 (<800 行)
- [ ] 无深层嵌套 (>4 层)
- [ ] 正确的错误处理
- [ ] 无 console.log/print 调试语句
- [ ] 无硬编码值
- [ ] 无修改 (使用不可变模式)
- [ ] 类型注解完整
