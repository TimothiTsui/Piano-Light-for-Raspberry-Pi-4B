pyanoled
=======

Piano LED visualizer based in Python 3.x. Inspired by the [onlaj/Piano-LED-Visualizer](https://github.com/onlaj/Piano-LED-Visualizer) project.

# Table of Contents
* [Hardware Setup](#setup)
    * [LED](#led)
    * [Raspberry Pi](#raspberrypi)
* [Install/Run](#install-run)
* [TODO](#todo)

## Hardware Setup
Setup instructions for the hardware are covered in [onlaj/Piano-LED-Visualizer](https://github.com/onlaj/Piano-LED-Visualizer).
It lists out all of the parts and equipment, and references a lot of other sites with useful information on how
to setup and configure the hardware. Here are some of my takeaways: 

### LED
For a standard 88-key piano, the distance from lowest and highest key is just 4 meters. The WS2818B LEDs
have enough LED density to align with every key, so 4 meters of that will be around 172 LEDs. 
* It is recommended to purchase the longer-lengthed strip and cut it down to 4 meters. Soldering two
shorter strips together is more tedious. Here is a [good instructional video](https://www.youtube.com/watch?v=OLQs7S_Ou8U)
on how to do that.
* Finding vendors selling 4 meter long aluminum casing was also troublesome. Here is a [vendor](https://www.gladiatorlighting.com/)
that offers custom-length cases and lids.
* Get a 5V power supply that draws 10A of current.

### Raspberry Pi
The instructions for setting up the Raspberry Pi are pretty straight forward, but here are some issues that I ran into:
1) [Installing Rasbian](https://www.terminalbytes.com/raspberry-pi-without-monitor-keyboard/)
	* To enable wifi: do not need to set country code value in `wap_supplicant.conf` if you have Raspbery Pi Zero

2) [Configuring Raspbian to work with WS2128](https://tutorials-raspberrypi.com/connect-control-raspberry-pi-ws2812-rgb-led-strips/)
	- To disable sound: if `/etc/modprobe.d/alsa-base.conf` is not found, try `/usr/share/alsa/alsa.conf`

3) [Enabling SPI](https://www.raspberrypi-spy.co.uk/2014/08/enabling-the-spi-interface-on-the-raspberry-pi/)

4) [Configuring MIDI](https://neuma.studio/rpi-midi-complete.html)
    - Missing Jack module errors: `sudo apt-get install libjack-dev`
    - Python 3 packages: `libatlas-base-dev`
5) Additional packages that might be needed
    - `sudo apt-get install libjpeg-dev zlib1g-dev`

## Install/Run
1. Setup your virtual environment
    ```shell script
    virtualenv <path to env>
    source <path to env>/bin/activate
    ```

2. Install project from package or source 
    - To install from pypi:
        ```shell script
        # in raspberry pi, install the project from pypi
        pip3 install pyanoled
        ```

    - To install from source:
        ```shell script
        # in raspberry pi, clone repository
        git clone <repository>
        
        # in project root directory, run setuptools
        # note: some dependencies (like numpy) can take a long time to install this way. can install those
        # dependencies through pip first before running this step
        python3 setup.py develop
        ```
3. Run project
    ```shell script
    # console script setup as entrypoint
    pyanoled
    ```

## TODO
- Persist PyanoLED app configuration changes
- Dockerize PyanoLED
- MIDI playback
- Synthesia support
- Additional color schemes and effects
- Additional configuration exposed in UI