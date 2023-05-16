#centos
FROM centos:7

#--------------------手动安装python
RUN yum -y update && yum install -y python3.10 python3.10-dev python3.10-venv python3-pip python3-wheel build-essential && \
 yum clean all

# Add 3.7 to the available alternatives
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.6 1
# Set python3.7 as the default python
RUN update-alternatives --set python /usr/bin/python3.6 
RUN pip3 install openpyxl requests behave allure-behave -i https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host=pypi.tuna.tsinghua.edu.cn 

#--------------------手动安装python
#RUN yum update -y && yum install -y sudo
#RUN set -ex \
# && yum -y install zlib-devel bzip2-devel libffi-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make wget \
# && yum clean all \
# && mkdir /usr/local/python3 

##remove python2
#RUN rpm -qa|grep python|xargs rpm -ev --allmatches --nodeps
#RUN whereis python |xargs rm -frv

#COPY Python-3.10.11.tgz  /usr/local/python3/ 

#RUN set -ex \
# && cd /usr/local/python3 \
# && tar -xzvf  Python-3.10.11.tgz \
# && cd Python-3.10.11 \
# && ./configure prefix=/usr/local/python3 \
# && make && make install \
# && ln -s /usr/local/python3/bin/python3.10 /usr/local/bin/python \
# && ln -s /usr/local/python3/bin/pip3 /usr/local/bin/pip 

#RUN set -ex \
# && cd /usr/local/python3 \
# && python -V

#--------------------手动安装java
# 创建一个新目录来存储jdk文件
RUN mkdir /usr/local/java /usr/local/allure 

#将jdk压缩文件复制到镜像中，它将自动解压缩tar文件
ADD jre-8u371-linux-x64.tar.gz /usr/local/java/
ADD allure-2.22.0.tgz /usr/local/allure/

# 设置时区
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

# 设置环境变量
ENV JAVA_HOME /usr/local/java/jre1.8.0_371
ENV PATH $JAVA_HOME/bin:/usr/local/allure/allure-2.22.0/bin:$PATH

#拷贝SBE文件
RUN mkdir /tmp/demo
COPY  Demo /tmp/demo

EXPOSE 3001