import threading
import time
import RPi.GPIO as GPIO
import psutil
import datetime
import socket
from waitress import serve
from library.neopixel import *


def find_between(s, start, end):
    try:
        return (s.split(start))[1].split(end)[0]
    except:
        return False

def clamp(val, val_min, val_max):
    return max(val_min, min(val, val_max))
  
def get_rainbow_colors(pos, color):
    pos = int(pos)
    if pos < 85:
        if color == "green":
            return pos * 3
        elif color == "red":
            return 255 - pos * 3
        elif color == "blue":
            return 0
    elif pos < 170:
        pos -= 85
        if color == "green":
            return 255 - pos * 3
        elif color == "red":
            return 0
        elif color == "blue":
            return pos * 3
    else:
        pos -= 170
        if color == "green":
            return 0
        elif color == "red":
            return pos * 3
        elif color == "blue":
            return 255 - pos * 3

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip

# Get note position on the strip
def get_note_position(note, ledstrip, ledsettings):
    note_offsets = ledsettings.note_offsets
    note_offset = 0
    for i in range(0, len(note_offsets)):
        if note > note_offsets[i][0]:
            note_offset = note_offsets[i][1]
            break
    note_offset -= ledstrip.shift

    if (ledsettings.low_density == 1):
        density = 1
    else:
        density = 2

    note_pos_raw = density * (note - 20) - note_offset
    if ledstrip.reverse:
        return max(0, ledstrip.led_number - note_pos_raw)
    else:
        return max(0, note_pos_raw)
    
def check_if_led_can_be_overwrite(i, ledstrip, ledsettings):
    if ledsettings.adjacent_mode == "Off":
        if ledstrip.keylist_status[i] == 0 and ledstrip.keylist[i] == 0:
            return True
    else:
        if i > 1 and i < (ledstrip.led_number - 1):
            if ledstrip.keylist[i + 1] == ledstrip.keylist[i - 1] == ledstrip.keylist[i] \
                    == ledstrip.keylist_status[i + 1] == ledstrip.keylist_status[i - 1] == ledstrip.keylist_status[i]:
                return True
        else:
            return True
    return False

    
# LED animations
def fastColorWipe(strip, update, ledsettings):
    brightness = ledsettings.backlight_brightness_percent / 100
    red = int(ledsettings.get_backlight_color("Red") * brightness)
    green = int(ledsettings.get_backlight_color("Green") * brightness)
    blue = int(ledsettings.get_backlight_color("Blue") * brightness)
    color = Color(green, red, blue)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    if update:
        strip.show()
        
def get_scale_color(scale, note_position, ledsettings):
    notes_in_scale = [0, 2, 4, 5, 7, 9, 11]
    scale = int(scale)
    note_position = (note_position - scale) % 12

    if note_position in notes_in_scale:
        return list(ledsettings.key_in_scale.values())
    else:
        return list(ledsettings.key_not_in_scale.values())


SENSECOVER = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSECOVER, GPIO.IN, GPIO.PUD_UP)

def theaterChase(ledstrip, color, ledsettings, menu, wait_ms=25):
    """Movie theater light style chaser animation."""
    strip = ledstrip.strip
    menu.screensaver_is_running = False
    time.sleep(0.5)
    if menu.screensaver_is_running:
        return
    menu.t = threading.currentThread()
    j = 0
    menu.screensaver_is_running = True

    while menu.screensaver_is_running:
        last_state = 1
        cover_opened = GPIO.input(SENSECOVER)
        while not cover_opened:
            if last_state != cover_opened:
                # clear if changed
                fastColorWipe(strip, True, ledsettings)
            time.sleep(.1)
            last_state = cover_opened
            cover_opened = GPIO.input(SENSECOVER)

        if ledsettings.backlight_brightness_percent == 0:
            brightness = 100
        else:
            brightness = ledsettings.backlight_brightness_percent

        brightness /= 100

        red = int(ledsettings.get_backlight_color("Red") * brightness)
        green = int(ledsettings.get_backlight_color("Green") * brightness)
        blue = int(ledsettings.get_backlight_color("Blue") * brightness)

        for q in range(5):
            for i in range(0, strip.numPixels(), 5):
                if check_if_led_can_be_overwrite(i, ledstrip, ledsettings):
                    strip.setPixelColor(i + q, Color(green, red, blue))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 5):
                if check_if_led_can_be_overwrite(i, ledstrip, ledsettings):
                    strip.setPixelColor(i + q, 0)
        j += 1
        if j > 256:
            j = 0
    menu.screensaver_is_running = False
    fastColorWipe(strip, True, ledsettings)

