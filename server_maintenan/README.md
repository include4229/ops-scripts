
---

**1. server_monitor.go**

- **实现功能**：在问题服务器上执行，一次性采集该服务器的完整信息（CPU架构/核心数、内存使用、磁盘分区、网卡IP及速率、系统整体性能状态），打印到终端。
- **依赖**：Go 1.16+ 编译环境；问题服务器需安装 `lscpu`、`free`、`df`、`ip`、`ethtool`、`vmstat`（通常已预装）。
- **启动方式**（在问题服务器上操作）：
  ```bash
  go build -o server_monitor server_monitor.go
  ./server_monitor
  ```

---

**2. monitor.go + collect_logs.py**

- **实现功能**：`monitor.go` 在问题服务器上持续运行，每12小时记录 CPU 负载、内存、磁盘到 `server_monitor.log`；`collect_logs.py` 在运维人员操作的服务器上执行，通过 SSH 远程拉取问题服务器的日志文件到本地。两者配合实现日志集中收集。
- **依赖**：
  - `monitor.go`：Go 1.16+（仅编译时需要，编译后二进制文件可直接运行）；问题服务器需有 `uptime`、`free`、`df` 命令。
  - `collect_logs.py`：运维人员操作的服务器需安装 Python 3 + `paramiko`（`pip install paramiko`）。
- **启动方式**：
  ```bash
  # monitor.go - 在有 Go 环境的机器上编译
  go build -o server_monitor monitor.go
  # 将编译好的 server_monitor 上传到问题服务器
  chmod +x server_monitor
  nohup ./server_monitor > /dev/null 2>&1 &

  # collect_logs.py - 在运维人员操作的服务器上执行
  # 修改脚本中 SERVERS 列表的 IP 为问题服务器 IP
  python3 collect_logs.py
  ```

---

**3. cpu_alert.go**

- **实现功能**：在问题服务器上持续运行，每2秒采样 CPU 使用率，当 ≥99% 时自动执行 `ps` 抓取 Top5 高 CPU 进程并打印到终端，进入10秒冷却期防止重复告警。
- **依赖**：Go 1.16+（仅编译时需要，编译后二进制文件可直接运行）；问题服务器需有 `ps` 命令。
- **启动方式**（在问题服务器上操作）：
  ```bash
  go build -o cpu_alert cpu_alert.go
  chmod +x cpu_alert
  ./cpu_alert
  ```

---

**4. fetch_cpu_scene.py**

- **实现功能**：在运维人员操作的服务器上执行，通过 SSH 远程连接到问题服务器，抓取当前 CPU 占用最高的5个进程，追加保存到本地 `cpu_scene.log`。适用于收到告警后人工介入排查。
- **依赖**：运维人员操作的服务器需安装 Python 3 + `paramiko`（`pip install paramiko`）。
- **启动方式**（在运维人员操作的服务器上操作）：修改脚本中的 `target_ip` 为问题服务器 IP，然后执行：
  ```bash
  python3 fetch_cpu_scene.py
  ```

---

**5. run_benchmarks.go + collect_benchmarks.py**

- **实现功能**：`run_benchmarks.go` 在问题服务器上执行 sysbench、Geekbench、UnixBench、SPECCPU2017 基准测试，结果汇总到 `benchmark_results.txt`；`collect_benchmarks.py` 在运维人员操作的服务器上执行，通过 SSH 远程拉取问题服务器的结果文件到本地。两者配合实现压测结果集中收集。
- **依赖**：
  - `run_benchmarks.go`：Go 1.16+（仅编译时需要，编译后二进制文件可直接运行）；问题服务器需**预先安装** sysbench、geekbench6、UnixBench、SPECCPU2017。
  - `collect_benchmarks.py`：运维人员操作的服务器需安装 Python 3 + `paramiko`（`pip install paramiko`）。
- **启动方式**：
  ```bash
  # run_benchmarks.go - 在有 Go 环境的机器上编译
  go build -o run_benchmarks run_benchmarks.go
  # 将编译好的 run_benchmarks 上传到问题服务器
  chmod +x run_benchmarks
  nohup ./run_benchmarks > /dev/null 2>&1 &

  # collect_benchmarks.py - 在运维人员操作的服务器上执行
  # 修改脚本中 SERVERS 列表的 IP 为问题服务器 IP
  python3 collect_benchmarks.py
  ```

---

