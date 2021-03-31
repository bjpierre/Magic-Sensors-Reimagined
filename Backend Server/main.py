import os
import sys
import psutil

def generate_pid_file():
    pid = str(os.getpid())
    pidfile = "/tmp/server_daemon.pid"
    
    print(f"Creating proc {pid}")

    with open(pidfile, "w") as f:
        f.write(pid)

if __name__ == "__main__":

    print("App launch")
    
    generate_pid_file()

    while(True):
        pass
