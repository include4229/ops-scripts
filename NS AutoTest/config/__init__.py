#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试项目配置模块
"""

# 直接暴露配置对象，外部用法：from config import config
from .settings import config


__all__ = ['config']
