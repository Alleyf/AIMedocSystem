# 建立 python3.7 环境
FROM python:3.10

# 镜像作者
MAINTAINER Alleyf

# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1
# 添加这两行
RUN apt-get update
RUN apt-get install python3-dev default-libmysqlclient-dev -y

# 设置pip源为国内源
COPY pip.conf /root/.pip/pip.conf

# 在容器内创建mysite文件夹
RUN mkdir /aimedocsys

# 设置容器内工作目录
WORKDIR /aimedocsys

# 更新 pip
RUN pip install pip -U

# 将 requirements.txt 复制到容器的 code 目录
ADD requirements.txt /aimedocsys/

# pip安装依赖
RUN pip install -r requirements.txt

# 将当前目录文件加入到容器工作目录中（. 表示当前宿主机目录）
ADD . /aimedocsys/