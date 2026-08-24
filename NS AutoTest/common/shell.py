# Shell命令执行器
import subprocess
import logging
from config.settings import config

logger = logging.getLogger(__name__)

def run_cmd(cmd: str, timeout=None, check=False):
    """执行Shell命令，返回(返回码, 标准输出, 标准错误)"""
    if timeout is None:
        timeout = config.CMD_TIMEOUT
    
    logger.info(f"Executing: {cmd}")
    try:
        proc = subprocess.run(
            cmd, shell=True, capture_output=True, 
            text=True, timeout=timeout, executable="/bin/bash"
        )
        stdout, stderr = proc.stdout.strip(), proc.stderr.strip()
        
        if check and proc.returncode != 0:
            raise subprocess.CalledProcessError(proc.returncode, cmd, stdout, stderr)
        
        return proc.returncode, stdout, stderr
    except subprocess.TimeoutExpired:
        logger.error(f"Command timeout: {cmd}")
        raise
    except Exception as e:
        logger.error(f"Command error: {e}")
        raise

def run_cmd_success(cmd: str, timeout=None):
    """执行命令并断言返回码为0"""
    ret, out, err = run_cmd(cmd, timeout, check=True)
    return out, err

def get_output(cmd: str, timeout=None) -> str:
    """仅获取命令的标准输出"""
    _, out, _ = run_cmd(cmd, timeout)
    return out

def cmd_exists(cmd: str) -> bool:
    """检查命令是否存在"""
    ret, _, _ = run_cmd(f"command -v {cmd}")
    return ret == 0
