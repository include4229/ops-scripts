#!/bin/bash
# 凝思系统自动化测试环境准备脚本

set -e
echo "========== 凝思系统自动化测试环境准备 =========="

# 检查Python
python3 --version || { echo "Python3未安装"; exit 1; }

# 安装pip
if ! command -v pip3 &> /dev/null; then
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm -f get-pip.py
fi

# 安装Python依赖
pip3 install -r requirements.txt

# 安装系统工具
if command -v yum &> /dev/null; then
    yum install -y stress hdparm iperf3 sysstat || true
elif command -v apt &> /dev/null; then
    apt update
    apt install -y stress hdparm iperf3 sysstat || true
fi

echo "========== 环境准备完成 =========="
