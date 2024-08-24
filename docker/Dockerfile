FROM python:3.9.1

# USER $USER

WORKDIR /usr/src/app

ENV DEPS  libgcc1

RUN apt upgrade -y && apt update -y

RUN apt install -y \
                wget \
                curl \
                unzip \
                vim
                # sqlite3 \
                # cron \

RUN wget https://mirrors.edge.kernel.org/ubuntu/pool/main/g/gcc-10/gcc-10-base_10-20200411-0ubuntu1_amd64.deb && dpkg -i gcc-10-base_10-20200411-0ubuntu1_amd64.deb && \
    wget https://mirrors.edge.kernel.org/ubuntu/pool/main/g/gcc-10/libgcc-s1_10-20200411-0ubuntu1_amd64.deb && dpkg -i libgcc-s1_10-20200411-0ubuntu1_amd64.deb

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y google-chrome-stable && \
    rm -rf google-chrome-stable_current_amd64.deb

COPY ./config/script.sh /script.sh
COPY ./config/requirements.txt /requirements.txt

# COPY . .

# RUN pip install -r requirements.txt

ENTRYPOINT ["/bin/bash" , "/script.sh"]