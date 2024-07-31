FROM python:3.11-slim
COPY ./app ./watchtower
COPY ./supervisord.conf ./watchtower/supervisord.conf
RUN find /etc/apt/ -type f -exec sed -i 's#http://deb.debian.org#https://mirrors.163.com#g' {} +
RUN apt update
RUN apt install -y libglib2.0-dev libsm6 libxrender1 libxext-dev supervisor build-essential
RUN rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
RUN pip3 install -r ./watchtower/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
EXPOSE 8015
CMD ["supervisord","-c","/watchtower/supervisord.conf"]