def breathing(ledstrip, ledsettings, menu, wait_ms=2):
    menu.screensaver_is_running = False
    time.sleep(0.1)
    strip = ledstrip.strip
    if menu.screensaver_is_running:
        return
    fastColorWipe(strip, True, ledsettings)
    menu.t = threading.currentThread()
    menu.screensaver_is_running = True

    multiplier = 24
    direction = 2
    while menu.screensaver_is_running:
        last_state = 1
        cover_opened = GPIO.input(SENSECOVER)
        while not cover_opened:
            if last_state != cover_opened:
                # clear if changed
                fastColorWipe(strip, True, ledsettings)
            time.sleep(.1)
            last_state = cover_opened
            cover_opened = GPIO.input(SENSECOVER)

        if multiplier >= 98 or multiplier < 24:
            direction *= -1
        multiplier += direction

        if ledsettings.backlight_brightness_percent == 0:
            brightness = 100
        else:
            brightness = ledsettings.backlight_brightness_percent

        brightness /= 100

        divide = (multiplier / float(100)) * brightness
        red = int(round(float(ledsettings.get_backlight_color("Red")) * float(divide)))
        green = int(round(float(ledsettings.get_backlight_color("Green")) * float(divide)))
        blue = int(round(float(ledsettings.get_backlight_color("Blue")) * float(divide)))

        for i in range(strip.numPixels()):
            if check_if_led_can_be_overwrite(i, ledstrip, ledsettings):
                strip.setPixelColor(i, Color(green, red, blue))
        strip.show()
        if wait_ms > 0:
            time.sleep(wait_ms / 1000.0)
    menu.screensaver_is_running = False
    fastColorWipe(strip, True, ledsettings)

def rainbow(ledstrip, ledsettings, menu, wait_ms=20):
    """Draw rainbow that fades across all pixels at once."""
    menu.screensaver_is_running = False
    time.sleep(0.2)
    strip = ledstrip.strip
    if menu.screensaver_is_running:
        return
    fastColorWipe(strip, True, ledsettings)
    menu.t = threading.currentThread()
    j = 0
    menu.screensaver_is_running = True
    while menu.screensaver_is_running:
        last_state = 1
        cover_opened = GPIO.input(SENSECOVER)
        while not cover_opened:
            if last_state != cover_opened:
                # clear if changed
                fastColorWipe(strip, True, ledsettings)
            time.sleep(.1)
            last_state = cover_opened
            cover_opened = GPIO.input(SENSECOVER)

        for i in range(strip.numPixels()):
            if check_if_led_can_be_overwrite(i, ledstrip, ledsettings):
                strip.setPixelColor(i, wheel(j & 255, ledsettings))
        j += 1
        if j >= 256:
            j = 0
        strip.show()
        time.sleep(wait_ms / 1000.0)
    menu.screensaver_is_running = False
    fastColorWipe(strip, True, ledsettings)


def wheel(pos, ledsettings):
    """Generate rainbow colors across 0-255 positions."""

    if ledsettings.backlight_brightness_percent == 0:
        brightness = 100
    else:
        brightness = ledsettings.backlight_brightness_percent

    brightness /= 100

    if pos < 85:
        return Color(int((pos * 3) * brightness), int((255 - pos * 3) * brightness), 0)
    elif pos < 170:
        pos -= 85
        return Color(int((255 - pos * 3) * brightness), 0, int((pos * 3) * brightness))
    else:
        pos -= 170
        return Color(0, int((pos * 3) * brightness), int((255 - pos * 3) * brightness))
    
    
