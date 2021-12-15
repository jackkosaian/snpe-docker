FROM ubuntu:20.04

ARG SNPE_ZIP

ADD $SNPE_ZIP /$SNPE_ZIP

RUN apt-get update \
    && apt-get install -y zip \
    && unzip /$SNPE_ZIP > /tmp/unzip_log.txt \
    && unzipped_dir=$(cat /tmp/unzip_log.txt | grep -m1 'creating:' | cut -d' ' -f5-) \
    && mv $unzipped_dir /snpe

RUN echo "export SNPE_DIR=/snpe" >> ~/.bashrc

# Install Python 3.6 and other requirements
RUN apt-get update \
    && apt install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt update \
    && apt install -y python3.6 \
    && apt install -y python3-pip vim git \
    && apt-get install libpython3.6

# Set Python defaults
RUN rm -rf /usr/bin/python \
    && ln /usr/bin/python3.6 /usr/bin/python \
    && rm -rf /usr/bin/python3 \
    && ln /usr/bin/python3.6 /usr/bin/python3

# Install TensorFlow
RUN python -m pip install keras==2.6.0 tensorflow-cpu==2.6.0
RUN echo "export TENSORFLOW_DIR=$(python -m pip show tensorflow-cpu | grep Location | awk -F' ' '{print $NF}')" >> ~/.bashrc
RUN echo "source \$SNPE_DIR/bin/envsetup.sh -t \$TENSORFLOW_DIR" >> ~/.bashrc
