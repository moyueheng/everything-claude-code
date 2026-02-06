#!/usr/bin/env bash
# 按分类添加代理规则到 Clash 配置

RUNTIME_CONFIG="${HOME}/clashctl/resources/runtime.yaml"
RULES_FILE="$(dirname "$0")/../references/proxy-rules.yaml"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 显示帮助
show_help() {
    cat << EOF
用法: $(basename "$0") [选项] [分类1,分类2,...]

选项:
    -h, --help      显示帮助信息
    -l, --list      列出所有可用分类

分类:
    discord     Discord 聊天
    apple       Apple 服务 (App Store, iCloud)
    openai      OpenAI/ChatGPT
    claude      Claude AI
    google      Google 服务
    x           X/Twitter
    tiktok      TikTok
    detection   IP 检测服务

示例:
    $(basename "$0") openai                    # 添加 OpenAI 规则
    $(basename "$0") openai,claude,google      # 添加多个分类
    $(basename "$0") --list                    # 列出所有分类
EOF
}

# 列出所有分类
list_categories() {
    echo "可用分类:"
    echo ""
    grep -E "^[a-z]+:" "$RULES_FILE" | grep -v "^rules:" | sed 's/://g' | while read -r line; do
        echo "  • $line"
    done
    echo ""
    echo "使用方式:"
    echo "  $(basename "$0") <分类名>"
    echo "  $(basename "$0") openai,claude,google"
}

# 检查文件是否存在
check_files() {
    if [ ! -f "$RUNTIME_CONFIG" ]; then
        echo -e "${RED}❌ 未找到配置文件: $RUNTIME_CONFIG${NC}"
        echo "请先安装 Clash"
        exit 1
    fi

    if [ ! -f "$RULES_FILE" ]; then
        echo -e "${RED}❌ 未找到规则文件: $RULES_FILE${NC}"
        exit 1
    fi
}

# 提取指定分类的规则
extract_rules() {
    local category="$1"
    local in_category=false
    local rules=""

    while IFS= read -r line; do
        # 检测分类开始 (格式: "category:")
        if [[ "$line" =~ ^$category:$ ]]; then
            in_category=true
            continue
        fi

        # 检测下一个分类开始（结束当前分类）
        if [ "$in_category" = true ] && [[ "$line" =~ ^[a-z]+:$ ]]; then
            break
        fi

        # 提取规则行 (以 "  - " 开头的 YAML 数组项)
        if [ "$in_category" = true ] && [[ "$line" =~ ^[[:space:]]*-[[:space:]] ]]; then
            rules+="$line"
            rules+=$'\n'
        fi
    done < "$RULES_FILE"

    echo "$rules"
}

# 添加规则到 runtime.yaml
add_rules_to_config() {
    local category="$1"
    local rules

    rules=$(extract_rules "$category")

    if [ -z "$rules" ]; then
        echo -e "${YELLOW}⚠️ 分类 '$category' 未找到或没有规则${NC}"
        return 1
    fi

    # 检查是否已存在该分类的规则
    if grep -q "# $category rules" "$RUNTIME_CONFIG" 2>/dev/null; then
        echo -e "${YELLOW}⚠️ 分类 '$category' 的规则已存在，跳过${NC}"
        return 0
    fi

    # 备份原配置
    cp "$RUNTIME_CONFIG" "${RUNTIME_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)"

    # 创建临时文件
    temp_file=$(mktemp)

    # 读取原文件，在 MATCH 规则前插入新规则
    awk -v rules="$rules" -v category="$category" '
    /^  - MATCH/ {
        print "  # " category " rules"
        print rules
        print ""
    }
    { print }
    ' "$RUNTIME_CONFIG" > "$temp_file"

    # 替换原文件
    mv "$temp_file" "$RUNTIME_CONFIG"

    # 统计规则数量
    local count
    count=$(echo "$rules" | grep -c "DOMAIN" || echo "0")
    echo -e "${GREEN}✅ 已添加 '$category' 分类 ($count 条规则)${NC}"

    return 0
}

# 主逻辑
main() {
    # 检查参数
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi

    # 解析参数
    case "$1" in
        -h|--help)
            show_help
            exit 0
            ;;
        -l|--list)
            list_categories
            exit 0
            ;;
    esac

    # 检查文件
    check_files

    # 解析分类（逗号分隔）
    IFS=',' read -ra CATEGORIES <<< "$1"

    echo -e "${GREEN}📝 正在添加规则...${NC}"
    echo ""

    local success_count=0
    for category in "${CATEGORIES[@]}"; do
        # 去除前后空格
        category=$(echo "$category" | xargs)
        if add_rules_to_config "$category"; then
            ((success_count++))
        fi
    done

    echo ""
    echo -e "${GREEN}✅ 完成！已添加 $success_count 个分类${NC}"
    echo ""
    echo "🔄 请运行以下命令重启代理以生效:"
    echo "   clashoff && clashon"
}

main "$@"
