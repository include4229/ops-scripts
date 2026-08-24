# 用户管理测试
import pytest
import time
from common.shell import run_cmd

pytestmark = pytest.mark.user

class TestUserManagement:
    """用户管理功能测试"""
    
    @pytest.fixture
    def test_user(self):
        """创建临时测试用户"""
        username = f"testuser_{int(time.time())}"
        run_cmd(f"useradd -m {username}")
        yield username
        run_cmd(f"userdel -r {username}")
    
    def test_create_user(self, test_user):
        """测试创建用户"""
        ret, out, err = run_cmd(f"id {test_user}")
        assert ret == 0, f"用户 {test_user} 不存在"
    
    def test_user_has_home_dir(self, test_user):
        """测试用户家目录"""
        ret, out, err = run_cmd(f"ls -la /home/{test_user}")
        assert ret == 0, f"用户家目录不存在"
    
    def test_set_user_password(self, test_user):
        """测试设置用户密码"""
        ret, out, err = run_cmd(f"echo '{test_user}:Test123!' | chpasswd")
        assert ret == 0, f"设置密码失败: {err}"
