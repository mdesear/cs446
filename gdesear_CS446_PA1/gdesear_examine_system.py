import os, sys, subprocess

os.system("echo 'CPU information: ' > gdesear_systemDetails.txt")
os.system("cat /proc/cpuinfo >> gdesear_systemDetails.txt")
os.system("echo '\n' >> gdesear_systemDetails.txt")
os.system("cat /proc/version >> gdesear_systemDetails.txt")
os.system("echo '\n' >> gdesear_systemDetails.txt")
os.system("echo 'Time since last boot (secs): ' >> gdesear_systemDetails.txt")
os.system("cat /proc/uptime >> gdesear_systemDetails.txt")
os.system("echo '\n' >> gdesear_systemDetails.txt")
os.system("systemd-analyze dump | grep 'Timestamp userspace' >> gdesear_systemDetails.txt")
os.system("echo '\n' >> gdesear_systemDetails.txt")
os.system("echo 'Number of disk requests: ' >> gdesear_systemDetails.txt")
os.system("cat /proc/diskstats >> gdesear_systemDetails.txt");
os.system("echo '\n' >> gdesear_systemDetails.txt")
os.system("cat /proc/stat | grep 'processes' >> gdesear_systemDetails.txt")
