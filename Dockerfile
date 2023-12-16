FROM python:3.8

WORKDIR /app

COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN apt-get update && \
    apt-get install -yq \
        unzip \
        wget \
        libglib2.0-0 \
        libnss3 \
        libgconf-2-4 \
        libfontconfig1 \
        chromium \
        && apt-get install -y wget unzip \
        && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
        && apt install -y ./google-chrome-stable_current_amd64.deb \
        && rm google-chrome-stable_current_amd64.deb \
        && apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir \
        pandas


CMD [ "python", "main.py" ]
