FROM apache/nifi:1.10.0

LABEL maintainer="Rafael Gratão <grataoro@gmail.com>"

USER root

# copy files
COPY ./nifi/ ./poli-nifi/
COPY ./flow.xml.gz ./conf/
COPY ./Python-3.6.10.tgz /usr/src/

RUN apt-get update

RUN apt install -y build-essential checkinstall

RUN apt install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev liblzma-dev
 
WORKDIR /usr/src/

RUN tar xzf ./Python-3.6.10.tgz

RUN ./Python-3.6.10/configure --enable-optimizations

RUN make altinstall

WORKDIR /opt/nifi/nifi-current

COPY requirements.txt ./

RUN pip3.6 install -r requirements.txt
