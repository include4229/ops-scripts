# 网络功能测试
import pytest
import re
from common.shell import run_cmd
from config.settings import config

pytestmark = pytest.mark.network

class TestNetwork:
    """网络功能测试"""
    
    def test_interface_exists(self):
        """测试网络接口存在"""
        iface = config.TEST_INTERFACE
        ret, out, err = run_cmd(f"ip link show {iface}")
        assert ret == 0, f"网络接口 {iface} 不存在"
    
    def test_interface_up(self):
        """测试网络接口状态为UP"""
        iface = config.TEST_INTERFACE
        ret, out, err = run_cmd(f"ip link show {iface}")
        assert ret == 0, f"获取接口状态失败: {err}"
        assert "state UP" in out or "state UNKNOWN" in out, f"接口 {iface} 未启动"
    
    def test_ip_configured(self):
        """测试网络接口已配置IP"""
        iface = config.TEST_INTERFACE
        ret, out, err = run_cmd(f"ip addr show {iface}")
        assert ret == 0, f"获取IP信息失败: {err}"
        assert re.search(r'inet \d+\.\d+\.\d+\.\d+', out), f"接口 {iface} 未配置IPv4地址"
    
    def test_ping_gateway(self):
        """测试Ping网关连通性"""
        gateway = config.TEST_GATEWAY
        ret, out, err = run_cmd(f"ping -c 4 -W 2 {gateway}")
        assert ret == 0, f"Ping网关 {gateway} 失败"
        assert "0% packet loss" in out, f"网关 {gateway} 丢包"
    
    def test_sshd_service(self):
        """测试SSH服务运行正常"""
        ret, out, err = run_cmd("systemctl is-active sshd")
        if ret != 0:
            ret, out, err = run_cmd("systemctl is-active ssh")
        assert ret == 0, f"SSH服务未运行: {err}"
