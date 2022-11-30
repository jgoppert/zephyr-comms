FROM zephyrprojectrtos/zephyr-build:v0.24.6

# install net tools for ethernet connection with zephyr
RUN sudo git clone --depth 1 https://github.com/zephyrproject-rtos/net-tools.git /opt/net-tools

# required to allow nanopb to build on ubuntu 22.04 currently
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# change to root to install
USER root

# install iputils
RUN apt-get -y update && \
	apt-get install --no-install-recommends -y \
	iputils-ping

# Clean up stale packages
RUN apt-get clean -y && \
	apt-get autoremove --purge -y && \
	rm -rf /var/lib/apt/lists/*

RUN chown -R user:user /workdir

USER user
