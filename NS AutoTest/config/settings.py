# 全局配置（IP、路径、超时等）
import os

class Config:
    # 测试环境
    TEST_ENV = os.getenv("NSI_TEST_ENV", "local")
    
    # 超时配置
    CMD_TIMEOUT = int(os.getenv("NSI_CMD_TIMEOUT", 60))
    TEST_TIMEOUT = int(os.getenv("NSI_TEST_TIMEOUT", 300))
    
    # 网络测试配置
    TEST_GATEWAY = os.getenv("NSI_GATEWAY", "192.168.1.1")
    TEST_PING_HOST = os.getenv("NSI_PING_HOST", "www.baidu.com")
    TEST_INTERFACE = os.getenv("NSI_INTERFACE", "eth0")
    
    # 磁盘测试配置
    TEST_DISK = os.getenv("NSI_TEST_DISK", "/dev/sda")
    TEST_MOUNT_POINT = os.getenv("NSI_MOUNT_POINT", "/mnt/test")
    
    # 性能测试配置
    STRESS_CPU_CORES = int(os.getenv("NSI_STRESS_CORES", 4))
    STRESS_DURATION = int(os.getenv("NSI_STRESS_DURATION", 60))
    
    # 报告路径
    REPORT_DIR = os.getenv("NSI_REPORT_DIR", "reports")
    LOG_DIR = os.path.join(REPORT_DIR, "logs")
    
    # 调试模式
    DEBUG = os.getenv("NSI_DEBUG", "false").lower() == "true"

    # 是否启用远程模式（true: 通过 SSH 执行命令到远程主机；false: 本地执行）
    REMOTE_MODE = os.getenv("NSI_REMOTE_MODE", "true").lower() == "true"
    
    # 远程主机连接信息
    SSH_HOST = os.getenv("NSI_SSH_HOST", "192.168.1.10")
    SSH_PORT = int(os.getenv("NSI_SSH_PORT", 22))
    SSH_USERNAME = os.getenv("NSI_SSH_USERNAME", "root")
    SSH_PASSWORD = os.getenv("NSI_SSH_PASSWORD", "")          # 密码或密钥二选一
    SSH_KEY_FILE = os.getenv("NSI_SSH_KEY_FILE", "")          # 私钥文件路径（如 ~/.ssh/id_rsa）
    SSH_CONNECT_TIMEOUT = int(os.getenv("NSI_SSH_TIMEOUT", 10))  # 连接超时（秒）

config = Config()
