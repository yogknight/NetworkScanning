# NetworkScanning
NetworkScanning是一个以Tkinter为图形界面编写的网络扫描及测试工具，应用与Windows系统(其他系统未测试)。也可以下载源码自己构建适合自己系统的版本(假如你的系统不是Windows的话~)。

# 安装
## 使用源码

1. 环境需求
- python3.x
- pillow
- tkinter           ————python默认库

2. 获取源码  
`git clone git@github.com:Toykang/NetworkScanning.git`

3. 启动  
cmd切换到项目目录运行`python TK_NetworkScanning.py` 

## 使用编译免安装包
下载压缩包解压后进入解压目录单击即可运行  
[下载地址：NetworkScanning v0.1](https://pan.baidu.com/s/1agUzUNzKfeZ7Fb8Im1ddpg)  
[下载地址：NetworkScanning v0.1.1](https://pan.baidu.com/s/16msWQUSOue2TehwS5mmtWQ)

## 功能
- [x] 单个网段IP地址扫描
- [x] 自定义文本文件内IP地址扫描
- [x] 导出扫描结果
- [x] 实时显示测试IP网络延迟

## 运行展示
![单个IP地址扫描](https://raw.githubusercontent.com/Toykang/NetworkScanning/master/Doc_Image/main_page.PNG)
![单个网段IP地址扫描](https://raw.githubusercontent.com/Toykang/NetworkScanning/master/Doc_Image/IP_test.PNG)
![自定义文本文件内IP地址扫描](https://raw.githubusercontent.com/Toykang/NetworkScanning/master/Doc_Image/txt_IP_test.PNG)

## LICENSE
MIT License

Copyright (c) 2018 Toykang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.