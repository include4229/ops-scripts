package main

import (
	"bytes"
	"fmt"
	"log"
	"os"
	"os/exec"
	"time"
)

// runCommand 封装系统命令执行
func runCommand(name string, args ...string) string {
	cmd := exec.Command(name, args...)
	var out bytes.Buffer
	cmd.Stdout = &out
	err := cmd.Run()
	if err != nil {
		return fmt.Sprintf("执行失败: %v", err)
	}
	return out.String()
}

// doMonitor 核心监控逻辑
func doMonitor() {
	log.Println("=== 开始执行服务器状态检查 ===")

	// 1. 检查 CPU 负载 (使用 uptime 提取 1, 5, 15 分钟的平均负载)
	log.Println("【CPU 负载】:")
	log.Print(runCommand("uptime"))

	// 2. 检查内存使用情况
	log.Println("【内存使用】:")
	log.Print(runCommand("free", "-h"))

	// 3. 检查磁盘容量
	log.Println("【磁盘使用】:")
	log.Print(runCommand("df", "-h"))

	log.Println("=== 检查完毕 ===\n")
}

func main() {
	// 1. 设置日志文件 (如果不存在则创建，如果存在则追加)
	logFile, err := os.OpenFile("server_monitor.log", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		fmt.Println("打开日志文件失败:", err)
		return
	}
	defer logFile.Close()
	
	// 让自带的 log 包直接把内容写进文件，并自动带上时间戳
	log.SetOutput(logFile) 
	log.SetFlags(log.Ldate | log.Ltime)

	fmt.Println("监控程序已启动，正在后台运行...")
	fmt.Println("每 12 小时检查一次，日志将保存在当前目录的 server_monitor.log 文件中。")

	// 2. 程序刚启动时，先立刻执行一次检查
	doMonitor()

	// 3. 设置定时器：每 12 小时触发一次（即每天检查两次）
	ticker := time.NewTicker(12 * time.Hour)
	defer ticker.Stop()

	// 4. 死循环：阻塞在这里，每次定时器滴答作响，就执行一次监控
	for {
		<-ticker.C // 等待定时器信号
		doMonitor()
	}
}