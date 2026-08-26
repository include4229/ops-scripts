package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"time"
)

// getCPUSample 读取 /proc/stat 获取当前的 CPU 总时间与空闲时间
func getCPUSample() (idle, total uint64) {
	file, err := os.Open("/proc/stat")
	if err != nil {
		log.Fatal("读取 /proc/stat 失败:", err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		// 只看第一行以 "cpu " 开头的总线数据
		if strings.HasPrefix(line, "cpu ") {
			fields := strings.Fields(line)[1:]
			for i, val := range fields {
				v, _ := strconv.ParseUint(val, 10, 64)
				total += v
				// 第 4 列是 idle(空闲)，第 5 列是 iowait(等待IO)
				if i == 3 || i == 4 {
					idle += v
				}
			}
			return
		}
	}
	return
}

// captureScene 抓取现场（类似之前 Python 做的动作）
func captureScene() {
	fmt.Println(">>> 正在执行紧急现场抓取 (ps 命令)...")
	// 执行 ps 命令抓取前 5 个最耗 CPU 的进程
	cmd := exec.Command("sh", "-c", "ps -eo pid,user,%cpu,%mem,command --sort=-%cpu | head -n 6")
	out, err := cmd.CombinedOutput()
	if err != nil {
		fmt.Println("抓取失败:", err)
		return
	}
	
	// 这里为了演示直接打印，实际工作中可以写入本地日志文件
	fmt.Println("========== 🚨 抓取结果 ==========")
	fmt.Println(string(out))
	fmt.Println("=================================")
}

func main() {
	fmt.Println("启动本地 CPU 实时监控探针...")
	fmt.Println("每 2 秒检测一次，阈值设为: >= 99%")

	threshold := 99.0

	for {
		// 1. 获取第 1 次 CPU 快照
		idle1, total1 := getCPUSample()
		
		// 2. 挂起等待 2 秒（这是计算使用率必须的时间差）
		time.Sleep(2 * time.Second)
		
		// 3. 获取第 2 次 CPU 快照
		idle2, total2 := getCPUSample()

		// 4. 计算这 2 秒内的真实使用率
		deltaTotal := float64(total2 - total1)
		deltaIdle := float64(idle2 - idle1)
		cpuUsage := 100.0 * (deltaTotal - deltaIdle) / deltaTotal

		// 打印当前实时状态（可以注释掉，让它在后台默默运行）
		fmt.Printf("[%s] 当前 CPU 使用率: %.2f%%\n", time.Now().Format("15:04:05"), cpuUsage)

		// 5. 触发告警逻辑
		if cpuUsage >= threshold {
			fmt.Println("\n🚨 警告！检测到 CPU 飙升，触发告警！")
			
			// 触发抓取现场的动作
			captureScene()
			
			// 为了防止 CPU 持续 100% 时疯狂抓取，抓完一次后休眠 10 秒（冷却时间）
			fmt.Println("进入冷却期 10 秒，防止重复告警...")
			time.Sleep(10 * time.Second)
		}
	}
}