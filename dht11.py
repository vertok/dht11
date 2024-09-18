"""
this code continuously reads temperature and humidity data from a DHT11 sensor connected to Joy-Pi.
It then displays these readings on a 16x2 character LCD display connected via I2C.
dht11 pin 4
lcd pin 0x21
"""
import RPi.GPIO as GPIO
import dht11
import time
import datetime
import board
import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Connect the DHT11 sensor to the designated data pin on your Joy-Pi
# You might need to adjust this pin based on your Joy-Pi's layout
dht_pin = 4  # Replace with the correct pin if necessary

# Initialize the DHT11 sensor
instance = dht11.DHT11(pin=dht_pin)

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Set up the LCD (adjust columns, rows, and address if necessary)
lcd_columns = 16
lcd_rows = 2
lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows, 0x21)  # Use 0x21 as the address

while True:
    result = instance.read()
    if result.is_valid():
        # Read temperature and humidity
        temperature = result.temperature
        humidity = result.humidity

        # Display on the LCD screen
        lcd.clear()
        lcd.message = "Temp: {:.1f} C\nHumidity: {}%".format(temperature, humidity)

        time.sleep(2)  # Update every 2 seconds

    else:
        print("programm is running...")
        time.sleep(2.0)
