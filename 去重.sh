#/bin/bash
# 利用正则表达式去重,效果->
# a.b.com avv.b.com b.com 只留下 b.com
cat 全部网站_sorted | grep  "^\w*\.\w*$" > 全部网站_sorted去重
