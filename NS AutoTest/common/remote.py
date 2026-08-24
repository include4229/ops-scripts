#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
远程 SSH 命令执行器（单例模式）
负责管理与远程主机的 SSH 连接，并执行命令。
"""
import paramiko
import logging
from config.settings import config

logger = logging.getLogger(__name__)


class RemoteExecutor:
    """SSH 远程执行器（单例）"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._client = None
        self._connect()

    def _connect(self):
        """建立 SSH 连接"""
        if not config.REMOTE_MODE:
            logger.info("远程模式未启用，跳过 SSH 连接")
            return

        try:
            self._client = paramiko.SSHClient()
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            connect_kwargs = {
                "hostname": config.SSH_HOST,
                "port": config.SSH_PORT,
                "username": config.SSH_USERNAME,
                "timeout": config.SSH_CONNECT_TIMEOUT,
            }

            # 优先使用密钥，否则使用密码
            if config.SSH_KEY_FILE:
                connect_kwargs["key_filename"] = config.SSH_KEY_FILE
                logger.info(f"使用密钥文件连接 {config.SSH_HOST}")
            elif config.SSH_PASSWORD:
                connect_kwargs["password"] = config.SSH_PASSWORD
                logger.info(f"使用密码连接 {config.SSH_HOST}")
            else:
                raise ValueError("未配置 SSH 密码或密钥文件")

            self._client.connect(**connect_kwargs)
            logger.info(f"SSH 连接成功: {config.SSH_HOST}:{config.SSH_PORT}")

        except Exception as e:
            logger.error(f"SSH 连接失败: {e}")
            raise

    def execute(self, command: str, timeout: int = None) -> tuple:
        """
        在远程主机执行命令
        
        返回: (返回码, 标准输出, 标准错误)
        """
        if not config.REMOTE_MODE:
            raise RuntimeError("远程模式未启用，不能调用远程执行")

        if self._client is None:
            self._connect()

        try:
            stdin, stdout, stderr = self._client.exec_command(command, timeout=timeout)
            # 读取输出（需等待命令结束）
            out = stdout.read().decode('utf-8', errors='ignore').strip()
            err = stderr.read().decode('utf-8', errors='ignore').strip()
            # 获取返回码
            exit_code = stdout.channel.recv_exit_status()
            return exit_code, out, err
        except Exception as e:
            logger.error(f"远程命令执行失败: {command}, 错误: {e}")
            raise

    def close(self):
        """关闭 SSH 连接"""
        if self._client:
            self._client.close()
            logger.info("SSH 连接已关闭")

    # 支持上下文管理器
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


# 全局单例实例（使用时自动连接）
remote_executor = RemoteExecutor()
