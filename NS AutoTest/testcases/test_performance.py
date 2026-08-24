# 性能基准测试
import pytest
import time
from common.shell import run_cmd, cmd_exists
from config.settings import config

pytestmark = pytest.mark.performance

class TestPerformance:
    """性能基准测试"""
    
    @pytest.mark.slow
    def test_cpu_stress(self):
        """测试CPU压力测试"""
        if not cmd_exists("stress"):
            pytest.skip("stress未安装")
        cores = config.STRESS_CPU_CORES
        duration = config.STRESS_DURATION
        start = time.time()
        ret, out, err = run_cmd(f"stress --cpu {cores} --timeout {duration}")
        end = time.time()
        elapsed = end - start
        assert elapsed >= duration * 0.9, f"压力测试提前结束: {elapsed}s"
    
    def test_memory_usage(self):
        """测试内存使用率检查"""
        ret, out, err = run_cmd("free -m")
        assert ret == 0, f"获取内存信息失败: {err}"
        import re
        for line in out.strip().split('\n'):
            if 'Mem:' in line:
                parts = re.split(r'\s+', line)
                if len(parts) >= 3:
                    total, used = int(parts[1]), int(parts[2])
                    usage_rate = used / total * 100
                    assert usage_rate < 90, f"内存使用率过高: {usage_rate:.1f}%"
                break
