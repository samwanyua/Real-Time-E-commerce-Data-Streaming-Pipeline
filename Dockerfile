# Dockerfile for PyFlink-enabled JobManager and TaskManager
FROM flink:1.17.1-scala_2.12

USER root

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install apache-flink

# Optional: Set python3 as default
RUN ln -s /usr/bin/python3 /usr/bin/python

USER flink
