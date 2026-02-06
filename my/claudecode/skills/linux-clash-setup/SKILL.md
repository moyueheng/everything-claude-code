---
name: linux-clash-setup
description: 在 Linux 终端环境下配置 Clash/Mihomo 代理服务。适用于需要配置 SOCKS5/HTTP 代理、管理代理规则、设置 OpenAI/ChatGPT/Claude/Discord/TikTok 等特定域名走代理的场景。支持一键安装、配置代理节点、按分类添加分流规则（discord/apple/openai/claude/google/x/tiktok/detection）。
---

# Linux Clash 代理配置

## 快速开始

### 1. 一键安装

```bash
bash ~/.claude/skills/linux-clash-setup/scripts/install.sh
```

或手动安装：

```bash
git clone --branch master --depth 1 https://github.com/nelvko/clash-for-linux-install.git \
  && cd clash-for-linux-install \
  && bash install.sh
```

### 2. 配置代理节点

编辑 `~/clashctl/resources/runtime.yaml`：

```yaml
proxies:
  - name: "代理节点名称"
    type: socks5  # 或 http
    server: 代理服务器地址
    port: 代理端口
    username: 用户名
    password: 密码
    udp: true

proxy-groups:
  - name: "🚀 节点选择"
    type: select
    proxies:
      - "代理节点名称"
      - DIRECT
```

### 3. 添加分流规则

#### 方式一：使用脚本添加（推荐）

```bash
# 添加 OpenAI 规则
bash ~/.claude/skills/linux-clash-setup/scripts/add-rules.sh openai

# 添加多个分类
bash ~/.claude/skills/linux-clash-setup/scripts/add-rules.sh openai,claude,google

# 查看所有可用分类
bash ~/.claude/skills/linux-clash-setup/scripts/add-rules.sh --list
```

#### 方式二：手动复制规则

参考 `references/proxy-rules.yaml`，复制需要的分类规则到 `runtime.yaml`：

```yaml
rules:
  - DOMAIN,api64.ipify.org,DIRECT
  # OpenAI 相关
  - DOMAIN-SUFFIX,openai.com,🚀 节点选择
  - DOMAIN-SUFFIX,chatgpt.com,🚀 节点选择
  # ... 其他规则
  - MATCH,🚀 节点选择
```

### 4. 启动代理

```bash
clashon       # 开启代理
clashoff      # 关闭代理
clashctl status   # 查看状态
```

## 规则分类

| 分类 | 说明 | 主要域名 |
|------|------|----------|
| `discord` | Discord 聊天 | discord |
| `apple` | Apple 服务 | apple.com, icloud.com, app store |
| `openai` | OpenAI/ChatGPT | openai.com, chatgpt.com, copilot |
| `claude` | Claude AI | claude.ai, anthropic.com |
| `google` | Google 服务 | google.com, youtube, recaptcha |
| `x` | X/Twitter | x.com, twitter.com, twimg.com |
| `tiktok` | TikTok | tiktok.com, byteoversea.com |
| `detection` | IP 检测服务 | ipinfo.io, browserleaks.com |

## 常用命令

| 命令 | 作用 |
|------|------|
| `clashon` / `clashctl on` | 开启代理 |
| `clashoff` / `clashctl off` | 关闭代理 |
| `clashctl status` | 查看内核状态 |
| `clashui` | 显示 Web 面板地址 |
| `clashctl sub add <url>` | 添加订阅 |
| `clashmixin -e` | 编辑 Mixin 配置 |
| `clashmixin -r` | 查看运行时配置 |

## 配置文件位置

- **运行时配置**: `~/clashctl/resources/runtime.yaml`
- **Mixin 配置**: `~/clashctl/resources/mixin.yaml`
- **规则参考**: `~/.claude/skills/linux-clash-setup/references/proxy-rules.yaml`
- **日志文件**: `~/clashctl/resources/mihomo.log`

## 故障排查

### 端口冲突
编辑 `runtime.yaml` 修改端口：
```yaml
mixed-port: 7890
external-controller: "0.0.0.0:9090"
dns:
  listen: 0.0.0.0:1053
```

### 验证配置
```bash
~/clashctl/bin/mihomo -t -f ~/clashctl/resources/runtime.yaml
```

### 查看日志
```bash
tail -f ~/clashctl/resources/mihomo.log
```
