import RPi.GPIO as GPIO
import time
import numpy as np
import LCD_Config

class LCD(object):

    def __init__(self):
        
        self._e = LCD_Config.LCD_E
        self._rst = LCD_Config.LCD_RS
        self._d4 = LCD_Config.LCD_D4
        self._d5 = LCD_Config.LCD_D5
        self._d6 = LCD_Config.LCD_D6
        self._d7 = LCD_Config.LCD_D7
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(LCD_Config.LCD_E, GPIO.OUT)  # E
        GPIO.setup(LCD_Config.LCD_RS, GPIO.OUT) # RS
        GPIO.setup(LCD_Config.LCD_D4, GPIO.OUT) # DB4
        GPIO.setup(LCD_Config.LCD_D5, GPIO.OUT) # DB5
        GPIO.setup(LCD_Config.LCD_D6, GPIO.OUT) # DB6
        GPIO.setup(LCD_Config.LCD_D7, GPIO.OUT) # DB7
        
    def LCD_Init(self):   
        # Initialise display
        self.lcd_byte(0x33,LCD_Config.LCD_CMD) # 110011 Initialise
        self.lcd_byte(0x32,LCD_Config.LCD_CMD) # 110010 Initialise
        self.lcd_byte(0x06,LCD_Config.LCD_CMD) # 000110 Cursor move direction
        self.lcd_byte(0x0C,LCD_Config.LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
        self.lcd_byte(0x28,LCD_Config.LCD_CMD) # 101000 Data length, number of lines,
        self.lcd_byte(0x01,LCD_Config.LCD_CMD) # 000001 Clear display
        time.sleep(LCD_Config.E_DELAY)
        
        self.lcd_string("CSE467S",LCD_Config.LCD_LINE_1)
        
    
    def lcd_byte(self,bits,mode):
        # Send byte to data pins
        # bits = data
        # mode = True  for character
        #        False for command
        
        GPIO.output(LCD_Config.LCD_RS, mode) # RS
        
        # High bits
        GPIO.output(LCD_Config.LCD_D4, False)
        GPIO.output(LCD_Config.LCD_D5, False)
        GPIO.output(LCD_Config.LCD_D6, False)
        GPIO.output(LCD_Config.LCD_D7, False)
        if bits&0x10==0x10:
            GPIO.output(LCD_Config.LCD_D4, True)
        if bits&0x20==0x20:
            GPIO.output(LCD_Config.LCD_D5, True)
        if bits&0x40==0x40:
            GPIO.output(LCD_Config.LCD_D6, True)
        if bits&0x80==0x80:
            GPIO.output(LCD_Config.LCD_D7, True)
        
        # Toggle 'Enable' pin
        self.lcd_toggle_enable()
        
        # Low bits
        GPIO.output(LCD_Config.LCD_D4, False)
        GPIO.output(LCD_Config.LCD_D5, False)
        GPIO.output(LCD_Config.LCD_D6, False)
        GPIO.output(LCD_Config.LCD_D7, False)
        if bits&0x01==0x01:
            GPIO.output(LCD_Config.LCD_D4, True)
        if bits&0x02==0x02:
            GPIO.output(LCD_Config.LCD_D5, True)
        if bits&0x04==0x04:
            GPIO.output(LCD_Config.LCD_D6, True)
        if bits&0x08==0x08:
            GPIO.output(LCD_Config.LCD_D7, True)
        
        # Toggle 'Enable' pin
        self.lcd_toggle_enable()
        
        
    def lcd_toggle_enable(self):
        # Toggle enable
        time.sleep(LCD_Config.E_DELAY)
        GPIO.output(LCD_Config.LCD_E, True)
        time.sleep(LCD_Config.E_PULSE)
        GPIO.output(LCD_Config.LCD_E, False)
        time.sleep(LCD_Config.E_DELAY)
        
    def lcd_string(self, message,line):
        # Send string to display
        
        message = message.ljust(LCD_Config.LCD_WIDTH," ")
        
        self.lcd_byte(self, line, LCD_Config.LCD_CMD)
        
        for i in range(LCD_Config.LCD_WIDTH):
            self.lcd_byte(self, ord(message[i]),LCD_Config.LCD_CHR)

    def LCD_Clear(self):
        self.lcd_byte(0x01,LCD_Config.LCD_CMD) # 000001 Clear display