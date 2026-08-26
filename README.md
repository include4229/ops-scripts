项目结构说明

| 文件路径 | 说明 |
| --- | --- |
| `NS AutoTest` | Linux自动化测试脚本 |
| `server_maintenance` | 服务器维护脚本 |
| `server_maintenance/server_monitor.go` | 一次性采集CPU、内存、磁盘、网卡等基础信息，打印到终端 |
| `server_maintenance/monitor.go`<br>`server_maintenance/collect_logs.py` | 定时记录系统资源使用情况，并远程收集日志集中归档 |
| `server_maintenance/cpu_alert.go` | CPU使用率超阈值时自动抓取高CPU进程 |
| `server_maintenance/fetch_cpu_scene.py` | 远程抓取问题服务器当前CPU最高的5个进程，保存到本地日志 |
| `server_maintenance/run_benchmarks.go`<br>`server_maintenance/collect_benchmarks.py` | 执行基准性能测试，并远程收集结果集中归档 |