def rainbowCycle(ledstrip, ledsettings, menu, wait_ms=20):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    menu.screensaver_is_running = False
    time.sleep(0.2)
    strip = ledstrip.strip
    if menu.screensaver_is_running:
        return
    fastColorWipe(strip, True, ledsettings)
    menu.t = threading.currentThread()
    j = 0
    menu.screensaver_is_running = True
    while menu.screensaver_is_running:
        last_state = 1
        cover_opened = GPIO.input(SENSECOVER)
        while not cover_opened:
            if last_state != cover_opened:
                # clear if changed
                fastColorWipe(strip, True, ledsettings)
            time.sleep(.1)
            last_state = cover_opened
            cover_opened = GPIO.input(SENSECOVER)

        for i in range(strip.numPixels()):
            if check_if_led_can_be_overwrite(i, ledstrip, ledsettings):
                strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255, ledsettings))
        j += 1
        if j >= 256:
            j = 0
        strip.show()
        time.sleep(wait_ms / 1000.0)
    menu.screensaver_is_running = False
    fastColorWipe(strip, True, ledsettings)


def theaterChaseRainbow(ledstrip, ledsettings, menu, wait_ms=25):
    """Rainbow movie theater light style chaser animation."""
    menu.screensaver_is_running = False
    time.sleep(0.5)
    strip = ledstrip.strip
    if menu.screensaver_is_running:
        return
    fastColorWipe(strip, True, ledsettings)
    menu.t = threading.currentThread()
    j = 0
    menu.screensaver_is_running = True
    while menu.screensaver_is_running:
        last_state = 1
        cover_opened = GPIO.input(SENSECOVER)
        while not cover_opened:
            if last_state != cover_opened:
                # clear if changed
                fastColorWipe(strip, True, ledsettings)
            time.sleep(.1)
            last_state = cover_opened
            cover_opened = GPIO.input(SENSECOVER)

        for q in range(5):
            for i in range(0, strip.numPixels(), 5):
                if check_if_led_can_be_overwrite(i, ledstrip, ledsettings):
                    strip.setPixelColor(i + q, wheel((i + j) % 255, ledsettings))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 5):
                if check_if_led_can_be_overwrite(i, ledstrip, ledsettings):
                    strip.setPixelColor(i + q, 0)
        j += 1

        if j > 256:
            j = 0
    menu.screensaver_is_running = False
    fastColorWipe(strip, True, ledsettings)

def sound_of_da_police(ledstrip, ledsettings, menu, wait_ms=5):
    menu.screensaver_is_running = False
    time.sleep(0.1)
    strip = ledstrip.strip
    if menu.screensaver_is_running:
        return
    fastColorWipe(strip, True, ledsettings)
    menu.t = threading.currentThread()
    menu.screensaver_is_running = True
    middle = strip.numPixels() / 2
    r_start = 0
    l_start = 196
    while menu.screensaver_is_running:
        last_state = 1
        cover_opened = GPIO.input(SENSECOVER)
        while not cover_opened:
            if last_state != cover_opened:
                # clear if changed
                fastColorWipe(strip, True, ledsettings)
            time.sleep(.1)
            last_state = cover_opened
            cover_opened = GPIO.input(SENSECOVER)

        r_start += 14
        l_start -= 14

        if ledsettings.backlight_brightness_percent == 0:
            brightness = 100
        else:
            brightness = ledsettings.backlight_brightness_percent

        brightness /= 100

        for i in range(strip.numPixels()):
            if check_if_led_can_be_overwrite(i, ledstrip, ledsettings):
                if (i > middle) and i > r_start and i < (r_start + 40):
                    strip.setPixelColor(i, Color(0, int(255 * brightness), 0))
                elif (i < middle) and i < l_start and i > (l_start - 40):
                    strip.setPixelColor(i, Color(0, 0, int(255 * brightness)))
                else:
                    strip.setPixelColor(i, Color(0, 0, 0))
        if r_start > 150:
            r_start = 0
            l_start = 175
        strip.show()
        time.sleep(wait_ms / 1000.0)
    menu.screensaver_is_running = False
    fastColorWipe(strip, True, ledsettings)


