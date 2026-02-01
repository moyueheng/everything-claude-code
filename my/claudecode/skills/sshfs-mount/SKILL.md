---
name: sshfs-mount
description: SSH 远程目录挂载到本地，像 NAS 一样访问。当用户需要"把远程服务器的某个路径挂载到本地"、"在 Finder 中访问远程文件"、"像 NAS 一样访问服务器目录"时使用。支持 macOS (FUSE-T) 和 Linux。包含自动挂载脚本、登录项配置和开关控制。
---

# SSHFS 远程挂载

通过 SSHFS 将远程服务器目录挂载到本地，无需在服务器上安装任何服务。

## 快速开始

### 1. 确认 SSH 免密登录

```bash
# 测试免密登录
ssh user@hostname "echo ok"
```

如果需要密码，先配置 SSH key：

```bash
# 生成密钥（如果没有）
ssh-keygen -t ed25519

# 复制公钥到服务器
ssh-copy-id user@hostname
```

### 2. 安装 SSHFS

**macOS (推荐 FUSE-T，无需内核扩展):**

```bash
brew tap macos-fuse-t/homebrew-cask
brew install fuse-t fuse-t-sshfs
```

**Linux:**

```bash
# Ubuntu/Debian
sudo apt install sshfs

# CentOS/RHEL
sudo yum install fuse-sshfs
```

### 3. 挂载

```bash
# 创建挂载点
mkdir -p ~/Remote/server-name

# 挂载远程目录
sshfs user@hostname:/remote/path ~/Remote/server-name -o reconnect

# macOS 在 Finder 中打开
open ~/Remote/server-name
```

## 自动挂载

### 创建挂载脚本

使用 `scripts/mount.sh` 模板，修改变量：

- `MOUNT_POINT`: 本地挂载路径
- `REMOTE_HOST`: SSH 连接地址 (user@host)
- `REMOTE_PATH`: 远程目录路径

将脚本放到 `~/.local/bin/` 并添加执行权限：

```bash
chmod +x ~/.local/bin/mount-remote.sh
```

### macOS LaunchAgent

使用 `scripts/macos-launchagent.sh` 生成并加载 LaunchAgent：

```bash
bash scripts/macos-launchagent.sh
```

### macOS 登录项

1. 系统设置 → 通用 → 登录项
2. 点击 + 添加 `~/.local/bin/mount-remote.sh`

### Linux systemd

使用 `scripts/linux-systemd.sh` 配置：

```bash
bash scripts/linux-systemd.sh
```

## 控制开关

添加到 shell 配置 (`~/.zshrc` 或 `~/.bashrc`)：

```bash
# 禁用自动挂载
sshfs-disable() {
    mkdir -p ~/.config
    touch ~/.config/sshfs-mount-disabled
    echo "开机自动挂载已禁用"
}

# 启用自动挂载
sshfs-enable() {
    rm -f ~/.config/sshfs-mount-disabled
    echo "开机自动挂载已启用"
}

# 查看状态
sshfs-status() {
    if [ -f ~/.config/sshfs-mount-disabled ]; then
        echo "开机自动挂载：已禁用"
    else
        echo "开机自动挂载：已启用"
    fi
}
```

## 常用操作

```bash
# 查看挂载状态
mount | grep -E "sshfs|fuse-t"

# 查看日志
tail -f /tmp/sshfs-mount.log

# 卸载
umount ~/Remote/server-name

# macOS 强制卸载
diskutil unmount ~/Remote/server-name
```

## 故障排查

| 问题 | 解决方案 |
|------|----------|
| `fuse: unknown option` | 删除不支持的选项（如 `connect_timeout`） |
| `remote host has disconnected` | 网络未就绪，脚本会自动等待重试 |
| `permission denied` | 检查 SSH 免密登录配置 |
| 挂载目录为空 | 检查远程路径是否正确 |

## 资源

- `scripts/mount.sh` - 挂载脚本模板（带网络等待和开关）
- `scripts/macos-launchagent.sh` - macOS LaunchAgent 生成器
- `scripts/linux-systemd.sh` - Linux systemd 配置脚本
