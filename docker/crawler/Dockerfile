
FROM phusion/baseimage:0.10.0
LABEL Name=pidcheck-crawler Version=0.0.1

## Image config

# Use baseimage-docker's init process.
CMD ["/sbin/my_init"]

# Update installed APT packages
RUN apt-get update && apt-get upgrade -y -o Dpkg::Options::="--force-confold" && \
    apt-get install -y ntp wget tzdata python-dev python-pip libxml2-dev \
    libxslt1-dev zlib1g-dev libffi-dev libssl-dev python3 python3-dev

# Fetch PIP install script and run
ADD "https://bootstrap.pypa.io/get-pip.py" /tmp/get-pip.py
RUN python3 /tmp/get-pip.py

# Cleanup
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

## Crawler setup

# Copy the crawler to app folder
COPY crawler /home/app

# Set working directory to crawler
WORKDIR /home/app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install PidCheck as a service
RUN mkdir /etc/service/pidcheck
COPY docker/crawler/pidcheck.sh /etc/service/pidcheck/run
RUN chmod +x /etc/service/pidcheck/run