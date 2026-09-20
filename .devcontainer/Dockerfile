FROM mcr.microsoft.com/devcontainers/python:1-3.11-bullseye

COPY requirements.txt /tmp/requirements.txt

RUN rm -f /etc/apt/sources.list.d/yarn.list \
    && export DEBIAN_FRONTEND=noninteractive \
    && for i in 1 2 3; do \
        apt-get update && apt-get install -y --no-install-recommends \
            chromium \
            chromium-driver \
            xvfb \
        && break || { echo "apt-get attempt $i failed, retrying..."; sleep 5; }; \
    done \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Installed in its own layer so a transient apt-get/mirror failure above
# never prevents the Python requirements from being installed.
RUN python -m pip install --upgrade pip \
    && python -m pip install -r /tmp/requirements.txt \
    && rm -f /tmp/requirements.txt

ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER=/usr/bin/chromedriver