def scanner(ledstrip, ledsettings, menu, wait_ms=1):
    menu.screensaver_is_running = False
    time.sleep(0.1)
    strip = ledstrip.strip
    if menu.screensaver_is_running:
        return
    fastColorWipe(strip, True, ledsettings)
    menu.t = threading.currentThread()
    menu.screensaver_is_running = True

    position = 0
    direction = 3
    scanner_length = 20

    red_fixed = ledsettings.get_backlight_color("Red")
    green_fixed = ledsettings.get_backlight_color("Green")
    blue_fixed = ledsettings.get_backlight_color("Blue")
    while menu.screensaver_is_running:
        last_state = 1
        cover_opened = GPIO.input(SENSECOVER)
        while not cover_opened:
            if last_state != cover_opened:
                # clear if changed
                fastColorWipe(strip, True, ledsettings)
            time.sleep(.1)
            last_state = cover_opened
            cover_opened = GPIO.input(SENSECOVER)

        position += direction
        for i in range(strip.numPixels()):
            if i > (position - scanner_length) and i < (position + scanner_length):
                distance_from_position = position - i
                if distance_from_position < 0:
                    distance_from_position *= -1

                if ledsettings.backlight_brightness_percent == 0:
                    brightness = 100
                else:
                    brightness = ledsettings.backlight_brightness_percent

                brightness /= 100

                divide = ((scanner_length / 2) - distance_from_position) / float(scanner_length / 2)

                red = int(float(red_fixed) * float(divide) * brightness)
                green = int(float(green_fixed) * float(divide) * brightness)
                blue = int(float(blue_fixed) * float(divide) * brightness)

                if check_if_led_can_be_overwrite(i, ledstrip, ledsettings):
                    if divide > 0:
                        strip.setPixelColor(i, Color(green, red, blue))
                    else:
                        strip.setPixelColor(i, Color(0, 0, 0))

        if position >= strip.numPixels() or position <= 1:
            direction *= -1
        strip.show()
        time.sleep(wait_ms / 1000.0)

    menu.screensaver_is_running = False
    fastColorWipe(strip, True, ledsettings)


        
