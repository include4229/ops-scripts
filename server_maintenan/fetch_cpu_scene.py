import paramiko
import os
from datetime import datetime

# 定义日志文件保存路径（默认保存在当前目录）
LOG_FILE_PATH = "cpu_scene.log"

def get_top_cpu_processes(ip, username, password):
    """
    远程登录服务器，获取当前占用 CPU 最高的 5 个进程
    """
    print(f"[{datetime.now()}] 接收到报警，正在紧急连接 {ip} 抓取现场...")
    
    ssh = paramiko.SSHClient()
    # 自动接受未知的 SSH 密钥指纹
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 设置超时时间为 5 秒，防止死机导致的死等
        ssh.connect(hostname=ip, port=22, username=username, password=password, timeout=5)
        
        # 核心 Linux 命令：按 %cpu 倒序排列，取前 6 行 (1行表头 + 5行进程数据)
        cmd = "ps -eo pid,user,%cpu,%mem,command --sort=-%cpu | head -n 6"
        
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.read().decode('utf-8')
        
        return result
        
    except Exception as e:
        return f"无法获取故障现场，连接或执行失败: {e}"
    finally:
        ssh.close()

def save_scene_to_log(ip, process_info):
    """
    将抓取到的现场数据，格式化后追加到本地日志文件中
    """
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 构造要写入日志的文本格式
    log_content = (
        f"========== 🚨 CPU 异常现场记录 ==========\n"
        f"报警主机: {ip}\n"
        f"抓取时间: {time_str}\n"
        f"Top 5 高耗能进程:\n"
        f"{process_info}\n"
        f"======================================\n\n"
    )
    
    try:
        # 以追加模式 ('a') 打开日志文件，写入数据
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(log_content)
        print(f"[{datetime.now()}] ✅ 现场数据已成功保存在本地日志: {LOG_FILE_PATH}")
    except Exception as e:
        print(f"写入日志文件失败: {e}")

if __name__ == "__main__":
    # 实际工作中，IP通常是监控系统传过来的参数
    target_ip = "192.168.1.100"
    
    # 1. 抓取现场数据
    scene_data = get_top_cpu_processes(target_ip, "root", "your_password")
    
    # 2. 直接保存到本地日志，不发送到外部网络
    save_scene_to_log(target_ip, scene_data)