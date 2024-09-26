import time
import RPi.GPIO as GPIO
import dht11
from datetime import datetime
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, CP437_FONT

# Define sun and moon bitmaps (8x8)
sun_bitmap = [
    0b00111100,
    0b01111110,
    0b11111111,
    0b01111110,
    0b00111100,
    0b00011000,
    0b00000000,
    0b00000000,
]

moon_bitmap = [
    0b00111100,
    0b01111110,
    0b01110000,
    0b01100000,
    0b00111000,
    0b00011100,
    0b00000000,
    0b00000000,
]

def get_day_night():
    current_hour = datetime.now().hour
    return "Sun" if 6 <= current_hour < 18 else "Moon"

def draw_symbol(device, symbol):
    with canvas(device) as draw:
        for y in range(8):
            for x in range(8):
                if symbol[y] & (1 << (7 - x)):
                    draw.point((x, y), fill="white")

def main(cascaded, block_orientation, rotate):
    # Initialize LED matrix
    serial = spi(port=0, device=1, gpio=noop())
    device = max7219(serial, cascaded=cascaded or 1, block_orientation=block_orientation, rotate=rotate or 0)
    print("[-] Matrix initialized")

    # Initialize GPIO for DHT11
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()

    # Read data using pin 4
    instance = dht11.DHT11(pin=4)

    while True:
        # Get temperature and humidity
        result = instance.read()
        
        # Wait until we get valid results
        while not result.is_valid():
            time.sleep(1)
            result = instance.read()

        temperature = result.temperature
        humidity = result.humidity

        # Get day/night status
        day_night_status = get_day_night()
        
        # Create the message to display
        msg = f"Temp: {temperature}C  Hum: {humidity}%  {day_night_status}"
        
        # Print the message in console
        print("[-] Printing: %s" % msg)

        # Show message on LED matrix
        show_message(device, msg, fill="white", font=proportional(CP437_FONT), scroll_delay=0.1)

        # Choose the symbol based on the time of day
        symbol = sun_bitmap if day_night_status == "Sun" else moon_bitmap

        # Draw the symbol on the matrix
        draw_symbol(device, symbol)

        # Display the symbol for 5 seconds
        time.sleep(5)

if __name__ == "__main__":
    try:
        main(cascaded=1, block_orientation=90, rotate=0)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

