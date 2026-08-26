import paramiko
import os
from datetime import datetime

# 1. 基础配置
REMOTE_LOG_PATH = "/root/server_monitor.log"  # Go脚本在服务器上生成的日志路径
LOCAL_SAVE_DIR = "/opt/monitor_results"       # 下载到中控机本地的存放目录

# 2. 定义你要去收集信息的服务器列表
# 实际生产中，密码通常换成 SSH 密钥 (私钥) 登录更安全
SERVERS = [
    {"ip": "192.168.1.101", "port": 22, "user": "root", "password": "your_password_1"},
    {"ip": "192.168.1.102", "port": 22, "user": "root", "password": "your_password_2"},
]

def fetch_log_from_server(server_info, date_str):
    ip = server_info["ip"]
    print(f"开始连接服务器: {ip} ...")
    
    # 初始化 SSH 客户端
    ssh = paramiko.SSHClient()
    # 自动接受未知的 SSH 密钥指纹
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # 连接服务器
        ssh.connect(
            hostname=ip, 
            port=server_info["port"], 
            username=server_info["user"], 
            password=server_info["password"],
            timeout=10 # 10秒连不上就报错，防止卡死
        )
        
        # 开启 SFTP 用于文件传输
        sftp = ssh.open_sftp()
        
        # 规划本地保存的文件名 (例如: 192.168.1.101_20260727.log)
        local_filename = f"{ip}_{date_str}.log"
        local_filepath = os.path.join(LOCAL_SAVE_DIR, local_filename)
        
        # 执行下载操作: sftp.get(远程路径, 本地路径)
        sftp.get(REMOTE_LOG_PATH, local_filepath)
        print(f"✅ 成功! {ip} 的日志已保存至: {local_filepath}")
        
        # 可选操作：下载完后，清空目标服务器上的日志，防止文件越积越大
        # ssh.exec_command(f"> {REMOTE_LOG_PATH}") 

    except Exception as e:
        print(f"❌ 失败! 无法获取 {ip} 的日志。报错信息: {e}")
        
    finally:
        # 关闭连接，释放资源
        ssh.close()

if __name__ == "__main__":
    # 创建本地存放目录（如果不存在）
    if not os.path.exists(LOCAL_SAVE_DIR):
        os.makedirs(LOCAL_SAVE_DIR)
        
    # 获取今天的日期字符串，用作文件名标识
    today_str = datetime.now().strftime("%Y%m%d")
    print(f"=== 巡检日志收集任务开始 ({today_str}) ===")
    
    for server in SERVERS:
        fetch_log_from_server(server, today_str)
        
    print("=== 所有收集任务执行完毕 ===")