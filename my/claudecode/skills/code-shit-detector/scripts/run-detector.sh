#!/bin/bash
#
# 代码屎山检测脚本
# 使用 fuck-u-code 工具进行代码质量分析
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 默认配置
LANGUAGE="zh-CN"
TOP_COUNT=15
ISSUES_COUNT=5
OUTPUT_FILE=""
MODE="standard"

# 检查 fuck-u-code 是否安装
check_tool() {
    if ! command -v fuck-u-code &> /dev/null; then
        # 尝试从 Go bin 目录查找
        if [ -x "$HOME/go/bin/fuck-u-code" ]; then
            export PATH="$PATH:$HOME/go/bin"
        elif [ -x "$(go env GOPATH)/bin/fuck-u-code" ]; then
            export PATH="$PATH:$(go env GOPATH)/bin"
        else
            echo -e "${RED}错误: fuck-u-code 工具未安装${NC}"
            echo "请运行: go install github.com/Done-0/fuck-u-code/cmd/fuck-u-code@latest"
            exit 1
        fi
    fi
}

# 显示帮助
show_help() {
    cat << EOF
代码屎山检测器

用法: $0 <项目路径> [选项]

选项:
    --full              生成完整详细报告
    --summary, -s       仅显示总结
    --markdown, -m      生成 Markdown 格式报告
    --top N             显示最烂的前 N 个文件 (默认: 15)
    --issues N          每文件显示 N 个问题 (默认: 5)
    --lang LANG         报告语言: zh-CN/en-US/ru-RU (默认: zh-CN)
    --output FILE, -o   输出到文件
    --help, -h          显示此帮助

示例:
    $0 /path/to/project
    $0 /path/to/project --full
    $0 /path/to/project --markdown --output report.md
    $0 /path/to/project --summary --top 10
EOF
}

# 解析参数
parse_args() {
    if [ $# -eq 0 ]; then
        show_help
        exit 1
    fi

    # 第一个参数是项目路径
    PROJECT_PATH="$1"
    shift

    while [[ $# -gt 0 ]]; do
        case $1 in
            --full)
                MODE="full"
                shift
                ;;
            --summary|-s)
                MODE="summary"
                shift
                ;;
            --markdown|-m)
                MODE="markdown"
                shift
                ;;
            --top)
                TOP_COUNT="$2"
                shift 2
                ;;
            --issues)
                ISSUES_COUNT="$2"
                shift 2
                ;;
            --lang)
                LANGUAGE="$2"
                shift 2
                ;;
            --output|-o)
                OUTPUT_FILE="$2"
                shift 2
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                echo -e "${RED}未知选项: $1${NC}"
                show_help
                exit 1
                ;;
        esac
    done
}

# 运行检测
run_detection() {
    local cmd="fuck-u-code"

    # 构建命令
    case $MODE in
        summary)
            cmd="$cmd \"$PROJECT_PATH\" --summary --lang $LANGUAGE"
            ;;
        markdown)
            cmd="$cmd \"$PROJECT_PATH\" --markdown --top $TOP_COUNT --lang $LANGUAGE"
            ;;
        full)
            cmd="$cmd \"$PROJECT_PATH\" --verbose --top $TOP_COUNT --issues $ISSUES_COUNT --lang $LANGUAGE"
            ;;
        *)
            cmd="$cmd \"$PROJECT_PATH\" --top $TOP_COUNT --issues $ISSUES_COUNT --lang $LANGUAGE"
            ;;
    esac

    echo -e "${BLUE}正在分析项目: $PROJECT_PATH${NC}"
    echo -e "${BLUE}模式: $MODE, 语言: $LANGUAGE${NC}"
    echo ""

    if [ -n "$OUTPUT_FILE" ]; then
        eval "$cmd" > "$OUTPUT_FILE" 2>&1
        echo -e "${GREEN}报告已保存到: $OUTPUT_FILE${NC}"
    else
        eval "$cmd" 2>&1"
    fi
}

# 主函数
main() {
    check_tool
    parse_args "$@"
    run_detection
}

main "$@"
