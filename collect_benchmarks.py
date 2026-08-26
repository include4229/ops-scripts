import paramiko
import os
from datetime import datetime

# 基础配置
REMOTE_TXT_PATH = "/root/benchmark_results.txt"  # Go脚本在被测服务器上生成的 txt 路径
LOCAL_SAVE_DIR = "/opt/benchmark_reports"        # 收集到中控机本地的存放目录

# 需要收集跑分结果的服务器列表
SERVERS = [
    {"ip": "192.168.1.201", "port": 22, "user": "root", "password": "your_password_1"},
    {"ip": "192.168.1.202", "port": 22, "user": "root", "password": "your_password_2"},
]

def fetch_benchmark_results(server_info, date_str):
    ip = server_info["ip"]
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 开始连接并收集 {ip} 的跑分数据...")
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(
            hostname=ip, 
            port=server_info["port"], 
            username=server_info["user"], 
            password=server_info["password"],
            timeout=10
        )
        
        sftp = ssh.open_sftp()
        
        # 本地文件命名格式：IP_日期_benchmark.txt
        local_filename = f"{ip}_{date_str}_benchmark.txt"
        local_filepath = os.path.join(LOCAL_SAVE_DIR, local_filename)
        
        sftp.get(REMOTE_TXT_PATH, local_filepath)
        print(f"✅ 成功! {ip} 的压测结果已保存至: {local_filepath}")
        
    except FileNotFoundError:
        print(f"⚠️ {ip} 上未找到结果文件，可能压测还未跑完。")
    except Exception as e:
        print(f"❌ 失败! 无法获取 {ip} 的数据。报错: {e}")
    finally:
        ssh.close()

if __name__ == "__main__":
    if not os.path.exists(LOCAL_SAVE_DIR):
        os.makedirs(LOCAL_SAVE_DIR)
        
    today_str = datetime.now().strftime("%Y%m%d")
    print(f"=== 自动收集服务器压测结果任务开始 ===")
    
    for server in SERVERS:
        fetch_benchmark_results(server, today_str)
        
    print("=== 收集任务执行完毕 ===")