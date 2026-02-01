#!/bin/bash
# Linux systemd 用户服务配置脚本
# 配置 SSHFS 自动挂载的 systemd 服务

SCRIPT_PATH="${HOME}/.local/bin/mount-remote.sh"
SERVICE_NAME="sshfs-mount"
SERVICE_PATH="${HOME}/.config/systemd/user/${SERVICE_NAME}.service"

# 检查脚本是否存在
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "错误: 挂载脚本不存在: $SCRIPT_PATH"
    echo "请先创建挂载脚本并放到 ~/.local/bin/mount-remote.sh"
    exit 1
fi

# 创建服务目录
mkdir -p "$(dirname "$SERVICE_PATH")"

# 创建 systemd 服务文件
cat > "$SERVICE_PATH" << EOF
[Unit]
Description=SSHFS Auto Mount
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=${SCRIPT_PATH}
RemainAfterExit=yes

[Install]
WantedBy=default.target
EOF

# 重新加载 systemd 并启用服务
systemctl --user daemon-reload
systemctl --user enable "$SERVICE_NAME"
systemctl --user start "$SERVICE_NAME"

echo "systemd 服务已创建并启用: $SERVICE_PATH"
echo "状态检查: systemctl --user status $SERVICE_NAME"
