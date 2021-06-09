FROM openfaas/of-watchdog:0.5.3 as watchdog
FROM continuumio/miniconda3:4.8.2
WORKDIR /home/app
RUN apt-get install ca-certificates \
    && addgroup --system app && adduser  --system app && adduser app app \
    && mkdir -p /home/app \
    && chown app /home/app
#复制handler目录,来自用户写handler文件
COPY function ./function
#安装用户需要的依赖,来handler目录的requirements.txt

RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
RUN conda install --yes -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ --file ./function/conda_requirements.txt
RUN pip install flask -i http://pypi.douban.com/simple --trusted-host=pypi.douban.com

RUN pip install -r ./function/pip_requirements.txt -i http://pypi.douban.com/simple --trusted-host=pypi.douban.com


#复制fwatchdog程序过来
COPY --from=watchdog /fwatchdog .
#主要python文件和gunicorn配置文件
COPY main.py .
COPY __init__.py .

#fwatchdog运行权限
RUN chmod +x fwatchdog
#使用app用户
RUN chown -R app /home/app

#使用app用户
USER app
RUN export FLASK_APP=main.py

#使用gunicorn运行
ENV fprocess="python main.py"
ENV cgi_headers="true"
#http协议
ENV mode="http"
#反向代理flask服务的5000端口
ENV upstream_url="http://127.0.0.1:5000"


EXPOSE 8080

HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1

CMD ["./fwatchdog"]
