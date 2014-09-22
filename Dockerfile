############################################################
# Dockerfile to build Flask example container
# Based on Ubuntu
############################################################

FROM ubuntu
MAINTAINER Skylar Saveland

RUN apt-get -y update
# Do everything in the docker file because
# ansible runs are not cacheable enough
# if we have to do templating later ... idk ...
# RUN apt-get install -y python-yaml python-jinja2 git
# RUN git clone http://github.com/ansible/ansible.git /tmp/ansible
# WORKDIR /tmp/ansible
# ENV PATH /tmp/ansible/bin:$PATH
# ENV ANSIBLE_LIBRARY /tmp/ansible/library
# ENV PYTHONPATH /tmp/ansible/lib:$PYTHON_PATH
# ADD . /rest-battles
# WORKDIR /rest-battles/ansible
# RUN ansible-playbook playbook.yml -c local -i inventory

# Breaking it up so that we can get some intermediate caching
RUN apt-get -y install build-essential libncurses5-dev
RUN apt-get -y install postgresql postgis postgresql-contrib
RUN apt-get -y install python3-pip python3-psycopg2
# pg_ctl ...
#RUN apt-get -y install postgres-xc postgres-xc-client
# http://docs.docker.com/examples/postgresql_service/
USER postgres
RUN /etc/init.d/postgresql start &&\
    createdb battles
USER root
# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]
# Set the default command to run when starting the container
CMD ["/usr/lib/postgresql/9.3/bin/postgres", \
     "-D", "/var/lib/postgresql/9.3/main", \
     "-c", "config_file=/etc/postgresql/9.3/main/postgresql.conf"]

USER root
ADD . /rest-battles

EXPOSE 80
ENV CONFIG_MODULE config.postgres
ENV HOST 0.0.0.0
ENV PORT 80

WORKDIR /rest-battles
RUN pip3 install -r requirements.txt
CMD python3 run.py
