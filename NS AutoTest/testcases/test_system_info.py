# 系统信息测试
import pytest
import re
from common.shell import run_cmd

pytestmark = pytest.mark.system

class TestSystemInfo:
    """系统基本信息测试"""
    
    def test_os_version(self):
        """测试凝思系统版本"""
        ret, out, err = run_cmd("cat /etc/issue")
        assert ret == 0, f"获取系统版本失败: {err}"
        assert "Lines" in out or "凝思" in out, f"未识别为凝思系统: {out}"
    
    def test_kernel_version(self):
        """测试内核版本"""
        ret, out, err = run_cmd("uname -r")
        assert ret == 0, f"获取内核版本失败: {err}"
        assert re.match(r'\d+\.\d+\.\d+', out), f"内核版本格式异常: {out}"
    
    def test_cpu_architecture(self):
        """测试CPU架构"""
        ret, out, err = run_cmd("uname -m")
        assert ret == 0, f"获取CPU架构失败: {err}"
        supported = ["x86_64", "aarch64", "loongarch64", "mips64"]
        assert out in supported, f"不支持的CPU架构: {out}"