def screensaver(menu, midiports, saving, ledstrip, ledsettings):
    KEY2 = 20
    GPIO.setup(KEY2, GPIO.IN, GPIO.PUD_UP)

    delay = 0.1
    interval = 3 / float(delay)
    i = 0
    cpu_history = [None] * int(interval)
    cpu_chart = [0] * 28
    cpu_average = 0

    upload = 0
    download = 0
    upload_start = 0
    download_start = 0
    local_ip = 0

    if menu.screensaver_settings["local_ip"] == "1":
        local_ip = get_ip_address()

    try:
        midiports.inport.poll()
    except:
        pass
    while True:
        if (time.time() - saving.start_time) > 3600 and delay < 0.5 and menu.screensaver_is_running == False:
            delay = 0.9
            interval = 5 / float(delay)
            cpu_history = [None] * int(interval)
            cpu_average = 0
            i = 0

        if int(menu.screen_off_delay) > 0 and ((time.time() - saving.start_time) > (int(menu.screen_off_delay) * 60)):
            menu.screen_status = 0
            GPIO.output(24, 0)

        if int(menu.led_animation_delay) > 0 and ((time.time() - saving.start_time) > (
                int(menu.led_animation_delay) * 60)) and menu.screensaver_is_running == False:
            menu.screensaver_is_running = True
            if menu.led_animation == "Theater Chase":
                menu.t = threading.Thread(target=theaterChase, args=(ledstrip.strip,
                                                                     Color(127, 127, 127),
                                                                     ledsettings,
                                                                     menu))
                menu.t.start()
            if menu.led_animation == "Breathing Slow":
                menu.t = threading.Thread(target=breathing, args=(ledstrip.strip,
                                                                  ledsettings,
                                                                  menu, 25))
                menu.t.start()
            if menu.led_animation == "Rainbow Slow":
                menu.t = threading.Thread(target=rainbow, args=(ledstrip.strip,
                                                                ledsettings,
                                                                menu, 50))
                menu.t.start()
            if menu.led_animation == "Rainbow Cycle Slow":
                menu.t = threading.Thread(target=rainbowCycle, args=(ledstrip.strip,
                                                                     ledsettings,
                                                                     menu, 50))
                menu.t.start()
            if menu.led_animation == "Theater Chase Rainbow":
                menu.t = threading.Thread(target=theaterChaseRainbow, args=(ledstrip.strip,
                                                                            ledsettings,
                                                                            menu, 5))
                menu.t.start()
            if menu.led_animation == "Sound of da police":
                menu.t = threading.Thread(target=sound_of_da_police, args=(ledstrip.strip,
                                                                           ledsettings,
                                                                           menu, 1))
                menu.t.start()
            if menu.led_animation == "Scanner":
                menu.t = threading.Thread(target=scanner, args=(ledstrip.strip,
                                                                ledsettings,
                                                                menu, 1))
                menu.t.start()

        hour = datetime.datetime.now().strftime("%H:%M:%S")
        date = datetime.datetime.now().strftime("%d-%m-%Y")
        cpu_usage = psutil.cpu_percent()
        cpu_history[i] = cpu_usage
        cpu_chart.append(cpu_chart.pop(0))
        cpu_chart[27] = cpu_usage

        if i >= (int(interval) - 1):
            i = 0
            try:
                cpu_average = sum(cpu_history) / (float(len(cpu_history) + 1))
                last_cpu_average = cpu_average
            except:
                cpu_average = last_cpu_average

        if menu.screensaver_settings["ram"] == "1":
            ram_usage = psutil.virtual_memory()[2]
        else:
            ram_usage = 0

        if menu.screensaver_settings["temp"] == "1":
            try:
                temp = find_between(str(psutil.sensors_temperatures()["cpu_thermal"]), "current=", ",")
            except:
                temp = find_between(str(psutil.sensors_temperatures()["cpu-thermal"]), "current=", ",")
            temp = round(float(temp), 1)
        else:
            temp = 0

        if menu.screensaver_settings["network_usage"] == "1":
            upload_end = psutil.net_io_counters().bytes_sent
            download_end = psutil.net_io_counters().bytes_recv

            if upload_start:
                upload = upload_end - upload_start
                upload = upload * (1 / delay)
                upload = upload / 1000000
                upload = round(upload, 2)

            if download_start:
                download = download_end - download_start
                download = download * (1 / delay)
                download = download / 1000000
                download = round(download, 2)

            upload_start = upload_end
            download_start = download_end
        else:
            upload = 0
            download = 0
        if menu.screensaver_settings["sd_card_space"] == "1":
            card_space = psutil.disk_usage('/')
        else:
            card_space = 0

        menu.render_screensaver(hour, date, cpu_usage, round(cpu_average, 1), ram_usage, temp, cpu_chart, upload,
                                download, card_space, local_ip)
        time.sleep(delay)
        i += 1
        try:
            if str(midiports.inport.poll()) != "None":
                menu.screensaver_is_running = False
                saving.start_time = time.time()
                menu.screen_status = 1
                GPIO.output(24, 1)
                midiports.reconnect_ports()
                midiports.last_activity = time.time()
                menu.show()
                break
        except:
            pass
        if GPIO.input(KEY2) == 0:
            menu.screensaver_is_running = False
            saving.start_time = time.time()
            menu.screen_status = 1
            GPIO.output(24, 1)
            midiports.reconnect_ports()
            menu.show()
            break
