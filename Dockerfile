FROM python:3.8.1-slim

RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

WORKDIR /workshop
COPY app ./app
COPY start.sh ./start.sh
RUN chmod a+x start.sh

CMD [ "./start.sh" ]