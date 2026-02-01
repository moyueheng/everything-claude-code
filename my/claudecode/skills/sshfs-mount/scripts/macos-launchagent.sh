#!/bin/bash
# macOS LaunchAgent 配置脚本
# 生成并加载 SSHFS 自动挂载的 LaunchAgent

SCRIPT_PATH="${HOME}/.local/bin/mount-remote.sh"
PLIST_NAME="com.user.sshfs-mount"
PLIST_PATH="${HOME}/Library/LaunchAgents/${PLIST_NAME}.plist"

# 检查脚本是否存在
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "错误: 挂载脚本不存在: $SCRIPT_PATH"
    echo "请先创建挂载脚本并放到 ~/.local/bin/mount-remote.sh"
    exit 1
fi

# 创建 LaunchAgent plist
cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${PLIST_NAME}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>${SCRIPT_PATH}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>WorkingDirectory</key>
    <string>${HOME}</string>
    <key>StandardOutPath</key>
    <string>/tmp/sshfs-launch.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/sshfs-launch.err</string>
</dict>
</plist>
EOF

# 加载 LaunchAgent
launchctl unload "$PLIST_PATH" 2>/dev/null
launchctl load "$PLIST_PATH"

echo "LaunchAgent 已创建并加载: $PLIST_PATH"
echo "状态检查: launchctl list | grep ${PLIST_NAME}"
