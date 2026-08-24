# Shell命令执行器
import subprocess
import logging
from config.settings import config

# [NEW] 导入远程执行器
from common.remote import remote_executor

logger = logging.getLogger(__name__)


def run_cmd(cmd: str, timeout=None, check=False, force_local=False):
    """
    执行Shell命令，支持本地或远程（根据配置自动选择）
    
    参数:
        cmd: 要执行的命令
        timeout: 超时秒数
        check: 是否检查返回码
        force_local: 强制本地执行（忽略 REMOTE_MODE 设置）
    
    返回:
        (返回码, 标准输出, 标准错误)
    """
    if timeout is None:
        timeout = config.CMD_TIMEOUT

    # [MODIFIED] 根据配置选择执行方式
    if not force_local and config.REMOTE_MODE:
        logger.info(f"[Remote] Executing: {cmd}")
        try:
            ret, out, err = remote_executor.execute(cmd, timeout=timeout)
        except Exception as e:
            logger.error(f"远程执行失败: {e}")
            raise
    else:
        logger.info(f"[Local] Executing: {cmd}")
        ret, out, err = _local_run_cmd(cmd, timeout)

    # 统一日志记录（已有）
    if ret == 0:
        logger.debug(f"Success: {out[:200]}{'...' if len(out) > 200 else ''}")
    else:
        logger.warning(f"Command returned {ret}: {err[:200]}")

    if check and ret != 0:
        raise subprocess.CalledProcessError(ret, cmd, out, err)

    return ret, out, err


def _local_run_cmd(cmd: str, timeout: int) -> tuple:
    """本地执行（原 run_cmd 的核心逻辑）"""
    try:
        proc = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            executable="/bin/bash"
        )
        stdout = proc.stdout.strip()
        stderr = proc.stderr.strip()
        return proc.returncode, stdout, stderr
    except subprocess.TimeoutExpired:
        logger.error(f"本地命令超时: {cmd}")
        raise
    except Exception as e:
        logger.error(f"本地命令执行错误: {e}")
        raise


# 保留原有辅助函数（无需修改）
def run_cmd_success(cmd: str, timeout=None, force_local=False):
    """执行命令并断言返回码为0"""
    ret, out, err = run_cmd(cmd, timeout, check=True, force_local=force_local)
    return out, err


def get_output(cmd: str, timeout=None, force_local=False) -> str:
    """仅获取标准输出"""
    _, out, _ = run_cmd(cmd, timeout, force_local=force_local)
    return out


def cmd_exists(cmd: str, force_local=False) -> bool:
    """检查命令是否存在（本地或远程）"""
    ret, _, _ = run_cmd(f"command -v {cmd}", force_local=force_local)
    return ret == 0
