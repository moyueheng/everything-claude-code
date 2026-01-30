# Python 现代异步编程模式 (2025)

本文档介绍 Python 3.11+ 的现代异步编程最佳实践。

## 目录

1. [结构化并发](#结构化并发)
2. [超时管理](#超时管理)
3. [异常处理](#异常处理)
4. [资源管理](#资源管理)
5. [并发控制](#并发控制)
6. [类型安全](#类型安全)

---

## 结构化并发

### TaskGroup (Python 3.11+)

`TaskGroup` 是 Python 3.11 引入的结构化并发原语，它确保所有任务在退出上下文时完成。

**基本用法:**
```python
import asyncio

async def fetch_data(id: int) -> dict:
    await asyncio.sleep(1)
    return {"id": id, "data": f"data-{id}"}

async def main():
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(fetch_data(1))
        t2 = tg.create_task(fetch_data(2))
        t3 = tg.create_task(fetch_data(3))

    # 所有任务完成后才到达这里
    print(f"Results: {t1.result()}, {t2.result()}, {t3.result()}")

asyncio.run(main())
```

**嵌套 TaskGroup:**
```python
async def process_batch(items: list[int]) -> list[dict]:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch_data(i)) for i in items]
    return [t.result() for t in tasks]

async def main():
    batches = [[1, 2], [3, 4, 5]]
    async with asyncio.TaskGroup() as tg:
        for batch in batches:
            tg.create_task(process_batch(batch))
```

**动态添加任务:**
```python
async def worker(tg: asyncio.TaskGroup, queue: asyncio.Queue):
    while True:
        item = await queue.get()
        if item is None:  # 结束信号
            break
        tg.create_task(process_item(item))

async def main():
    queue = asyncio.Queue()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(worker(tg, queue))
        # 可以持续添加任务
        for item in items:
            await queue.put(item)
```

---

## 超时管理

### asyncio.timeout (Python 3.11+)

**单个操作超时:**
```python
async def fetch_with_timeout():
    try:
        async with asyncio.timeout(5.0):
            return await fetch_data()
    except TimeoutError:
        return {"error": "timeout"}
```

**多个操作整体超时:**
```python
async def process_with_timeout():
    async with asyncio.timeout(10.0):
        async with asyncio.TaskGroup() as tg:
            t1 = tg.create_task(fetch_data(1))
            t2 = tg.create_task(fetch_data(2))
            t3 = tg.create_task(fetch_data(3))
        # 所有任务必须在 10 秒内完成
```

**可取消的超时:**
```python
async def cancellable_operation():
    async with asyncio.timeout(5.0) as timeout:
        # 执行一些操作
        result = await step1()

        # 可以延长超时
        timeout.reschedule(asyncio.get_running_loop().time() + 10.0)

        result = await step2()
```

---

## 异常处理

### ExceptionGroup 和 except* (Python 3.11+)

**处理多个异常:**
```python
async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(may_raise_value_error())
            tg.create_task(may_raise_type_error())
            tg.create_task(may_raise_key_error())
    except* ValueError as eg:
        # 处理所有 ValueError
        for exc in eg.exceptions:
            logger.error(f"Value error: {exc}")
    except* TypeError as eg:
        # 处理所有 TypeError
        for exc in eg.exceptions:
            logger.error(f"Type error: {exc}")
    except* Exception as eg:
        # 处理其他异常
        for exc in eg.exceptions:
            logger.error(f"Other error: {exc}")
```

**自定义 ExceptionGroup:**
```python
def group_exceptions(exceptions: list[Exception]) -> ExceptionGroup:
    return ExceptionGroup("multiple errors", exceptions)

# 使用
raise group_exceptions([exc1, exc2, exc3])
```

### 正确处理 CancelledError

```python
async def worker():
    try:
        while True:
            item = await queue.get()
            await process(item)
    except asyncio.CancelledError:
        logger.info("Worker cancelled, cleaning up...")
        # 清理资源
        await cleanup()
        raise  # 必须重新抛出!
```

---

## 资源管理

### 异步上下文管理器

**自定义异步上下文管理器:**
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def managed_resource():
    resource = await create_resource()
    try:
        yield resource
    finally:
        await resource.close()

# 使用
async with managed_resource() as res:
    await res.do_something()
```

**多个资源管理:**
```python
async def process():
    async with (
        aiohttp.ClientSession() as session,
        aiosqlite.connect('db.sqlite') as db,
        asyncio.TaskGroup() as tg
    ):
        # 所有资源都已准备好
        tg.create_task(fetch_and_store(session, db))
```

### 连接池模式

```python
class ConnectionPool:
    def __init__(self, max_size: int = 10):
        self.max_size = max_size
        self._pool = asyncio.Queue(maxsize=max_size)
        self._semaphore = asyncio.Semaphore(max_size)

    async def acquire(self) -> Connection:
        async with self._semaphore:
            try:
                conn = self._pool.get_nowait()
            except asyncio.QueueEmpty:
                conn = await create_connection()
            return conn

    async def release(self, conn: Connection):
        await self._pool.put(conn)

    @asynccontextmanager
    async def connection(self):
        conn = await self.acquire()
        try:
            yield conn
        finally:
            await self.release(conn)
```

---

## 并发控制

### 信号量 (Semaphore)

```python
async def limited_concurrency(items: list, max_concurrent: int = 10):
    semaphore = asyncio.Semaphore(max_concurrent)

    async def process_with_limit(item):
        async with semaphore:
            return await process(item)

    async with asyncio.TaskGroup() as tg:
        for item in items:
            tg.create_task(process_with_limit(item))
```

### 速率限制 (Rate Limiting)

```python
import time

class RateLimiter:
    def __init__(self, rate: int, period: float = 1.0):
        self.rate = rate
        self.period = period
        self.tokens = rate
        self.updated_at = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self):
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self.updated_at
            self.tokens = min(self.rate, self.tokens + elapsed * self.rate / self.period)
            self.updated_at = now

            if self.tokens < 1:
                sleep_time = (1 - self.tokens) * self.period / self.rate
                await asyncio.sleep(sleep_time)
                self.tokens = 0
            else:
                self.tokens -= 1

# 使用
limiter = RateLimiter(rate=10, period=1.0)  # 每秒 10 个请求

async def fetch_with_rate_limit(url: str):
    await limiter.acquire()
    return await fetch(url)
```

### 批量处理

```python
async def process_in_batches(items: list, batch_size: int = 100):
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        async with asyncio.TaskGroup() as tg:
            for item in batch:
                tg.create_task(process(item))
        # 批次间暂停，避免过载
        await asyncio.sleep(0.1)
```

---

## 类型安全

### 完整类型注解

```python
from typing import TypeVar, Generic, AsyncIterator, Awaitable
import asyncio

T = TypeVar('T')

async def fetch_data(url: str) -> dict[str, Any]:
    ...

async def process_items(
    items: list[int]
) -> AsyncIterator[dict[str, Any]]:
    for item in items:
        yield await process(item)

# 协程类型
coro: Awaitable[int] = some_async_function()

# Task 类型
task: asyncio.Task[dict] = asyncio.create_task(fetch_data())
```

### 泛型异步类

```python
from typing import TypeVar, Generic, AsyncIterator

T = TypeVar('T')

class AsyncQueue(Generic[T]):
    def __init__(self):
        self._queue: asyncio.Queue[T] = asyncio.Queue()

    async def put(self, item: T) -> None:
        await self._queue.put(item)

    async def get(self) -> T:
        return await self._queue.get()

    def __aiter__(self) -> AsyncIterator[T]:
        return self

    async def __anext__(self) -> T:
        try:
            return await self.get()
        except asyncio.CancelledError:
            raise StopAsyncIteration
```

### 异步协议

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class AsyncClosable(Protocol):
    async def close(self) -> None:
        ...

async def safe_close(obj: AsyncClosable) -> None:
    await obj.close()
```

---

## 测试模式

### pytest-asyncio (严格模式)

```python
# pyproject.toml
# [tool.pytest.ini_options]
# asyncio_mode = "strict"

import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await fetch_data()
    assert result["status"] == "ok"

@pytest.mark.asyncio
async def test_with_taskgroup():
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(fetch_data(1))
        t2 = tg.create_task(fetch_data(2))

    assert t1.result()["id"] == 1
    assert t2.result()["id"] == 2
```

### 模拟异步函数

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_with_mock():
    with patch('module.fetch_data', new_callable=AsyncMock) as mock:
        mock.return_value = {"data": "mocked"}
        result = await process()
        assert result == {"data": "mocked"}
        mock.assert_awaited_once()
```

---

## 性能优化

### 避免不必要的上下文切换

```python
# 不好 - 频繁切换
async def process_items(items):
    for item in items:
        await asyncio.sleep(0)  # 强制切换
        await process(item)

# 好 - 批量处理
async def process_items(items):
    async with asyncio.TaskGroup() as tg:
        for item in items:
            tg.create_task(process(item))
```

### 使用 uvloop (生产环境)

```python
import uvloop

async def main():
    ...

if __name__ == "__main__":
    uvloop.install()  # 替换默认事件循环
    asyncio.run(main())
```

### 内存优化

```python
# 使用 __slots__ 减少内存占用
class AsyncTask:
    __slots__ = ['id', 'coro', '_result']

    def __init__(self, id: int, coro: Coroutine):
        self.id = id
        self.coro = coro
        self._result = None
```
