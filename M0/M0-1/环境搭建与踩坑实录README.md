# 环境搭建与踩坑实录


## 1. 模块简介
本项目为智能车备赛的 M0 模块环境搭建记录。
开发环境基于 VirtualBox 虚拟机 + Ubuntu 22.04 LTS，已完成 Git 版本控制配置及基础工具链安装。

## 2. 环境配置清单
- 宿主机系统：Windows 11
- 虚拟机软件：Oracle VirtualBox 7.x
- 客户机系统：Ubuntu 22.04 LTS
- 版本控制：Git + GitHub（SSH 方式）
- 开发板：待接入 OrangePi

## 3. 搭建步骤
1. 安装 VirtualBox 并创建 Ubuntu 22.04 虚拟机。
2. 安装 VirtualBox 增强功能（共享剪贴板、自适应分辨率）。
3. 更换国内软件源（阿里云镜像）并更新系统。
4. 安装 Git：`sudo apt install git`。
5. 配置 Git 用户信息：用户名：Lzh0812-scut


##4、踩坑实录
1、安装ubuntu系统的时候在官网上没找到22.04版本，询问AI后得知可以在镜像站下载。
2、安装ubuntu系统的时候忘记设置40-50G的硬盘容量，询问AI后在virtual上设置容量为50G，并在ubuntu终端里使用扩容代码扩展分区和文件系统完成操作系统硬盘容量扩容。
3、无法打开终端，询问AI，切换系统语言为中文，并补齐中文语言安装包后终端才可打开，使用代码：sudo apt install -y language-pack-zh-hans ibus-libpinyin
                                                                                      sudo locale-gen zh_CN.UTF-8 en_US.UTF-8
                                                                                      sudo update-locale LANG=en_US.UTF-8
                                                                                      sudo reboot
4、apt连默认源被拒，装不了cloud-guest-utils。报错原文：Err:1 http://cn.archive.ubuntu.com/ubuntu ... Connection refused [Errno 111]。解决方案：sudo sed -i 's/cn.archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list
                                                     E: Unable to locate package cloud-guest-utils                                           sudo apt update
                                                                                                                                             sudo apt install -y cloud-guest-utils
                                                     

