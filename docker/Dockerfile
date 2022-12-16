FROM tianon/raspbian:bullseye-slim

COPY . /opt/app
WORKDIR /opt/app

RUN apt-get update \
    && apt-get install -y \
    abcmidi autoconf autotools-dev \
    build-essential \
    fonts-freefont-ttf \
    gcc git \
    libasound2-dev libasound2-dev libatlas-base-dev libavahi-client3 libdbus-1-dev libglib2.0-dev libical-dev libjack-dev libjack0 libopenjp2-7 libreadline-dev libtiff5 libtool libudev-dev libusb-dev \
    make \
    scons swig \
    && apt-get install -y python-dev python3-dev python3-pip python3-venv python3-spidev

CMD ["tail", "-f", "/dev/null"]