# 从仓库拉取 带有 python 3.9 的 Linux 环境
FROM python:3.9

# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1

# 创建 code 文件夹并将其设置为工作目录
RUN mkdir /code
WORKDIR /code
RUN pip3 --version

# 更新 pip
#RUN pip install --upgrade pip

# 将 requirements.txt 复制到容器的 code 目录
ADD requirements.txt /code/

# 解决安装anyjson时错误
RUN pip install setuptools==56.0.0

# 安装库
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 将当前目录复制到容器的 code 目录
ADD . /code/