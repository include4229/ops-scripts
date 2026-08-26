package main

import (
	"bytes"
	"fmt"
	"net"
	"os/exec"
	"strings"
)

// runCommand 封装系统命令执行，支持捕获标准输出和标准错误
func runCommand(name string, args ...string) string {
	cmd := exec.Command(name, args...)
	var out bytes.Buffer
	var stderr bytes.Buffer
	cmd.Stdout = &out
	cmd.Stderr = &stderr
	
	err := cmd.Run()
	if err != nil {
		return fmt.Sprintf("执行命令 [%s] 失败: %v\n错误信息: %s", name, err, strings.TrimSpace(stderr.String()))
	}
	return strings.TrimSpace(out.String())
}

// getPhysicalInterface 自动获取第一个处于 UP 状态且非环回的物理网卡名称
func getPhysicalInterface() string {
	interfaces, err := net.Interfaces()
	if err != nil {
		return ""
	}
	for _, iface := range interfaces {
		// 排除环回接口 (lo) ，要求网卡必须是 UP 状态，且包含 MAC 地址
		if iface.Flags&net.FlagLoopback == 0 && iface.Flags&net.FlagUp != 0 && len(iface.HardwareAddr) > 0 {
			return iface.Name
		}
	}
	return ""
}

func main() {
	fmt.Println("==================================================")
	fmt.Println("              服务器基础信息自动采集脚本              ")
	fmt.Println("==================================================\n")

	// 1. CPU架构、核心数、线程数
	fmt.Println(">>> [1/5] CPU 架构与核心信息 (lscpu) <<<")
	fmt.Println(runCommand("lscpu"))
	fmt.Println("\n--------------------------------------------------\n")

	// 2. 内存总量与使用情况
	fmt.Println(">>> [2/5] 内存使用情况 (free -h) <<<")
	fmt.Println(runCommand("free", "-h"))
	fmt.Println("\n--------------------------------------------------\n")

	// 3. 磁盘分区与容量
	fmt.Println(">>> [3/5] 磁盘分区与容量 (df -h) <<<")
	fmt.Println(runCommand("df", "-h"))
	fmt.Println("\n--------------------------------------------------\n")

	// 4. 网卡型号与速率
	fmt.Println(">>> [4/5] 网络接口状态 (ip a & ethtool) <<<")
	fmt.Println("【IP 地址信息】:")
	fmt.Println(runCommand("ip", "a"))

	ifaceName := getPhysicalInterface()
	if ifaceName != "" {
		fmt.Printf("\n【探测到活跃物理网卡: %s，执行 ethtool 获取速率】:\n", ifaceName)
		// 注意：ethtool 通常需要 root 权限才能获取到完整的硬件参数
		fmt.Println(runCommand("ethtool", ifaceName))
	} else {
		fmt.Println("\n【未找到活动的物理网卡，跳过 ethtool 检测】")
	}
	fmt.Println("\n--------------------------------------------------\n")

	// 5. 系统整体状态
	fmt.Println(">>> [5/5] 系统整体性能状态 (vmstat 1 10) <<<")
	fmt.Println("正在采集 vmstat 数据，耗时约 10 秒，请稍候...")
	// vmstat 1 10 会阻塞 10 秒钟以完成采集
	fmt.Println(runCommand("vmstat", "1", "10"))
	
	fmt.Println("\n==================================================")
	fmt.Println("                   信息采集完毕                   ")
	fmt.Println("==================================================")
}
