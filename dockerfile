FROM python:3.8-slim-buster

#RUN apt-get update && apt-get install -y \
#    git \
#    && rm -rf /var/lib/apt/lists/*
#RUN mkdir -p /opt/chromium
#WORKDIR /opt/chromium
#RUN git clone --depth 1 https://chromium.googlesource.com/chromium/tools/depot_tools.git

WORKDIR /usr/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


#COPY src/ ./
COPY app.py ./

#CMD [ "python", "app.py" ]