# 项目目录结构说明

| 目录/文件 | 说明 |
| :--- | :--- |
| **NS-AutoTest/** | 项目根目录 |
| ├── **config/** | 配置文件目录 |
| │   ├── `__init__.py` | 包标识文件 |
| │   ├── `settings.py` | 全局配置（IP、路径、超时等） |
| │   └── `hosts.yaml` | 多主机环境配置（可选） |
| ├── **common/** | 公共函数库 |
| │   ├── `__init__.py` | 包标识文件 |
| │   ├── `shell.py` | Shell命令执行器 |
| │   ├── `logger.py` | 日志模块 |
| │   ├── `report.py` | 报告生成辅助 |
| │   └── `exceptions.py` | 自定义异常 |
| ├── **testcases/** | 测试用例（按模块划分） |
| │   ├── `__init__.py` | 包标识文件 |
| │   ├── `test_system_info.py` | 系统信息测试 |
| │   ├── `test_user_mgmt.py` | 用户管理测试 |
| │   ├── `test_network.py` | 网络功能测试 |
| │   ├── `test_disk_io.py` | 磁盘I/O测试 |
| │   ├── `test_security.py` | 安全功能测试 |
| │   └── `test_performance.py` | 性能基准测试 |
| ├── **fixtures/** | 测试数据（JSON/YAML文件） |
| │   ├── `test_users.json` | 用户测试数据 |
| │   └── `network_config.json` | 网络测试数据 |
| ├── **reports/** | 测试报告输出目录 |
| │   ├── **html/** | HTML报告 |
| │   └── **logs/** | 日志文件 |
| ├── **scripts/** | 辅助脚本 |
| │   ├── `setup_env.sh` | 环境准备脚本 |
| │   └── `run_tests.sh` | 一键运行脚本 |
| ├── `requirements.txt` | Python依赖 |
| ├── `pytest.ini` | Pytest配置 |
| ├── `conftest.py` | Pytest共享fixtures |
| ├── `pyproject.toml` | 项目元数据（可选） |
| └── `README.md` | 项目说明文档 |
