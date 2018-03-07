import time
import os


# 记录程序运行状态
def log(s, n=0):
    fmt = '\033[0;3{}m{}\033[0m'.format  # 设置输出文字的颜色
    BLACK = 0  # 黑
    RED = 1  # 红
    GREEN = 2  # 绿
    YELLOW = 3  # 棕
    BLUE = 4  # 蓝
    PURPLE = 5  # 紫
    CYAN = 6  # 青
    GRAY = 7  # 灰
    if n == 0:
        s = '【INFO】' + s
        text = time.strftime("【%Y-%m-%d-%H:%M:%S】", time.localtime()) + s + '\n'
        print(fmt(GREEN, text))
        return
    elif n == 1:
        s = '【ERROR】' + s
        text = time.strftime("【%Y-%m-%d-%H:%M:%S】", time.localtime()) + s + '\n'
        print(fmt(RED, text))
    elif n == 2:
        s = '【SETTING】' + s
        text = time.strftime("【%Y-%m-%d-%H:%M:%S】", time.localtime()) + s + '\n'
        print(fmt(BLUE, text))
    with open('spider.log', 'a') as file:
        file.write(text)


# 切换ip
def change_ip():
    cmd = os.popen("sudo poff -a")
    cmd.close()
    time.sleep(8)
