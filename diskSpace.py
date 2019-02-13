#!/usr/bin/env python3
import shutil
total, used, free = shutil.disk_usage(__file__)
print(int(total/1024), int(used/1024/1024), int(free/1024))
print("Total : " + str(int(total/1024/1024)) +"MB")
print("Total : " + str(int(total/1024/1024/1024)) +"GB")

print("Used : " + str(int(used/1024/1024)) +"MB")
print("Used : " + str(int(used/1024/1024/1024)) +"GB")
print("Used : " + str(round(used/total*100,2)) + "%")

print("Free : " + str(int(free/1024/1024)) +"MB")
print("Free : " + str(int(free/1024/1024/1024)) +"GB")
print("Free : " + str(round(free/total*100,2)) + "%")
