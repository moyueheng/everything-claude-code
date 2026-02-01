#!/bin/bash
# SSHFS 自动挂载脚本
# 用法: 修改变量后放到 ~/.local/bin/mount-remote.sh，添加执行权限

# ============== 配置区域 ==============
MOUNT_POINT="$HOME/Remote/server-name"      # 本地挂载路径
REMOTE_HOST="user@hostname"                 # SSH 连接地址
REMOTE_PATH="/remote/path"                  # 远程目录路径
# ============== 配置结束 ==============

LOG_FILE="/tmp/sshfs-mount.log"
DISABLE_FILE="$HOME/.config/sshfs-mount-disabled"
SSHFS_CMD="sshfs"

# macOS 检测
if [[ "$OSTYPE" == "darwin"* ]]; then
    SSHFS_CMD="/usr/local/bin/sshfs"
fi

# 检查是否禁用
if [ -f "$DISABLE_FILE" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 自动挂载已禁用，跳过" >> "$LOG_FILE"
    exit 0
fi

# 等待网络和 SSH 就绪
wait_for_ssh() {
    local max_attempts=30
    local attempt=0

    while [ $attempt -lt $max_attempts ]; do
        if ssh -o ConnectTimeout=5 -o BatchMode=yes "$REMOTE_HOST" "echo ok" >/dev/null 2>&1; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] SSH 连接成功" >> "$LOG_FILE"
            return 0
        fi
        ((attempt++))
        sleep 2
    done

    echo "[$(date '+%Y-%m-%d %H:%M:%S')] SSH 连接超时" >> "$LOG_FILE"
    return 1
}

# 创建挂载点
mkdir -p "$MOUNT_POINT"

# 检查是否已挂载
if mount | grep -q "$MOUNT_POINT"; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 已挂载，跳过" >> "$LOG_FILE"
    exit 0
fi

# 等待 SSH 就绪
wait_for_ssh || exit 1

# 卸载可能存在的残留挂载
umount "$MOUNT_POINT" 2>/dev/null
sleep 1

# 挂载
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始挂载..." >> "$LOG_FILE"
$SSHFS_CMD "$REMOTE_HOST:$REMOTE_PATH" "$MOUNT_POINT" \
    -o reconnect \
    -o follow_symlinks \
    -o defer_permissions \
    2>> "$LOG_FILE"

if [ $? -eq 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 挂载成功" >> "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 挂载失败" >> "$LOG_FILE"
    exit 1
fi
