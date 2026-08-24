# 磁盘I/O测试
import pytest
import os
from common.shell import run_cmd, cmd_exists
from config.settings import config

pytestmark = pytest.mark.disk

class TestDiskIO:
    """磁盘I/O测试"""
    
    @pytest.mark.skipif(
        not os.path.exists(config.TEST_DISK),
        reason=f"测试磁盘 {config.TEST_DISK} 不存在"
    )
    def test_disk_read_performance(self):
        """测试磁盘读取性能"""
        if not cmd_exists("hdparm"):
            pytest.skip("hdparm未安装")
        disk = config.TEST_DISK
        ret, out, err = run_cmd(f"hdparm -tT {disk}")
        assert ret == 0, f"磁盘性能测试失败: {err}"
    
    def test_disk_space(self):
        """测试磁盘空间检查"""
        ret, out, err = run_cmd("df -h /")
        assert ret == 0, f"获取磁盘空间失败: {err}"
        # 解析使用率
        lines = out.strip().split('\n')
        if len(lines) >= 2:
            parts = lines[1].split()
            if len(parts) >= 5:
                usage = int(parts[4].replace('%', ''))
                assert usage < 90, f"根分区使用率过高: {usage}%"
