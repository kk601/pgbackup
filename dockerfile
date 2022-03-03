FROM ubuntu:20.04 
#TODO use more optimal image

ENV POSTGRES_DB=test_db

COPY ./dist/pgbackup-1.1.0-py3-none-any.whl /
COPY ./build/sample_db.sql /
COPY ./import_db.sh /

RUN apt-get update \
    && apt-get install -y gnupg wget lsb-release unzip curl apt-utils
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata

RUN bash -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -

RUN apt-get update \
    && apt-get install -y python3 python3-pip postgresql postgresql-client

RUN pip3 install pgbackup-1.1.0-py3-none-any.whl

#Install azure cli
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash

#Install aws cli
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install

RUN ["chmod","+x","import_db.sh"]
USER postgres
RUN [ "./import_db.sh" ]
USER root

ENTRYPOINT ["/bin/bash","-c","service postgresql start && pgbackup --help && /bin/bash"]
