项目结构说明



| 文件路径 | 说明 |
| :--- | :--- |
| **config/** | **配置** |
| `NS-AutoTest/config/__init__.py` | 包标识文件 |
| `NS-AutoTest/config/settings.py` | 全局配置（IP、路径、超时等） |
| `NS-AutoTest/config/hosts.yaml` | 多主机环境配置（可选） |
| **common/** | |
| `NS-AutoTest/common/__init__.py` | 包标识文件 |
| `NS-AutoTest/common/shell.py` | Shell命令执行器 |
| `NS-AutoTest/common/logger.py` | 日志模块 |
| `NS-AutoTest/common/report.py` | 报告生成辅助 |
| `NS-AutoTest/common/exceptions.py` | 自定义异常 |
| **testcases/** | |
| `NS-AutoTest/testcases/__init__.py` | 包标识文件 |
| `NS-AutoTest/testcases/test_system_info.py` | 系统信息测试 |
| `NS-AutoTest/testcases/test_user_mgmt.py` | 用户管理测试 |
| `NS-AutoTest/testcases/test_network.py` | 网络功能测试 |
| `NS-AutoTest/testcases/test_disk_io.py` | 磁盘I/O测试 |
| `NS-AutoTest/testcases/test_security.py` | 安全功能测试 |
| `NS-AutoTest/testcases/test_performance.py` | 性能基准测试 |
| **fixtures/** | |
| `NS-AutoTest/fixtures/test_users.json` | 用户测试数据 |
| `NS-AutoTest/fixtures/network_config.json` | 网络测试数据 |
| **reports/** | |
| `NS-AutoTest/reports/html/` | HTML报告目录 |
| `NS-AutoTest/reports/logs/` | 日志文件目录 |
| **scripts/** | |
| `NS-AutoTest/scripts/setup_env.sh` | 环境准备脚本 |
| `NS-AutoTest/scripts/run_tests.sh` | 一键运行脚本 |
| **根目录文件** | |
| `NS-AutoTest/requirements.txt` | Python依赖 |
| `NS-AutoTest/pytest.ini` | Pytest配置 |
| `NS-AutoTest/conftest.py` | Pytest共享fixtures |
| `NS-AutoTest/pyproject.toml` | 项目元数据（可选） |
| `NS-AutoTest/README.md` | 项目说明文档 |
