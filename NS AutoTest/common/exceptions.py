# 自定义异常
class NSITestError(Exception):
    """凝思测试基础异常"""
    pass

class CommandExecutionError(NSITestError):
    """命令执行失败"""
    pass

class TestEnvironmentError(NSITestError):
    """测试环境异常"""
    pass

class PerformanceThresholdError(NSITestError):
    """性能指标超出阈值"""
    pass
