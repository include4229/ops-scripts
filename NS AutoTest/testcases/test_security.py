# 安全功能测试
import pytest
import re
from common.shell import run_cmd

pytestmark = pytest.mark.security

class TestSecurity:
    """安全功能测试"""
    
    def test_selinux_status(self):
        """测试SELinux状态"""
        ret, out, err = run_cmd("getenforce")
        if ret != 0:
            pytest.skip("SELinux未安装")
        assert out in ["Enforcing", "Permissive", "Disabled"], f"SELinux状态异常: {out}"
    
    def test_password_policy(self):
        """测试密码策略"""
        ret, out, err = run_cmd("grep ^PASS_MIN_LEN /etc/login.defs")
        if ret == 0:
            match = re.search(r'PASS_MIN_LEN\s+(\d+)', out)
            if match:
                min_len = int(match.group(1))
                assert min_len >= 8, f"密码最小长度不足: {min_len}"
    
    def test_sudo_config(self):
        """测试sudo配置安全检查"""
        ret, out, err = run_cmd("visudo -c")
        assert ret == 0, f"sudo配置语法错误: {err}"
