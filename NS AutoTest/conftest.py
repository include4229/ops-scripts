# Pytest共享fixtures
import pytest
import logging
import time
from common.shell import run_cmd
from common.logger import setup_logger

# [NEW] 导入远程执行器，方便测试中直接获取连接
from common.remote import remote_executor

setup_logger()

@pytest.fixture(scope="session")
def system_info():
    """获取系统基本信息（支持远程）"""
    _, os_version, _ = run_cmd("cat /etc/issue")
    _, kernel, _ = run_cmd("uname -r")
    _, arch, _ = run_cmd("uname -m")
    return {"os": os_version, "kernel": kernel, "arch": arch}

@pytest.fixture(scope="function")
def test_user():
    """创建临时测试用户（远程同样有效）"""
    username = f"testuser_{int(time.time())}"
    run_cmd(f"useradd -m {username}")
    yield username
    run_cmd(f"userdel -r {username}")

@pytest.fixture(scope="function")
def temp_file():
    """创建临时测试文件（本地文件，远程测试需注意路径）"""
    import tempfile, os
    fd, path = tempfile.mkstemp(prefix="nsi_test_")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)

@pytest.fixture
def test_data():
    import json, os
    data_path = os.path.join(os.path.dirname(__file__), "fixtures", "test_users.json")
    if os.path.exists(data_path):
        with open(data_path, 'r') as f:
            return json.load(f)
    return {}

# ========== [NEW] 提供远程执行器 fixture，方便测试中直接调用 ==========
@pytest.fixture(scope="session")
def ssh_executor():
    """返回远程执行器单例（可用于高级操作）"""
    return remote_executor
