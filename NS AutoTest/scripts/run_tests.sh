#!/bin/bash
# 一键运行所有测试

set -e
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "========== 凝思系统自动化测试 =========="
echo "开始时间: $(date)"

mkdir -p reports/html reports/logs

pytest testcases/ \
    --html=reports/html/report.html \
    --self-contained-html \
    -v \
    --tb=short \
    --maxfail=5 \
    "$@"

echo "结束时间: $(date)"
echo "测试报告: $PROJECT_DIR/reports/html/report.html"
