import os
import psutil
import time

def check_main_pid():
    pidfile = "/tmp/server_daemon.pid"
    file_path = "/home/sd2021/gitRepo/Magic-Sensors-Reimagined/Backend Server"
    file_name = "main.py"
    if os.path.isfile(pidfile):
        with open(pidfile, "r") as f:
            pid = int(f.readline())
            if psutil.pid_exists(pid):
               p = psutil.Process(pid)
               p.kill()
    os.chdir(file_path)
    os.system("git pull origin master")
    os.system(f"python3 {file_name}")

if __name__ == "__main__":
    check_main_pid()
