package main

import (
	"bytes"
	"fmt"
	"log"
	"os"
	"os/exec"
	"time"
)

const resultFile = "benchmark_results.txt"

// runTest 封装命令行调用逻辑，并将结果写入文件
func runTest(toolName, command string, args ...string) {
	file, err := os.OpenFile(resultFile, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalf("无法打开结果文件: %v", err)
	}
	defer file.Close()

	header := fmt.Sprintf("\n========== 正在执行: %s (%s) ==========\n", toolName, time.Now().Format("2006-01-02 15:04:05"))
	fmt.Print(header)
	file.WriteString(header)

	cmd := exec.Command(command, args...)
	var out bytes.Buffer
	var stderr bytes.Buffer
	cmd.Stdout = &out
	cmd.Stderr = &stderr

	err = cmd.Run()
	if err != nil {
		errMsg := fmt.Sprintf("运行失败: %v\n错误输出: %s\n", err, stderr.String())
		fmt.Print(errMsg)
		file.WriteString(errMsg)
		return
	}

	fmt.Println("执行完成，正在记录结果...")
	file.WriteString(out.String())
	file.WriteString("\n=======================================================\n")
}

func main() {
	// 清空历史测试记录
	os.Remove(resultFile)

	fmt.Println("🚀 开始全套服务器基准性能测试...")

	// 1. sysbench：质数计算，测试整数运算能力
	// 实际命令根据系统安装路径可能有所不同
	runTest("Sysbench", "sysbench", "cpu", "--cpu-max-prime=20000", "run")

	// 2. Geekbench：模拟照片处理、压缩、ML 等真实负载
	// 假设 geekbench6 可执行文件在当前目录或 PATH 中
	runTest("Geekbench", "geekbench6", "--sysinfo") // 这里使用 --sysinfo 快速打印以作演示，全套跑分可不带参数

	// 3. UnixBench：包含 Dhrystone (整数)、Whetstone (浮点) 等 13 个子测试项
	// 通常在 UnixBench 目录下执行 ./Run
	runTest("UnixBench", "./Run", "-c", "1") // -c 1 表示单核测试，多核可改为 -c 8 等

	// 4. SPECCPU2017：行业标准测试，分整数和浮点两大套件
	// 极度耗时的企业级跑分，此处为演示命令结构
	runTest("SPECCPU2017", "runcpu", "--config=default.cfg", "--action=build", "intrate") 

	fmt.Printf("✅ 所有测试结束！结果已保存至: %s\n", resultFile)
}