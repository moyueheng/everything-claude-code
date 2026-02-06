#!/usr/bin/env bash
# Linux Clash 一键安装脚本

set -e

CLASH_DIR="${HOME}/clashctl"

echo "🚀 开始安装 Clash for Linux..."

# 检查是否已安装
if [ -d "$CLASH_DIR" ]; then
    echo "⚠️ 检测到已存在的安装，正在重新安装..."
    rm -rf "$CLASH_DIR"
fi

# 克隆仓库
echo "📦 下载安装脚本..."
cd /tmp
rm -rf clash-for-linux-install
git clone --branch master --depth 1 https://github.com/nelvko/clash-for-linux-install.git

# 运行安装
cd clash-for-linux-install
bash install.sh

echo "✅ 安装完成！"
echo ""
echo "常用命令:"
echo "  clashon      - 开启代理"
echo "  clashoff     - 关闭代理"
echo "  clashctl status - 查看状态"
echo "  clashui      - 查看 Web 面板地址"
