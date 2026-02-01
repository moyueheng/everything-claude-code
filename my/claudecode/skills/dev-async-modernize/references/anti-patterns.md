# Python 异步反模式目录

本文档列出常见的 Python 异步代码反模式及其修复方案。

## 目录

1. [阻塞调用](#阻塞调用)
2. [协程管理](#协程管理)
3. [异常处理](#异常处理)
4. [资源管理](#资源管理)
5. [并发控制](#并发控制)

---

## 阻塞调用

### 1. `time.sleep()` 在异步函数中

**反模式:**
```python
import time

async def fetch_data():
    time.sleep(1)  # 阻塞整个事件循环!
    return data
```

**修复:**
```python
import asyncio

async def fetch_data():
    await asyncio.sleep(1)
    return data
```

### 2. 使用同步 HTTP 库

**反模式:**
```python
import requests

async def fetch_url(url):
    response = requests.get(url)  # 阻塞!
    return response.json()
```

**修复:**
```python
import aiohttp

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
```

### 3. 同步文件 I/O

**反模式:**
```python
async def read_config(path):
    with open(path) as f:  # 阻塞!
        return f.read()
```

**修复:**
```python
import aiofiles

async def read_config(path):
    async with aiofiles.open(path) as f:
        return await f.read()
```

### 4. 同步数据库操作

**反模式:**
```python
import sqlite3

async def query_db(sql):
    conn = sqlite3.connect('db.sqlite')  # 阻塞!
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()
```

**修复:**
```python
import aiosqlite

async def query_db(sql):
    async with aiosqlite.connect('db.sqlite') as db:
        async with db.execute(sql) as cursor:
            return await cursor.fetchall()
```

---

## 协程管理

### 1. 忘记 await

**反模式:**
```python
async def process():
    fetch_data()  # 协程被创建但从未执行!
    print("done")
```

**修复:**
```python
async def process():
    await fetch_data()
    print("done")
```

### 2. 裸协程调用

**反模式:**
```python
async def main():
    for url in urls:
        fetch_url(url)  # 什么都不做!
```

**修复:**
```python
async def main():
    async with asyncio.TaskGroup() as tg:
        for url in urls:
            tg.create_task(fetch_url(url))
```

### 3. 未保存的任务引用

**反模式:**
```python
async def main():
    asyncio.create_task(fetch_data())
    # 如果 main 结束，任务可能被取消
```

**修复:**
```python
async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(fetch_data())
    # TaskGroup 确保所有任务完成
```

### 4. 过时: `asyncio.gather()` 无异常处理

**反模式:**
```python
async def main():
    results = await asyncio.gather(
        fetch_data(1),
        fetch_data(2),
        fetch_data(3),
    )
    # 如果一个任务失败，其他任务被取消但异常处理困难
```

**修复 (Python 3.11+):**
```python
async def main():
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(fetch_data(1))
        t2 = tg.create_task(fetch_data(2))
        t3 = tg.create_task(fetch_data(3))
    # 结果: t1.result(), t2.result(), t3.result()
```

---

## 异常处理

### 1. 吞掉异常

**反模式:**
```python
async def main():
    try:
        await asyncio.gather(*tasks, return_exceptions=True)
    except Exception:
        pass  # 所有异常都被静默吞掉
```

**修复:**
```python
async def main():
    try:
        async with asyncio.TaskGroup() as tg:
            for task in tasks:
                tg.create_task(task)
    except* ValueError as eg:
        for exc in eg.exceptions:
            logger.error(f"ValueError: {exc}")
```

### 2. 忽略 CancelledError

**反模式:**
```python
async def worker():
    try:
        await process()
    except Exception:
        logger.error("Error")
        # CancelledError 被吞掉，任务无法被取消!
```

**修复:**
```python
async def worker():
    try:
        await process()
    except asyncio.CancelledError:
        logger.info("Task cancelled")
        raise  # 必须重新抛出!
    except Exception:
        logger.error("Error")
```

### 3. 不使用 ExceptionGroup

**反模式 (Python 3.11+):**
```python
try:
    await asyncio.gather(*tasks)
except Exception as e:
    # 只能捕获第一个异常
    handle_error(e)
```

**修复:**
```python
try:
    async with asyncio.TaskGroup() as tg:
        for task in tasks:
            tg.create_task(task)
except* ExceptionGroup as eg:
    # 可以处理所有异常
    for exc in eg.exceptions:
        handle_error(exc)
```

---

## 资源管理

### 1. 忘记关闭会话

**反模式:**
```python
async def fetch():
    session = aiohttp.ClientSession()
    async with session.get(url) as resp:
        return await resp.text()
    # session 没有关闭!
```

**修复:**
```python
async def fetch():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()
```

### 2. 不使用 async with

**反模式:**
```python
async def process():
    f = await aiofiles.open(path)
    data = await f.read()
    # 如果异常发生，文件不会关闭!
```

**修复:**
```python
async def process():
    async with await aiofiles.open(path) as f:
        data = await f.read()
```

---

## 并发控制

### 1. 无限制并发

**反模式:**
```python
async def fetch_all(items):
    tasks = [fetch(item) for item in items]
    await asyncio.gather(*tasks)
    # 如果 items 有 10000 个，会创建 10000 个并发任务!
```

**修复:**
```python
async def fetch_all(items):
    semaphore = asyncio.Semaphore(100)

    async def fetch_with_limit(item):
        async with semaphore:
            return await fetch(item)

    async with asyncio.TaskGroup() as tg:
        for item in items:
            tg.create_task(fetch_with_limit(item))
```

### 2. 不使用超时

**反模式:**
```python
async def fetch():
    # 可能永远挂起!
    return await slow_operation()
```

**修复:**
```python
async def fetch():
    async with asyncio.timeout(5.0):
        return await slow_operation()
```

---

## 过时 API

### 1. `asyncio.get_event_loop()`

**过时:**
```python
loop = asyncio.get_event_loop()  # Python 3.10+ 已过时
loop.run_until_complete(main())
```

**现代:**
```python
asyncio.run(main())  # Python 3.7+
```

### 2. `asyncio.ensure_future()`

**过时:**
```python
task = asyncio.ensure_future(coroutine())
```

**现代:**
```python
task = asyncio.create_task(coroutine())
```

### 3. `@asyncio.coroutine`

**过时:**
```python
@asyncio.coroutine
def old_style():
    yield from asyncio.sleep(1)
```

**现代:**
```python
async def new_style():
    await asyncio.sleep(1)
```
